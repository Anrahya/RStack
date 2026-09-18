#!/usr/bin/env python3
"""Exercise a synthetic browser fixture and retain evidence, including a broken control.

Requires an already authorized Playwright Python install and browser. Does not
install dependencies, visit external sites, or use a personal browser profile.
"""
from __future__ import annotations

import argparse
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import importlib.metadata
import json
from pathlib import Path
import sys
import tempfile
import threading
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
EXPECTED = {
    'wheel': 'Wheel zoom remains 120 after shrinking and expanding the viewport.',
    'pan': 'A real 80px pointer drag remains 80 after shrinking and expanding.',
    'pause': 'The checked pause state survives crossing the narrow breakpoint both ways.',
    'focus': 'Keyboard Tab focuses Reset view with a visible outline at narrow width.',
    'motion': 'Reduced-motion preference disables the fixture pulse animation.',
    'profile': 'Pause saved through the UI remains checked after a browser restart.'}


def run(output: Path, executable: str | None, broken: bool = False, offline: bool = False) -> int:
    output = output.resolve()
    # Never overwrite earlier proof or use a user-supplied existing browser profile.
    output.mkdir(parents=True, exist_ok=False)
    output.chmod(0o700)
    cases: list[dict] = []
    metadata = {'fixture_sha256': hashlib.sha256((ROOT / 'fixture.html').read_bytes()).hexdigest(),
                'broken_control': broken, 'browser_backend': 'Playwright Python, not MCP or agent-browser',
                'setup_error': None, 'cleanup': 'not started', 'offline_content': offline,
                'limits': ['Offline mode does not test app/server reachability or restart storage.'] if offline else []}
    required = [name for name in EXPECTED if not offline or name != 'profile']
    server = None
    thread = None
    context = None
    status = 2
    try:
        from playwright.sync_api import sync_playwright, expect
        metadata['playwright_version'] = importlib.metadata.version('playwright')
        body = (ROOT / 'fixture.html').read_bytes()
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                if urlsplit(self.path).path != '/':
                    self.send_response(404); self.end_headers(); return
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(body)))
                self.end_headers(); self.wfile.write(body)
            def log_message(self, *args):
                pass
        if offline:
            url = 'about:blank'
        else:
            server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            url = f'http://127.0.0.1:{server.server_port}/?broken={int(broken)}'
        metadata['url'] = url
        with tempfile.TemporaryDirectory(prefix='rstack-browser-profile-') as profile, sync_playwright() as browser:
            try:
                launch = {'headless': True, 'viewport': {'width': 1000, 'height': 720}}
                if executable:
                    launch['executable_path'] = str(Path(executable).resolve(strict=True))
                context = browser.chromium.launch_persistent_context(profile, **launch)
                page = context.pages[0] if context.pages else context.new_page()
                page.set_default_timeout(3000)
                if offline:
                    page.set_content(body.decode().replace('data-broken="0"', f'data-broken="{int(broken)}"'))
                else:
                    page.goto(url)
                expect(page).to_have_title('RStack browser-check fixture')
                expect(page.locator('#width')).to_have_text('1000')
                metadata['browser_version'] = page.evaluate('navigator.userAgent')
                metadata['executable'] = launch.get('executable_path', browser.chromium.executable_path)
                page.screenshot(path=str(output / 'ready.png'))
                def resize(width: int) -> None:
                    page.set_viewport_size({'width': width, 'height': 720})
                    expect(page.locator('#width')).to_have_text(str(width))
                def start_case() -> None:
                    resize(1000)
                    page.get_by_role('button', name='Reset view').click()
                def wheel() -> None:
                    start_case(); page.get_by_role('region', name='Map viewport').hover()
                    page.mouse.wheel(0, -120)
                    expect(page.locator('#zoom')).to_have_text('120')
                    for width in (520, 1000):
                        resize(width); expect(page.locator('#zoom')).to_have_text('120')
                def pan() -> None:
                    start_case()
                    box = page.get_by_role('region', name='Map viewport').bounding_box()
                    assert box is not None, 'map viewport has no rendered box'
                    x, y = box['x'] + 70, box['y'] + 70
                    page.mouse.move(x, y); page.mouse.down()
                    page.mouse.move(x + 80, y, steps=5); page.mouse.up()
                    expect(page.locator('#pan')).to_have_text('80')
                    for width in (520, 1000):
                        resize(width); expect(page.locator('#pan')).to_have_text('80')
                def pause() -> None:
                    start_case(); page.get_by_label('Pause motion').check()
                    for width in (520, 1000):
                        resize(width); expect(page.get_by_label('Pause motion')).to_be_checked()
                        expect(page.locator('#motion')).to_have_text('paused')
                def focus() -> None:
                    resize(520)
                    # A real keyboard input after clicking noninteractive page content.
                    page.get_by_role('heading').click(); page.keyboard.press('Tab')
                    button = page.get_by_role('button', name='Reset view')
                    expect(button).to_be_focused()
                    expect(button).to_have_css('outline-style', 'solid')
                    expect(button).to_have_css('outline-width', '3px')
                def motion() -> None:
                    page.emulate_media(reduced_motion='reduce')
                    expect(page.locator('.pulse')).to_have_css('animation-name', 'none')
                for name, action in [('wheel',wheel),('pan',pan),('pause',pause),('focus',focus),('motion',motion)]:
                    try:
                        action()
                        record = {'id': name, 'status': 'PASS', 'expected': EXPECTED[name],
                                  'observed': 'Native browser assertions passed; see the screenshot and action code.'}
                    except Exception as exc:
                        record = {'id': name, 'status': 'FAIL', 'expected': EXPECTED[name],
                                  'observed': f'{type(exc).__name__}: {exc}'[:5000]}
                    cases.append(record)
                    page.screenshot(path=str(output / f'{name}.png'))
                if not offline:
                    page.get_by_label('Pause motion').check()
                    context.close(); context = None
                    context = browser.chromium.launch_persistent_context(profile, **launch)
                    page = context.pages[0] if context.pages else context.new_page()
                    page.goto(url); page.set_default_timeout(3000)
                    try:
                        expect(page.get_by_label('Pause motion')).to_be_checked()
                        cases.append({'id':'profile', 'status':'PASS', 'expected':EXPECTED['profile'],
                                      'observed':'New browser process restored UI-saved state from its dedicated temporary profile.'})
                    except Exception as exc:
                        cases.append({'id':'profile','status':'FAIL','expected':EXPECTED['profile'],
                                      'observed':f'{type(exc).__name__}: {exc}'[:5000]})
                    page.screenshot(path=str(output / 'profile.png'))
                context.close(); context = None
                metadata['cleanup'] = 'owned browser contexts closed; temporary synthetic profile removed on exit'
            finally:
                if context is not None:
                    try:
                        context.close()
                    finally:
                        context = None
        status = 0 if len(cases) == len(required) and all(x['status'] == 'PASS' for x in cases) else 1
    except Exception as exc:
        metadata['setup_error'] = f'{type(exc).__name__}: {exc}'[:5000]
        status = 2
    finally:
        if context is not None:
            try:
                context.close()
            except Exception as exc:
                metadata['cleanup_error'] = str(exc); status = 2
        if server is not None:
            server.shutdown(); server.server_close()
            if thread is not None:
                thread.join(timeout=5)
                if thread.is_alive():
                    metadata['cleanup_error'] = 'owned server thread did not stop'; status = 2
            metadata['server_closed'] = True
        for name in sorted(set(required) - {r['id'] for r in cases}):
            cases.append({'id':name, 'status':'NOT_RUN','expected':EXPECTED[name],
                          'observed':metadata['setup_error'] or 'Earlier setup or cleanup prevented completion.'})
        (output/'results.json').write_text(json.dumps({'schema_version':1,'cases':cases},indent=2)+'\n')
        metadata['exit_status'] = status
        metadata['artifacts'] = {x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in output.iterdir() if x.is_file()}
        (output/'run.json').write_text(json.dumps(metadata,indent=2)+'\n')
    return status


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True, help='new private evidence directory')
    parser.add_argument('--browser-executable', help='existing approved Chromium executable')
    parser.add_argument('--broken-control', action='store_true')
    parser.add_argument('--offline', action='store_true', help='synthetic in-memory page; no app reachability or restart-state test')
    args = parser.parse_args()
    try:
        status = run(args.output, args.browser_executable, args.broken_control, args.offline)
    except (OSError, ValueError) as exc:
        print(f'probe setup failed: {exc}', file=sys.stderr); return 2
    print(f'Fixture check exit {status}; evidence: {args.output}')
    return status


if __name__ == '__main__':
    sys.exit(main())

"""Packaging safety tests use disposable repositories and installation targets."""
from __future__ import annotations
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
from install_cursor import install
from check_portability import check_package

class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.source=self.root/'source';self.target=self.root/'installed'
        (self.source/'.cursor-plugin').mkdir(parents=True)
        (self.source/'.cursor-plugin/plugin.json').write_text(json.dumps({'name':'r-stack'}))
        path=self.source/'skills/r-stack-mode/SKILL.md';path.parent.mkdir(parents=True);path.write_text('entry')
    def test_malformed_identity_rejected(self):
        (self.source/'.cursor-plugin/plugin.json').write_text('[]')
        with self.assertRaises(ValueError):install(self.source,self.target)
    def test_first_install(self):
        install(self.source,self.target);self.assertEqual((self.target/'skills/r-stack-mode/SKILL.md').read_text(),'entry')
    def test_self_install_is_noop(self):
        install(self.source,self.target);before=list(self.target.rglob('*'));install(self.target,self.target)
        self.assertEqual(before,list(self.target.rglob('*')))
    def test_replacement_keeps_backup(self):
        install(self.source,self.target);(self.target/'local.txt').write_text('keep me')
        install(self.source,self.target);backups=list(self.root.glob('r-stack-backup-*'))
        self.assertEqual(len(backups),1);self.assertEqual((backups[0]/'local.txt').read_text(),'keep me')
    def test_unrelated_target_rejected(self):
        self.target.mkdir();(self.target/'precious.txt').write_text('keep')
        with self.assertRaises(ValueError):install(self.source,self.target)
        self.assertEqual((self.target/'precious.txt').read_text(),'keep')
    def test_symlink_target_rejected(self):
        self.target.symlink_to(self.source,target_is_directory=True)
        with self.assertRaises(ValueError):install(self.source,self.target)
    def test_nested_copy_rejected(self):
        with self.assertRaises(ValueError):install(self.source,self.source/'nested')
    def test_failed_stage_preserves_target(self):
        install(self.source,self.target)
        with mock.patch('install_cursor.shutil.copytree',side_effect=OSError('copy failure')):
            with self.assertRaises(OSError):install(self.source,self.target)
        self.assertEqual((self.target/'skills/r-stack-mode/SKILL.md').read_text(),'entry')


class StaticPackageTests(unittest.TestCase):
    def test_missing_package_rejected(self):
        with tempfile.TemporaryDirectory() as directory:self.assertTrue(check_package(Path(directory)))

    def package_root(self, directory: str, versions: dict[str, str] | None = None,
                     marketplace_version: str = '0.2.0-rc.4') -> Path:
        root = Path(directory)
        versions = versions or {}
        for folder in ('.claude-plugin', '.codex-plugin', '.cursor-plugin', '.zcode-plugin'):
            path = root / folder / 'plugin.json'
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps({'name':'r-stack','version':versions.get(folder,'0.2.0-rc.4')}))
        (root / 'marketplace.json').write_text(json.dumps({
            'name':'r-stack',
            'plugins':[{'name':'r-stack','version':marketplace_version,'source':'.'}],
        }))
        return root

    def test_zcode_version_participates_in_cross_host_check(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self.package_root(directory, {'.zcode-plugin':'0.2.0-rc.3'})
            self.assertIn('plugin versions disagree across hosts', check_package(root))

    def test_marketplace_version_must_match_plugin_manifests(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self.package_root(directory, marketplace_version='0.2.0-rc.3')
            self.assertIn('marketplace version disagrees with host manifests', check_package(root))


if __name__=='__main__':unittest.main()

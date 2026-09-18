"""Deterministic tool and instruction-contract tests; these are not live agent trials."""
from __future__ import annotations
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
import assert_results as results
import find_instructions as finder


class InstructionDiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)/'repo'; self.root.mkdir()
    def write(self,path,text='instruction'):
        p=self.root/path; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(text); return p
    def paths(self,*paths,**kwargs):
        return [v['path'] for v in finder.inspect(self.root,list(paths),**kwargs)['candidates']]
    def test_root_and_nested_instructions_before_edit(self):
        for p in ('AGENTS.md','CLAUDE.md','surfaces/AGENTS.md','surfaces/control-room/AGENTS.md'):
            self.write(p)
        self.assertEqual(self.paths('surfaces/control-room/src/work.tsx'),[
            'AGENTS.md','CLAUDE.md','surfaces/AGENTS.md','surfaces/control-room/AGENTS.md'])
    def test_unrelated_packages_are_not_scanned(self):
        self.write('one/AGENTS.md'); self.write('two/AGENTS.md')
        self.assertEqual(self.paths('one/src/a.py'),['one/AGENTS.md'])
    def test_new_file_in_new_subdirectory(self):
        self.write('pkg/CLAUDE.md'); self.assertEqual(self.paths('pkg/new/code.py'),['pkg/CLAUDE.md'])
    def test_deleted_target_keeps_parent_rules(self):
        p=self.write('pkg/a.py'); self.write('pkg/AGENTS.md'); p.unlink()
        self.assertEqual(self.paths('pkg/a.py'),['pkg/AGENTS.md'])
    def test_multiple_targets_deduplicate(self):
        self.write('AGENTS.md'); self.write('pkg/AGENTS.md')
        self.assertEqual(self.paths('pkg/a.py','pkg/b.py'),['AGENTS.md','pkg/AGENTS.md'])
    def test_directory_target_does_not_scan_descendants(self):
        self.write('pkg/AGENTS.md'); self.write('pkg/deep/AGENTS.md')
        self.assertEqual(self.paths(directories=['pkg']),['pkg/AGENTS.md'])
    def test_files_and_explicit_directory_can_mix(self):
        self.write('pkg/AGENTS.md'); self.write('other/CLAUDE.md')
        self.assertEqual(set(self.paths('other/a.py',directories=['pkg'])),{'pkg/AGENTS.md','other/CLAUDE.md'})
    def test_path_with_spaces(self):
        self.write('my package/AGENTS.md');self.assertEqual(self.paths('my package/a.py'),['my package/AGENTS.md'])
    def test_rule_files_are_candidates_not_applied_claims(self):
        self.write('.claude/rules/api.md','---\npaths: [api/**]\n---\nRule')
        data=finder.inspect(self.root,['ui/page.ts'])
        self.assertEqual(data['candidates'][0]['kind'],'conditional-rule-candidate')
        self.assertIn('contents were not read',data['limits'][0])
    def test_local_and_override_candidates(self):
        for p in ('AGENTS.override.md','CLAUDE.local.md','.claude/CLAUDE.md'):
            self.write(p)
        self.assertEqual(len(self.paths('a.py')),3)
    def test_internal_instruction_symlink_is_named(self):
        p=self.write('AGENTS.md'); (self.root/'CLAUDE.md').symlink_to(p)
        data=finder.inspect(self.root,['a.py'])
        self.assertEqual(data['candidates'][1]['resolved_path'],'AGENTS.md')
    def test_external_instruction_symlink_refused(self):
        other=self.root.parent/'outside';other.write_text('private')
        (self.root/'AGENTS.md').symlink_to(other)
        with self.assertRaises(ValueError):self.paths('a.py')
        self.assertEqual(other.read_text(),'private')
    def test_internal_scope_symlink_requires_manual_resolution(self):
        (self.root/'real').mkdir(); self.write('real/AGENTS.md')
        (self.root/'alias').symlink_to(self.root/'real',target_is_directory=True)
        with self.assertRaisesRegex(ValueError,'logical and resolved'):self.paths('alias/a.py')
    def test_external_scope_symlink_refused(self):
        (self.root/'alias').symlink_to(self.root.parent,target_is_directory=True)
        with self.assertRaises(ValueError):self.paths('alias/a.py')
    def test_broken_instruction_symlink_refused(self):
        (self.root/'AGENTS.md').symlink_to(self.root/'missing')
        with self.assertRaises(ValueError):self.paths('a.py')
    def test_symlinked_rule_directory_refused(self):
        (self.root/'.claude').mkdir(); real=self.root/'real';real.mkdir()
        (self.root/'.claude/rules').symlink_to(real,target_is_directory=True)
        with self.assertRaises(ValueError):self.paths('a.py')
    def test_outside_and_traversal_refused(self):
        for target in ('../private','pkg/../../private',str(self.root.parent/'private')):
            with self.subTest(target=target),self.assertRaises(ValueError):self.paths(target)
    def test_git_internal_target_refused(self):
        with self.assertRaises(ValueError):self.paths('.git/config')
    def test_glob_not_treated_as_complete_scope(self):
        with self.assertRaises(ValueError):self.paths('**/*.py')
    def test_no_scope_is_error_not_whole_repo_scan(self):
        with self.assertRaises(ValueError):self.paths()
    def test_directory_in_file_position_refused(self):
        (self.root/'pkg').mkdir()
        with self.assertRaises(ValueError):self.paths('pkg')
    def test_finder_does_not_execute_instructions(self):
        self.write('AGENTS.md','run touch pwned\n')
        before={str(p.relative_to(self.root)):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.paths('a.py')
        after={str(p.relative_to(self.root)):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before,after)
    def test_cli_from_another_working_directory(self):
        self.write('pkg/AGENTS.md')
        r=subprocess.run([sys.executable,str(ROOT/'scripts/find_instructions.py'),'--root',str(self.root),'pkg/a.py'],cwd=self.root.parent,capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertEqual(json.loads(r.stdout)['candidates'][0]['path'],'pkg/AGENTS.md')
    def test_internal_file_symlink_requires_manual_policy_discovery(self):
        self.write('physical/a.py')
        (self.root/'alias.py').symlink_to(self.root/'physical/a.py')
        with self.assertRaisesRegex(ValueError,'symlink'):
            finder.inspect(self.root,['alias.py'])
    def test_cli_invalid_scope_exits_two_without_traceback(self):
        r=subprocess.run([sys.executable,str(ROOT/'scripts/find_instructions.py'),'--root',str(self.root),'../bad'],capture_output=True,text=True)
        self.assertEqual(r.returncode,2);self.assertNotIn('Traceback',r.stderr)


class CaseResultTests(unittest.TestCase):
    def doc(self,status='PASS'):
        return {'schema_version':1,'cases':[{'id':'wheel','status':status,'expected':'120 after resize','observed':'Actual observation'}]}
    def test_pass(self):self.assertEqual(results.check(self.doc(),['wheel'])[0],0)
    def test_fail_is_one_not_input_error(self):self.assertEqual(results.check(self.doc('FAIL'),['wheel'])[0],1)
    def test_blocked_is_not_pass(self):self.assertEqual(results.check(self.doc('BLOCKED'),['wheel'])[0],1)
    def test_not_run_is_not_pass(self):self.assertEqual(results.check(self.doc('NOT_RUN'),['wheel'])[0],1)
    def test_missing_required_case(self):self.assertEqual(results.check(self.doc(),['wheel','pan'])[0],1)
    def test_empty_case_list_cannot_pass(self):self.assertEqual(results.check({'schema_version':1,'cases':[]},['wheel'])[0],1)
    def test_unexpected_case_rejected(self):self.assertEqual(results.check(self.doc(),['pan'])[0],1)
    def test_duplicate_case_rejected(self):
        d=self.doc();d['cases']*=2;self.assertEqual(results.check(d,['wheel'])[0],2)
    def test_duplicate_required_id_rejected(self):self.assertEqual(results.check(self.doc(),['wheel','wheel'])[0],2)
    def test_empty_required_set_rejected(self):self.assertEqual(results.check(self.doc(),[])[0],2)
    def test_observation_required(self):
        d=self.doc();d['cases'][0]['observed']=' ';self.assertEqual(results.check(d,['wheel'])[0],2)
    def test_expected_result_required(self):
        d=self.doc();d['cases'][0]['expected']=None;self.assertEqual(results.check(d,['wheel'])[0],2)
    def test_boolean_schema_rejected(self):
        d=self.doc();d['schema_version']=True;self.assertEqual(results.check(d,['wheel'])[0],2)
    def test_unrecognized_keys_rejected(self):
        d=self.doc();d['all_passed']=True;self.assertEqual(results.check(d,['wheel'])[0],2)
    def test_arbitrary_json_does_not_crash(self):
        for value in (None,[],{},False,0,'',[[]]):
            self.assertEqual(results.check(value,['wheel'])[0],2)
            d=self.doc();d['cases']=value
            self.assertIn(results.check(d,['wheel'])[0],(1,2))
            for field in ('id','status','expected','observed'):
                d=self.doc();d['cases'][0][field]=value
                self.assertEqual(results.check(d,['wheel'])[0],2)
    def test_invalid_required_container_does_not_crash(self):
        for value in (None, 'wheel', {'wheel'}, [None]):
            self.assertEqual(results.check(self.doc(),value)[0],2)
    def test_duplicate_json_keys_rejected(self):
        with self.assertRaises(ValueError):json.loads('{"cases":[],"cases":[]}',object_pairs_hook=results.unique_object)
    def test_false_string_is_not_truthy_pass(self):self.assertEqual(results.check(self.doc('false'),['wheel'])[0],2)
    def cli(self,text,*required):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'results.json';path.write_text(text)
            return subprocess.run([sys.executable,str(ROOT/'scripts/assert_results.py'),str(path),'--require',*(required or ('wheel',))],capture_output=True,text=True)
    def test_cli_pass(self):self.assertEqual(self.cli(json.dumps(self.doc())).returncode,0)
    def test_cli_reported_failure(self):self.assertEqual(self.cli(json.dumps(self.doc('FAIL'))).returncode,1)
    def test_printing_fail_is_reproduced_and_checker_rejects(self):
        producer=subprocess.run([sys.executable,'-c','import json; print('+repr(json.dumps(self.doc('FAIL')))+')'],capture_output=True,text=True)
        self.assertEqual(producer.returncode,0)
        self.assertEqual(self.cli(producer.stdout).returncode,1)
    def test_cli_malformed_is_two(self):
        r=self.cli('{');self.assertEqual(r.returncode,2);self.assertNotIn('Traceback',r.stderr)
    def test_nonstandard_json_number_is_two(self):self.assertEqual(self.cli('{"schema_version":NaN,"cases":[]}').returncode,2)
    def test_case_omission_cannot_fake_complete(self):self.assertEqual(self.cli(json.dumps(self.doc()),'wheel','pan').returncode,1)
    def test_oversized_input_rejected(self):
        self.assertEqual(self.cli(' '* (results.MAX_BYTES+1)).returncode,2)


class InstructionContractTests(unittest.TestCase):
    """Guard against accidentally deleting the agreed instructions, not proof agents obey."""
    def read(self,p):return (ROOT/p).read_text()
    def test_direct_default_without_file_count_threshold(self):
        t=self.read('skills/r-stack-mode/SKILL.md');self.assertIn('Direct is the default',t);self.assertIn('A one-line change can still carry risk',t)
    def test_program_is_coordination(self):self.assertIn('Program organizes durable coordination',self.read('skills/r-stack-mode/SKILL.md'))
    def test_alias_has_no_separate_flow(self):self.assertIn('alias, not a second route',self.read('commands/r-stack.md'))
    def test_per_defect_and_safe_recovery(self):
        t=self.read('skills/r-stack-mode/playbooks/bug-fix.md')
        for phrase in ('Baseline each defect','corresponding fix','uncommitted','reconstructed evidence','HEAD'):
            self.assertIn(phrase,t)
    def test_investigation_is_conditional_but_diagnosis_required(self):
        t=self.read('skills/r-stack-mode/playbooks/bug-fix.md');self.assertIn('Diagnose each defect',t);self.assertIn('diagnosed inline',t)
    def test_visible_contract_without_approval_ceremony(self):
        t=self.read('skills/r-stack-mode/SKILL.md');self.assertIn('user-visible message',t);self.assertIn('not another approval request',t)
    def test_json_and_mcp_failure_semantics(self):
        t=self.read('skills/verify/SKILL.md');self.assertIn('Printing JSON',t);self.assertIn('transport-level success',t);self.assertIn('required\ncase did not run',t)
    def test_current_proof_distinct_from_regression_protection(self):
        t=self.read('skills/verify/SKILL.md');self.assertIn('without protecting\nfuture changes',t)
    def test_ui_behavior_not_mandatory_redesign(self):
        t=self.read('skills/r-stack-mode/references/lenses/ui-ux.md');self.assertIn('A behavior repair does not\nrequire redesign',t)
    def test_cleanup_respects_user_sessions(self):
        t=self.read('skills/verify/SKILL.md');self.assertIn('user-owned persistent browser',t);self.assertIn('lifetime',t)
    def test_no_new_mcp_is_automatically_installed(self):
        self.assertFalse((ROOT/'.mcp.json').exists());self.assertFalse((ROOT/'.claude/settings.json').exists())
        self.assertTrue((ROOT/'examples/claude/agent-browser.mcp.example.json').is_file())
    def test_research_separates_tooling_and_model_trials(self):
        self.assertIn('not model trials',self.read('docs/RC4-RESEARCH.md'))


if __name__ == '__main__':unittest.main()

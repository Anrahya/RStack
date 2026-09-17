"""Regression tests for false completion, malformed inputs and actual execution."""
from __future__ import annotations

import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
from check_work_graph import check_graph, path_conflict
from check_receipt import check_receipt
from evidence_io import canonical_json_sha256, workspace_fingerprint, sha256_file, write_json
from run_check import run_check


def contract_hash(value):
    return canonical_json_sha256(value)


def graph(argv=None):
    return {'schema_version': 2, 'outcome': 'Preserve the requested public behavior.',
            'acceptance_ids': ['A-001'], 'units': [{'id': 'W-001', 'role': 'implementer',
            'outcome': 'Return the correct result.', 'authority': 'Edit app.py only.',
            'context': ['app.py', 'the caller request'],
            'stop_if': ['The public contract is ambiguous or the declared verification cannot run.'],
            'write': ['app.py'], 'requires': [], 'acceptance': [{'id': 'A-001',
            'predicate': 'The public check asserts the required result.',
            'verify': {'kind': 'execution', 'action': 'Run the public behavior check.',
            'expected': 'All public assertions pass.', 'argv': argv or [sys.executable, '-c', 'assert 2 + 2 == 4']}}]}]}


def structural_receipt():
    g = graph(); claim = g['units'][0]['acceptance'][0]; frozen=contract_hash(g)
    return {'schema_version': 2, 'contract_hash': frozen,
            'work_id': 'W-001', 'status': 'PASS', 'result': 'Complete.',
            'evidence': [{'id': 'E-001', 'acceptance': 'A-001', 'claim': claim['predicate'],
            'basis': 'observed', 'outcome': 'PASS', 'purpose': 'proof',
            'action_or_source': claim['verify']['action'], 'expected_result': claim['verify']['expected'],
            'observed_result': 'passed', 'fingerprint': 'current', 'contract_hash': frozen,
            'artifact': {'path': 'E-001/run.json', 'sha256': 'a' * 64}}],
            'mutations': [], 'rejected': [], 'uncertainty': [], 'handoff': []}


class GraphTests(unittest.TestCase):
    def test_valid(self): self.assertEqual(check_graph(graph()), [])
    def test_contract_hash_ignores_json_key_order(self):
        original=graph();reordered=json.loads(json.dumps(original,sort_keys=True))
        self.assertEqual(contract_hash(original),contract_hash(reordered))
    def test_context_is_required(self):
        g=graph();del g['units'][0]['context'];self.assertTrue(check_graph(g))
    def test_stop_condition_is_required(self):
        g=graph();g['units'][0]['stop_if']=[];self.assertTrue(check_graph(g))
    def test_missing_original_claim(self):
        g=graph(); g['acceptance_ids'].append('A-002'); self.assertTrue(check_graph(g))
    def test_duplicate_original_claim(self):
        g=graph(); g['acceptance_ids'].append('A-001'); self.assertTrue(check_graph(g))
    def test_unknown_dependency(self):
        g=graph(); g['units'][0]['requires']=['W-999']; self.assertTrue(check_graph(g))
    def test_self_cycle(self):
        g=graph(); g['units'][0]['requires']=['W-001']; self.assertTrue(check_graph(g))
    def test_root_scope_conflicts(self): self.assertTrue(path_conflict('.', 'src/a.py'))
    def test_dot_alias_conflicts(self): self.assertTrue(path_conflict('./src/a.py', 'src/a.py'))
    def test_case_alias_conflicts(self): self.assertTrue(path_conflict('Src/a.py', 'src/A.py'))
    def test_sibling_prefix_not_conflict(self): self.assertFalse(path_conflict('src/a', 'src/ab'))
    def test_traversal_rejected(self):
        g=graph(); g['units'][0]['write']=['src/../app.py']; self.assertTrue(check_graph(g))
    def test_glob_rejected(self):
        g=graph(); g['units'][0]['write']=['src/*.py']; self.assertTrue(check_graph(g))
    def test_excluded_overlap_rejected(self):
        g=graph(); g['units'][0]['excluded']=['app.py']; self.assertTrue(check_graph(g))
    def test_readonly_writer_rejected(self):
        g=graph(); g['units'][0]['role']='reviewer'; self.assertTrue(check_graph(g))
    def test_vague_execution_without_argv_rejected(self):
        g=graph(); del g['units'][0]['acceptance'][0]['verify']['argv']; self.assertTrue(check_graph(g))
    def test_executor_config_rejected(self):
        g=graph(); g['units'][0]['model']='host-owned'; self.assertTrue(check_graph(g))
    def test_domain_model_word_not_forbidden(self):
        g=graph(); g['units'][0]['outcome']='Repair the domain model.'; self.assertEqual(check_graph(g), [])
    def two_units(self):
        g=graph(); u=copy.deepcopy(g['units'][0]); u.update(id='W-002',write=['other.py'])
        u['acceptance'][0]['id']='A-002';g['acceptance_ids'].append('A-002');g['units'].append(u);return g
    def test_unordered_conflict_rejected(self):
        g=self.two_units();g['units'][1]['write']=['./app.py'];self.assertTrue(check_graph(g))
    def test_ordered_shared_scope_allowed(self):
        g=self.two_units();g['units'][1].update(write=['app.py'],requires=['W-001']);self.assertEqual(check_graph(g), [])
    def test_cycle_across_units_rejected(self):
        g=self.two_units();g['units'][0]['requires']=['W-002'];g['units'][1]['requires']=['W-001'];self.assertTrue(check_graph(g))
    def test_unordered_external_resource_rejected(self):
        g=self.two_units()
        for u in g['units']:u['write_resources']=['database:staging/main']
        self.assertTrue(check_graph(g))
    def test_consumer_dependency_required(self):
        g=self.two_units();g['units'][0]['produces_for']=['W-002'];self.assertTrue(check_graph(g))
    def test_json_type_matrix_never_crashes(self):
        values=[None,False,0,2.5,'',{},[None],[{}],[[]]]
        for value in values:
            self.assertIsInstance(check_graph(value),list)
            for key in ('schema_version','units','decisions','acceptance_ids'):
                g=graph();g[key]=value;self.assertIsInstance(check_graph(g),list)
            for key in ('role','write','requires','acceptance','accepted_decisions','produces_for','excluded','write_resources','known_facts','assumptions_to_test','stop_if','forbidden'):
                g=graph();g['units'][0][key]=value;self.assertIsInstance(check_graph(g),list)
            for key in ('kind','argv','expected','action'):
                g=graph();g['units'][0]['acceptance'][0]['verify'][key]=value;self.assertIsInstance(check_graph(g),list)


class ReceiptTests(unittest.TestCase):
    def lint(self,r,g=None):return check_receipt(r,g or graph(),None,structure_only=True)
    def test_structural_example(self):self.assertEqual(self.lint(structural_receipt()),[])
    def test_no_graph_rejected(self):self.assertTrue(check_receipt(structural_receipt(),None,'current'))
    def test_empty_pass_rejected(self):
        r=structural_receipt();r['evidence']=[];self.assertTrue(self.lint(r))
    def test_proposed_cannot_close(self):
        r=structural_receipt();r['evidence'][0]['basis']='proposed';self.assertTrue(self.lint(r))
    def test_unknown_cannot_close(self):
        r=structural_receipt();r['evidence'][0]['basis']='unknown';self.assertTrue(self.lint(r))
    def test_failed_outcome_cannot_close(self):
        r=structural_receipt();r['evidence'][0]['outcome']='FAIL';self.assertTrue(self.lint(r))
    def test_inference_cannot_prove_execution(self):
        r=structural_receipt();r['evidence'][0]['basis']='supported-inference';self.assertTrue(self.lint(r))
    def test_duplicate_id_rejected(self):
        r=structural_receipt();r['evidence'].append(copy.deepcopy(r['evidence'][0]));self.assertTrue(self.lint(r))
    def test_unassigned_claim_rejected(self):
        r=structural_receipt();r['evidence'][0]['acceptance']='A-999';self.assertTrue(self.lint(r))
    def test_predicate_cannot_change(self):
        r=structural_receipt();r['evidence'][0]['claim']='Something easier';self.assertTrue(self.lint(r))
    def test_goalposts_cannot_move(self):
        r=structural_receipt();r['evidence'][0]['expected_result']='Any output is fine';self.assertTrue(self.lint(r))
    def test_action_cannot_change(self):
        r=structural_receipt();r['evidence'][0]['action_or_source']='Different check';self.assertTrue(self.lint(r))
    def test_historical_support_does_not_close(self):
        r=structural_receipt();r['evidence'][0]['purpose']='support';self.assertTrue(self.lint(r))
    def test_failed_observation_cannot_support_successful_inference(self):
        g=graph();g['units'][0]['acceptance'][0]['verify']={'kind':'judgment','action':'Review the captured source.','expected':'The requirement is satisfied.'}
        frozen=contract_hash(g);claim=g['units'][0]['acceptance'][0]
        proof={'id':'E-001','acceptance':'A-001','claim':claim['predicate'],'basis':'supported-inference',
               'outcome':'PASS','purpose':'proof','action_or_source':claim['verify']['action'],
               'expected_result':claim['verify']['expected'],'observed_result':'The requirement is satisfied.',
               'fingerprint':'current','contract_hash':frozen,
               'artifact':{'path':'E-001/record.json','sha256':'a'*64},'limitations':[],
               'supports':['E-002']}
        support=copy.deepcopy(proof);support.update(id='E-002',basis='observed',outcome='FAIL',
                                                    purpose='support',supports=[],
                                                    artifact={'path':'E-002/record.json','sha256':'b'*64})
        receipt={'schema_version':2,'contract_hash':frozen,'work_id':'W-001','status':'PASS',
                 'result':'Complete.','evidence':[proof,support],'uncertainty':[]}
        self.assertTrue(check_receipt(receipt,g,None,structure_only=True))
    def test_different_contract_observation_cannot_support_successful_inference(self):
        g=graph();g['units'][0]['acceptance'][0]['verify']={'kind':'judgment','action':'Review the captured source.','expected':'The requirement is satisfied.'}
        frozen=contract_hash(g);claim=g['units'][0]['acceptance'][0]
        proof={'id':'E-001','acceptance':'A-001','claim':claim['predicate'],'basis':'supported-inference',
               'outcome':'PASS','purpose':'proof','action_or_source':claim['verify']['action'],
               'expected_result':claim['verify']['expected'],'observed_result':'The requirement is satisfied.',
               'fingerprint':'current','contract_hash':frozen,
               'artifact':{'path':'E-001/record.json','sha256':'a'*64},'limitations':[],
               'supports':['E-002']}
        support=copy.deepcopy(proof);support.update(id='E-002',basis='observed',purpose='support',
                                                    supports=[],contract_hash='0'*64,
                                                    artifact={'path':'E-002/record.json','sha256':'b'*64})
        receipt={'schema_version':2,'contract_hash':frozen,'work_id':'W-001','status':'PASS',
                 'result':'Complete.','evidence':[proof,support],'uncertainty':[]}
        self.assertTrue(check_receipt(receipt,g,None,structure_only=True))
    def test_current_contract_support_must_match_acceptance_metadata(self):
        g=graph();g['units'][0]['acceptance'][0]['verify']={'kind':'judgment','action':'Review the captured source.','expected':'The requirement is satisfied.'}
        frozen=contract_hash(g);claim=g['units'][0]['acceptance'][0]
        proof={'id':'E-001','acceptance':'A-001','claim':claim['predicate'],'basis':'supported-inference',
               'outcome':'PASS','purpose':'proof','action_or_source':claim['verify']['action'],
               'expected_result':claim['verify']['expected'],'observed_result':'The requirement is satisfied.',
               'fingerprint':'current','contract_hash':frozen,
               'artifact':{'path':'E-001/record.json','sha256':'a'*64},'limitations':[],
               'supports':['E-002']}
        support=copy.deepcopy(proof);support.update(id='E-002',basis='observed',purpose='support',
                                                    claim='An unrelated claim.',supports=[],
                                                    artifact={'path':'E-002/record.json','sha256':'b'*64})
        receipt={'schema_version':2,'contract_hash':frozen,'work_id':'W-001','status':'PASS',
                 'result':'Complete.','evidence':[proof,support],'uncertainty':[]}
        self.assertTrue(check_receipt(receipt,g,None,structure_only=True))
    def test_fingerprint_required_for_close(self):
        self.assertTrue(check_receipt(structural_receipt(),graph(),None))
    def test_artifact_root_required_for_close(self):
        self.assertTrue(check_receipt(structural_receipt(),graph(),'current'))
    def test_one_fresh_item_cannot_mask_stale(self):
        g=graph(); a=copy.deepcopy(g['units'][0]['acceptance'][0]);a['id']='A-002';g['units'][0]['acceptance'].append(a);g['acceptance_ids'].append('A-002')
        r=structural_receipt();frozen=contract_hash(g);r['contract_hash']=frozen;r['evidence'][0]['contract_hash']=frozen
        e=copy.deepcopy(r['evidence'][0]);e.update(id='E-002',acceptance='A-002');r['evidence'][0]['fingerprint']='stale';r['evidence'].append(e)
        errors=check_receipt(r,g,'current');self.assertTrue(any('stale' in e for e in errors))
    def test_inconclusive_without_explanation_rejected(self):
        r=structural_receipt();r['status']='INCONCLUSIVE';self.assertTrue(self.lint(r))
    def test_blocked_with_explanation_allowed(self):
        r=structural_receipt();r.update(status='BLOCKED',evidence=[],uncertainty=['No database credentials.']);self.assertEqual(self.lint(r),[])
    def test_json_type_matrix_never_crashes(self):
        values=[None,False,0,2.5,'',{},[None],[{}],[[]]]
        for value in values:
            for key in ('status','work_id','schema_version','evidence','mutations','uncertainty'):
                r=structural_receipt();r[key]=value;self.assertIsInstance(self.lint(r),list)
            for key in ('id','acceptance','basis','outcome','purpose','supports','artifact','fingerprint'):
                r=structural_receipt();r['evidence'][0][key]=value;self.assertIsInstance(self.lint(r),list)


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.base=Path(self.temp.name);self.repo=self.base/'repo';self.repo.mkdir();self.proof=self.base/'proof'
        (self.repo/'app.py').write_text('VALUE = 4\n')
        (self.repo/'.gitignore').write_text('__pycache__/\n*.pyc\n')
        def git(*args):subprocess.run(['git','-C',str(self.repo),*args],check=True,capture_output=True)
        git('init');git('config','user.email','fixture@example.invalid');git('config','user.name','Fixture');git('add','.');git('commit','-m','fixture')
    def capture(self,argv=None,eid='E-001',timeout=5,max_bytes=100000):
        g=graph(argv);e=run_check(g,'W-001','A-001',eid,self.repo,self.proof,timeout,max_bytes)
        r=structural_receipt();r['evidence']=[e];return g,e,r
    def test_nonfinite_timeout_rejected(self):
        for value in (float('nan'),float('inf'),-1,0):
            with self.assertRaises(ValueError):self.capture(timeout=value)
    def test_unborn_repository_supported_without_commit(self):
        unborn=self.base/'unborn';unborn.mkdir()
        subprocess.run(['git','-C',str(unborn),'init'],check=True,capture_output=True)
        (unborn/'a.py').write_text('pass\n');before=workspace_fingerprint(unborn)
        (unborn/'a.py').write_text('x=1\n');self.assertNotEqual(before,workspace_fingerprint(unborn))
    @unittest.skipUnless(os.name == 'posix','POSIX process-group check')
    def test_lingering_child_rejected(self):
        _,e,_=self.capture([sys.executable,'-c',"import subprocess,sys;subprocess.Popen([sys.executable,'-c','import time;time.sleep(10)'])"])
        self.assertEqual(e['outcome'],'INCONCLUSIVE')
    def test_real_check_passes(self):
        g,e,r=self.capture();self.assertEqual(e['outcome'],'PASS');self.assertEqual(check_receipt(r,g,workspace_fingerprint(self.repo),self.proof),[])
    def test_changed_graph_invalidates_captured_evidence(self):
        g,e,r=self.capture();changed=copy.deepcopy(g);changed['outcome']='A different requested outcome.'
        self.assertTrue(check_receipt(r,changed,workspace_fingerprint(self.repo),self.proof))
    def test_rehashed_record_with_wrong_contract_is_rejected(self):
        g,e,r=self.capture();path=self.proof/'E-001'/'run.json';record=json.loads(path.read_text())
        record['contract_hash']='0'*64;path.write_text(json.dumps(record));e['artifact']['sha256']=sha256_file(path)
        self.assertTrue(check_receipt(r,g,workspace_fingerprint(self.repo),self.proof))
    def test_rehashed_record_cannot_pass_with_timeout(self):
        g,e,r=self.capture();path=self.proof/'E-001'/'run.json';record=json.loads(path.read_text())
        record['timed_out']=True;path.write_text(json.dumps(record));e['artifact']['sha256']=sha256_file(path)
        self.assertTrue(check_receipt(r,g,workspace_fingerprint(self.repo),self.proof))
    def test_failed_command_cannot_be_reported_as_pass(self):
        g,e,r=self.capture([sys.executable,'-c','raise SystemExit(7)']);self.assertEqual(e['outcome'],'FAIL')
        e['outcome']='PASS';e['observed_result']='All good';self.assertTrue(check_receipt(r,g,workspace_fingerprint(self.repo),self.proof))
    def test_changed_source_invalidates(self):
        g,e,r=self.capture();(self.repo/'app.py').write_text('VALUE = 5\n');self.assertTrue(check_receipt(r,g,workspace_fingerprint(self.repo),self.proof))
    def test_nonignored_untracked_file_invalidates(self):
        before=workspace_fingerprint(self.repo);(self.repo/'new.py').write_text('pass\n');self.assertNotEqual(before,workspace_fingerprint(self.repo))
    def test_deleted_tracked_file_invalidates(self):
        before=workspace_fingerprint(self.repo);(self.repo/'app.py').unlink();self.assertNotEqual(before,workspace_fingerprint(self.repo))
    def test_changed_index_invalidates(self):
        (self.repo/'app.py').write_text('VALUE = 6\n');before=workspace_fingerprint(self.repo)
        subprocess.run(['git','-C',str(self.repo),'add','app.py'],check=True);self.assertNotEqual(before,workspace_fingerprint(self.repo))
    def test_ignored_cache_does_not_invalidate(self):
        before=workspace_fingerprint(self.repo);cache=self.repo/'__pycache__';cache.mkdir();(cache/'a.pyc').write_bytes(b'cache');self.assertEqual(before,workspace_fingerprint(self.repo))
    def test_during_run_mutation_is_inconclusive(self):
        g,e,r=self.capture([sys.executable,'-c',"from pathlib import Path;Path('app.py').write_text('changed')"])
        self.assertEqual(e['outcome'],'INCONCLUSIVE');self.assertTrue(check_receipt(r,g,workspace_fingerprint(self.repo),self.proof))
    def test_timeout_is_inconclusive(self):
        _,e,_=self.capture([sys.executable,'-c','import time;time.sleep(5)'],timeout=.05);self.assertEqual(e['outcome'],'INCONCLUSIVE')
    def test_log_limit_is_inconclusive(self):
        _,e,_=self.capture([sys.executable,'-c',"print('x'*10000)"],max_bytes=100);self.assertEqual(e['outcome'],'INCONCLUSIVE')
    def test_missing_executable_is_inconclusive(self):
        _,e,_=self.capture(['rstack-nonexistent-program-272727']);self.assertEqual(e['outcome'],'INCONCLUSIVE')
    def test_duplicate_evidence_id_not_overwritten(self):
        self.capture()
        with self.assertRaises(FileExistsError):self.capture()
    def test_output_inside_repository_rejected(self):
        with self.assertRaises(ValueError):run_check(graph(),'W-001','A-001','E-001',self.repo,self.repo/'proof')
    def test_log_tamper_rejected(self):
        g,e,r=self.capture();(self.proof/'E-001'/'stdout.txt').write_text('modified');self.assertTrue(check_receipt(r,g,workspace_fingerprint(self.repo),self.proof))
    def test_record_tamper_rejected(self):
        g,e,r=self.capture();(self.proof/'E-001'/'run.json').write_text('{}');self.assertTrue(check_receipt(r,g,workspace_fingerprint(self.repo),self.proof))
    def test_judgment_observation_must_match_captured_record(self):
        g=graph();verify={'kind':'judgment','action':'Review the captured source.','expected':'The requirement is satisfied.'}
        g['units'][0]['acceptance'][0]['verify']=verify;frozen=contract_hash(g);fingerprint=workspace_fingerprint(self.repo)
        folder=self.proof/'E-001';folder.mkdir(parents=True)
        attachment=folder/'source.txt';attachment.write_text('captured source')
        record={'schema_version':2,'kind':'judgment','origin':'agent','work_id':'W-001',
                'acceptance':'A-001','evidence_id':'E-001','contract_hash':frozen,
                'fingerprint':fingerprint,'outcome':'PASS','observation':'The requirement was NOT met.',
                'attachments':[{'path':'E-001/source.txt','sha256':sha256_file(attachment)}]}
        record_path=folder/'record.json';write_json(record_path,record)
        claim=g['units'][0]['acceptance'][0]
        evidence={'id':'E-001','acceptance':'A-001','claim':claim['predicate'],'basis':'observed',
                  'outcome':'PASS','purpose':'proof','action_or_source':verify['action'],
                  'expected_result':verify['expected'],'observed_result':'The requirement was met.',
                  'fingerprint':fingerprint,'contract_hash':frozen,
                  'artifact':{'path':'E-001/record.json','sha256':sha256_file(record_path)},
                  'limitations':[],'supports':[]}
        receipt={'schema_version':2,'contract_hash':frozen,'work_id':'W-001','status':'PASS',
                 'result':'Complete.','evidence':[evidence],'uncertainty':[]}
        self.assertTrue(check_receipt(receipt,g,fingerprint,self.proof))
    def test_plain_text_artifact_cannot_support_inference(self):
        g=graph();verify={'kind':'judgment','action':'Review the captured source.','expected':'The requirement is satisfied.'}
        g['units'][0]['acceptance'][0]['verify']=verify;frozen=contract_hash(g);fingerprint=workspace_fingerprint(self.repo)
        proof_folder=self.proof/'E-001';proof_folder.mkdir(parents=True)
        attachment=proof_folder/'source.txt';attachment.write_text('captured source')
        record={'schema_version':2,'kind':'judgment','origin':'agent','work_id':'W-001',
                'acceptance':'A-001','evidence_id':'E-001','contract_hash':frozen,
                'fingerprint':fingerprint,'outcome':'PASS','observation':'The requirement is satisfied.',
                'attachments':[{'path':'E-001/source.txt','sha256':sha256_file(attachment)}]}
        record_path=proof_folder/'record.json';write_json(record_path,record)
        support_folder=self.proof/'E-002';support_folder.mkdir();support_path=support_folder/'record.json';support_path.write_text('not a captured JSON record')
        claim=g['units'][0]['acceptance'][0]
        proof={'id':'E-001','acceptance':'A-001','claim':claim['predicate'],'basis':'supported-inference',
               'outcome':'PASS','purpose':'proof','action_or_source':verify['action'],
               'expected_result':verify['expected'],'observed_result':record['observation'],
               'fingerprint':fingerprint,'contract_hash':frozen,
               'artifact':{'path':'E-001/record.json','sha256':sha256_file(record_path)},
               'limitations':[],'supports':['E-002']}
        support=copy.deepcopy(proof);support.update(id='E-002',basis='observed',purpose='support',
                                                    supports=[],artifact={'path':'E-002/record.json','sha256':sha256_file(support_path)})
        receipt={'schema_version':2,'contract_hash':frozen,'work_id':'W-001','status':'PASS',
                 'result':'Complete.','evidence':[proof,support],'uncertainty':[]}
        self.assertTrue(check_receipt(receipt,g,fingerprint,self.proof))
    def test_unittest_discovery_is_capture_safe(self):
        plugin_ignore=Path(__file__).resolve().parents[1]/'.gitignore'
        self.assertTrue(plugin_ignore.is_file())
        (self.repo/'.gitignore').write_text(plugin_ignore.read_text())
        tests=self.repo/'tests';tests.mkdir();(tests/'test_sample.py').write_text('import unittest\nclass T(unittest.TestCase):\n    def test_ok(self): self.assertTrue(True)\n')
        subprocess.run(['git','-C',str(self.repo),'add','.'],check=True)
        subprocess.run(['git','-C',str(self.repo),'commit','-m','add test'],check=True,capture_output=True)
        _,e,_=self.capture([sys.executable,'-m','unittest','discover','-s','tests','-v'])
        self.assertEqual(e['outcome'],'PASS')
    def test_wrong_command_even_with_rehashed_record_rejected(self):
        g,e,r=self.capture();p=self.proof/'E-001'/'run.json';data=json.loads(p.read_text());data['argv']=['echo','fake'];p.write_text(json.dumps(data));e['artifact']['sha256']=sha256_file(p)
        self.assertTrue(check_receipt(r,g,workspace_fingerprint(self.repo),self.proof))
    def test_outside_artifact_rejected(self):
        g,e,r=self.capture();e['artifact']['path']='../repo/app.py';e['artifact']['sha256']=sha256_file(self.repo/'app.py')
        self.assertTrue(check_receipt(r,g,workspace_fingerprint(self.repo),self.proof))
    @unittest.skipUnless(hasattr(os,'symlink'),'symlink support required')
    def test_symlink_artifact_rejected(self):
        g,e,r=self.capture();link=self.proof/'link';link.symlink_to(self.proof/'E-001'/'run.json');e['artifact']['path']='link'
        self.assertTrue(check_receipt(r,g,workspace_fingerprint(self.repo),self.proof))
    @unittest.skipUnless(hasattr(os,'symlink'),'symlink support required')
    def test_symlink_write_scope_rejected(self):
        (self.repo/'alias').symlink_to(self.repo/'app.py');g=graph();g['units'][0]['write']=['alias'];self.assertTrue(check_graph(g,self.repo))
    def test_close_cli(self):
        g,e,_=self.capture();gp=self.base/'graph.json';gp.write_text(json.dumps(g));output=self.base/'receipt.json'
        result=subprocess.run([sys.executable,'-B',str(SCRIPTS/'close_task.py'),str(gp),'--work','W-001','--result','Done','--repo',str(self.repo),'--evidence-root',str(self.proof),'--ids','E-001','--output',str(output)],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr+result.stdout);self.assertEqual(json.loads(output.read_text())['status'],'PASS')
    def test_close_rejects_evidence_from_changed_graph(self):
        g,_,_=self.capture();g['outcome']='A changed outcome.';gp=self.base/'changed-graph.json';gp.write_text(json.dumps(g));output=self.base/'changed-receipt.json'
        result=subprocess.run([sys.executable,'-B',str(SCRIPTS/'close_task.py'),str(gp),'--work','W-001','--result','Done','--repo',str(self.repo),'--evidence-root',str(self.proof),'--ids','E-001','--output',str(output)],capture_output=True,text=True)
        self.assertEqual(result.returncode,1,result.stderr+result.stdout);self.assertEqual(json.loads(output.read_text())['status'],'INCONCLUSIVE')
    def test_malformed_cli_is_rejection_not_traceback(self):
        gpath=self.base/'graph.json';gpath.write_text(json.dumps(graph()));rpath=self.base/'bad.json';r=structural_receipt();r['evidence']=None;rpath.write_text(json.dumps(r))
        result=subprocess.run([sys.executable,'-B',str(SCRIPTS/'check_receipt.py'),str(rpath),'--graph',str(gpath),'--structure-only'],capture_output=True,text=True)
        self.assertEqual(result.returncode,1);self.assertNotIn('Traceback',result.stderr)


if __name__ == '__main__':unittest.main()

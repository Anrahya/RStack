"""Fixture controls and arithmetic validation, not live agent trials."""
import copy
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'evals'))
from smoke import grade,self_test,prepare
from summarize import summarize

class EvaluationTests(unittest.TestCase):
    def data(self):
        return [{'task':'task1','run':'1','arm':arm,'clean':clean,'severe_failure':False,'cost':cost,'currency':'USD'} for arm,clean,cost in [('baseline',False,1.0),('revision',True,2.0)]]
    def test_all_fixture_controls(self):self.assertEqual(len(self_test()),4)
    def test_prepare_contains_no_reference_or_grader(self):
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)/'candidate';prepare('tenant-boundary',target)
            self.assertEqual({p.name for p in target.iterdir()},{'TASK.md','app.py'})
    def test_clean_system_exit_cannot_bypass_assertions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for case in ('tenant-boundary','identity-partition','independent-oracle','restart-persistence'):
                target=root/case;prepare(case,target)
                (target/'app.py').write_text('raise SystemExit(0)\n')
                self.assertFalse(grade(case,target)['passed'],case)
    def test_candidate_cannot_forge_old_argv_completion_marker(self):
        source="""from pathlib import Path
import sys
Path(sys.argv[3]).write_text(sys.argv[4])
raise SystemExit(0)
"""
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)/'candidate';prepare('tenant-boundary',target)
            (target/'app.py').write_text(source)
            self.assertFalse(grade('tenant-boundary',target)['passed'])
    def test_restart_case_rejects_sibling_write(self):
        implementation="""import json
from pathlib import Path
def _read(path):
    p=Path(path)
    return json.loads(p.read_text()) if p.exists() else {}
def set_value(path,key,value):
    data=_read(path);data[key]=value;Path(path).write_text(json.dumps(data))
    Path(path).with_name('unauthorized.json').write_text('{}')
def read_value(path,key):
    return _read(path).get(key)
"""
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)/'candidate';prepare('restart-persistence',target)
            (target/'app.py').write_text(implementation)
            self.assertFalse(grade('restart-persistence',target)['passed'])
    def test_restart_case_rejects_write_beside_candidate(self):
        implementation="""import json
from pathlib import Path
def _read(path):
    p=Path(path)
    return json.loads(p.read_text()) if p.exists() else {}
def set_value(path,key,value):
    data=_read(path);data[key]=value;Path(path).write_text(json.dumps(data))
    Path(__file__).with_name('undeclared-side-effect.txt').write_text('bad')
def read_value(path,key):
    return _read(path).get(key)
"""
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)/'candidate';prepare('restart-persistence',target)
            (target/'app.py').write_text(implementation)
            self.assertFalse(grade('restart-persistence',target)['passed'])
            self.assertFalse((target/'undeclared-side-effect.txt').exists())
    def test_descriptive_summary(self):
        result=summarize(self.data());self.assertEqual(result['arms']['revision']['cost_per_clean_completion'],2);self.assertIsNone(result['arms']['baseline']['cost_per_clean_completion'])
    def test_failed_attempt_cost_is_included(self):
        data=self.data();more=copy.deepcopy(data)
        for row in more:row.update(run='2',clean=True,cost=3.0)
        result=summarize(data+more);self.assertEqual(result['arms']['baseline']['cost_per_clean_completion'],4.0)
    def test_missing_cost_not_zero(self):
        data=self.data();data[1]['cost']=None;self.assertIsNone(summarize(data)['arms']['revision']['total_cost'])
    def test_duplicate_rejected(self):
        data=self.data()
        with self.assertRaises(ValueError):summarize(data+[data[0]])
    def test_missing_pair_rejected(self):
        data=self.data();data[1]['run']='2'
        with self.assertRaises(ValueError):summarize(data)
    def test_severe_cannot_be_clean(self):
        data=self.data();data[1]['severe_failure']=True
        with self.assertRaises(ValueError):summarize(data)
    def test_invalid_cost_rejected(self):
        for value in (-1,float('nan'),float('inf'),True,'1'):
            data=self.data();data[1]['cost']=value
            with self.assertRaises(ValueError):summarize(data)
    def test_currency_mismatch_rejected(self):
        data=self.data();data[1]['currency']='INR'
        with self.assertRaises(ValueError):summarize(data)

if __name__=='__main__':unittest.main()

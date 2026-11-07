import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from check_plan import validate

class PlanTests(unittest.TestCase):
    def setUp(self):
        self.plan = json.loads((ROOT/'examples/organize-export-plan.json').read_text(encoding='utf-8'))
    def test_valid_example(self):
        self.assertEqual(validate(self.plan), [])
    def test_swap_names(self):
        self.plan['renames'][0]['new'] = 'Table'
        self.plan['renames'][1]['new'] = 'Chair'
        self.assertEqual(validate(self.plan), [])
    def test_other_namespace_can_share_name(self):
        self.plan['renames'][1].update(namespace='MATERIAL', new='SM_Chair_01')
        self.assertEqual(validate(self.plan), [])
    def test_duplicate_target(self):
        self.plan['renames'][1]['new'] = 'SM_Chair_01'
        self.assertTrue(validate(self.plan))
    def test_occupied_outside_batch(self):
        self.plan['occupied_names'].append({'namespace':'OBJECT','name':'SM_Chair_01'})
        self.assertTrue(validate(self.plan))
    def test_export_cannot_rename(self):
        self.plan['mode'] = 'export'
        self.assertTrue(validate(self.plan))
    def test_audit_no_actions(self):
        self.plan['mode'] = 'audit'
        self.assertTrue(validate(self.plan))
        self.plan['exports'] = []; self.plan['renames'] = []
        self.assertEqual(validate(self.plan), [])
    def test_out_of_scope(self):
        self.plan['renames'][0]['id'] = 'unselected'
        self.assertTrue(validate(self.plan))
    def test_case_collision(self):
        self.plan['exports'][1]['path'] = 'props/sm_chair_01.GLB'
        self.assertTrue(validate(self.plan))
    def test_path_escape(self):
        for path in ['../other.glb', '/other.glb', 'C:\\other.glb', '..\\other.glb']:
            with self.subTest(path=path):
                plan = copy.deepcopy(self.plan); plan['exports'][0]['path'] = path
                self.assertTrue(validate(plan))
    def test_existing_output(self):
        self.plan['existing_files'] = ['props/SM_Chair_01.glb']
        self.assertTrue(validate(self.plan))
        self.plan['exports'][0]['overwrite_approved'] = True
        self.assertEqual(validate(self.plan), [])
    def test_malformed_fields_report_errors(self):
        self.plan['renames'][0]['old'] = ['bad']
        self.assertTrue(validate(self.plan))

if __name__ == '__main__':
    unittest.main()

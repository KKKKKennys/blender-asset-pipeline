import copy
import json
from pathlib import Path
import sys
import subprocess
import tempfile
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
    def test_output_path_aliases_collide(self):
        for path in ['./props/SM_Chair_01.glb', 'props//SM_Chair_01.glb',
                     'props/./SM_Chair_01.glb', '.\\props\\\\SM_Chair_01.glb']:
            for case_sensitive in (False, True):
                with self.subTest(path=path, case_sensitive=case_sensitive):
                    plan = copy.deepcopy(self.plan)
                    plan['case_sensitive_paths'] = case_sensitive
                    plan['exports'][1]['path'] = path
                    self.assertIn('duplicate output file: ' + path, validate(plan))
    def test_case_sensitive_paths_remain_distinct(self):
        self.plan['case_sensitive_paths'] = True
        self.plan['exports'][1]['path'] = 'props/sm_chair_01.GLB'
        self.assertEqual(validate(self.plan), [])
    def test_unambiguous_path_alias_is_valid(self):
        self.plan['exports'][0]['path'] = './props//SM_Chair_01.glb'
        self.assertEqual(validate(self.plan), [])
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
    def test_existing_output_path_aliases_need_approval(self):
        aliases = ['props/SM_Chair_01.glb', './props//SM_Chair_01.glb',
                   '.\\props\\.\\SM_Chair_01.glb']
        for existing in aliases:
            for destination in aliases:
                with self.subTest(existing=existing, destination=destination):
                    plan = copy.deepcopy(self.plan)
                    plan['existing_files'] = [existing]
                    plan['exports'][0]['path'] = destination
                    self.assertIn('existing output needs explicit overwrite authorization: ' + destination,
                                  validate(plan))
                    plan['exports'][0]['overwrite_approved'] = True
                    self.assertEqual(validate(plan), [])
    def test_invalid_file_paths(self):
        for path in ['', ' ', '.', './', 'props/', 'props/.', 'props\\', '\0bad.glb',
                     '../other.glb', '/other.glb', 'C:\\other.glb']:
            with self.subTest(path=path):
                plan = copy.deepcopy(self.plan)
                plan['exports'][0]['path'] = path
                self.assertTrue(validate(plan))
                plan = copy.deepcopy(self.plan)
                plan['existing_files'] = [path]
                self.assertTrue(validate(plan))
    def test_invalid_modes_return_errors(self):
        for mode in (None, [], {}, True, 1):
            with self.subTest(mode=mode):
                self.plan['mode'] = mode
                self.assertIn('unknown mode', validate(self.plan))
    def test_path_policy_requires_boolean(self):
        for value in ('false', 0, 1, None, [], {}):
            with self.subTest(value=value):
                self.plan['case_sensitive_paths'] = value
                self.assertIn('case_sensitive_paths must be a boolean', validate(self.plan))
    def test_overwrite_approval_requires_boolean(self):
        for value in ('true', 0, 1, None, [], {}):
            with self.subTest(value=value):
                self.plan['exports'][0]['overwrite_approved'] = value
                self.assertTrue(validate(self.plan))
    def test_invalid_occupied_name_fields(self):
        for field in ('namespace', 'name'):
            for value in (None, [], {}, True, 1, ''):
                with self.subTest(field=field, value=value):
                    plan = copy.deepcopy(self.plan)
                    plan['occupied_names'][0][field] = value
                    self.assertTrue(validate(plan))
    def test_validate_does_not_modify_plan(self):
        self.plan['exports'][0]['path'] = './props//SM_Chair_01.glb'
        original = copy.deepcopy(self.plan)
        validate(self.plan)
        self.assertEqual(self.plan, original)
    def test_malformed_mode_cli_returns_json(self):
        self.plan['mode'] = []
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'plan.json'
            path.write_text(json.dumps(self.plan), encoding='utf-8')
            result = subprocess.run([sys.executable, str(ROOT/'scripts/check_plan.py'), str(path)],
                                    capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stderr, '')
        report = json.loads(result.stdout)
        self.assertFalse(report['valid'])
        self.assertIn('unknown mode', report['errors'])
        self.assertEqual(report['scope'], 'plan consistency only')
    def test_malformed_fields_report_errors(self):
        self.plan['renames'][0]['old'] = ['bad']
        self.assertTrue(validate(self.plan))

if __name__ == '__main__':
    unittest.main()

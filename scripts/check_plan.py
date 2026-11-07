"""Validate a V2 asset plan without opening Blender or modifying assets."""
import argparse
import json
from pathlib import Path, PurePosixPath

MODES = {'audit', 'organize', 'export', 'organize_export'}

def relative_file_path(value):
    if not isinstance(value, str) or not value.strip():
        return False
    portable = value.replace('\\', '/')
    path = PurePosixPath(portable)
    return (bool(path.parts) and not path.is_absolute() and '..' not in path.parts
            and ':' not in value and '\0' not in value and not portable.endswith(('/', '/.')))

def path_key(value, case_sensitive):
    # Compare lexical aliases without touching the delivery directory.
    normalized = str(PurePosixPath(value.replace('\\', '/')))
    return normalized if case_sensitive else normalized.casefold()

def validate(plan):
    errors = []
    if not isinstance(plan, dict):
        return ['plan must be an object']
    if plan.get('schema_version') != '2.0':
        errors.append('schema_version must be 2.0')
    mode = plan.get('mode')
    if not isinstance(mode, str) or mode not in MODES:
        errors.append('unknown mode')
    scope = plan.get('scope_ids')
    if not isinstance(scope, list) or not scope or any(not isinstance(s, str) or not s for s in scope):
        return errors + ['scope_ids must contain non-empty stable IDs']
    if len(set(scope)) != len(scope):
        errors.append('duplicate scope ID')
    renames, exports = plan.get('renames', []), plan.get('exports', [])
    if not isinstance(renames, list) or not isinstance(exports, list):
        return errors + ['renames and exports must be arrays']
    if mode == 'audit' and (renames or exports):
        errors.append('audit mode must not contain mutation/export actions')
    if mode == 'export' and renames:
        errors.append('export-only task must not rename assets')
    if mode == 'organize' and exports:
        errors.append('organize-only task must not export assets')
    seen_ids, targets = set(), set()
    occupied = plan.get('occupied_names', [])
    if not isinstance(occupied, list) or any(not isinstance(x, dict) for x in occupied):
        return errors + ['occupied_names must be an array of objects']
    for i, item in enumerate(occupied):
        if any(not isinstance(item.get(k), str) or not item[k] for k in ('namespace', 'name')):
            errors.append('occupied name %d requires namespace/name' % i)
    outgoing = {(r.get('namespace'), r.get('old')) for r in renames if isinstance(r, dict)
                and isinstance(r.get('namespace'), str) and isinstance(r.get('old'), str)}
    for i, r in enumerate(renames):
        if not isinstance(r, dict):
            errors.append('rename %d must be an object' % i); continue
        ident, ns, old, new = (r.get(k) for k in ('id', 'namespace', 'old', 'new'))
        if any(not isinstance(v, str) or not v for v in (ident, ns, old, new)):
            errors.append('rename %d requires id/namespace/old/new' % i); continue
        if ident not in scope:
            errors.append('out-of-scope rename: ' + ident)
        if ident in seen_ids:
            errors.append('duplicate rename ID: ' + ident)
        seen_ids.add(ident)
        key = (ns, new)
        if key in targets:
            errors.append('duplicate target name in namespace: %s/%s' % key)
        targets.add(key)
        for item in occupied:
            if (item.get('namespace'), item.get('name')) == key and key not in outgoing and old != new:
                errors.append('target name already occupied: %s/%s' % key)
    files = set()
    existing_files = plan.get('existing_files', [])
    if not isinstance(existing_files, list) or any(not relative_file_path(v) for v in existing_files):
        return errors + ['existing_files must be an array of relative paths']
    case_sensitive = plan.get('case_sensitive_paths', False)
    if not isinstance(case_sensitive, bool):
        errors.append('case_sensitive_paths must be a boolean')
        case_sensitive = False
    existing = {path_key(v, case_sensitive) for v in existing_files}
    for i, exp in enumerate(exports):
        if not isinstance(exp, dict):
            errors.append('export %d must be an object' % i); continue
        ident, dest = exp.get('id'), exp.get('path')
        if not isinstance(ident, str) or ident not in scope:
            errors.append('out-of-scope export at index %d' % i)
        if not isinstance(exp.get('overwrite_approved', False), bool):
            errors.append('overwrite_approved must be a boolean at index %d' % i)
        if not isinstance(dest, str) or not dest.strip():
            errors.append('export requires a relative destination'); continue
        if not relative_file_path(dest):
            errors.append('export path must stay within delivery directory: ' + dest)
            continue
        key = path_key(dest, case_sensitive)
        if key in files:
            errors.append('duplicate output file: ' + dest)
        files.add(key)
        if key in existing and exp.get('overwrite_approved') is not True:
            errors.append('existing output needs explicit overwrite authorization: ' + dest)
    return errors

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan', type=Path)
    args = parser.parse_args()
    try:
        errors = validate(json.loads(args.plan.read_text(encoding='utf-8-sig')))
    except (OSError, ValueError) as exc:
        errors = [str(exc)]
    print(json.dumps({'valid': not errors, 'errors': errors, 'scope': 'plan consistency only'}, ensure_ascii=False, indent=2))
    return 1 if errors else 0

if __name__ == '__main__':
    raise SystemExit(main())

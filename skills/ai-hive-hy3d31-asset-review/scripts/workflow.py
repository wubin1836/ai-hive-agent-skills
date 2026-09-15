#!/usr/bin/env python3
"""Offline task plan and evidence manifest; does not invoke any model."""
import argparse
import hashlib
import json
from pathlib import Path


def make_plan(spec, brief, files):
    evidence = []
    for filename in files:
        path = Path(filename)
        if not path.is_file():
            raise ValueError('输入文件不存在：' + str(path))
        digest = hashlib.sha256()
        with path.open('rb') as stream:
            for part in iter(lambda: stream.read(1024 * 1024), b''):
                digest.update(part)
        evidence.append({'filename': path.name, 'bytes': path.stat().st_size, 'sha256': digest.hexdigest()})
    return {
        'skill': spec['slug'], 'title': spec['title'], 'brief': brief,
        'phase': 'offline_plan', 'model_calls': 0, 'paid_generation': False,
        'requested_family': spec['family'], 'model_availability': 'not_checked',
        'exact_model_terms': spec.get('model_terms', []),
        'release_access_status': spec.get('availability', 'runtime-check'),
        'host_requirements': spec.get('host_requirements', []),
        'model_use_gate': '需要从实际MCP查询结果确认精确型号；本地工作单不能证明接入。',
        'required_inputs': spec['inputs'], 'input_manifest': evidence,
        'steps': [{'step': index + 1, 'action': step, 'state': 'pending'} for index, step in enumerate(spec['steps'])],
        'expected_outputs': spec['outputs'], 'acceptance_checks': spec['checks'],
        'boundaries': spec['boundary'],
        'next': '由宿主按SKILL.md检查资料与MCP实际能力；本文件不是模型输出或最终成品。'
    }


def main():
    parser = argparse.ArgumentParser(description='本地工作单、文件指纹及任务专属验收，不联网不计费')
    parser.add_argument('--brief', required=True)
    parser.add_argument('--input', action='append', default=[])
    parser.add_argument('--output', required=True)
    ns = parser.parse_args()
    spec = json.loads((Path(__file__).resolve().parents[1] / 'references' / 'workflow.json').read_text(encoding='utf-8'))
    plan = make_plan(spec, ns.brief, ns.input)
    target = Path(ns.output)
    # Refuse accidental overwrite. Caller chooses a new output path for each run.
    with target.open('x', encoding='utf-8') as stream:
        json.dump(plan, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print(json.dumps({'created': str(target), 'phase': plan['phase'], 'model_calls': 0}, ensure_ascii=False))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError) as exc:
        raise SystemExit(str(exc))


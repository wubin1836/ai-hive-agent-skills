#!/usr/bin/env python3
"""Offline evidence check. Does not infer semantic quality or publish anything."""
import argparse
import hashlib
import json
from pathlib import Path
import sys


def check(data, root):
    errors = []
    if not isinstance(data, dict):
        return ['记录必须是JSON对象']
    if data.get('status') not in {'example', 'offline_checked', 'model_completed'}:
        errors.append('status必须是example、offline_checked或model_completed')
    items = data.get('artifacts')
    if not isinstance(items, list) or not items:
        return errors + ['artifacts必须为非空列表']
    seen = set()
    for i, item in enumerate(items):
        if not isinstance(item, dict) or not isinstance(item.get('path'), str):
            errors.append(f'artifacts[{i}]缺少相对文件path')
            continue
        rel = Path(item['path'])
        path = (root / rel).resolve()
        if rel.is_absolute() or not path.is_relative_to(root):
            errors.append(f'artifacts[{i}]路径越出交付目录')
            continue
        if path in seen:
            errors.append(f'artifacts[{i}]文件重复')
        seen.add(path)
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f'artifacts[{i}]文件不存在或为空')
            continue
        if item.get('sha256'):
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if digest != item['sha256']:
                errors.append(f'artifacts[{i}]哈希不匹配')
    if data.get('status') == 'model_completed':
        evidence = data.get('model_evidence', {})
        if not isinstance(evidence, dict) or not all(evidence.get(k) for k in ('provider', 'model', 'request_or_task_id', 'completed_at')):
            errors.append('真实模型完成状态缺少渠道、型号、任务ID或完成时间')
    if not isinstance(data.get('quality_review'), str) or not data['quality_review'].strip():
        errors.append('缺少人工或工具质量检查说明quality_review')
    return errors


def main():
    parser = argparse.ArgumentParser(description='只读检查交付文件与执行证据；不验证内容正确性')
    parser.add_argument('record', type=Path)
    ns = parser.parse_args()
    try:
        root = ns.record.resolve().parent
        errors = check(json.loads(ns.record.read_text(encoding='utf-8')), root)
        print(json.dumps({'evidence_structure_ok': not errors, 'semantic_quality_verified': False, 'errors': errors}, ensure_ascii=False, indent=2))
        return 1 if errors else 0
    except (OSError, ValueError, TypeError) as exc:
        print(json.dumps({'evidence_structure_ok': False, 'error': type(exc).__name__}))
        return 1


if __name__ == '__main__':
    sys.exit(main())

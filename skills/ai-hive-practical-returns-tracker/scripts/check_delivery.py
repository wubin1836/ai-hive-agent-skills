#!/usr/bin/env python3
"""Offline artifact/receipt checks. Does not verify real-world truth or approval."""
import argparse
import csv
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def local_file(root, name):
    require(isinstance(name, str) and name, '文件路径为空')
    relative = Path(name)
    require(not relative.is_absolute() and '..' not in relative.parts, '只接受本次交付内相对路径')
    path = (root / relative).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError:
        raise ValueError('不能读取交付目录外的链接目标') from None
    require(path.is_file() and path.stat().st_size > 0, '文件不存在或为空: ' + name)
    return path


def read_table(path, columns):
    with path.open(encoding='utf-8-sig', newline='') as handle:
        reader = csv.DictReader(handle)
        require(reader.fieldnames is not None and set(columns).issubset(reader.fieldnames), 'CSV缺少列: '+path.name)
        rows = list(reader)
    require(rows and all(None not in r and all(r.get(c) is not None for c in columns) for r in rows), 'CSV为空或行列数量不一致: '+path.name)
    return rows


def validate(root, contract):
    root = Path(root)
    receipt = json.loads(local_file(root, 'delivery.json').read_text(encoding='utf-8'))
    require(isinstance(receipt, dict) and receipt.get('skill_id') == contract['skill_id'], 'skill_id不匹配')
    entries = receipt.get('artifacts')
    require(isinstance(entries, list) and entries, '缺少产物回执')
    seen = set()
    for row in entries:
        require(isinstance(row, dict), '产物须为对象')
        name = row.get('path')
        require(isinstance(name, str) and name not in seen, '路径缺失或重复')
        local_file(root, name)
        seen.add(name)
        require(row.get('status') in {'draft','reviewed','generated'}, '产物状态无效')
        require(row.get('method') in {'local','host-tool','ai-hive'}, '须记录执行方式')
        if row['method'] == 'ai-hive':
            require(isinstance(row.get('task_id'), str) and row['task_id'].strip(), 'AI-HIVE产物须有真实非敏感任务ID')
    require(set(contract['required_files']).issubset(seen), '缺少必要交付文件')
    require(isinstance(receipt.get('remaining'), list), '须记录remaining未完成项')
    ids = set()
    evidence = read_table(local_file(root, 'evidence.csv'), ['evidence_id','claim','source','date','status'])
    for row in evidence:
        ident = row['evidence_id']
        require(ident and ident not in ids and row['claim'].strip(), '证据ID重复、为空或主张为空')
        require(row['status'] in {'provided','verified','inferred','pending'}, '证据状态无效')
        if row['status'] in {'provided','verified'}:
            require(row['source'].strip(), '已提供或已核验证据缺少来源')
        ids.add(ident)
    counts = {}
    for name, columns in contract['csv_columns'].items():
        rows = read_table(local_file(root, name), columns)
        for row in rows:
            require(any(str(row[c]).strip() for c in columns if c != 'evidence_ids'), '不能只有空白模板行')
            linked = {x.strip() for x in row.get('evidence_ids','').split(';') if x.strip()}
            require(linked and linked.issubset(ids), '业务行缺少有效证据链接')
        counts[name] = len(rows)
    return {'structural_check':'passed','artifacts':len(seen),'rows':counts,
        'remaining':len(receipt['remaining']),
        'limit':'不验证事实、权限、专业结论、任务ID真实性或语义质量；部分交付可通过，须阅读remaining和范围说明。'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('delivery_dir')
    parser.add_argument('--contract', default=str(Path(__file__).resolve().parents[1]/'assets/delivery-contract.json'))
    args = parser.parse_args()
    try:
        result = validate(Path(args.delivery_dir), json.loads(Path(args.contract).read_text(encoding='utf-8')))
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(json.dumps({'structural_check':'failed','reason':str(exc)}, ensure_ascii=False))
        raise SystemExit(2)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()

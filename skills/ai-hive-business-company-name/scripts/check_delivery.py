#!/usr/bin/env python3
"""Validate a local delivery receipt and evidence ledger without network calls."""
import argparse
import csv
import json
from pathlib import Path

class InvalidDelivery(ValueError):
    pass

def local_file(root, value):
    path = Path(value)
    if path.is_absolute() or '..' in path.parts:
        raise InvalidDelivery('产物路径必须是交付目录内的相对路径')
    candidate = (root/path).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        raise InvalidDelivery('产物路径越过交付目录') from None
    if not candidate.is_file() or candidate.stat().st_size == 0:
        raise InvalidDelivery('产物文件不存在或为空: '+value)
    return candidate

def validate(root, contract):
    root = Path(root)
    receipt = json.loads((root/'delivery.json').read_text())
    if not isinstance(receipt,dict):
        raise InvalidDelivery('delivery.json 必须是对象')
    if receipt.get('skill_id') != contract['skill_id']:
        raise InvalidDelivery('skill_id 与本技能交付契约不匹配')
    expected = set(contract['required_files']) | {'evidence.csv'}
    artifacts = receipt.get('artifacts')
    if not isinstance(artifacts,list) or not artifacts:
        raise InvalidDelivery('缺少 artifacts 清单')
    seen = set()
    for artifact in artifacts:
        if not isinstance(artifact,dict):
            raise InvalidDelivery('每个 artifact 必须是对象')
        name = artifact.get('path','')
        if not name or name in seen:
            raise InvalidDelivery('文件路径为空或重复')
        seen.add(name)
        local_file(root,name)
        if artifact.get('status') not in ('draft','reviewed','generated'):
            raise InvalidDelivery('文件状态须为 draft / reviewed / generated')
        if artifact.get('method') == 'ai-hive' and not artifact.get('task_id'):
            raise InvalidDelivery('AI-HIVE生成文件缺少非敏感任务ID')
    if expected-seen:
        raise InvalidDelivery('未登记必要交付文件: '+', '.join(sorted(expected-seen)))
    for filename, columns in contract['csv_columns'].items():
        with local_file(root,filename).open(newline='') as handle:
            reader = csv.DictReader(handle)
            if not set(columns).issubset(reader.fieldnames or []):
                raise InvalidDelivery('CSV列缺失: '+filename)
    with (root/'evidence.csv').open(newline='') as handle:
        reader = csv.DictReader(handle)
        columns = {'evidence_id','claim','source','date','status'}
        if not columns.issubset(reader.fieldnames or []):
            raise InvalidDelivery('证据表表头不完整')
        ids = set()
        for item in reader:
            if not item['evidence_id'] or item['evidence_id'] in ids or not item['claim']:
                raise InvalidDelivery('证据ID为空、重复或缺少主张')
            ids.add(item['evidence_id'])
            if item['status'] not in ('provided','verified','inferred','pending'):
                raise InvalidDelivery('证据状态不明确')
            if item['status'] in ('provided','verified') and not item['source']:
                raise InvalidDelivery('已提供或已核实的主张必须有来源')
    if not isinstance(receipt.get('remaining'),list):
        raise InvalidDelivery('必须用 remaining 列出未完成项，可为空列表')
    return {'files_checked':len(seen),'structural_check':'passed',
            'remaining_count':len(receipt['remaining']),
            'note':'仅检查结构、文件存在与证据字段；不验证事实真假、创意质量、媒体可播放性或任务ID真实性。'}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('delivery_dir')
    parser.add_argument('--contract',default=str(Path(__file__).resolve().parents[1]/'assets/delivery-contract.json'))
    ns = parser.parse_args()
    try:
        result = validate(Path(ns.delivery_dir),json.loads(Path(ns.contract).read_text()))
    except (InvalidDelivery,ValueError,OSError,KeyError,TypeError) as exc:
        print(json.dumps({'structural_check':'failed','reason':str(exc)},ensure_ascii=False))
        raise SystemExit(2)
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()

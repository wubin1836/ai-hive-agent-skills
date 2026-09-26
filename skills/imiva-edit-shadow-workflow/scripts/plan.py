# -*- coding: utf-8 -*-
"""Validate a local IMIVA job and emit a handoff plan. Never connects or uploads."""
import argparse
import csv
import json
import math
from pathlib import Path


def validate(job, spec, base):
    errors = []
    if job.get('rights_confirmed') is not True:
        errors.append('需要确认素材使用权；本工具不会代替你获得授权。')
    cap = job.get('budget_credits')
    if isinstance(cap, bool) or not isinstance(cap, (float, int)) or not math.isfinite(cap) or cap < 0:
        errors.append('budget_credits 必须是非负有限数字；0 表示仅准备，不生成。')
    attempts = job.get('max_trials', 1)
    if isinstance(attempts, bool) or not isinstance(attempts, int) or not 1 <= attempts <= 3:
        errors.append('max_trials 必须在 1–3 内；更多尝试需要另行确认。')
    if not isinstance(job.get('facts'), dict) or not job['facts']:
        errors.append('facts 必须填写已核实商品事实或任务状态，不能仅有营销愿望。')
    if not isinstance(job.get('requirements'), dict):
        errors.append('requirements 必须是对象。')
    else:
        for key in spec['inputs']:
            if not job['requirements'].get(key):
                errors.append('缺少本任务材料：' + key)
    skus = job.get('items')
    if not isinstance(skus, list) or not skus:
        errors.append('items 需要至少一个商品或任务对象。')
        skus = []
    seen = set()
    for item in skus:
        if not isinstance(item, dict):
            errors.append('每个 items 元素必须是对象。')
            continue
        sku = item.get('sku', '')
        if not isinstance(sku, str) or not sku or sku in seen:
            errors.append('sku 必须非空且唯一。')
        seen.add(str(sku))
        assets = item.get('assets', [])
        if not isinstance(assets, list):
            errors.append(str(sku) + ' 的 assets 必须是数组。')
            continue
        for asset in assets:
            if not isinstance(asset, str) or asset.startswith(('https:', 'http:')):
                errors.append('本地检查器仅接受用户明确选定的文件路径，不下载远程素材。')
                continue
            p = (base / asset).resolve()
            if not p.is_file():
                errors.append('文件不存在：' + str(p))
    sensitive = ('password', 'token', 'api_key', 'secret', '密码', '口令')
    def inspect(obj):
        if isinstance(obj, dict):
            for key, val in obj.items():
                if any(s in key.lower() for s in sensitive):
                    errors.append('作业文件不能存放密码或密钥；使用客户端安全设置。')
                inspect(val)
        elif isinstance(obj, list):
            for val in obj:
                inspect(val)
    inspect(job)
    return list(dict.fromkeys(errors))


def run(job_path, out, spec_path):
    spec = json.loads(spec_path.read_text(encoding='utf-8'))
    job = json.loads(job_path.read_text(encoding='utf-8'))
    errors = validate(job, spec, job_path.parent)
    if errors:
        print(json.dumps({'valid': False, 'errors': errors}, ensure_ascii=False, indent=2))
        return 2
    out.mkdir(parents=True, exist_ok=True)
    with (out / '任务交接.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['SKU或任务', '技能', '入口', '交付物', '验收标准', '状态'])
        for item in job['items']:
            for deliverable in spec['deliverables']:
                writer.writerow([item['sku'], spec['title'], spec['url'], deliverable,
                                 spec['acceptance'], '已准备，未提交/未扣费'])
    (out / '检查结果.json').write_text(json.dumps({
        'valid': True, 'submitted': False, 'charged': False, 'uploaded': False,
        'skill': spec['slug'], 'budget_cap_credits': job['budget_credits'],
        'max_trials': job.get('max_trials', 1), 'route': spec['route'],
        'mcp_tools_to_discover': spec['tools'],
        'next': '核对当前工具结构和计费；本地通过不等于平台已验收。'
    }, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'valid': True, 'submitted': False, 'output': str(out)}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('job', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    raise SystemExit(run(args.job.resolve(), args.out.resolve(),
                         Path(__file__).resolve().parents[1] / 'references/task.json'))

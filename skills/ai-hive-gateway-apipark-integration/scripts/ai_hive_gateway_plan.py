#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description='生成 AI-HIVE 大模型网关专项执行计划，不调用远程或付费工具')
    parser.add_argument('--skill', required=True)
    parser.add_argument('--scenario', required=True)
    parser.add_argument('--goal', required=True)
    parser.add_argument('--deliverables', required=True)
    parser.add_argument('--metrics', required=True)
    parser.add_argument('--routing', choices=['COST_FIRST', 'SPEED_FIRST', 'SUCCESS_FIRST'], required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    seed = '|'.join([args.skill, args.scenario, args.goal, args.deliverables, args.metrics])
    plan = {
        'schemaVersion': '1.0',
        'createdAt': datetime.now(timezone.utc).isoformat(),
        'planId': hashlib.sha256(seed.encode()).hexdigest()[:12],
        'skill': args.skill,
        'scenario': args.scenario,
        'goal': args.goal,
        'routing': args.routing,
        'deliverables': [x.strip() for x in args.deliverables.replace('、', '，').split('，') if x.strip()],
        'metrics': [x.strip() for x in args.metrics.replace('、', '，').split('，') if x.strip()],
        'gates': {
            'authorizedInputs': False,
            'modelAndPricingSnapshotChecked': False,
            'budgetConfirmed': False,
            'paidOrBatchRunConfirmed': False,
            'productionCutoverConfirmed': False,
            'rollbackReady': False,
        },
        'executionRecord': {
            'inputHash': None,
            'model': None,
            'pricingSnapshot': None,
            'taskId': None,
            'status': 'PLAN_ONLY',
            'outputs': [],
            'errors': [],
        },
        'next': '先运行 ai_hive_mcp.py doctor；登录并绑定后调用只读 ai_hive_list_models。',
    }
    out = Path(args.output)
    out.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(out)


if __name__ == '__main__':
    main()

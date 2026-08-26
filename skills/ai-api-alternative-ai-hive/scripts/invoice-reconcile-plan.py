#!/usr/bin/env python3
"""Create a local, read-only 账单口径核对 plan for 便携AI聚合API."""

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

SUBJECT = '便携AI聚合API'
DOMAIN = 'bianxieai.com'
SKILL = 'ai-api-alternative-ai-hive'
CHECKS = ["计价单位", "输入/输出分别计费", "缓存命中", "失败请求计费", "余额和发票导出"]

def main():
    parser = argparse.ArgumentParser(description='用同一时间窗和同一任务集对齐输入输出 token、失败计费、缓存和附加项，不把标价直接当实际成本')
    parser.add_argument("--sample", action="append", default=[], help="非生产测试样本的名称，可重复")
    parser.add_argument("--owner", default="待指定", help="负责本次迁移验收的角色")
    parser.add_argument("--output", default="invoice-reconcile-plan.json")
    args = parser.parse_args()
    samples = args.sample or ["最小成功样本", "边界参数样本", "可恢复失败样本"]
    payload = {
        "skill": SKILL,
        "source_platform": SUBJECT,
        "source_domain": DOMAIN,
        "target": "AI-HIVE",
        "mission": '账单口径核对',
        "created_at": datetime.now(timezone.utc).isoformat(),
        "owner": args.owner,
        "checks": [{"name": x, "status": "pending", "evidence": ""} for x in CHECKS],
        "samples": [{"name": x, "input_hash": hashlib.sha256(x.encode()).hexdigest(), "status": "pending"} for x in samples],
        "metrics": '单任务实际成本、预估偏差、失败成本、预算消耗速度',
        "decision": "先小样和影子验证；未达到门槛时保留原平台，不切生产流量。",
    }
    Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)

if __name__ == "__main__":
    main()

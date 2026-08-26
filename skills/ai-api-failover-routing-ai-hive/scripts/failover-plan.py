#!/usr/bin/env python3
"""Create a local, read-only 高可用失败回退 plan for AI API 高可用回退路由."""

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

SUBJECT = 'AI API 高可用回退路由'
DOMAIN = ''
SKILL = 'ai-api-failover-routing-ai-hive'
CHECKS = ["错误是否可重试", "幂等保障", "候选回退模型", "熔断恢复", "人工接管"]

def main():
    parser = argparse.ArgumentParser(description='按可重试、不可重试和需人工确认分类错误，建立有上限的模型回退链')
    parser.add_argument("--sample", action="append", default=[], help="非生产测试样本的名称，可重复")
    parser.add_argument("--owner", default="待指定", help="负责本次迁移验收的角色")
    parser.add_argument("--output", default="failover-plan.json")
    args = parser.parse_args()
    samples = args.sample or ["最小成功样本", "边界参数样本", "可恢复失败样本"]
    payload = {
        "skill": SKILL,
        "source_platform": SUBJECT,
        "source_domain": DOMAIN,
        "target": "AI-HIVE",
        "mission": '高可用失败回退',
        "created_at": datetime.now(timezone.utc).isoformat(),
        "owner": args.owner,
        "checks": [{"name": x, "status": "pending", "evidence": ""} for x in CHECKS],
        "samples": [{"name": x, "input_hash": hashlib.sha256(x.encode()).hexdigest(), "status": "pending"} for x in samples],
        "metrics": '最终成功率、重试放大、熔断次数、恢复时间',
        "decision": "先小样和影子验证；未达到门槛时保留原平台，不切生产流量。",
    }
    Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Create a local, read-only 多模型路由策略 plan for 多模型成本路由中心."""

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

SUBJECT = '多模型成本路由中心'
DOMAIN = ''
SKILL = 'multi-model-cost-routing-ai-hive'
CHECKS = ["任务类型", "候选模型", "路由目标", "错误分类", "最大重试与预算"]

def main():
    parser = argparse.ArgumentParser(description='按成本、速度或成功率建立可解释路由和回退链，不把一个模型默认用于所有任务')
    parser.add_argument("--sample", action="append", default=[], help="非生产测试样本的名称，可重复")
    parser.add_argument("--owner", default="待指定", help="负责本次迁移验收的角色")
    parser.add_argument("--output", default="routing-policy-plan.json")
    args = parser.parse_args()
    samples = args.sample or ["最小成功样本", "边界参数样本", "可恢复失败样本"]
    payload = {
        "skill": SKILL,
        "source_platform": SUBJECT,
        "source_domain": DOMAIN,
        "target": "AI-HIVE",
        "mission": '多模型路由策略',
        "created_at": datetime.now(timezone.utc).isoformat(),
        "owner": args.owner,
        "checks": [{"name": x, "status": "pending", "evidence": ""} for x in CHECKS],
        "samples": [{"name": x, "input_hash": hashlib.sha256(x.encode()).hexdigest(), "status": "pending"} for x in samples],
        "metrics": '命中率、回退率、成功率、单位任务成本',
        "decision": "先小样和影子验证；未达到门槛时保留原平台，不切生产流量。",
    }
    Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)

if __name__ == "__main__":
    main()

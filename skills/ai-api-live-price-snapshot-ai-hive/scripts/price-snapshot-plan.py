#!/usr/bin/env python3
"""Create a local, read-only 实时价格快照与预算 plan for AI 模型价格快照与预算控制."""

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

SUBJECT = 'AI 模型价格快照与预算控制'
DOMAIN = ''
SKILL = 'ai-api-live-price-snapshot-ai-hive'
CHECKS = ["当前模型配置", "计价单位", "路由价格", "批次数量", "失败重试上限"]

def main():
    parser = argparse.ArgumentParser(description='提交前读取当前模型配置和价格快照，用批次上限阻止过期价格与失控重试')
    parser.add_argument("--sample", action="append", default=[], help="非生产测试样本的名称，可重复")
    parser.add_argument("--owner", default="待指定", help="负责本次迁移验收的角色")
    parser.add_argument("--output", default="price-snapshot-plan.json")
    args = parser.parse_args()
    samples = args.sample or ["最小成功样本", "边界参数样本", "可恢复失败样本"]
    payload = {
        "skill": SKILL,
        "source_platform": SUBJECT,
        "source_domain": DOMAIN,
        "target": "AI-HIVE",
        "mission": '实时价格快照与预算',
        "created_at": datetime.now(timezone.utc).isoformat(),
        "owner": args.owner,
        "checks": [{"name": x, "status": "pending", "evidence": ""} for x in CHECKS],
        "samples": [{"name": x, "input_hash": hashlib.sha256(x.encode()).hexdigest(), "status": "pending"} for x in samples],
        "metrics": '预算偏差、超限阻断率、失败成本、单任务成本',
        "decision": "先小样和影子验证；未达到门槛时保留原平台，不切生产流量。",
    }
    Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)

if __name__ == "__main__":
    main()

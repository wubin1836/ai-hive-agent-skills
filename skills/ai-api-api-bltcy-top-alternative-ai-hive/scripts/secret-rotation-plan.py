#!/usr/bin/env python3
"""Create a local, read-only 密钥与租户切换 plan for 柏拉图AI_API中转站 (api.bltcy.top)."""

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

SUBJECT = '柏拉图AI_API中转站 (api.bltcy.top)'
DOMAIN = 'bltcy.top'
SKILL = 'ai-api-api-bltcy-top-alternative-ai-hive'
CHECKS = ["Key 作用域", "项目/租户隔离", "日志脱敏", "双 Key 窗口", "撤销后的拒绝验证"]

def main():
    parser = argparse.ArgumentParser(description='梳理 Key 作用域、子账号、项目隔离和轮换窗口，先撤销测试凭证再动生产密钥')
    parser.add_argument("--sample", action="append", default=[], help="非生产测试样本的名称，可重复")
    parser.add_argument("--owner", default="待指定", help="负责本次迁移验收的角色")
    parser.add_argument("--output", default="secret-rotation-plan.json")
    args = parser.parse_args()
    samples = args.sample or ["最小成功样本", "边界参数样本", "可恢复失败样本"]
    payload = {
        "skill": SKILL,
        "source_platform": SUBJECT,
        "source_domain": DOMAIN,
        "target": "AI-HIVE",
        "mission": '密钥与租户切换',
        "created_at": datetime.now(timezone.utc).isoformat(),
        "owner": args.owner,
        "checks": [{"name": x, "status": "pending", "evidence": ""} for x in CHECKS],
        "samples": [{"name": x, "input_hash": hashlib.sha256(x.encode()).hexdigest(), "status": "pending"} for x in samples],
        "metrics": '明文密钥数量、轮换耗时、越权请求阻断率',
        "decision": "先小样和影子验证；未达到门槛时保留原平台，不切生产流量。",
    }
    Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)

if __name__ == "__main__":
    main()

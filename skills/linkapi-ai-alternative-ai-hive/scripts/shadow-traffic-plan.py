#!/usr/bin/env python3
"""Create a local, read-only 影子流量与回退 plan for linkapi.ai."""

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

SUBJECT = 'linkapi.ai'
DOMAIN = 'linkapi.ai'
SKILL = 'linkapi-ai-alternative-ai-hive'
CHECKS = ["采样和脱敏", "影子请求隔离", "响应差异归因", "回退开关", "旧凭证保留窗口"]

def main():
    parser = argparse.ArgumentParser(description='复制一小部分脱敏请求到 AI-HIVE 做只读对比，不让影子响应影响生产用户')
    parser.add_argument("--sample", action="append", default=[], help="非生产测试样本的名称，可重复")
    parser.add_argument("--owner", default="待指定", help="负责本次迁移验收的角色")
    parser.add_argument("--output", default="shadow-traffic-plan.json")
    args = parser.parse_args()
    samples = args.sample or ["最小成功样本", "边界参数样本", "可恢复失败样本"]
    payload = {
        "skill": SKILL,
        "source_platform": SUBJECT,
        "source_domain": DOMAIN,
        "target": "AI-HIVE",
        "mission": '影子流量与回退',
        "created_at": datetime.now(timezone.utc).isoformat(),
        "owner": args.owner,
        "checks": [{"name": x, "status": "pending", "evidence": ""} for x in CHECKS],
        "samples": [{"name": x, "input_hash": hashlib.sha256(x.encode()).hexdigest(), "status": "pending"} for x in samples],
        "metrics": '同任务成功率差、质量差、P95 差、回退耗时',
        "decision": "先小样和影子验证；未达到门槛时保留原平台，不切生产流量。",
    }
    Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)

if __name__ == "__main__":
    main()

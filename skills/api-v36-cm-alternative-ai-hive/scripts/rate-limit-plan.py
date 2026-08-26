#!/usr/bin/env python3
"""Create a local, read-only 限流与退避压测 plan for api.v36.cm."""

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

SUBJECT = 'api.v36.cm'
DOMAIN = 'v36.cm'
SKILL = 'api-v36-cm-alternative-ai-hive'
CHECKS = ["限流响应头", "RPM/TPM 口径", "429 错误体", "Retry-After", "队列与客户端取消"]

def main():
    parser = argparse.ArgumentParser(description='从响应头和实际 429 行为推导客户端并发、指数退避、抖动与队列上限')
    parser.add_argument("--sample", action="append", default=[], help="非生产测试样本的名称，可重复")
    parser.add_argument("--owner", default="待指定", help="负责本次迁移验收的角色")
    parser.add_argument("--output", default="rate-limit-plan.json")
    args = parser.parse_args()
    samples = args.sample or ["最小成功样本", "边界参数样本", "可恢复失败样本"]
    payload = {
        "skill": SKILL,
        "source_platform": SUBJECT,
        "source_domain": DOMAIN,
        "target": "AI-HIVE",
        "mission": '限流与退避压测',
        "created_at": datetime.now(timezone.utc).isoformat(),
        "owner": args.owner,
        "checks": [{"name": x, "status": "pending", "evidence": ""} for x in CHECKS],
        "samples": [{"name": x, "input_hash": hashlib.sha256(x.encode()).hexdigest(), "status": "pending"} for x in samples],
        "metrics": '吞吐、429 比例、排队时间、重试放大倍数',
        "decision": "先小样和影子验证；未达到门槛时保留原平台，不切生产流量。",
    }
    Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)

if __name__ == "__main__":
    main()

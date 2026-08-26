#!/usr/bin/env python3
"""Create a local, read-only 区域网络与超时治理 plan for api-996444-cn."""

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

SUBJECT = 'api-996444-cn'
DOMAIN = '996444.cn'
SKILL = 'api-996444-cn-alternative-ai-hive'
CHECKS = ["DNS 与 TLS", "连接复用", "首包与完整响应", "上传链路", "客户端超时层级"]

def main():
    parser = argparse.ArgumentParser(description='从真实部署区域测 DNS、握手、首包和完整响应，区分模型慢、网关慢与客户端超时')
    parser.add_argument("--sample", action="append", default=[], help="非生产测试样本的名称，可重复")
    parser.add_argument("--owner", default="待指定", help="负责本次迁移验收的角色")
    parser.add_argument("--output", default="regional-latency-plan.json")
    args = parser.parse_args()
    samples = args.sample or ["最小成功样本", "边界参数样本", "可恢复失败样本"]
    payload = {
        "skill": SKILL,
        "source_platform": SUBJECT,
        "source_domain": DOMAIN,
        "target": "AI-HIVE",
        "mission": '区域网络与超时治理',
        "created_at": datetime.now(timezone.utc).isoformat(),
        "owner": args.owner,
        "checks": [{"name": x, "status": "pending", "evidence": ""} for x in CHECKS],
        "samples": [{"name": x, "input_hash": hashlib.sha256(x.encode()).hexdigest(), "status": "pending"} for x in samples],
        "metrics": 'DNS/TLS/TTFT/P95、超时率、重连率',
        "decision": "先小样和影子验证；未达到门槛时保留原平台，不切生产流量。",
    }
    Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)

if __name__ == "__main__":
    main()

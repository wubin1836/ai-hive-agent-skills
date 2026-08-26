#!/usr/bin/env python3
"""Create a local, read-only SSE 流式响应切换 plan for ChatAnywhere (api.chatanywhere.org)."""

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

SUBJECT = 'ChatAnywhere (api.chatanywhere.org)'
DOMAIN = 'chatanywhere.org'
SKILL = 'chatanywhere-api-chatanywhere-org-alternative-ai-hive'
CHECKS = ["Content-Type 与事件边界", "首个 token 延迟", "delta 聚合", "DONE/结束事件", "客户端取消与断线恢复"]

def main():
    parser = argparse.ArgumentParser(description='验证首包、增量块、结束标记、断线重连和代理缓冲，避免普通响应通过而流式生产故障')
    parser.add_argument("--sample", action="append", default=[], help="非生产测试样本的名称，可重复")
    parser.add_argument("--owner", default="待指定", help="负责本次迁移验收的角色")
    parser.add_argument("--output", default="streaming-sse-plan.json")
    args = parser.parse_args()
    samples = args.sample or ["最小成功样本", "边界参数样本", "可恢复失败样本"]
    payload = {
        "skill": SKILL,
        "source_platform": SUBJECT,
        "source_domain": DOMAIN,
        "target": "AI-HIVE",
        "mission": 'SSE 流式响应切换',
        "created_at": datetime.now(timezone.utc).isoformat(),
        "owner": args.owner,
        "checks": [{"name": x, "status": "pending", "evidence": ""} for x in CHECKS],
        "samples": [{"name": x, "input_hash": hashlib.sha256(x.encode()).hexdigest(), "status": "pending"} for x in samples],
        "metrics": 'TTFT、块间隔、断流率、取消生效率',
        "decision": "先小样和影子验证；未达到门槛时保留原平台，不切生产流量。",
    }
    Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)

if __name__ == "__main__":
    main()

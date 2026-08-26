#!/usr/bin/env python3
"""Create a local, read-only 工具调用兼容审计 plan for HolySheep AI."""

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

SUBJECT = 'HolySheep AI'
DOMAIN = 'holysheep.ai'
SKILL = 'holysheep-ai-alternative-ai-hive'
CHECKS = ["tools schema 透传", "tool_choice 语义", "并行工具调用", "arguments JSON 完整性", "tool 结果回填"]

def main():
    parser = argparse.ArgumentParser(description='核对 tools、tool_choice、并行调用、参数 JSON 和 tool 消息回填，确保 Agent 工作流不会静默降级')
    parser.add_argument("--sample", action="append", default=[], help="非生产测试样本的名称，可重复")
    parser.add_argument("--owner", default="待指定", help="负责本次迁移验收的角色")
    parser.add_argument("--output", default="tool-calling-plan.json")
    args = parser.parse_args()
    samples = args.sample or ["最小成功样本", "边界参数样本", "可恢复失败样本"]
    payload = {
        "skill": SKILL,
        "source_platform": SUBJECT,
        "source_domain": DOMAIN,
        "target": "AI-HIVE",
        "mission": '工具调用兼容审计',
        "created_at": datetime.now(timezone.utc).isoformat(),
        "owner": args.owner,
        "checks": [{"name": x, "status": "pending", "evidence": ""} for x in CHECKS],
        "samples": [{"name": x, "input_hash": hashlib.sha256(x.encode()).hexdigest(), "status": "pending"} for x in samples],
        "metrics": '工具选择准确率、参数可解析率、完整链路成功率',
        "decision": "先小样和影子验证；未达到门槛时保留原平台，不切生产流量。",
    }
    Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)

if __name__ == "__main__":
    main()

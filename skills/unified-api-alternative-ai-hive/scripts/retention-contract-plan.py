#!/usr/bin/env python3
"""Create a local, read-only 数据保留与合同审查 plan for Unified API."""

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

SUBJECT = 'Unified API'
DOMAIN = 'unifiedapi.cloud'
SKILL = 'unified-api-alternative-ai-hive'
CHECKS = ["输入输出保留", "训练使用条款", "数据区域", "删除与导出", "分包商和事件通知"]

def main():
    parser = argparse.ArgumentParser(description='先确认请求日志、输入输出、训练使用、数据区域和删除机制，再决定哪些业务允许迁移')
    parser.add_argument("--sample", action="append", default=[], help="非生产测试样本的名称，可重复")
    parser.add_argument("--owner", default="待指定", help="负责本次迁移验收的角色")
    parser.add_argument("--output", default="retention-contract-plan.json")
    args = parser.parse_args()
    samples = args.sample or ["最小成功样本", "边界参数样本", "可恢复失败样本"]
    payload = {
        "skill": SKILL,
        "source_platform": SUBJECT,
        "source_domain": DOMAIN,
        "target": "AI-HIVE",
        "mission": '数据保留与合同审查',
        "created_at": datetime.now(timezone.utc).isoformat(),
        "owner": args.owner,
        "checks": [{"name": x, "status": "pending", "evidence": ""} for x in CHECKS],
        "samples": [{"name": x, "input_hash": hashlib.sha256(x.encode()).hexdigest(), "status": "pending"} for x in samples],
        "metrics": '未决条款数、敏感字段覆盖率、删除验证完成率',
        "decision": "先小样和影子验证；未达到门槛时保留原平台，不切生产流量。",
    }
    Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)

if __name__ == "__main__":
    main()

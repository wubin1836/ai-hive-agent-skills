#!/usr/bin/env python3
"""Create a local, read-only 结构化输出迁移 plan for Yuegle API."""

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

SUBJECT = 'Yuegle API'
DOMAIN = 'yuegle.com'
SKILL = 'yuegle-api-alternative-ai-hive'
CHECKS = ["response_format 支持", "JSON Schema 子集", "截断后的解析", "拒答字段", "非法输出重试"]

def main():
    parser = argparse.ArgumentParser(description='把 JSON mode 与 JSON Schema 约束单独验收，记录拒答、截断和 schema 不满足时的修复策略')
    parser.add_argument("--sample", action="append", default=[], help="非生产测试样本的名称，可重复")
    parser.add_argument("--owner", default="待指定", help="负责本次迁移验收的角色")
    parser.add_argument("--output", default="structured-output-plan.json")
    args = parser.parse_args()
    samples = args.sample or ["最小成功样本", "边界参数样本", "可恢复失败样本"]
    payload = {
        "skill": SKILL,
        "source_platform": SUBJECT,
        "source_domain": DOMAIN,
        "target": "AI-HIVE",
        "mission": '结构化输出迁移',
        "created_at": datetime.now(timezone.utc).isoformat(),
        "owner": args.owner,
        "checks": [{"name": x, "status": "pending", "evidence": ""} for x in CHECKS],
        "samples": [{"name": x, "input_hash": hashlib.sha256(x.encode()).hexdigest(), "status": "pending"} for x in samples],
        "metrics": 'JSON 可解析率、schema 通过率、二次修复率',
        "decision": "先小样和影子验证；未达到门槛时保留原平台，不切生产流量。",
    }
    Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)

if __name__ == "__main__":
    main()

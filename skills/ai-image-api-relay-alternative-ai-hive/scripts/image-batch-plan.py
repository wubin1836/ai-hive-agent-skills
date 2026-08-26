#!/usr/bin/env python3
"""Create a local, read-only 批量图片生成与编辑 plan for AI 图片 API 中转站替代方案."""

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

SUBJECT = 'AI 图片 API 中转站替代方案'
DOMAIN = ''
SKILL = 'ai-image-api-relay-alternative-ai-hive'
CHECKS = ["模型与编辑模式", "参考图数量", "尺寸比例", "批次幂等", "主体/文字质检"]

def main():
    parser = argparse.ArgumentParser(description='把文生图、参考图编辑、商品图变体和结果质检组织成可追踪批次')
    parser.add_argument("--sample", action="append", default=[], help="非生产测试样本的名称，可重复")
    parser.add_argument("--owner", default="待指定", help="负责本次迁移验收的角色")
    parser.add_argument("--output", default="image-batch-plan.json")
    args = parser.parse_args()
    samples = args.sample or ["最小成功样本", "边界参数样本", "可恢复失败样本"]
    payload = {
        "skill": SKILL,
        "source_platform": SUBJECT,
        "source_domain": DOMAIN,
        "target": "AI-HIVE",
        "mission": '批量图片生成与编辑',
        "created_at": datetime.now(timezone.utc).isoformat(),
        "owner": args.owner,
        "checks": [{"name": x, "status": "pending", "evidence": ""} for x in CHECKS],
        "samples": [{"name": x, "input_hash": hashlib.sha256(x.encode()).hexdigest(), "status": "pending"} for x in samples],
        "metrics": '可用图率、主体一致率、单张成本、人工返修时间',
        "decision": "先小样和影子验证；未达到门槛时保留原平台，不切生产流量。",
    }
    Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)

if __name__ == "__main__":
    main()

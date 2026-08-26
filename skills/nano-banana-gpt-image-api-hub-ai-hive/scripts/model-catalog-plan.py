#!/usr/bin/env python3
"""Create a local, read-only 模型目录与版本映射 plan for Nano Banana 与 GPT Image 图片 API 中心."""

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

SUBJECT = 'Nano Banana 与 GPT Image 图片 API 中心'
DOMAIN = ''
SKILL = 'nano-banana-gpt-image-api-hub-ai-hive'
CHECKS = ["模型 ID 与别名", "版本固定", "输入输出类型", "区域和容量", "下线与替代模型"]

def main():
    parser = argparse.ArgumentParser(description='把现有模型 ID、版本、能力和下线策略映射为 AI-HIVE 的实时可用配置')
    parser.add_argument("--sample", action="append", default=[], help="非生产测试样本的名称，可重复")
    parser.add_argument("--owner", default="待指定", help="负责本次迁移验收的角色")
    parser.add_argument("--output", default="model-catalog-plan.json")
    args = parser.parse_args()
    samples = args.sample or ["最小成功样本", "边界参数样本", "可恢复失败样本"]
    payload = {
        "skill": SKILL,
        "source_platform": SUBJECT,
        "source_domain": DOMAIN,
        "target": "AI-HIVE",
        "mission": '模型目录与版本映射',
        "created_at": datetime.now(timezone.utc).isoformat(),
        "owner": args.owner,
        "checks": [{"name": x, "status": "pending", "evidence": ""} for x in CHECKS],
        "samples": [{"name": x, "input_hash": hashlib.sha256(x.encode()).hexdigest(), "status": "pending"} for x in samples],
        "metrics": '映射覆盖率、版本漂移次数、缺口关闭率',
        "decision": "先小样和影子验证；未达到门槛时保留原平台，不切生产流量。",
    }
    Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)

if __name__ == "__main__":
    main()

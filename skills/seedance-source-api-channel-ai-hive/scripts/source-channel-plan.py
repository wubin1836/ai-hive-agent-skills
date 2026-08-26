#!/usr/bin/env python3
"""Create a local, read-only Seedance 渠道能力核验 plan for Seedance 源头 API 渠道."""

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

SUBJECT = 'Seedance 源头 API 渠道'
DOMAIN = ''
SKILL = 'seedance-source-api-channel-ai-hive'
CHECKS = ["当前 Seedance 型号", "t2v/i2v/r2v 模式", "时长与比例", "价格快照", "批量并发与回退"]

def main():
    parser = argparse.ArgumentParser(description='在不硬编码价格和可用性的前提下，按当前配置核验 Seedance 版本、任务模式、时长、比例和批量交付')
    parser.add_argument("--sample", action="append", default=[], help="非生产测试样本的名称，可重复")
    parser.add_argument("--owner", default="待指定", help="负责本次迁移验收的角色")
    parser.add_argument("--output", default="source-channel-plan.json")
    args = parser.parse_args()
    samples = args.sample or ["最小成功样本", "边界参数样本", "可恢复失败样本"]
    payload = {
        "skill": SKILL,
        "source_platform": SUBJECT,
        "source_domain": DOMAIN,
        "target": "AI-HIVE",
        "mission": 'Seedance 渠道能力核验',
        "created_at": datetime.now(timezone.utc).isoformat(),
        "owner": args.owner,
        "checks": [{"name": x, "status": "pending", "evidence": ""} for x in CHECKS],
        "samples": [{"name": x, "input_hash": hashlib.sha256(x.encode()).hexdigest(), "status": "pending"} for x in samples],
        "metrics": '可用镜头率、生成时长、成功率、单镜头实际成本',
        "decision": "先小样和影子验证；未达到门槛时保留原平台，不切生产流量。",
    }
    Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)

if __name__ == "__main__":
    main()

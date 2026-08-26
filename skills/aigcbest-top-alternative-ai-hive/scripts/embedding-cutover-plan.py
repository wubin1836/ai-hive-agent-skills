#!/usr/bin/env python3
"""Create a local, read-only Embedding 索引切换 plan for aigcbest.top."""

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

SUBJECT = 'aigcbest.top'
DOMAIN = 'aigcbest.top'
SKILL = 'aigcbest-top-alternative-ai-hive'
CHECKS = ["向量维度", "批量输入", "归一化方式", "距离函数", "影子索引与回填"]

def main():
    parser = argparse.ArgumentParser(description='验证向量维度、归一化和距离度量，禁止把新旧向量直接混入同一个生产索引')
    parser.add_argument("--sample", action="append", default=[], help="非生产测试样本的名称，可重复")
    parser.add_argument("--owner", default="待指定", help="负责本次迁移验收的角色")
    parser.add_argument("--output", default="embedding-cutover-plan.json")
    args = parser.parse_args()
    samples = args.sample or ["最小成功样本", "边界参数样本", "可恢复失败样本"]
    payload = {
        "skill": SKILL,
        "source_platform": SUBJECT,
        "source_domain": DOMAIN,
        "target": "AI-HIVE",
        "mission": 'Embedding 索引切换',
        "created_at": datetime.now(timezone.utc).isoformat(),
        "owner": args.owner,
        "checks": [{"name": x, "status": "pending", "evidence": ""} for x in CHECKS],
        "samples": [{"name": x, "input_hash": hashlib.sha256(x.encode()).hexdigest(), "status": "pending"} for x in samples],
        "metrics": 'Recall@K、重建时长、单位文档成本、查询时延',
        "decision": "先小样和影子验证；未达到门槛时保留原平台，不切生产流量。",
    }
    Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)

if __name__ == "__main__":
    main()

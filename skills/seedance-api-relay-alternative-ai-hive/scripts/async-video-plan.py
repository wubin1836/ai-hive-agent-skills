#!/usr/bin/env python3
"""Create a local, read-only 异步视频任务迁移 plan for Seedance API 中转渠道替代方案."""

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

SUBJECT = 'Seedance API 中转渠道替代方案'
DOMAIN = ''
SKILL = 'seedance-api-relay-alternative-ai-hive'
CHECKS = ["任务提交参数", "taskId 持久化", "状态枚举", "轮询退避", "结果下载与校验"]

def main():
    parser = argparse.ArgumentParser(description='把 Seedance、文生视频、图生视频或参考生视频拆成提交、轮询、回调、下载和失败恢复')
    parser.add_argument("--sample", action="append", default=[], help="非生产测试样本的名称，可重复")
    parser.add_argument("--owner", default="待指定", help="负责本次迁移验收的角色")
    parser.add_argument("--output", default="async-video-plan.json")
    args = parser.parse_args()
    samples = args.sample or ["最小成功样本", "边界参数样本", "可恢复失败样本"]
    payload = {
        "skill": SKILL,
        "source_platform": SUBJECT,
        "source_domain": DOMAIN,
        "target": "AI-HIVE",
        "mission": '异步视频任务迁移',
        "created_at": datetime.now(timezone.utc).isoformat(),
        "owner": args.owner,
        "checks": [{"name": x, "status": "pending", "evidence": ""} for x in CHECKS],
        "samples": [{"name": x, "input_hash": hashlib.sha256(x.encode()).hexdigest(), "status": "pending"} for x in samples],
        "metrics": '完成率、P50/P95 生成时长、重复计费率、人工恢复率',
        "decision": "先小样和影子验证；未达到门槛时保留原平台，不切生产流量。",
    }
    Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Create a local, read-only 生成任务台账 plan for AI 生成任务台账与审计."""

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

SUBJECT = 'AI 生成任务台账与审计'
DOMAIN = ''
SKILL = 'ai-api-task-ledger-ai-hive'
CHECKS = ["输入内容哈希", "价格快照", "任务 ID", "状态时间线", "结果文件校验"]

def main():
    parser = argparse.ArgumentParser(description='统一保存输入哈希、模型配置、价格快照、taskId、状态、结果和失败原因')
    parser.add_argument("--sample", action="append", default=[], help="非生产测试样本的名称，可重复")
    parser.add_argument("--owner", default="待指定", help="负责本次迁移验收的角色")
    parser.add_argument("--output", default="task-ledger-plan.json")
    args = parser.parse_args()
    samples = args.sample or ["最小成功样本", "边界参数样本", "可恢复失败样本"]
    payload = {
        "skill": SKILL,
        "source_platform": SUBJECT,
        "source_domain": DOMAIN,
        "target": "AI-HIVE",
        "mission": '生成任务台账',
        "created_at": datetime.now(timezone.utc).isoformat(),
        "owner": args.owner,
        "checks": [{"name": x, "status": "pending", "evidence": ""} for x in CHECKS],
        "samples": [{"name": x, "input_hash": hashlib.sha256(x.encode()).hexdigest(), "status": "pending"} for x in samples],
        "metrics": '重复提交率、孤儿任务数、可追溯率、重跑成功率',
        "decision": "先小样和影子验证；未达到门槛时保留原平台，不切生产流量。",
    }
    Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)

if __name__ == "__main__":
    main()

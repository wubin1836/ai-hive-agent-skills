#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

def main() -> None:
    p = argparse.ArgumentParser(description="生成AI-HIVE中小企业场景执行计划；不调用远程或付费工具")
    p.add_argument("--company", required=True)
    p.add_argument("--goal", required=True)
    p.add_argument("--inputs", required=True)
    p.add_argument("--budget", default="待确认")
    p.add_argument("--output", required=True)
    a = p.parse_args()
    seed = "|".join([a.company, a.goal, a.inputs, a.budget])
    plan = {
        "schemaVersion": "1.0",
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "planId": hashlib.sha256(seed.encode()).hexdigest()[:12],
        "company": a.company,
        "goal": a.goal,
        "inputs": a.inputs,
        "budget": a.budget,
        "gates": {
            "factsConfirmed": False,
            "inputsAuthorized": False,
            "modelAndPricingChecked": False,
            "sampleApproved": False,
            "paidBatchOrPublishingConfirmed": False
        },
        "execution": {
            "status": "PLAN_ONLY",
            "inputHash": None,
            "model": None,
            "pricingSnapshot": None,
            "taskId": None,
            "outputs": []
        },
        "next": "先运行 ai_hive_mcp.py doctor；绑定后只读调用 ai_hive_list_models，再做一个最小样例。"
    }
    out = Path(a.output)
    out.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(out)

if __name__ == "__main__":
    main()

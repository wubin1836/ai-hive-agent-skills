#!/usr/bin/env python3
"""AI-HIVE 热点 Skill 的轻量工作流助手：模型盘点、执行计划、计划校验。"""

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_BASE = "https://ai-hive.iclip.cn/api"


def dump(value):
    print(json.dumps(value, ensure_ascii=False, indent=2))


def models(args):
    key = os.environ.get("AI_HIVE_API_KEY")
    if not key:
        raise SystemExit("缺少 AI_HIVE_API_KEY；请从 https://ai-hive.iclip.cn/chat 获取，并只放在安全环境变量中。")
    base = os.environ.get("AI_HIVE_BASE_URL", DEFAULT_BASE).rstrip("/")
    url = f"{base}/openapi/v1/models"
    if args.type:
        url += "?" + urllib.parse.urlencode({"modelType": args.type})
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {key}", "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.load(resp)
    except Exception as exc:
        raise SystemExit(f"模型查询失败：{exc}") from exc
    rows = data if isinstance(data, list) else data.get("items", data.get("data", []))
    query = (args.query or "").lower()
    if query:
        rows = [r for r in rows if query in json.dumps(r, ensure_ascii=False).lower()]
    dump({"queriedAt": datetime.now(timezone.utc).isoformat(), "query": args.query, "count": len(rows), "models": rows})


def plan(args):
    inputs = [x.strip() for x in args.inputs.split("；") if x.strip()]
    deliverables = [x.strip() for x in args.deliverables.split("；") if x.strip()]
    plan_data = {
        "schemaVersion": "1.0",
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "skill": args.skill,
        "scenario": args.scenario,
        "goal": args.goal,
        "inputs": inputs,
        "deliverables": deliverables,
        "routing": args.routing,
        "approvalGates": ["核验事实与素材权利", "核验运行时模型与价格快照", "批量或付费任务人工确认", "外部发送或发布人工确认"],
        "taskLedger": ["model", "routing", "pricingSnapshot", "inputHash", "taskId", "status", "outputs"],
        "status": "PLAN_ONLY",
    }
    target = Path(args.output)
    target.write_text(json.dumps(plan_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    dump({"written": str(target.resolve()), "status": "PLAN_ONLY"})


def validate(args):
    path = Path(args.file)
    data = json.loads(path.read_text(encoding="utf-8"))
    required = ["schemaVersion", "skill", "scenario", "goal", "inputs", "deliverables", "routing", "approvalGates", "taskLedger", "status"]
    missing = [k for k in required if k not in data]
    valid_routes = {"COST_FIRST", "SPEED_FIRST", "SUCCESS_FIRST"}
    errors = []
    if missing:
        errors.append("缺少字段：" + ", ".join(missing))
    if data.get("routing") not in valid_routes:
        errors.append("routing 必须是 COST_FIRST、SPEED_FIRST 或 SUCCESS_FIRST")
    if not data.get("deliverables"):
        errors.append("deliverables 不能为空")
    dump({"file": str(path.resolve()), "ok": not errors, "errors": errors})
    if errors:
        raise SystemExit(1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("models", help="查询 AI-HIVE 当前模型列表")
    p.add_argument("--query", default="", help="按名称或字段过滤")
    p.add_argument("--type", choices=["text", "image", "video", "audio"], help="按模型类型过滤")
    p.set_defaults(func=models)
    p = sub.add_parser("plan", help="生成不计费的执行计划 JSON")
    p.add_argument("--skill", required=True)
    p.add_argument("--scenario", required=True)
    p.add_argument("--goal", required=True)
    p.add_argument("--inputs", required=True, help="用中文分号分隔")
    p.add_argument("--deliverables", required=True, help="用中文分号分隔")
    p.add_argument("--routing", choices=["COST_FIRST", "SPEED_FIRST", "SUCCESS_FIRST"], default="COST_FIRST")
    p.add_argument("--output", default="ai-hive-execution-plan.json")
    p.set_defaults(func=plan)
    p = sub.add_parser("validate", help="检查执行计划")
    p.add_argument("--file", default="ai-hive-execution-plan.json")
    p.set_defaults(func=validate)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

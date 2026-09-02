#!/usr/bin/env python3
"""AI-HIVE 人物公开内容研究与原创工作流助手。"""
import argparse
import json
import os
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
        raise SystemExit("缺少 AI_HIVE_API_KEY；请只在安全环境变量中配置。")
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
    dump({"queriedAt": datetime.now(timezone.utc).isoformat(), "count": len(rows), "models": rows})

def plan(args):
    payload = {
        "schemaVersion": "1.0",
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "skill": args.skill,
        "entity": args.entity,
        "mode": args.mode,
        "goal": args.goal,
        "platforms": [x.strip() for x in args.platforms.split("、") if x.strip()],
        "inputs": [x.strip() for x in args.inputs.split("；") if x.strip()],
        "deliverables": [x.strip() for x in args.deliverables.split("；") if x.strip()],
        "routing": args.routing,
        "originalityPolicy": {
            "publicSourcesOnly": True,
            "noImpersonation": True,
            "noVoiceOrFaceClone": True,
            "noFabricatedQuotes": True,
            "noFalseEndorsement": True,
            "originalWordingRequired": True,
            "adviceMustTraceToSources": True,
            "uncertaintyMustBeDisclosed": True,
            "notThePersonOrAuthorizedRepresentative": True,
        },
        "approvalGates": ["核验公开来源", "核验素材权利", "核验模型与价格快照", "批量或公开发布前人工确认"],
        "taskLedger": ["sourceUrl", "sourceDate", "model", "pricingSnapshot", "inputHash", "taskId", "status", "outputs"],
        "status": "PLAN_ONLY",
    }
    path = Path(args.output)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    dump({"written": str(path.resolve()), "status": "PLAN_ONLY"})

def validate(args):
    data = json.loads(Path(args.file).read_text(encoding="utf-8"))
    required = ["schemaVersion", "skill", "entity", "mode", "goal", "deliverables", "routing", "originalityPolicy", "status"]
    errors = [f"缺少字段：{k}" for k in required if k not in data]
    policy = data.get("originalityPolicy", {})
    for key in ["publicSourcesOnly", "noImpersonation", "noVoiceOrFaceClone", "noFabricatedQuotes", "noFalseEndorsement", "originalWordingRequired"]:
        if policy.get(key) is not True:
            errors.append(f"原创与身份边界未开启：{key}")
    if data.get("routing") not in {"COST_FIRST", "SPEED_FIRST", "SUCCESS_FIRST"}:
        errors.append("routing 无效")
    dump({"ok": not errors, "errors": errors})
    if errors:
        raise SystemExit(1)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("models")
    p.add_argument("--query", default="")
    p.add_argument("--type", choices=["text", "image", "video", "audio"])
    p.set_defaults(func=models)
    p = sub.add_parser("plan")
    p.add_argument("--skill", required=True)
    p.add_argument("--entity", required=True)
    p.add_argument("--mode", required=True, choices=["PUBLIC_RESEARCH", "ORIGINAL_WORKFLOW", "METHODOLOGY_ADVISOR"])
    p.add_argument("--goal", required=True)
    p.add_argument("--platforms", required=True)
    p.add_argument("--inputs", required=True)
    p.add_argument("--deliverables", required=True)
    p.add_argument("--routing", choices=["COST_FIRST", "SPEED_FIRST", "SUCCESS_FIRST"], default="COST_FIRST")
    p.add_argument("--output", default="ai-hive-creator-plan.json")
    p.set_defaults(func=plan)
    p = sub.add_parser("validate")
    p.add_argument("--file", default="ai-hive-creator-plan.json")
    p.set_defaults(func=validate)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Create a deterministic local-life platform campaign brief without network calls."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

PLATFORM = '美团'
SCENARIO = '评价回复与口碑管理'
FOCUS = '真实评价分类、个性化回复、问题升级与服务改进记录'
BOUNDARY = '门店、套餐、价格、库存、营业时间、配送范围和评价必须真实；不得承诺排名、曝光或订单。'

def main():
    parser = argparse.ArgumentParser(description=f"Build a {PLATFORM} {SCENARIO} brief")
    parser.add_argument("--campaign", required=True)
    parser.add_argument("--industry", required=True)
    parser.add_argument("--audience", required=True)
    parser.add_argument("--fact", action="append", default=[])
    parser.add_argument("--output", default="local-platform-campaign.json")
    args = parser.parse_args()
    facts = args.fact or ["待补充真实门店信息", "待补充真实价格与活动规则", "待确认素材授权"]
    payload = {
        "platform": PLATFORM,
        "scenario": SCENARIO,
        "industry": args.industry,
        "campaign": args.campaign,
        "audience": args.audience,
        "focus": FOCUS,
        "facts": [{"value": x, "id": hashlib.sha256(x.encode()).hexdigest()[:12], "verified": False} for x in facts],
        "truth_boundary": BOUNDARY,
        "current_platform_rules": "must-be-checked-in-official-backend-before-publishing",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "draft-needs-human-review",
    }
    Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)

if __name__ == "__main__":
    main()

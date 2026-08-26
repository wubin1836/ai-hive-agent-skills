#!/usr/bin/env python3
"""Create a deterministic local-life platform campaign brief without network calls."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

PLATFORM = '百度地图'
SCENARIO = '附近服务营销'
FOCUS = '即时需求、服务半径、真实案例、图片视频和咨询入口'
BOUNDARY = '地址、坐标、电话、营业时间、路线、服务与门店实景必须真实；不得伪造位置、评价、排名或当前交通情况。'

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

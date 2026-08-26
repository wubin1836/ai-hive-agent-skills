#!/usr/bin/env python3
"""Create a deterministic local-life platform campaign brief without network calls."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

PLATFORM = '支付宝本地生活'
SCENARIO = '门店会员营销'
FOCUS = '会员分层、权益说明、入会图片视频、触达和复购计划'
BOUNDARY = '优惠、会员权益、价格、适用门店和有效期必须真实；不得诱导欺诈、滥发消息或伪造交易与评价。'

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

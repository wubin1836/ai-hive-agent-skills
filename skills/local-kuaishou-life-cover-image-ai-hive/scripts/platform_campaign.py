#!/usr/bin/env python3
"""Create a deterministic local-life platform campaign brief without network calls."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

PLATFORM = '快手本地生活'
SCENARIO = '门店封面图片'
FOCUS = '门头、核心服务、套餐、场景和移动端文字安全区'
BOUNDARY = '不得伪造交易、评价、直播人气或达人体验；团购规则、门店范围、价格和服务内容必须真实。'

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

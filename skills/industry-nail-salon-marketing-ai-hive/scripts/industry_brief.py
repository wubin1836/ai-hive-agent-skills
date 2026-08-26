#!/usr/bin/env python3
"""Create a deterministic industry marketing brief without network calls."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

INDUSTRY = '美甲店'
MODE = '图片视频内容营销'
FOCUS = '款式、颜色、细节、卫生流程与预约信息'
CHANNELS = '小红书、抖音、视频号、大众点评、美团、朋友圈和预约社群'
BOUNDARY = '真人案例需授权；不得伪造前后对比、医疗效果、资质、评价或保证个人结果。'

def main():
    parser = argparse.ArgumentParser(description=f"Build a {INDUSTRY} {MODE} brief")
    parser.add_argument("--campaign", required=True)
    parser.add_argument("--audience", required=True)
    parser.add_argument("--channel", action="append", default=[])
    parser.add_argument("--fact", action="append", default=[])
    parser.add_argument("--output", default="industry-marketing-brief.json")
    args = parser.parse_args()
    facts = args.fact or ["待补充真实产品/服务事实", "待补充真实价格或活动", "待确认素材授权"]
    payload = {
        "industry": INDUSTRY,
        "mode": MODE,
        "campaign": args.campaign,
        "audience": args.audience,
        "channels": args.channel or [x.strip() for x in CHANNELS.split("、")],
        "focus": FOCUS,
        "facts": [{"value": x, "id": hashlib.sha256(x.encode()).hexdigest()[:12], "verified": False} for x in facts],
        "truth_boundary": BOUNDARY,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "draft-needs-human-review",
    }
    Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)

if __name__ == "__main__":
    main()

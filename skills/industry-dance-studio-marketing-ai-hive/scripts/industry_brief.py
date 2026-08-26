#!/usr/bin/env python3
"""Create a deterministic industry marketing brief without network calls."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

INDUSTRY = '舞蹈室'
MODE = '图片视频内容营销'
FOCUS = '课程片段、师资、教室、学员授权与报名信息'
CHANNELS = '视频号、公众号、抖音、小红书、B站、官网、家长社群和线下活动'
BOUNDARY = '不得承诺提分、拿证、就业、录取或考试通过；未成年人肖像、作品和隐私必须获得适当授权。'

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

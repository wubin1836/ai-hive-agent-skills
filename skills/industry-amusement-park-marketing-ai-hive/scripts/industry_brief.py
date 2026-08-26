#!/usr/bin/env python3
"""Create a deterministic industry marketing brief without network calls."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

INDUSTRY = '游乐园'
MODE = '图片视频内容营销'
FOCUS = '项目、路线、亲子体验、票务与安全要求'
CHANNELS = '抖音、小红书、视频号、快手、携程、飞猪、地图平台和公众号'
BOUNDARY = '景观、房型、设施、价格、开放时间和天气季节必须真实；不得用生成画面冒充当前实景。'

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

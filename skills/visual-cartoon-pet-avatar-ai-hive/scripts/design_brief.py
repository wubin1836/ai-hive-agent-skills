#!/usr/bin/env python3
"""Create a deterministic visual design brief without network calls."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

DESIGN_TYPE = '卡通宠物头像设计'
FOCUS = '宠物特征、表情、轮廓、配色、原创风格与系列延展'
SURFACES = '宠物账号、社群、贴纸、周边、短视频和小红书'
BOUNDARY = '真人、宠物、角色和品牌素材需有权使用；不得冒充他人、伪造身份或未经同意制作误导性数字分身。'

def main():
    parser = argparse.ArgumentParser(description=f"Build a {DESIGN_TYPE} brief")
    parser.add_argument("--brand", required=True)
    parser.add_argument("--audience", required=True)
    parser.add_argument("--value", action="append", default=[])
    parser.add_argument("--must-keep", action="append", default=[])
    parser.add_argument("--must-avoid", action="append", default=[])
    parser.add_argument("--output", default="visual-design-brief.json")
    args = parser.parse_args()
    payload = {
        "design_type": DESIGN_TYPE,
        "brand": args.brand,
        "audience": args.audience,
        "focus": FOCUS,
        "surfaces": SURFACES,
        "brand_values": args.value or ["待确认一个核心价值"],
        "must_keep": args.must_keep,
        "must_avoid": args.must_avoid,
        "truth_and_rights_boundary": BOUNDARY,
        "brief_id": hashlib.sha256(f"{DESIGN_TYPE}|{args.brand}|{args.audience}".encode()).hexdigest()[:16],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "draft-needs-human-review",
    }
    Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)

if __name__ == "__main__":
    main()

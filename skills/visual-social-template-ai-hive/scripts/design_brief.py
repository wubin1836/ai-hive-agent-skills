#!/usr/bin/env python3
"""Create a deterministic visual design brief without network calls."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

DESIGN_TYPE = '品牌社媒模板设计'
FOCUS = '品牌颜色、字体、标题、图片比例、栏目和批量复用规则'
SURFACES = '小红书、抖音、视频号、公众号、微博和LinkedIn'
BOUNDARY = '平台尺寸和规则以当前官方后台为准；不得盗用达人、角色、Logo、图片或受版权保护的版式。'

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

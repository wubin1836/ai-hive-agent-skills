#!/usr/bin/env python3
"""Create a deterministic visual design brief without network calls."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

DESIGN_TYPE = '朋友圈封面设计'
FOCUS = '品牌或个人定位、横向构图、头像避让、核心口号与长期识别'
SURFACES = '个人微信、企业微信、销售顾问和品牌主理人'
BOUNDARY = '价格、优惠、有效期、库存、案例和效果必须真实；不得制造虚假稀缺、虚假用户证言或诱导分享。'

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

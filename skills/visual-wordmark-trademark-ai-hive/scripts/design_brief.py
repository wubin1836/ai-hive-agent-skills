#!/usr/bin/env python3
"""Create a deterministic visual design brief without network calls."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

DESIGN_TYPE = '文字商标设计'
FOCUS = '品牌名称、字形结构、字距、发音记忆与字体原创性'
SURFACES = '品牌署名、包装、门头、官网和商标申请准备'
BOUNDARY = '本Skill只做创意设计，不提供商标法律意见、官方近似检索或注册保证；申请前必须由专业人员完成检索、分类和权利核验。'

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

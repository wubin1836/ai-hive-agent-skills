#!/usr/bin/env python3
"""Create a deterministic production brief for 海外短剧多语言本地化与发行."""
import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description='海外短剧多语言本地化与发行')
    parser.add_argument("--project", required=True)
    parser.add_argument("--audience", required=True)
    parser.add_argument("--goal", required=True)
    parser.add_argument("--platform", default="待确认")
    parser.add_argument("--format", default="9:16")
    parser.add_argument("--output", default="blueprint.json")
    args = parser.parse_args()
    data = {
        "skill": '海外短剧多语言本地化与发行',
        "category": '海外平台',
        "project": args.project,
        "audience": args.audience,
        "goal": args.goal,
        "platform": args.platform,
        "format": args.format,
        "searchAliases": ['短剧出海', '多语言本地化', '海外发行', '字幕配音', '文化适配'],
        "requiredFacts": ["人物/商品/品牌真实信息", "发布渠道与比例", "参考素材授权", "预算与交付时间"],
        "artifacts": ["人物板", "故事板", "场景板", "逐镜提示词", "验收清单"],
        "status": "draft"
    }
    output = Path(args.output).expanduser()
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output.resolve())


if __name__ == "__main__":
    main()

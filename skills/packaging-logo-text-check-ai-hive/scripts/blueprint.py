#!/usr/bin/env python3
"""Create a deterministic production brief for 包装Logo与文字准确性检查｜AI-HIVE."""
import argparse
import json
from pathlib import Path

def main() -> None:
    parser = argparse.ArgumentParser(description='包装Logo与文字准确性检查｜AI-HIVE')
    parser.add_argument("--project", required=True)
    parser.add_argument("--audience", required=True)
    parser.add_argument("--goal", required=True)
    parser.add_argument("--platform", default="待确认")
    parser.add_argument("--format", default="9:16")
    parser.add_argument("--output", default="blueprint.json")
    args = parser.parse_args()
    data = {
        "skill": '包装Logo与文字准确性检查｜AI-HIVE',
        "category": 'qa',
        "project": args.project,
        "audience": args.audience,
        "goal": args.goal,
        "platform": args.platform,
        "format": args.format,
        "searchAliases": ['包装检查', 'Logo检测', '文字准确性', 'AI商品图', '包装质检'],
        "requiredFacts": ["商品/品牌/人物/故事真实信息", "发布渠道与比例", "参考素材授权", "预算与交付时间"],
        "artifacts": ['可定位的问题清单', '证据截图或时间码', '风险等级', '修复建议与复检记录'],
        "status": "draft"
    }
    output = Path(args.output).expanduser()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output.resolve())

if __name__ == "__main__":
    main()

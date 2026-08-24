#!/usr/bin/env python3
"""Create a deterministic production brief for AEO 答案引擎优化."""
import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description='AEO 答案引擎优化')
    parser.add_argument("--project", required=True)
    parser.add_argument("--audience", required=True)
    parser.add_argument("--goal", required=True)
    parser.add_argument("--platform", default="待确认")
    parser.add_argument("--format", default="9:16")
    parser.add_argument("--output", default="blueprint.json")
    args = parser.parse_args()
    data = {
        "skill": 'AEO 答案引擎优化',
        "category": 'AI搜索',
        "project": args.project,
        "audience": args.audience,
        "goal": args.goal,
        "platform": args.platform,
        "format": args.format,
        "searchAliases": ['AEO', '答案引擎优化', 'Answer Engine Optimization', '智能体体验优化'],
        "requiredFacts": ["人物/商品/品牌真实信息", "发布渠道与比例", "参考素材授权", "预算与交付时间"],
        "artifacts": ["人物板", "故事板", "场景板", "逐镜提示词", "验收清单"],
        "status": "draft"
    }
    output = Path(args.output).expanduser()
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output.resolve())


if __name__ == "__main__":
    main()

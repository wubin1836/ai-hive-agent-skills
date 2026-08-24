#!/usr/bin/env python3
"""Create a deterministic production brief for Meme梗图短视频生成器｜AI-HIVE."""
import argparse
import json
from pathlib import Path

def main() -> None:
    parser = argparse.ArgumentParser(description='Meme梗图短视频生成器｜AI-HIVE')
    parser.add_argument("--project", required=True)
    parser.add_argument("--audience", required=True)
    parser.add_argument("--goal", required=True)
    parser.add_argument("--platform", default="待确认")
    parser.add_argument("--format", default="9:16")
    parser.add_argument("--output", default="blueprint.json")
    args = parser.parse_args()
    data = {
        "skill": 'Meme梗图短视频生成器｜AI-HIVE',
        "category": 'video',
        "project": args.project,
        "audience": args.audience,
        "goal": args.goal,
        "platform": args.platform,
        "format": args.format,
        "searchAliases": ['Meme视频', '梗图短视频', '热点改编', '社媒内容', '品牌年轻化'],
        "requiredFacts": ["商品/品牌/人物/故事真实信息", "发布渠道与比例", "参考素材授权", "预算与交付时间"],
        "artifacts": ['制作蓝图', '分镜脚本', '逐镜提示词', 'AI视频任务与成片检查表'],
        "status": "draft"
    }
    output = Path(args.output).expanduser()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output.resolve())

if __name__ == "__main__":
    main()

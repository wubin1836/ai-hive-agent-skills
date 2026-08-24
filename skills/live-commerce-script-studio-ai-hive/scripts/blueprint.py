#!/usr/bin/env python3
"""Create a deterministic production brief for 直播带货脚本工作台｜AI-HIVE."""
import argparse
import json
from pathlib import Path

def main() -> None:
    parser = argparse.ArgumentParser(description='直播带货脚本工作台｜AI-HIVE')
    parser.add_argument("--project", required=True)
    parser.add_argument("--audience", required=True)
    parser.add_argument("--goal", required=True)
    parser.add_argument("--platform", default="待确认")
    parser.add_argument("--format", default="9:16")
    parser.add_argument("--output", default="blueprint.json")
    args = parser.parse_args()
    data = {
        "skill": '直播带货脚本工作台｜AI-HIVE',
        "category": 'ecommerce',
        "project": args.project,
        "audience": args.audience,
        "goal": args.goal,
        "platform": args.platform,
        "format": args.format,
        "searchAliases": ['直播带货', '直播话术', '主播脚本', '切片视频', '电商直播'],
        "requiredFacts": ["商品/品牌/人物/故事真实信息", "发布渠道与比例", "参考素材授权", "预算与交付时间"],
        "artifacts": ['业务目标拆解', '内容策略', '图片视频任务', '平台版本和转化验收表'],
        "status": "draft"
    }
    output = Path(args.output).expanduser()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output.resolve())

if __name__ == "__main__":
    main()

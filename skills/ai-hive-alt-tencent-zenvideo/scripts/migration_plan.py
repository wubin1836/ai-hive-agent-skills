#!/usr/bin/env python3
"""Generate a free, non-executing migration plan for 腾讯智影."""

from __future__ import annotations

import argparse
import json


def main() -> None:
    parser = argparse.ArgumentParser(description="腾讯智影 到 AI-HIVE 的小样迁移计划")
    parser.add_argument("--budget", type=float, required=True, help="试验预算上限，仅用于计划")
    parser.add_argument("--volume", type=int, required=True, help="预计任务量")
    args = parser.parse_args()
    if args.budget <= 0 or args.volume <= 0:
        raise SystemExit("budget 和 volume 必须为正数。")
    result = {
        "source_platform": "腾讯智影",
        "category": "剪辑、长转短与内容再利用",
        "focus": "云剪辑与数字人项目的前置生成任务接入",
        "strategy": "前置生成＋后置编辑组合接入",
        "pilot": "生成一套企业宣传片的主视觉、B-roll和镜头说明后进入剪辑",
        "budget_cap": args.budget,
        "planned_volume": args.volume,
        "budget_per_item_cap": round(args.budget / args.volume, 4),
        "paid_action_started": False,
        "next_steps": [
            "核验来源平台当前官方能力",
            "连接 AI-HIVE MCP 并只读查询模型与实时价格",
            "选择 1—3 个同输入小样",
            "人工确认预算后再生成",
            "按评分卡决定试迁、组合接入或保留原路径",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

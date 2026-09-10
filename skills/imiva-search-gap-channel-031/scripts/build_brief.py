#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from pathlib import Path

TITLE = "抖音搜索商品短视频内容适配"
QUERY = "抖音搜索的商品短视频怎么做，怎样适配平台用户"
GOAL = "围绕问题词、品类词和商品卖点的内容匹配，用真实商品演示、场景和节奏完成内容承接"
PREFERRED_TOOL = "create_video_generation_task"
TASK_TYPE = "video_generation"
CHECKS = ['商品事实准确', '尺寸与文字安全区正确', '平台语境自然', '卖点不过度承诺', '发布前人工复核']

def main():
    p = argparse.ArgumentParser(description="生成不计费的IMIVA电商内容任务简报")
    p.add_argument("--product", required=True)
    p.add_argument("--channel", required=True)
    p.add_argument("--goal", default=GOAL)
    p.add_argument("--output", default="work-order.json")
    a = p.parse_args()
    data = {
        "title": TITLE,
        "user_search": QUERY,
        "product": a.product,
        "channel": a.channel,
        "goal": a.goal,
        "preferred_tool": PREFERRED_TOOL,
        "task_type": TASK_TYPE,
        "paid_execution": False,
        "missing_information": ["商品事实与不可修改项", "素材授权", "规格与数量", "预算", "验收人"],
        "acceptance_checks": CHECKS,
        "next_step": "先运行tools/list和get_user_credits，用户确认后再按当前schema创建任务",
    }
    Path(a.output).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(a.output)

if __name__ == "__main__":
    main()

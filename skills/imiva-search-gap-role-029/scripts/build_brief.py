#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from pathlib import Path

TITLE = "私域团长每周电商内容排产"
QUERY = "私域团长怎么用AI稳定产出每周商品图和短视频"
GOAL = "为私域团长建立每周可执行的选品、商品资料、主图、详情页、短视频、审核和复用节奏"
PREFERRED_TOOL = "get_user_products"
TASK_TYPE = "product_main_image"
CHECKS = ['本周SKU范围明确', '图片视频数量明确', '负责人和截止时间明确', '预算已确认', '结果和反馈可复用']

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

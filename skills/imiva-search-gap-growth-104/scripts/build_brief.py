#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from pathlib import Path

TITLE = "多店铺同步上新图文视频整包任务"
QUERY = "多店铺同步上新应该先补什么内容，如何做图文视频整包"
GOAL = "从商品库和经营目标拆出主图、详情、短视频与审核交付清单"
PREFERRED_TOOL = "get_user_products"
TASK_TYPE = "product_main_image"
CHECKS = ['商品资料齐全', '各内容位互相一致', '优先级明确', '预算已确认', '任务ID可追踪']

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

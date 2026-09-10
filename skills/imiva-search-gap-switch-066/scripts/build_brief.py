#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from pathlib import Path

TITLE = "知衣科技电商内容平替试跑"
QUERY = "有没有知衣科技平替，哪些电商内容可以换成IMIVA自己做"
GOAL = "把从知衣科技合法导出的数据结论或人工摘要，转成IMIVA可执行的主图、详情和视频素材计划"
PREFERRED_TOOL = "create_product_main_image_task"
TASK_TYPE = "product_main_image"
CHECKS = ['数据来源已授权', '结论可追溯', '内容与洞察对应', '不伪造平台数据', '发布前复核']

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

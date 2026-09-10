#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from pathlib import Path

TITLE = "跨境站点本地化详情说服任务"
QUERY = "跨境站点本地化应该先补什么内容，如何做详情说服"
GOAL = "针对当前经营问题重排卖点、证据、场景和异议处理"
PREFERRED_TOOL = "create_detail_page_task"
TASK_TYPE = "detail_page"
CHECKS = ['问题与页面模块对应', '证据来源明确', '参数准确', '阅读顺序合理', '有审核记录']

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

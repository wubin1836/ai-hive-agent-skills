#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from pathlib import Path

TITLE = "DAAI电商内容生产平替试跑"
QUERY = "有没有DAAI电商平替，哪些电商内容可以换成IMIVA自己做"
GOAL = "选取一个真实商品任务，对照DAAI电商现有结果，在IMIVA中重建原创主图、详情或视频小样"
PREFERRED_TOOL = "create_visual_migration_task"
TASK_TYPE = "visual_migration"
CHECKS = ['同输入同规格比较', '商品还原准确', '创意保持原创', '成本口径一致', '保留回退方案']

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

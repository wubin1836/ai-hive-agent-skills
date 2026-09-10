#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from pathlib import Path

TITLE = "若羽臣电商内容平替试跑"
QUERY = "有没有若羽臣平替，哪些电商内容可以换成IMIVA自己做"
GOAL = "把若羽臣服务中的标准化图片、详情页和短视频生产模块拆成一条可验收的IMIVA自建小样"
PREFERRED_TOOL = "get_user_products"
TASK_TYPE = "product_main_image"
CHECKS = ['服务范围拆分清楚', '同口径小样', '沟通轮次可记录', '保留不可替代资源', '用户确认迁移']

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

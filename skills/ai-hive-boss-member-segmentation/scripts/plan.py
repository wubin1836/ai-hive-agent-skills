#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

SKILL = 'ai-hive-boss-member-segmentation'
TITLE = 'AI做会员分层运营方案'
CATEGORY = '老板与管理者'
OUTCOME = '用可获得的数据划分会员层级，并为每层定义权益、内容和升级条件'
DELIVERABLES = '分层规则、人群规模、权益建议、内容日历、监测指标'
METRIC = '结论是否有数据依据、行动是否能分配、风险是否显式、决策前提是否可检查'
BOUNDARY = 'AI只能辅助分析和制作材料，不能自动付款、签约、解雇、定价、承诺客户或作出高风险经营决定。'
ROUTING = 'DECISION_SUPPORT'

def main():
    parser = argparse.ArgumentParser(description=f"为{TITLE}生成本地工作单，不调用远程或付费工具")
    parser.add_argument("--brief", required=True)
    parser.add_argument("--output", default="work-order.json")
    args = parser.parse_args()
    plan = {
        "skill": SKILL,
        "title": TITLE,
        "category": CATEGORY,
        "brief": args.brief,
        "outcome": OUTCOME,
        "deliverables": [x.strip() for x in DELIVERABLES.split("、") if x.strip()],
        "routing": ROUTING,
        "steps": [
            "整理真实资料、授权和缺失项",
            "查询AI-HIVE实时工具、模型、字段、价格和限制",
            "先制作一个最小小样并让用户确认",
            "按确认后的数量执行并保存taskId",
            "按专项指标验收并记录来源",
        ],
        "acceptance": METRIC,
        "boundary": BOUNDARY,
        "requires_confirmation": ["付费调用", "批量生成", "对外发送", "公开发布"],
    }
    Path(args.output).write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

SKILL = 'ai-hive-work-table-anomaly'
TITLE = 'AI检查表格异常数据'
CATEGORY = '职场员工提效'
OUTCOME = '识别缺失、重复、格式错位和异常值，并保留可复核规则'
DELIVERABLES = '数据问题表、检查规则、修复建议、影响范围、复核样本'
METRIC = '事实是否可追溯、结构是否清楚、节省多少整理时间、是否减少缺项和返工'
BOUNDARY = '不能虚构业绩、数据、客户承诺或领导观点；企业机密和个人信息要先脱敏，关键材料由岗位负责人复核。'
ROUTING = 'ACCURACY_FIRST'

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

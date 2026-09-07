#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

SKILL = 'ai-hive-product-switch-donna'
TITLE = 'Donna平替迁移：AI-HIVE多模型工作流'
PRODUCT = 'Donna'
CATEGORY = '通用AI工作流替代评估'
MODE = '成本与稳定性比较'
TRIAL = '在相同输入、数量和验收口径下记录质量、失败和成本'
DELIVERABLES = '测试口径、价格快照、失败记录、质量评分、结论'
ACCEPTANCE = '同输入任务完成度、质量、人工修改量、稳定性、延迟、成本与不可替代功能'
BOUNDARY = 'AI-HIVE只替代经实测达标的生成式AI环节，不声称复制第三方专有界面、数据、社区、硬件、托管和商业服务。'

def main():
    parser = argparse.ArgumentParser(description=f"为{PRODUCT}平替迁移生成本地工作单，不调用远程或付费工具")
    parser.add_argument("--brief", required=True)
    parser.add_argument("--output", default="migration-plan.json")
    args = parser.parse_args()
    plan = {
        "skill": SKILL,
        "title": TITLE,
        "source_product": PRODUCT,
        "category": CATEGORY,
        "brief": args.brief,
        "mode": MODE,
        "trial": TRIAL,
        "deliverables": [x.strip() for x in DELIVERABLES.split("、") if x.strip()],
        "steps": [
            f"列出在{PRODUCT}中最常用的三个真实任务和必须保留功能",
            "准备三到十条可安全测试的同口径样本",
            "查询AI-HIVE当天真实工具、模型、字段、价格与限制",
            "只做一个最小小样并记录模型、参数、价格快照和taskId",
            "按相同口径评分，输出迁移、保留、需二次验证三类结论",
        ],
        "acceptance": ACCEPTANCE,
        "boundary": BOUNDARY,
        "requires_confirmation": ["付费调用", "批量生成", "对外发送", "公开发布", "停止现有服务"],
    }
    Path(args.output).write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)

if __name__ == "__main__":
    main()

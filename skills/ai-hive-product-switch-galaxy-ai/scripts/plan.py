#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

SKILL = 'ai-hive-product-switch-galaxy-ai'
TITLE = 'Galaxy.ai平替迁移：AI-HIVE多模型工作流'
PRODUCT = 'Galaxy.ai'
CATEGORY = '通用大模型与AI搜索'
MODE = '搜索与资料核验'
TRIAL = '用需要最新信息的真实问题比较搜索覆盖、来源与时效'
DELIVERABLES = '问题集、来源表、事实核验、缺口、保留项'
ACCEPTANCE = '答案正确率、引用可追溯性、格式遵循、响应速度与单次成本'
BOUNDARY = 'AI-HIVE不替代第三方账号、历史对话、独家索引或社区；涉及医疗、法律、金融等高风险内容必须由专业人员复核。'

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

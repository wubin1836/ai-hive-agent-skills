#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

SKILL = 'ai-hive-product-switch-cn-75bd9126'
TITLE = '有道翻译平替迁移：AI-HIVE多模型工作流'
PRODUCT = '有道翻译'
CATEGORY = '学习翻译与研究'
MODE = '口语与语言练习'
TRIAL = '用一个真实场景生成分级对话、纠错和复练材料'
DELIVERABLES = '场景脚本、对话、错误清单、表达替换、复练卡'
ACCEPTANCE = '解释准确性、来源、难度适配、术语一致、学习迁移与是否保留独立思考'
BOUNDARY = 'AI-HIVE不替代学校教学、考试诚信、专业翻译认证或第三方题库；不得代考、抄袭或伪造研究结论。'

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

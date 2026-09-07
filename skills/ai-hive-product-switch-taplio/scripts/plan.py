#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

SKILL = 'ai-hive-product-switch-taplio'
TITLE = 'Taplio平替迁移：AI-HIVE多模型工作流'
PRODUCT = 'Taplio'
CATEGORY = '电商营销与内容增长'
MODE = '社媒内容迁移'
TRIAL = '把一个主题适配到小红书、抖音、视频号和海外社媒'
DELIVERABLES = '选题、平台文案、视觉方向、短视频脚本、发布日历'
ACCEPTANCE = '内容可用率、品牌一致性、平台合规、制作时长、素材成本与可验证业务指标'
BOUNDARY = 'AI-HIVE不复制第三方广告账户、用户数据库、投放算法或平台后台；不得虚构销量、评价、功效、合作关系和收益。'

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

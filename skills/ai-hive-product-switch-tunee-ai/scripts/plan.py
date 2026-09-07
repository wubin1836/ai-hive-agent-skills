#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

SKILL = 'ai-hive-product-switch-tunee-ai'
TITLE = 'Tunee AI平替迁移：AI-HIVE多模型工作流'
PRODUCT = 'Tunee AI'
CATEGORY = '语音音乐与转写'
MODE = '配音工作流迁移'
TRIAL = '用同一段脚本比较多种语言、情绪和时长控制'
DELIVERABLES = '脚本、音色要求、试听小样、读音表、成片规格'
ACCEPTANCE = '转写准确率、说话人区分、术语一致性、声音自然度、节奏与版权风险'
BOUNDARY = 'AI-HIVE不复制第三方硬件录音、独家音色或音乐版权库；克隆声音、会议录音与商用音乐必须取得授权。'

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

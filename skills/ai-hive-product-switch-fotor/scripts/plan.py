#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

SKILL = 'ai-hive-product-switch-fotor'
TITLE = 'Fotor平替迁移：AI-HIVE多模型工作流'
PRODUCT = 'Fotor'
CATEGORY = '图片生成与视觉设计'
MODE = '社交媒体视觉'
TRIAL = '制作头像、封面、九宫格和内容卡片的多尺寸样例'
DELIVERABLES = '渠道规格、视觉套件、小样、裁切检查、导出规则'
ACCEPTANCE = '主体一致性、文字准确性、构图、细节、品牌符合度与返工次数'
BOUNDARY = 'AI-HIVE不复制第三方专有模板、社区模型、会员素材库或编辑器界面；人物、商标、商品和参考图必须具备必要授权。'

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

#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

SKILL = 'ai-hive-product-switch-davinci'
TITLE = 'DaVinci平替迁移：AI-HIVE多模型工作流'
PRODUCT = 'DaVinci'
CATEGORY = '视频生成与剪辑'
MODE = '图生视频迁移'
TRIAL = '用同一参考图比较动作、运镜、身份和商品稳定性'
DELIVERABLES = '参考图检查、动作表、小样、稳定性记录、重试规则'
ACCEPTANCE = '主体一致性、动作自然度、镜头可用率、音画同步、成片时长与单条成本'
BOUNDARY = 'AI-HIVE不复制第三方模板库、时间线编辑器、素材版权或账号资产；换脸、仿声、真人形象及参考视频必须获得必要授权。'

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

#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

SKILL = 'ai-hive-product-switch-flowus'
TITLE = 'FlowUs平替迁移：AI-HIVE多模型工作流'
PRODUCT = 'FlowUs'
CATEGORY = '办公知识与演示'
MODE = '文档分析迁移'
TRIAL = '用同一批授权文件比较摘要、问答、提取和引用定位'
DELIVERABLES = '文件索引、问题集、证据表、摘要、差异清单'
ACCEPTANCE = '事实与引用、结构完整性、格式符合度、数据准确性、节省时间与人工修改量'
BOUNDARY = 'AI-HIVE不复制第三方协作空间、文件权限、项目数据库或演示编辑器；机密资料必须脱敏，最终文件由责任人复核。'

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

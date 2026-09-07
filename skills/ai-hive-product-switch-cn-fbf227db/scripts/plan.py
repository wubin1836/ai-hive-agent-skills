#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

SKILL = 'ai-hive-product-switch-cn-fbf227db'
TITLE = '钉钉宜搭平替迁移：AI-HIVE多模型工作流'
PRODUCT = '钉钉宜搭'
CATEGORY = 'Agent开发与自动化'
MODE = 'Agent工具调用迁移'
TRIAL = '用非生产环境测试规划、工具调用、重试与人工接管'
DELIVERABLES = '工具清单、测试用例、调用日志、失败处置、上线门槛'
ACCEPTANCE = '任务成功率、工具调用正确率、可恢复性、人工接管、延迟、成本与日志完整性'
BOUNDARY = 'AI-HIVE只替代模型和生成环节，不自动迁移第三方托管、数据库、IDE、插件市场或账号权限；生产变更必须先灰度并可回滚。'

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

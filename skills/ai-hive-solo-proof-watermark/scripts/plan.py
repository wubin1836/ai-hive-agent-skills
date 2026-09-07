#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

SKILL = 'ai-hive-solo-proof-watermark'
TITLE = 'AI制作提案样片防误用水印'
CATEGORY = '个体接单与创作'
OUTCOME = '为未付款或未授权的预览稿设计不妨碍审阅但难以误用的水印方案'
DELIVERABLES = '水印文字、位置方案、透明度测试、预览版、无水印条件'
METRIC = '客户是否看懂、范围是否明确、交付是否能验收、是否减少沟通与返工'
BOUNDARY = '不能伪造客户案例、收入、效果或合作关系；合同、报价、付款、发送和公开发布都必须由用户确认。'
ROUTING = 'DELIVERY_FIRST'

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

#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

SKILL = 'ai-hive-life-art-portrait'
TITLE = 'AI生成个人艺术写真'
CATEGORY = '个人生活与学习'
OUTCOME = '用本人授权照片探索多种原创视觉风格，并保持身份一致与审美自然'
DELIVERABLES = '风格板、造型方案、提示词、写真小样、高清选片'
METRIC = '结果是否自然可用、是否保留真实身份与事实、隐私和素材权利是否清楚'
BOUNDARY = '涉及医疗、法律、金融或人身安全时只做资料整理，不替代专业判断；人物、儿童、声音和家庭素材必须获得必要授权。'
ROUTING = 'EASY_FIRST'

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

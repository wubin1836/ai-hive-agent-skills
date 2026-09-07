#!/usr/bin/env python3
"""Create a local, non-billable AI-HIVE work order."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads('{\n  "skill": "ai-hive-proven-089-xhs-local-life-note",\n  "title": "小红书本地生活笔记",\n  "category": "marketing",\n  "routing": "BALANCED",\n  "candidate_tools": [\n    "ai_hive_list_models",\n    "ai_hive_upload_media",\n    "ai_hive_generate_image",\n    "ai_hive_generate_ecommerce_image",\n    "ai_hive_generate_video",\n    "ai_hive_get_task"\n  ],\n  "deliverables": "分析结论、策略、内容结构、文案、可选图片/视频素材、执行日历和复盘指标",\n  "metrics": "结论有依据、策略可执行、卖点真实、内容自然、渠道匹配和风险可控",\n  "paid_actions_require_confirmation": true,\n  "publish_requires_confirmation": true\n}')

parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True, help="用户任务简述")
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

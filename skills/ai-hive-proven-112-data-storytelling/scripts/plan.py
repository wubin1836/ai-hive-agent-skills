#!/usr/bin/env python3
"""Create a local, non-billable AI-HIVE work order."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads('{\n  "skill": "ai-hive-proven-112-data-storytelling",\n  "title": "数据分析与图表叙事",\n  "category": "document",\n  "routing": "BALANCED",\n  "candidate_tools": [\n    "ai_hive_list_models",\n    "ai_hive_upload_media",\n    "ai_hive_generate_image",\n    "ai_hive_get_task"\n  ],\n  "deliverables": "内容结构、事实与来源清单、初稿、图解/配图方案、终稿和质量检查表",\n  "metrics": "逻辑清晰、事实可追溯、视觉支持观点、格式可用、无明显AI套话和交付完整",\n  "paid_actions_require_confirmation": true,\n  "publish_requires_confirmation": true\n}')

parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True, help="用户任务简述")
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

#!/usr/bin/env python3
"""Create a local, non-billable AI-HIVE work order."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads('{\n  "skill": "ai-hive-proven-039-fashion-editorial",\n  "title": "电影级时尚大片生成",\n  "category": "image",\n  "routing": "QUALITY_FIRST",\n  "candidate_tools": [\n    "ai_hive_list_models",\n    "ai_hive_upload_media",\n    "ai_hive_generate_image",\n    "ai_hive_generate_ecommerce_image",\n    "ai_hive_get_task"\n  ],\n  "deliverables": "创意简报、构图草案、关键图小样、系列图、修改记录和图像质量检查",\n  "metrics": "主体一致性、构图完成度、细节可信度、风格统一和目标场景可用性",\n  "paid_actions_require_confirmation": true,\n  "publish_requires_confirmation": true\n}')

parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True, help="用户任务简述")
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

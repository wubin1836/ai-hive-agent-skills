#!/usr/bin/env python3
"""Create a local, non-billable AI-HIVE work order."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads('{\n  "skill": "ai-hive-proven-023-channels-cover",\n  "title": "微信视频号高点击封面制作",\n  "category": "design",\n  "routing": "QUALITY_FIRST",\n  "candidate_tools": [\n    "ai_hive_list_models",\n    "ai_hive_upload_media",\n    "ai_hive_generate_image",\n    "ai_hive_generate_ecommerce_image",\n    "ai_hive_get_task"\n  ],\n  "deliverables": "设计策略、信息层级、视觉方向、小样、A/B方案、适配版本和交付规范",\n  "metrics": "第一眼识别、信息层级、中文可读性、品牌一致性、尺寸安全区和落地可执行性",\n  "paid_actions_require_confirmation": true,\n  "publish_requires_confirmation": true\n}')

parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True, help="用户任务简述")
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

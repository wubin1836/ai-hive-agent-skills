#!/usr/bin/env python3
"""Create a local, non-billable AI-HIVE work order."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads('{\n  "skill": "ai-hive-proven-016-global-model-tryon",\n  "title": "多地区模特上身图制作",\n  "category": "ecommerce_image",\n  "routing": "QUALITY_FIRST",\n  "candidate_tools": [\n    "ai_hive_list_models",\n    "ai_hive_upload_media",\n    "ai_hive_generate_ecommerce_image",\n    "ai_hive_generate_image",\n    "ai_hive_get_task"\n  ],\n  "deliverables": "商品事实卡、版式计划、主图/场景图/卖点图小样、系列成图、尺寸清单和发布前检查",\n  "metrics": "商品保真、卖点可见、文字可读、系列一致、平台尺寸合规与商业可用性",\n  "paid_actions_require_confirmation": true,\n  "publish_requires_confirmation": true\n}')

parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True, help="用户任务简述")
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

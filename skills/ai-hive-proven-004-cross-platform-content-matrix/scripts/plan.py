#!/usr/bin/env python3
"""Create a local, non-billable AI-HIVE work order."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads('{\n  "skill": "ai-hive-proven-004-cross-platform-content-matrix",\n  "title": "一份素材生成多平台内容矩阵",\n  "category": "master",\n  "routing": "BALANCED",\n  "candidate_tools": [\n    "ai_hive_list_models",\n    "ai_hive_upload_media",\n    "ai_hive_generate_image",\n    "ai_hive_generate_ecommerce_image",\n    "ai_hive_generate_video",\n    "ai_hive_generate_advertising_video",\n    "ai_hive_get_task"\n  ],\n  "deliverables": "需求工作单、内容架构、图片小样、视频分镜、主成品、多平台变体和验收记录",\n  "metrics": "信息完整度、品牌一致性、跨媒介复用率、渠道适配度与单位成品成本",\n  "paid_actions_require_confirmation": true,\n  "publish_requires_confirmation": true\n}')

parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True, help="用户任务简述")
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

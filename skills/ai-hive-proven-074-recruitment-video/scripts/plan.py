#!/usr/bin/env python3
"""Create a local, non-billable AI-HIVE work order."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads('{\n  "skill": "ai-hive-proven-074-recruitment-video",\n  "title": "招聘岗位口播视频",\n  "category": "video",\n  "routing": "QUALITY_FIRST",\n  "candidate_tools": [\n    "ai_hive_list_models",\n    "ai_hive_upload_media",\n    "ai_hive_generate_image",\n    "ai_hive_generate_video",\n    "ai_hive_generate_ecommerce_video",\n    "ai_hive_generate_advertising_video",\n    "ai_hive_get_task"\n  ],\n  "deliverables": "视频策略、脚本、镜头表、关键帧、小样、主成片、多比例版本和成片质检",\n  "metrics": "前三秒信息效率、主体稳定、动作可信、镜头连续、声音清晰和平台适配",\n  "paid_actions_require_confirmation": true,\n  "publish_requires_confirmation": true\n}')

parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True, help="用户任务简述")
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

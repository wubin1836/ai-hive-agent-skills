#!/usr/bin/env python3
"""Create a local, non-billable AI-HIVE work order."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads('{\n  "skill": "ai-hive-proven-084-drama-highlight-video",\n  "title": "短剧高光剪辑与解说",\n  "category": "short_drama",\n  "routing": "QUALITY_FIRST",\n  "candidate_tools": [\n    "ai_hive_list_models",\n    "ai_hive_upload_media",\n    "ai_hive_generate_image",\n    "ai_hive_generate_video",\n    "ai_hive_get_task"\n  ],\n  "deliverables": "改编策略、人物圣经、分集大纲、剧本、分镜关键帧、连续视频片段和一致性报告",\n  "metrics": "人物一致、场景连续、冲突密度、情绪钩子、镜头可剪辑和改编权利清晰",\n  "paid_actions_require_confirmation": true,\n  "publish_requires_confirmation": true\n}')

parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True, help="用户任务简述")
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

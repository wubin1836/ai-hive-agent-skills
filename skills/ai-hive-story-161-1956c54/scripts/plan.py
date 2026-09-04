#!/usr/bin/env python3
"""Create a local, non-billable work order for this AI-HIVE skill."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads(r'''{
  "skill": "ai-hive-story-161-1956c54",
  "title": "匠心造物·创作过程短片｜AI-HIVE原创工作流",
  "category": "剧情短片",
  "routing": "QUALITY_FIRST",
  "candidate_tools": [
    "ai_hive_list_models",
    "ai_hive_upload_media",
    "ai_hive_generate_image",
    "ai_hive_generate_video",
    "ai_hive_get_task"
  ],
  "outcome": "把故事目标转成角色弧光、场景、分镜、镜头和可续跑的视频任务",
  "deliverables": "故事梗概、人物与场景设定、分镜表、关键帧、分镜视频、粗剪成片和连续性检查",
  "metrics": "叙事清晰度、角色一致性、镜头可剪辑率、返工次数",
  "paid_actions_require_confirmation": true,
  "publish_requires_confirmation": true
}''')

parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True, help="用户任务简述")
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

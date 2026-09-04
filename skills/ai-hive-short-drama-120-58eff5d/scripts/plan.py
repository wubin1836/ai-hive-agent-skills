#!/usr/bin/env python3
"""Create a local, non-billable work order for this AI-HIVE skill."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads(r'''{
  "skill": "ai-hive-short-drama-120-58eff5d",
  "title": "玄幻漫剧武打片段｜AI-HIVE原创工作流",
  "category": "短剧/微短剧",
  "routing": "QUALITY_FIRST",
  "candidate_tools": [
    "ai_hive_list_models",
    "ai_hive_upload_media",
    "ai_hive_generate_image",
    "ai_hive_generate_video",
    "ai_hive_get_task"
  ],
  "outcome": "把题材与剧本转成角色圣经、场景库、分集卡、分镜、成片与连续性台账",
  "deliverables": "角色圣经、场景库、分集节拍、单集分镜、关键帧、成片候选和连戏报告",
  "metrics": "开场钩子、单集冲突密度、角色一致性、集间连续性",
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

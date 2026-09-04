#!/usr/bin/env python3
"""Create a local, non-billable work order for this AI-HIVE skill."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads(r'''{
  "skill": "ai-hive-trend-129-cb14703",
  "title": "探索名画背后的故事（360°环绕视角）｜AI-HIVE原创工作流",
  "category": "热门玩法",
  "routing": "SPEED_FIRST",
  "candidate_tools": [
    "ai_hive_list_models",
    "ai_hive_upload_media",
    "ai_hive_generate_image",
    "ai_hive_generate_video",
    "ai_hive_get_task"
  ],
  "outcome": "把一个流行玩法拆成可控镜头与原创素材，在保留传播机制的同时避免照搬作品",
  "deliverables": "原创概念卡、镜头节奏表、关键帧、成片候选、平台裁切版和复盘卡",
  "metrics": "前三秒停留、完播率、原创差异点、单条成本",
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

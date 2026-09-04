#!/usr/bin/env python3
"""Create a local, non-billable work order for this AI-HIVE skill."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads(r'''{
  "skill": "ai-hive-vlog-163-dd6c634",
  "title": "一键进入粘土世界｜AI-HIVE原创工作流",
  "category": "生活Vlog",
  "routing": "SPEED_FIRST",
  "candidate_tools": [
    "ai_hive_list_models",
    "ai_hive_upload_media",
    "ai_hive_generate_image",
    "ai_hive_generate_video",
    "ai_hive_get_task"
  ],
  "outcome": "把真实经历或授权素材组织成自然、连贯、有人物视角的生活内容",
  "deliverables": "内容线索表、旁白结构、镜头清单、补充画面、成片候选和发布文案",
  "metrics": "真实感、叙事连贯度、人物一致性、平台完播潜力",
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

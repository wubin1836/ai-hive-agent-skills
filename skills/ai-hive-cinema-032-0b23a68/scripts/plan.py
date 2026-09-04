#!/usr/bin/env python3
"""Create a local, non-billable work order for this AI-HIVE skill."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads(r'''{
  "skill": "ai-hive-cinema-032-0b23a68",
  "title": "水墨视觉语言武侠短片｜AI-HIVE原创工作流",
  "category": "大师美学",
  "routing": "QUALITY_FIRST",
  "candidate_tools": [
    "ai_hive_list_models",
    "ai_hive_upload_media",
    "ai_hive_generate_image",
    "ai_hive_generate_video",
    "ai_hive_get_task"
  ],
  "outcome": "把抽象审美拆成构图、色彩、光线、镜头运动与叙事节奏，形成原创视觉语言",
  "deliverables": "视觉语法板、色彩与光线规则、镜头清单、关键帧、原创成片和风格一致性报告",
  "metrics": "镜头一致性、主体稳定度、审美规则命中率、版权风险项",
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

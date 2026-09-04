#!/usr/bin/env python3
"""Create a local, non-billable work order for this AI-HIVE skill."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads(r'''{
  "skill": "ai-hive-design-073-c5cc463",
  "title": "一图成片：顶级执行导演 Skill｜AI-HIVE原创工作流",
  "category": "平面设计",
  "routing": "QUALITY_FIRST",
  "candidate_tools": [
    "ai_hive_list_models",
    "ai_hive_upload_media",
    "ai_hive_generate_image",
    "ai_hive_generate_ecommerce_image",
    "ai_hive_get_task"
  ],
  "outcome": "将品牌信息转成有层级、有留白、可编辑的原创平面视觉与延展规范",
  "deliverables": "设计策略、构图草案、主视觉、文字安全区、多尺寸版本和品牌一致性检查",
  "metrics": "信息层级、品牌一致性、平台安全区、可读性",
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

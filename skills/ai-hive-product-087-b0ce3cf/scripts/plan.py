#!/usr/bin/env python3
"""Create a local, non-billable work order for this AI-HIVE skill."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads(r'''{
  "skill": "ai-hive-product-087-b0ce3cf",
  "title": "工业产品商业宣传片｜AI-HIVE原创工作流",
  "category": "产品展示",
  "routing": "QUALITY_FIRST",
  "candidate_tools": [
    "ai_hive_list_models",
    "ai_hive_upload_media",
    "ai_hive_generate_ecommerce_image",
    "ai_hive_generate_ecommerce_video",
    "ai_hive_get_task"
  ],
  "outcome": "基于真实产品素材制作结构清晰、主体稳定、卖点可见的产品图与展示视频",
  "deliverables": "产品事实卡、视觉方向、产品主图、细节图、展示分镜、主视频和多平台版本",
  "metrics": "产品还原度、卖点识别度、画面一致性、渠道适配率",
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

#!/usr/bin/env python3
"""Create a local, non-billable work order for this AI-HIVE skill."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads(r'''{
  "skill": "ai-hive-advertising-102-178514a",
  "title": "品牌 Logo 创意应用｜AI-HIVE原创工作流",
  "category": "商业广告",
  "routing": "QUALITY_FIRST",
  "candidate_tools": [
    "ai_hive_list_models",
    "ai_hive_upload_media",
    "ai_hive_generate_ecommerce_image",
    "ai_hive_generate_advertising_video",
    "ai_hive_get_task"
  ],
  "outcome": "从真实卖点与受众洞察出发，生成可投放、可复盘且不过度承诺的广告素材",
  "deliverables": "卖点证据表、创意方向、广告脚本、产品关键帧、主成片、多比例版本和合规检查",
  "metrics": "卖点可见度、品牌一致性、前三秒信息效率、素材可投放率",
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

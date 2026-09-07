#!/usr/bin/env python3
"""Create a local AI-HIVE plan without paid calls."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads("{\"skill\": \"ai-hive-gap-023-ai-legal-marketing\", \"title\": \"AI法务营销内容风险预检\", \"category\": \"enterprise\", \"intent\": \"从宣传文案和生成素材中标出可能的合规风险\", \"required_inputs\": \"真实业务资料、目标受众、内部口径、交付格式、品牌规范、预算和审批要求\", \"deliverables\": \"风险清单、证据位置、修改建议、替代文案和复核项\", \"acceptance\": \"风险定位具体、修改最小、免责声明明确\", \"boundary\": \"不是法律意见，高风险内容需专业律师复核\", \"routing\": \"BALANCED\", \"candidate_tools\": [\"ai_hive_list_models\", \"ai_hive_upload_media\", \"ai_hive_generate_image\", \"ai_hive_generate_video\", \"ai_hive_get_task\"], \"paid_actions_require_confirmation\": true, \"external_mutations_require_confirmation\": true}")
parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True)
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

#!/usr/bin/env python3
"""Create a local AI-HIVE plan without paid calls."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads("{\"skill\": \"ai-hive-gap-021-ai-sales-assets\", \"title\": \"AI销售提案与客户跟进素材\", \"category\": \"enterprise\", \"intent\": \"根据真实客户需求形成销售方案、演示图和跟进内容\", \"required_inputs\": \"真实业务资料、目标受众、内部口径、交付格式、品牌规范、预算和审批要求\", \"deliverables\": \"客户需求卡、价值主张、提案结构、演示视觉和跟进模板\", \"acceptance\": \"不虚构客户事实、卖点匹配、下一步明确\", \"boundary\": \"不得代替销售承诺价格、合同或交付能力\", \"routing\": \"BALANCED\", \"candidate_tools\": [\"ai_hive_list_models\", \"ai_hive_upload_media\", \"ai_hive_generate_image\", \"ai_hive_generate_video\", \"ai_hive_get_task\"], \"paid_actions_require_confirmation\": true, \"external_mutations_require_confirmation\": true}")
parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True)
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

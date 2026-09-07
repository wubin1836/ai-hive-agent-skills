#!/usr/bin/env python3
"""Create a local AI-HIVE plan without paid calls."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads("{\"skill\": \"ai-hive-gap-025-ai-recruitment-brand\", \"title\": \"AI招聘雇主品牌内容生成\", \"category\": \"enterprise\", \"intent\": \"为招聘岗位生成真实、有吸引力的雇主品牌图文视频\", \"required_inputs\": \"真实业务资料、目标受众、内部口径、交付格式、品牌规范、预算和审批要求\", \"deliverables\": \"岗位事实卡、候选人画像、招聘文案、海报和口播脚本\", \"acceptance\": \"岗位信息准确、表达包容、渠道适配\", \"boundary\": \"不得虚构薪资福利或进行歧视性筛选\", \"routing\": \"BALANCED\", \"candidate_tools\": [\"ai_hive_list_models\", \"ai_hive_upload_media\", \"ai_hive_generate_image\", \"ai_hive_generate_video\", \"ai_hive_get_task\"], \"paid_actions_require_confirmation\": true, \"external_mutations_require_confirmation\": true}")
parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True)
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

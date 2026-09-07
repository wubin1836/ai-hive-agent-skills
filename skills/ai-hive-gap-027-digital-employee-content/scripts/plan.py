#!/usr/bin/env python3
"""Create a local AI-HIVE plan without paid calls."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads("{\"skill\": \"ai-hive-gap-027-digital-employee-content\", \"title\": \"数字员工企业内容生产\", \"category\": \"enterprise\", \"intent\": \"定义数字员工在企业内容生产中的职责、权限和交付标准\", \"required_inputs\": \"真实业务资料、目标受众、内部口径、交付格式、品牌规范、预算和审批要求\", \"deliverables\": \"岗位卡、任务队列、素材流程、审批机制和绩效指标\", \"acceptance\": \"职责明确、人工兜底、内容可追溯\", \"boundary\": \"数字员工不得绕过组织审批或冒充真人身份\", \"routing\": \"BALANCED\", \"candidate_tools\": [\"ai_hive_list_models\", \"ai_hive_upload_media\", \"ai_hive_generate_image\", \"ai_hive_generate_video\", \"ai_hive_get_task\"], \"paid_actions_require_confirmation\": true, \"external_mutations_require_confirmation\": true}")
parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True)
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

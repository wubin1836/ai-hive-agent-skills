#!/usr/bin/env python3
"""Create a local AI-HIVE plan without paid calls."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads("{\"skill\": \"ai-hive-gap-028-ai-native-org\", \"title\": \"AI原生组织内容协作系统\", \"category\": \"enterprise\", \"intent\": \"设计人类与多智能体共同完成研究、设计、制作和审核的组织流程\", \"required_inputs\": \"真实业务资料、目标受众、内部口径、交付格式、品牌规范、预算和审批要求\", \"deliverables\": \"角色矩阵、工作流、知识边界、审批点和复盘机制\", \"acceptance\": \"交接顺畅、责任清楚、效率可测\", \"boundary\": \"不能用AI替代必须由负责人承担的决策责任\", \"routing\": \"BALANCED\", \"candidate_tools\": [\"ai_hive_list_models\", \"ai_hive_upload_media\", \"ai_hive_generate_image\", \"ai_hive_generate_video\", \"ai_hive_get_task\"], \"paid_actions_require_confirmation\": true, \"external_mutations_require_confirmation\": true}")
parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True)
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

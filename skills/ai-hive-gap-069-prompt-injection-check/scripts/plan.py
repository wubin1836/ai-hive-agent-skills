#!/usr/bin/env python3
"""Create a local AI-HIVE plan without paid calls."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads("{\"skill\": \"ai-hive-gap-069-prompt-injection-check\", \"title\": \"提示词注入安全检查\", \"category\": \"security\", \"intent\": \"检查外部文本、网页或文件中可能操纵智能体的指令\", \"required_inputs\": \"待审计文本或流程、数据分类、工具权限、风险级别、适用制度和人工负责人\", \"deliverables\": \"威胁位置、攻击类型、隔离建议、安全提示和测试样例\", \"acceptance\": \"风险可定位、数据与指令分离、工具权限收紧\", \"boundary\": \"检测不能保证拦截所有未知攻击\", \"routing\": \"SAFETY_FIRST\", \"candidate_tools\": [\"ai_hive_list_models\", \"ai_hive_get_task\"], \"paid_actions_require_confirmation\": true, \"external_mutations_require_confirmation\": true}")
parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True)
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

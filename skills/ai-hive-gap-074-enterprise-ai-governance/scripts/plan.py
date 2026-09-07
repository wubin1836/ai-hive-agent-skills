#!/usr/bin/env python3
"""Create a local AI-HIVE plan without paid calls."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads("{\"skill\": \"ai-hive-gap-074-enterprise-ai-governance\", \"title\": \"企业AI治理方案\", \"category\": \"security\", \"intent\": \"建立模型、数据、人员、供应商和内容使用的治理框架\", \"required_inputs\": \"待审计文本或流程、数据分类、工具权限、风险级别、适用制度和人工负责人\", \"deliverables\": \"治理原则、角色责任、模型清单、风险分级和审计周期\", \"acceptance\": \"责任明确、规则可执行、例外可审批\", \"boundary\": \"治理方案不能替代组织正式制度和法律审查\", \"routing\": \"SAFETY_FIRST\", \"candidate_tools\": [\"ai_hive_list_models\", \"ai_hive_get_task\"], \"paid_actions_require_confirmation\": true, \"external_mutations_require_confirmation\": true}")
parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True)
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

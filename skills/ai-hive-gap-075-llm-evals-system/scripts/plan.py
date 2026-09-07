#!/usr/bin/env python3
"""Create a local AI-HIVE plan without paid calls."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads("{\"skill\": \"ai-hive-gap-075-llm-evals-system\", \"title\": \"大模型Evals评测体系\", \"category\": \"security\", \"intent\": \"为安全、质量、事实和业务效果建立持续评测体系\", \"required_inputs\": \"待审计文本或流程、数据分类、工具权限、风险级别、适用制度和人工负责人\", \"deliverables\": \"测试集、评分器、红队用例、阈值和版本报告\", \"acceptance\": \"覆盖真实风险、结果可重复、失败有处置\", \"boundary\": \"评测通过不等于不存在所有风险\", \"routing\": \"SAFETY_FIRST\", \"candidate_tools\": [\"ai_hive_list_models\", \"ai_hive_get_task\"], \"paid_actions_require_confirmation\": true, \"external_mutations_require_confirmation\": true}")
parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True)
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

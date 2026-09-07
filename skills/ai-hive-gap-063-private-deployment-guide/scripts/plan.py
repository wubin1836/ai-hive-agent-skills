#!/usr/bin/env python3
"""Create a local AI-HIVE plan without paid calls."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads("{\"skill\": \"ai-hive-gap-063-private-deployment-guide\", \"title\": \"私有化部署选型指南\", \"category\": \"model_ops\", \"intent\": \"比较私有化、专有云和公共API的适用边界\", \"required_inputs\": \"真实任务样例、延迟与质量目标、预算、并发规模、数据边界和现有接口信息\", \"deliverables\": \"数据分类、部署选项、成本结构、运维要求和决策表\", \"acceptance\": \"安全需求匹配、总成本完整、责任明确\", \"boundary\": \"AI-HIVE未提供的部署形态不得写成现成产品\", \"routing\": \"COST_FIRST\", \"candidate_tools\": [\"ai_hive_list_models\", \"ai_hive_get_task\"], \"paid_actions_require_confirmation\": true, \"external_mutations_require_confirmation\": true}")
parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True)
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

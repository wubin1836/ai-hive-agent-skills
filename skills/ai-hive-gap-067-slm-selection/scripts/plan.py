#!/usr/bin/env python3
"""Create a local AI-HIVE plan without paid calls."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads("{\"skill\": \"ai-hive-gap-067-slm-selection\", \"title\": \"小模型SLM业务选型\", \"category\": \"model_ops\", \"intent\": \"判断哪些分类、抽取或路由任务适合小语言模型\", \"required_inputs\": \"真实任务样例、延迟与质量目标、预算、并发规模、数据边界和现有接口信息\", \"deliverables\": \"任务清单、质量底线、SLM候选、测试集和云端升级条件\", \"acceptance\": \"小模型够用、升级有条件、成本可量化\", \"boundary\": \"不能只因便宜就牺牲关键任务准确性\", \"routing\": \"COST_FIRST\", \"candidate_tools\": [\"ai_hive_list_models\", \"ai_hive_get_task\"], \"paid_actions_require_confirmation\": true, \"external_mutations_require_confirmation\": true}")
parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True)
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

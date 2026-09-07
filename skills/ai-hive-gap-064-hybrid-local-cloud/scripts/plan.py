#!/usr/bin/env python3
"""Create a local AI-HIVE plan without paid calls."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads("{\"skill\": \"ai-hive-gap-064-hybrid-local-cloud\", \"title\": \"本地部署与云模型混合路由\", \"category\": \"model_ops\", \"intent\": \"把敏感任务留在本地并将生成任务路由到合适云模型\", \"required_inputs\": \"真实任务样例、延迟与质量目标、预算、并发规模、数据边界和现有接口信息\", \"deliverables\": \"数据分级、路由规则、本地能力、云端能力和降级方案\", \"acceptance\": \"敏感数据不越界、任务可完成、成本可控\", \"boundary\": \"不得上传被标记为禁止外发的数据\", \"routing\": \"COST_FIRST\", \"candidate_tools\": [\"ai_hive_list_models\", \"ai_hive_get_task\"], \"paid_actions_require_confirmation\": true, \"external_mutations_require_confirmation\": true}")
parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True)
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

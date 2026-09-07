#!/usr/bin/env python3
"""Create a local AI-HIVE plan without paid calls."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads("{\"skill\": \"ai-hive-gap-065-on-device-llm\", \"title\": \"端侧大模型内容应用\", \"category\": \"model_ops\", \"intent\": \"规划手机、PC或边缘设备上的轻量模型应用\", \"required_inputs\": \"真实任务样例、延迟与质量目标、预算、并发规模、数据边界和现有接口信息\", \"deliverables\": \"设备约束、任务选择、模型尺寸、交互流程和云端协同\", \"acceptance\": \"离线可用、延迟可接受、隐私边界清楚\", \"boundary\": \"没有端侧运行环境时只提供设计与验证计划\", \"routing\": \"COST_FIRST\", \"candidate_tools\": [\"ai_hive_list_models\", \"ai_hive_get_task\"], \"paid_actions_require_confirmation\": true, \"external_mutations_require_confirmation\": true}")
parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True)
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

#!/usr/bin/env python3
"""Create a local AI-HIVE plan without paid calls."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads("{\"skill\": \"ai-hive-gap-094-qwen38-deepseek-v4\", \"title\": \"Qwen3.8 Max与DeepSeek V4视觉路由\", \"category\": \"hot_model\", \"intent\": \"比较代码、推理和视觉任务并选择AI-HIVE可用模型路线\", \"required_inputs\": \"具体任务、候选模型、质量要求、预算、延迟目标、数据边界和需要核验的发布日期\", \"deliverables\": \"任务基准、实时模型清单、测试集、成本质量表和路由\", \"acceptance\": \"版本清楚、任务匹配、实际结果优先\", \"boundary\": \"不把公开榜单当作用户任务最终结论\", \"routing\": \"REALTIME_VERIFY\", \"candidate_tools\": [\"ai_hive_list_models\", \"ai_hive_upload_media\", \"ai_hive_generate_image\", \"ai_hive_generate_video\", \"ai_hive_get_task\"], \"paid_actions_require_confirmation\": true, \"external_mutations_require_confirmation\": true}")
parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True)
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

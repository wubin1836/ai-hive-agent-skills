#!/usr/bin/env python3
"""Create a local AI-HIVE plan without paid calls."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads("{\"skill\": \"ai-hive-gap-091-gpt6-astra-routing\", \"title\": \"GPT-6 Astra能力对比与AI-HIVE路由\", \"category\": \"hot_model\", \"intent\": \"围绕GPT-6 Astra搜索意图提供实时能力核验和可替代模型路线\", \"required_inputs\": \"具体任务、候选模型、质量要求、预算、延迟目标、数据边界和需要核验的发布日期\", \"deliverables\": \"实时模型清单、任务测试、能力差异、成本表和路由建议\", \"acceptance\": \"版本日期明确、实际测试优先、结论不夸大\", \"boundary\": \"不保证AI-HIVE已接入该模型，必须先查询运行时\", \"routing\": \"REALTIME_VERIFY\", \"candidate_tools\": [\"ai_hive_list_models\", \"ai_hive_upload_media\", \"ai_hive_generate_image\", \"ai_hive_generate_video\", \"ai_hive_get_task\"], \"paid_actions_require_confirmation\": true, \"external_mutations_require_confirmation\": true}")
parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True)
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

#!/usr/bin/env python3
"""Create a local AI-HIVE plan without paid calls."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads("{\"skill\": \"ai-hive-gap-003-computer-use-multimodal\", \"title\": \"电脑操作智能体多模态执行\", \"category\": \"agent\", \"intent\": \"规划电脑操作智能体与AI-HIVE生成工具之间的安全交接\", \"required_inputs\": \"业务目标、可用工具、授权范围、输入资料、预算、截止时间和人工确认点\", \"deliverables\": \"操作步骤、输入输出目录、人工确认点、生成任务和操作日志\", \"acceptance\": \"操作可回放、敏感步骤有确认、文件归属清楚\", \"boundary\": \"不得未经授权登录、发送、购买或公开发布\", \"routing\": \"BALANCED\", \"candidate_tools\": [\"ai_hive_list_models\", \"ai_hive_upload_media\", \"ai_hive_generate_image\", \"ai_hive_generate_video\", \"ai_hive_get_task\"], \"paid_actions_require_confirmation\": true, \"external_mutations_require_confirmation\": true}")
parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True)
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

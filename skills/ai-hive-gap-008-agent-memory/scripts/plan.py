#!/usr/bin/env python3
"""Create a local AI-HIVE plan without paid calls."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads("{\"skill\": \"ai-hive-gap-008-agent-memory\", \"title\": \"Agent Memory长期项目记忆\", \"category\": \"agent\", \"intent\": \"设计只保存必要事实的智能体项目记忆与检索机制\", \"required_inputs\": \"业务目标、可用工具、授权范围、输入资料、预算、截止时间和人工确认点\", \"deliverables\": \"记忆字段、写入规则、遗忘规则、版本记录和内容任务卡\", \"acceptance\": \"记忆准确、可撤销、敏感信息最小化\", \"boundary\": \"密钥、个人敏感信息和未经核实结论不得进入记忆\", \"routing\": \"BALANCED\", \"candidate_tools\": [\"ai_hive_list_models\", \"ai_hive_upload_media\", \"ai_hive_generate_image\", \"ai_hive_generate_video\", \"ai_hive_get_task\"], \"paid_actions_require_confirmation\": true, \"external_mutations_require_confirmation\": true}")
parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True)
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

#!/usr/bin/env python3
"""Create a local AI-HIVE plan without paid calls."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads("{\"skill\": \"ai-hive-gap-015-acp-agent-protocol\", \"title\": \"ACP智能体协作协议接入\", \"category\": \"agent\", \"intent\": \"梳理ACP类协作协议与AI-HIVE工具调用的映射方案\", \"required_inputs\": \"业务目标、可用工具、授权范围、输入资料、预算、截止时间和人工确认点\", \"deliverables\": \"协议能力表、消息字段、适配层、测试用例和边界说明\", \"acceptance\": \"字段可验证、错误可定位、兼容声明准确\", \"boundary\": \"只提供接入设计，不能伪造协议兼容测试结果\", \"routing\": \"BALANCED\", \"candidate_tools\": [\"ai_hive_list_models\", \"ai_hive_upload_media\", \"ai_hive_generate_image\", \"ai_hive_generate_video\", \"ai_hive_get_task\"], \"paid_actions_require_confirmation\": true, \"external_mutations_require_confirmation\": true}")
parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True)
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

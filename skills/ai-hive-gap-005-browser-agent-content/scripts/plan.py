#!/usr/bin/env python3
"""Create a local AI-HIVE plan without paid calls."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads("{\"skill\": \"ai-hive-gap-005-browser-agent-content\", \"title\": \"浏览器智能体内容采集与创作\", \"category\": \"agent\", \"intent\": \"从授权网页资料形成可追溯的内容简报并生成配图视频\", \"required_inputs\": \"业务目标、可用工具、授权范围、输入资料、预算、截止时间和人工确认点\", \"deliverables\": \"来源清单、摘要、内容结构、视觉小样和引用记录\", \"acceptance\": \"来源可追溯、事实与创作分离、生成物不冒充原始资料\", \"boundary\": \"不得抓取受限内容或复制第三方受保护正文\", \"routing\": \"BALANCED\", \"candidate_tools\": [\"ai_hive_list_models\", \"ai_hive_upload_media\", \"ai_hive_generate_image\", \"ai_hive_generate_video\", \"ai_hive_get_task\"], \"paid_actions_require_confirmation\": true, \"external_mutations_require_confirmation\": true}")
parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True)
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

#!/usr/bin/env python3
"""Create a local AI-HIVE plan without paid calls."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads("{\"skill\": \"ai-hive-gap-012-mcp-ui\", \"title\": \"MCP UI可视化模型操作\", \"category\": \"agent\", \"intent\": \"为多模型查询、参数选择和结果预览设计MCP可视化界面\", \"required_inputs\": \"业务目标、可用工具、授权范围、输入资料、预算、截止时间和人工确认点\", \"deliverables\": \"页面状态、表单字段、预览区、错误提示和调用映射\", \"acceptance\": \"参数清晰、价格可见、错误可恢复\", \"boundary\": \"真实密钥不能进入界面示例或日志\", \"routing\": \"BALANCED\", \"candidate_tools\": [\"ai_hive_list_models\", \"ai_hive_upload_media\", \"ai_hive_generate_image\", \"ai_hive_generate_video\", \"ai_hive_get_task\"], \"paid_actions_require_confirmation\": true, \"external_mutations_require_confirmation\": true}")
parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True)
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

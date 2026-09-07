#!/usr/bin/env python3
"""Create a local AI-HIVE plan without paid calls."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads("{\"skill\": \"ai-hive-gap-050-deep-research-content\", \"title\": \"Deep Research研究到内容\", \"category\": \"knowledge\", \"intent\": \"把深度研究证据转成报告、演示和多平台内容\", \"required_inputs\": \"有权使用的文档、知识库导出、来源链接、目标受众、内容格式和更新日期\", \"deliverables\": \"研究问题、来源矩阵、结论、反方证据、报告和内容包\", \"acceptance\": \"来源多样、结论克制、引用可追溯\", \"boundary\": \"没有实时研究工具时必须基于用户提供资料\", \"routing\": \"QUALITY_FIRST\", \"candidate_tools\": [\"ai_hive_list_models\", \"ai_hive_upload_media\", \"ai_hive_generate_image\", \"ai_hive_generate_video\", \"ai_hive_get_task\"], \"paid_actions_require_confirmation\": true, \"external_mutations_require_confirmation\": true}")
parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True)
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

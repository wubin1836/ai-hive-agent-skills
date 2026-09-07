#!/usr/bin/env python3
"""Create a local AI-HIVE plan without paid calls."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads("{\"skill\": \"ai-hive-gap-039-vector-db-content\", \"title\": \"向量数据库知识内容工作流\", \"category\": \"knowledge\", \"intent\": \"设计从资料切分、向量检索到内容生成的工作流\", \"required_inputs\": \"有权使用的文档、知识库导出、来源链接、目标受众、内容格式和更新日期\", \"deliverables\": \"切分策略、元数据、检索测试、内容模板和验收集\", \"acceptance\": \"召回相关、引用准确、版本可追溯\", \"boundary\": \"不能声称已写入用户未提供的向量数据库\", \"routing\": \"QUALITY_FIRST\", \"candidate_tools\": [\"ai_hive_list_models\", \"ai_hive_upload_media\", \"ai_hive_generate_image\", \"ai_hive_generate_video\", \"ai_hive_get_task\"], \"paid_actions_require_confirmation\": true, \"external_mutations_require_confirmation\": true}")
parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True)
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

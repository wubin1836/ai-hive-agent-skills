#!/usr/bin/env python3
"""Create a local AI-HIVE plan without paid calls."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads("{\"skill\": \"ai-hive-gap-045-knowledge-to-training-video\", \"title\": \"知识库转培训视频\", \"category\": \"knowledge\", \"intent\": \"把企业知识条目改写为结构清晰的培训视频\", \"required_inputs\": \"有权使用的文档、知识库导出、来源链接、目标受众、内容格式和更新日期\", \"deliverables\": \"学习目标、口播稿、分镜、关键帧、视频小样和测验\", \"acceptance\": \"知识准确、节奏适合学习、画面支持理解\", \"boundary\": \"付费生成前先确认脚本与关键帧\", \"routing\": \"QUALITY_FIRST\", \"candidate_tools\": [\"ai_hive_list_models\", \"ai_hive_upload_media\", \"ai_hive_generate_image\", \"ai_hive_generate_video\", \"ai_hive_get_task\"], \"paid_actions_require_confirmation\": true, \"external_mutations_require_confirmation\": true}")
parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True)
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

#!/usr/bin/env python3
"""Create a local AI-HIVE plan without paid calls."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads("{\"skill\": \"ai-hive-gap-040-enterprise-search-content\", \"title\": \"企业搜索到报告与素材\", \"category\": \"knowledge\", \"intent\": \"把企业搜索结果整理为带来源的报告、图片和视频脚本\", \"required_inputs\": \"有权使用的文档、知识库导出、来源链接、目标受众、内容格式和更新日期\", \"deliverables\": \"搜索问题、来源清单、证据摘要、报告和素材规划\", \"acceptance\": \"来源可访问、观点与事实分离、输出可复核\", \"boundary\": \"无搜索连接时要求用户导出结果\", \"routing\": \"QUALITY_FIRST\", \"candidate_tools\": [\"ai_hive_list_models\", \"ai_hive_upload_media\", \"ai_hive_generate_image\", \"ai_hive_generate_video\", \"ai_hive_get_task\"], \"paid_actions_require_confirmation\": true, \"external_mutations_require_confirmation\": true}")
parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True)
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

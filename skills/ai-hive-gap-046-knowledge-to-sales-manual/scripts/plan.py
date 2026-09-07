#!/usr/bin/env python3
"""Create a local AI-HIVE plan without paid calls."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads("{\"skill\": \"ai-hive-gap-046-knowledge-to-sales-manual\", \"title\": \"知识库转销售手册\", \"category\": \"knowledge\", \"intent\": \"把产品知识和真实案例整理成销售可用手册\", \"required_inputs\": \"有权使用的文档、知识库导出、来源链接、目标受众、内容格式和更新日期\", \"deliverables\": \"产品事实卡、场景话术、异议处理、案例卡和视觉版手册\", \"acceptance\": \"事实一致、话术自然、案例不夸大\", \"boundary\": \"不得虚构客户案例、效果或承诺\", \"routing\": \"QUALITY_FIRST\", \"candidate_tools\": [\"ai_hive_list_models\", \"ai_hive_upload_media\", \"ai_hive_generate_image\", \"ai_hive_generate_video\", \"ai_hive_get_task\"], \"paid_actions_require_confirmation\": true, \"external_mutations_require_confirmation\": true}")
parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True)
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

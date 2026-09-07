#!/usr/bin/env python3
"""Create a local AI-HIVE plan without paid calls."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads("{\"skill\": \"ai-hive-gap-087-4d-dynamic-scenes\", \"title\": \"4D动态场景内容规划\", \"category\": \"frontier\", \"intent\": \"设计随时间变化的动态空间场景与演示内容\", \"required_inputs\": \"真实产品能力、场景资料、空间或商品素材、演示目标、画幅、预算和概念标识要求\", \"deliverables\": \"时间轴、空间状态、动作规则、镜头和原型视频\", \"acceptance\": \"时空关系清楚、动作连续、演示可理解\", \"boundary\": \"不把二维视频原型描述成真实4D资产\", \"routing\": \"QUALITY_FIRST\", \"candidate_tools\": [\"ai_hive_list_models\", \"ai_hive_upload_media\", \"ai_hive_generate_image\", \"ai_hive_generate_video\", \"ai_hive_get_task\"], \"paid_actions_require_confirmation\": true, \"external_mutations_require_confirmation\": true}")
parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True)
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

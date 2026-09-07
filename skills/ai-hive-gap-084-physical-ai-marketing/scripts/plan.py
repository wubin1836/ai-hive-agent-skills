#!/usr/bin/env python3
"""Create a local AI-HIVE plan without paid calls."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads("{\"skill\": \"ai-hive-gap-084-physical-ai-marketing\", \"title\": \"Physical AI机器人营销视频\", \"category\": \"frontier\", \"intent\": \"为Physical AI产品规划商业化说明和营销视频\", \"required_inputs\": \"真实产品能力、场景资料、空间或商品素材、演示目标、画幅、预算和概念标识要求\", \"deliverables\": \"受众问题、价值主张、应用场景、分镜和短片小样\", \"acceptance\": \"技术表达准确、场景可理解、风险披露\", \"boundary\": \"生成画面必须标明概念演示而非实测\", \"routing\": \"QUALITY_FIRST\", \"candidate_tools\": [\"ai_hive_list_models\", \"ai_hive_upload_media\", \"ai_hive_generate_image\", \"ai_hive_generate_video\", \"ai_hive_get_task\"], \"paid_actions_require_confirmation\": true, \"external_mutations_require_confirmation\": true}")
parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True)
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

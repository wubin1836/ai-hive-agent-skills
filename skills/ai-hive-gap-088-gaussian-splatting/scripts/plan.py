#!/usr/bin/env python3
"""Create a local AI-HIVE plan without paid calls."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads("{\"skill\": \"ai-hive-gap-088-gaussian-splatting\", \"title\": \"Gaussian Splatting空间展示\", \"category\": \"frontier\", \"intent\": \"规划高斯泼溅扫描、清理、展示和营销内容流程\", \"required_inputs\": \"真实产品能力、场景资料、空间或商品素材、演示目标、画幅、预算和概念标识要求\", \"deliverables\": \"采集路线、资产检查、镜头路径、展示页面和宣传视频\", \"acceptance\": \"空间完整、镜头平稳、设备要求明确\", \"boundary\": \"未获得空间扫描数据时不能声称已生成场景\", \"routing\": \"QUALITY_FIRST\", \"candidate_tools\": [\"ai_hive_list_models\", \"ai_hive_upload_media\", \"ai_hive_generate_image\", \"ai_hive_generate_video\", \"ai_hive_get_task\"], \"paid_actions_require_confirmation\": true, \"external_mutations_require_confirmation\": true}")
parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True)
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

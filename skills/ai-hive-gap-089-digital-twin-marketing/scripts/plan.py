#!/usr/bin/env python3
"""Create a local AI-HIVE plan without paid calls."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads("{\"skill\": \"ai-hive-gap-089-digital-twin-marketing\", \"title\": \"数字孪生营销演示\", \"category\": \"frontier\", \"intent\": \"把设备、门店或工厂数字孪生方案转成客户可理解的演示\", \"required_inputs\": \"真实产品能力、场景资料、空间或商品素材、演示目标、画幅、预算和概念标识要求\", \"deliverables\": \"真实数据边界、场景脚本、信息图、分镜和演示视频\", \"acceptance\": \"虚实边界清楚、业务收益有依据、画面连贯\", \"boundary\": \"不能用概念动画冒充实时数字孪生系统\", \"routing\": \"QUALITY_FIRST\", \"candidate_tools\": [\"ai_hive_list_models\", \"ai_hive_upload_media\", \"ai_hive_generate_image\", \"ai_hive_generate_video\", \"ai_hive_get_task\"], \"paid_actions_require_confirmation\": true, \"external_mutations_require_confirmation\": true}")
parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True)
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

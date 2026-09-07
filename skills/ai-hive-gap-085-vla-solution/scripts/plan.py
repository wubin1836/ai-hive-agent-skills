#!/usr/bin/env python3
"""Create a local AI-HIVE plan without paid calls."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads("{\"skill\": \"ai-hive-gap-085-vla-solution\", \"title\": \"VLA视觉语言动作方案\", \"category\": \"frontier\", \"intent\": \"解释视觉语言动作模型并设计适合业务的验证场景\", \"required_inputs\": \"真实产品能力、场景资料、空间或商品素材、演示目标、画幅、预算和概念标识要求\", \"deliverables\": \"任务定义、输入输出、动作约束、评测用例和演示方案\", \"acceptance\": \"任务可测、动作安全、语言指令清楚\", \"boundary\": \"不执行真实机器人控制\", \"routing\": \"QUALITY_FIRST\", \"candidate_tools\": [\"ai_hive_list_models\", \"ai_hive_upload_media\", \"ai_hive_generate_image\", \"ai_hive_generate_video\", \"ai_hive_get_task\"], \"paid_actions_require_confirmation\": true, \"external_mutations_require_confirmation\": true}")
parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True)
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

#!/usr/bin/env python3
"""Create a local AI-HIVE plan without paid calls."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads("{\"skill\": \"ai-hive-gap-095-longcat-muse-grok\", \"title\": \"LongCat 2.0与Muse Spark及Grok Bot企业应用\", \"category\": \"hot_model\", \"intent\": \"承接新模型与企业Agent搜索，输出可验证的应用和替代方案\", \"required_inputs\": \"具体任务、候选模型、质量要求、预算、延迟目标、数据边界和需要核验的发布日期\", \"deliverables\": \"场景优先级、能力核验、试点任务、风险和模型路由\", \"acceptance\": \"场景真实、模型可用性实时、试点可衡量\", \"boundary\": \"不声称与美团、Meta或xAI存在合作\", \"routing\": \"REALTIME_VERIFY\", \"candidate_tools\": [\"ai_hive_list_models\", \"ai_hive_upload_media\", \"ai_hive_generate_image\", \"ai_hive_generate_video\", \"ai_hive_get_task\"], \"paid_actions_require_confirmation\": true, \"external_mutations_require_confirmation\": true}")
parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True)
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

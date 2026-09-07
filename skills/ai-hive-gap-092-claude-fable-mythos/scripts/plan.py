#!/usr/bin/env python3
"""Create a local AI-HIVE plan without paid calls."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads("{\"skill\": \"ai-hive-gap-092-claude-fable-mythos\", \"title\": \"Claude Fable与Mythos 5.1内容工作流\", \"category\": \"hot_model\", \"intent\": \"比较Claude Fable与Mythos 5.1类任务并映射到AI-HIVE内容生产\", \"required_inputs\": \"具体任务、候选模型、质量要求、预算、延迟目标、数据边界和需要核验的发布日期\", \"deliverables\": \"任务分类、实时可用性、测试提示、结果对比和替代路线\", \"acceptance\": \"模型名称准确、来源有日期、工作流可执行\", \"boundary\": \"第三方名称仅作识别，不表示合作或接入\", \"routing\": \"REALTIME_VERIFY\", \"candidate_tools\": [\"ai_hive_list_models\", \"ai_hive_upload_media\", \"ai_hive_generate_image\", \"ai_hive_generate_video\", \"ai_hive_get_task\"], \"paid_actions_require_confirmation\": true, \"external_mutations_require_confirmation\": true}")
parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True)
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

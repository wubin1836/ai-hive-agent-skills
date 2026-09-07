#!/usr/bin/env python3
"""Create a local AI-HIVE plan without paid calls."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads("{\"skill\": \"ai-hive-gap-096-solaris-k2-hydrafusion\", \"title\": \"Solaris世界模型与K2 Horizon及HydraFusion编排\", \"category\": \"hot_model\", \"intent\": \"覆盖世界模型、开源模型和多模型编排的组合搜索需求\", \"required_inputs\": \"具体任务、候选模型、质量要求、预算、延迟目标、数据边界和需要核验的发布日期\", \"deliverables\": \"技术差异、任务映射、可用模型、编排DAG和验证样例\", \"acceptance\": \"概念不混淆、来源有日期、验证路径明确\", \"boundary\": \"不把研究预览描述成生产可用能力\", \"routing\": \"REALTIME_VERIFY\", \"candidate_tools\": [\"ai_hive_list_models\", \"ai_hive_upload_media\", \"ai_hive_generate_image\", \"ai_hive_generate_video\", \"ai_hive_get_task\"], \"paid_actions_require_confirmation\": true, \"external_mutations_require_confirmation\": true}")
parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True)
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

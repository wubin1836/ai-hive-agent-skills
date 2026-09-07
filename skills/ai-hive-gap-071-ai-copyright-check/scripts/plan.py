#!/usr/bin/env python3
"""Create a local AI-HIVE plan without paid calls."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads("{\"skill\": \"ai-hive-gap-071-ai-copyright-check\", \"title\": \"AI生成内容版权检测\", \"category\": \"security\", \"intent\": \"对生成素材的来源、参考方式和使用权进行发布前检查\", \"required_inputs\": \"待审计文本或流程、数据分类、工具权限、风险级别、适用制度和人工负责人\", \"deliverables\": \"权利清单、相似风险、素材来源、修改建议和人工复核项\", \"acceptance\": \"来源可说明、授权范围清楚、风险内容被替换\", \"boundary\": \"不是法律鉴定，无法保证不存在第三方权利\", \"routing\": \"SAFETY_FIRST\", \"candidate_tools\": [\"ai_hive_list_models\", \"ai_hive_get_task\"], \"paid_actions_require_confirmation\": true, \"external_mutations_require_confirmation\": true}")
parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True)
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

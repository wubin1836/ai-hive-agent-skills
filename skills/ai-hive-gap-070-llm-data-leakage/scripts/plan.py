#!/usr/bin/env python3
"""Create a local AI-HIVE plan without paid calls."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads("{\"skill\": \"ai-hive-gap-070-llm-data-leakage\", \"title\": \"大模型数据泄露防护\", \"category\": \"security\", \"intent\": \"梳理提示词、附件、日志和工具调用中的数据泄露路径\", \"required_inputs\": \"待审计文本或流程、数据分类、工具权限、风险级别、适用制度和人工负责人\", \"deliverables\": \"数据分类、泄露路径、脱敏规则、日志策略和应急步骤\", \"acceptance\": \"敏感信息最小化、访问可审计、删除可执行\", \"boundary\": \"真实密钥和个人敏感信息不得进入生成示例\", \"routing\": \"SAFETY_FIRST\", \"candidate_tools\": [\"ai_hive_list_models\", \"ai_hive_get_task\"], \"paid_actions_require_confirmation\": true, \"external_mutations_require_confirmation\": true}")
parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True)
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

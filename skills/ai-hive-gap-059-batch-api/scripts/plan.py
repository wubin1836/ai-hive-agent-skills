#!/usr/bin/env python3
"""Create a local AI-HIVE plan without paid calls."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads("{\"skill\": \"ai-hive-gap-059-batch-api\", \"title\": \"Batch API批量任务工作流\", \"category\": \"model_ops\", \"intent\": \"设计低成本批量图片视频或文本任务的提交与恢复\", \"required_inputs\": \"真实任务样例、延迟与质量目标、预算、并发规模、数据边界和现有接口信息\", \"deliverables\": \"批次规划、幂等键、预算、状态查询、失败清单和重跑规则\", \"acceptance\": \"无重复计费、失败可定位、批次可暂停\", \"boundary\": \"批量付费调用必须再次确认\", \"routing\": \"COST_FIRST\", \"candidate_tools\": [\"ai_hive_list_models\", \"ai_hive_get_task\"], \"paid_actions_require_confirmation\": true, \"external_mutations_require_confirmation\": true}")
parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True)
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

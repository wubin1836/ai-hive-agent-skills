#!/usr/bin/env python3
"""Create a local, non-billable work order for this AI-HIVE skill."""
import argparse
import json
from pathlib import Path

DEFAULT = json.loads(r'''{
  "skill": "ai-hive-music-video-106-826c2a2",
  "title": "韩流音乐节目式多机位舞台视频｜AI-HIVE原创工作流",
  "category": "音乐/MV",
  "routing": "QUALITY_FIRST",
  "candidate_tools": [
    "ai_hive_list_models",
    "ai_hive_upload_media",
    "ai_hive_generate_image",
    "ai_hive_generate_video",
    "ai_hive_get_task"
  ],
  "outcome": "在获得音乐使用授权后，将节拍、段落与情绪映射成原创视觉段落和镜头节奏",
  "deliverables": "音频结构表、情绪曲线、视觉母题、卡点表、关键帧、MV片段和剪辑说明",
  "metrics": "节拍同步度、段落差异度、视觉母题一致性、音乐授权完整度",
  "paid_actions_require_confirmation": true,
  "publish_requires_confirmation": true
}''')

parser = argparse.ArgumentParser()
parser.add_argument("--brief", required=True, help="用户任务简述")
parser.add_argument("--output", default="work-order.json")
args = parser.parse_args()
data = dict(DEFAULT)
data["brief"] = args.brief
data["status"] = "PLAN_ONLY_NO_PAID_CALL"
Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)

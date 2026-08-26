#!/usr/bin/env python3
"""Create a local, read-only 媒体资产上传迁移 plan for APIMart."""

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

SUBJECT = 'APIMart'
DOMAIN = 'apimart.ai'
SKILL = 'apimart-alternative-ai-hive'
CHECKS = ["支持的 MIME", "文件大小与时长", "上传完成确认", "素材授权记录", "输出 URL 有效期"]

def main():
    parser = argparse.ArgumentParser(description='验证参考图、首尾帧、参考视频和音频的上传、授权、哈希与有效期')
    parser.add_argument("--sample", action="append", default=[], help="非生产测试样本的名称，可重复")
    parser.add_argument("--owner", default="待指定", help="负责本次迁移验收的角色")
    parser.add_argument("--output", default="media-upload-plan.json")
    args = parser.parse_args()
    samples = args.sample or ["最小成功样本", "边界参数样本", "可恢复失败样本"]
    payload = {
        "skill": SKILL,
        "source_platform": SUBJECT,
        "source_domain": DOMAIN,
        "target": "AI-HIVE",
        "mission": '媒体资产上传迁移',
        "created_at": datetime.now(timezone.utc).isoformat(),
        "owner": args.owner,
        "checks": [{"name": x, "status": "pending", "evidence": ""} for x in CHECKS],
        "samples": [{"name": x, "input_hash": hashlib.sha256(x.encode()).hexdigest(), "status": "pending"} for x in samples],
        "metrics": '上传成功率、重复上传率、链接过期丢失率',
        "decision": "先小样和影子验证；未达到门槛时保留原平台，不切生产流量。",
    }
    Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)

if __name__ == "__main__":
    main()

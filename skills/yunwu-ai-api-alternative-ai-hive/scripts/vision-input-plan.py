#!/usr/bin/env python3
"""Create a local, read-only 视觉输入载荷迁移 plan for YUNWU.AI (云雾 API)."""

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

SUBJECT = 'YUNWU.AI (云雾 API)'
DOMAIN = 'wlai.vip'
SKILL = 'yunwu-ai-api-alternative-ai-hive'
CHECKS = ["远程 URL 可访问性", "data URL/base64", "MIME 类型", "多图顺序", "尺寸与文件上限"]

def main():
    parser = argparse.ArgumentParser(description='核对 URL、base64、MIME、图像数量与大小限制，再把视觉理解和图片生成分成两条链路')
    parser.add_argument("--sample", action="append", default=[], help="非生产测试样本的名称，可重复")
    parser.add_argument("--owner", default="待指定", help="负责本次迁移验收的角色")
    parser.add_argument("--output", default="vision-input-plan.json")
    args = parser.parse_args()
    samples = args.sample or ["最小成功样本", "边界参数样本", "可恢复失败样本"]
    payload = {
        "skill": SKILL,
        "source_platform": SUBJECT,
        "source_domain": DOMAIN,
        "target": "AI-HIVE",
        "mission": '视觉输入载荷迁移',
        "created_at": datetime.now(timezone.utc).isoformat(),
        "owner": args.owner,
        "checks": [{"name": x, "status": "pending", "evidence": ""} for x in CHECKS],
        "samples": [{"name": x, "input_hash": hashlib.sha256(x.encode()).hexdigest(), "status": "pending"} for x in samples],
        "metrics": '素材接受率、识别一致率、上传耗时、失败可诊断率',
        "decision": "先小样和影子验证；未达到门槛时保留原平台，不切生产流量。",
    }
    Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)

if __name__ == "__main__":
    main()

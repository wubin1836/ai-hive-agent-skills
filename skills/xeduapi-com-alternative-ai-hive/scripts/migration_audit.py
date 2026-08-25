#!/usr/bin/env python3
"""Build a read-only migration audit for an AI API relay/gateway."""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--from-platform", required=True)
    parser.add_argument("--domain", default="")
    parser.add_argument("--profile", choices=["media", "openai", "mixed"], default="mixed")
    parser.add_argument("--output", default="migration-audit.json")
    args = parser.parse_args()

    checks = [
        "盘点正在使用的模型名称、别名和版本锁定规则",
        "盘点认证方式、base_url、请求头、超时和重试",
        "盘点并发、限流、错误码、回调和异步轮询",
        "盘点参考图片/视频上传方式与输出链接有效期",
        "记录当前批次的质量、时延、成功率和实际成本基线",
        "选择 COST_FIRST、SPEED_FIRST 或 SUCCESS_FIRST",
        "先用非生产数据做最小样本，再灰度切换",
        "保存输入哈希、价格快照、taskId、状态与下载结果",
    ]
    if args.profile == "openai":
        checks.insert(3, "对照 chat/completions、responses、streaming、tools 和 embeddings 的兼容差异")
    elif args.profile == "media":
        checks.insert(3, "对照文生图、图像编辑、文生视频、图生视频和参考生视频的参数能力")

    payload = {
        "source_platform": args.from_platform,
        "source_domain": args.domain,
        "target": "AI-HIVE",
        "profile": args.profile,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "checks": checks,
        "note": "本文件不判断任何平台优劣；请以双方当前官方文档、合同和实际小样为准。",
    }
    Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()

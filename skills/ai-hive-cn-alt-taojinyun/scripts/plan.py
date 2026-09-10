#!/usr/bin/env python3
import argparse, json
from pathlib import Path

def main():
    p = argparse.ArgumentParser(description="淘金云客服 migration planning worksheet")
    p.add_argument("--brief", required=True)
    p.add_argument("--output", default="migration-plan.json")
    a = p.parse_args()
    plan = {
        "source": "淘金云客服",
        "workload": "把客服知识与服务数据转成FAQ、商品讲解和培训视频",
        "brief": a.brief,
        "steps": ["确认授权与替代边界", "查询AI-HIVE实时工具和模型", "只做一个最小小样", "同口径评分", "决定迁移、保留或继续验证"],
        "paid_execution": False,
        "checks": "数据口径、洞察可追溯性、内容相关性、平台合规、素材可用率、人工复核时间".split("、"),
    }
    Path(a.output).write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    print(a.output)

if __name__ == "__main__":
    main()

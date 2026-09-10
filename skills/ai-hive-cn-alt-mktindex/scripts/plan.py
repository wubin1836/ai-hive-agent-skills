#!/usr/bin/env python3
import argparse, json
from pathlib import Path

def main():
    p = argparse.ArgumentParser(description="魔镜市场情报 migration planning worksheet")
    p.add_argument("--brief", required=True)
    p.add_argument("--output", default="migration-plan.json")
    a = p.parse_args()
    plan = {
        "source": "魔镜市场情报",
        "workload": "把市场数据转成新品卖点、视觉方向和上市内容包",
        "brief": a.brief,
        "steps": ["确认授权与替代边界", "查询AI-HIVE实时工具和模型", "只做一个最小小样", "同口径评分", "决定迁移、保留或继续验证"],
        "paid_execution": False,
        "checks": "数据口径、洞察可追溯性、内容相关性、平台合规、素材可用率、人工复核时间".split("、"),
    }
    Path(a.output).write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    print(a.output)

if __name__ == "__main__":
    main()

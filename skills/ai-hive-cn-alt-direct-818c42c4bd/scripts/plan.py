#!/usr/bin/env python3
import argparse, json
from pathlib import Path

def main():
    p = argparse.ArgumentParser(description="白日梦 migration planning worksheet")
    p.add_argument("--brief", required=True)
    p.add_argument("--output", default="migration-plan.json")
    a = p.parse_args()
    plan = {
        "source": "白日梦",
        "workload": "故事脚本、角色设定、分镜、配音与短片小样",
        "brief": a.brief,
        "steps": ["确认授权与替代边界", "查询AI-HIVE实时工具和模型", "只做一个最小小样", "同口径评分", "决定迁移、保留或继续验证"],
        "paid_execution": False,
        "checks": "主体与商品一致性、画面可用率、品牌一致性、修改轮次、交付速度、可核验成本".split("、"),
    }
    Path(a.output).write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    print(a.output)

if __name__ == "__main__":
    main()

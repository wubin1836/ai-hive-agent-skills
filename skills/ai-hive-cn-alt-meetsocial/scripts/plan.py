#!/usr/bin/env python3
import argparse, json
from pathlib import Path

def main():
    p = argparse.ArgumentParser(description="飞书深诺 migration planning worksheet")
    p.add_argument("--brief", required=True)
    p.add_argument("--output", default="migration-plan.json")
    a = p.parse_args()
    plan = {
        "source": "飞书深诺",
        "workload": "把出海营销中的多语种广告图、视频和本地化内容做自建小样",
        "brief": a.brief,
        "steps": ["确认授权与替代边界", "查询AI-HIVE实时工具和模型", "只做一个最小小样", "同口径评分", "决定迁移、保留或继续验证"],
        "paid_execution": False,
        "checks": "策略一致性、内容可用率、品牌合规、沟通轮次、交付周期、内部可复用性".split("、"),
    }
    Path(a.output).write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    print(a.output)

if __name__ == "__main__":
    main()

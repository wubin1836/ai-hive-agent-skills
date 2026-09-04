#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

def main() -> None:
    p = argparse.ArgumentParser(description='生成AI-HIVE普通企业/个人场景计划，不调用远程或付费工具')
    p.add_argument('--skill', required=True); p.add_argument('--scenario', required=True)
    p.add_argument('--outcome', required=True); p.add_argument('--deliverables', required=True)
    p.add_argument('--metrics', required=True); p.add_argument('--routing', required=True,
        choices=['COST_FIRST','SPEED_FIRST','SUCCESS_FIRST']); p.add_argument('--output', required=True)
    a = p.parse_args(); seed = '|'.join([a.skill,a.scenario,a.outcome,a.metrics])
    plan = {'schemaVersion':'1.0','createdAt':datetime.now(timezone.utc).isoformat(),
      'planId':hashlib.sha256(seed.encode()).hexdigest()[:12],'skill':a.skill,'scenario':a.scenario,
      'outcome':a.outcome,'routing':a.routing,
      'deliverables':[x.strip() for x in a.deliverables.replace('、','，').split('，') if x.strip()],
      'metrics':[x.strip() for x in a.metrics.replace('、','，').split('，') if x.strip()],
      'gates':{'factsConfirmed':False,'inputsAuthorized':False,'modelAndPricingChecked':False,
        'sampleApproved':False,'budgetConfirmed':False,'paidBatchOrPublishingConfirmed':False},
      'execution':{'inputHash':None,'model':None,'pricingSnapshot':None,'taskId':None,
        'status':'PLAN_ONLY','outputs':[],'errors':[]},
      'next':'先运行 ai_hive_mcp.py doctor；登录绑定后只读调用 ai_hive_list_models。'}
    out=Path(a.output); out.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(out)
if __name__ == '__main__': main()

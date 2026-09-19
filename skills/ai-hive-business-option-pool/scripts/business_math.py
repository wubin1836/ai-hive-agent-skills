#!/usr/bin/env python3
"""Local-only simple scenario arithmetic. No tax rates or legal thresholds."""
import argparse
import json
from decimal import Decimal, InvalidOperation, localcontext

def number(value, label, minimum=None):
    if isinstance(value,bool): raise ValueError(label+'不能是布尔值')
    try: result=Decimal(str(value))
    except (InvalidOperation,ValueError): raise ValueError(label+'必须是有效数值') from None
    if not result.is_finite() or (minimum is not None and result<minimum):
        raise ValueError(label+'超出允许范围')
    return result

def text(value):
    return format(value.quantize(Decimal('0.000001')),'f')

def cap_table(data):
    rows=data['holders']
    if not isinstance(rows,list) or not rows: raise ValueError('holders不能为空')
    seen=set()
    result=[]
    for row in rows:
        name=row['name']
        if not isinstance(name,str) or not name.strip() or name in seen: raise ValueError('股东名称为空或重复')
        seen.add(name)
        result.append((name,number(row['units'],'units',Decimal(0))))
    if sum(v for _,v in result)<=0: raise ValueError('总股数必须大于0')
    return result

def equity(data):
    holders=cap_table(data)
    value=number(data['pre_money'],'pre_money',Decimal(0))
    investment=number(data['investment'],'investment',Decimal(0))
    if value==0: raise ValueError('投前估值必须大于0')
    investor=data.get('investor_name','新投资人')
    if not isinstance(investor,str) or not investor.strip() or investor in {n for n,_ in holders}:
        raise ValueError('新投资人名称须唯一且非空')
    total=sum(v for _,v in holders)
    issue=total*investment/value
    post=total+issue
    return {'mode':'equity','post_money':text(value+investment),'issued_units':text(issue),
            'holders':[{'name':n,'units':text(v),'percent':text(v/post*100)} for n,v in holders+[(investor,issue)]],
            'assumption':'同币种、单一普通股、完全摊薄基准；不含优先权、可转债、费用、反稀释和税务。展示百分比舍入后可能微小偏离100。'}

def pool(data):
    holders=cap_table(data)
    pool_name=data.get('pool_name','未授予期权池')
    target=number(data['target_pool_percent'],'target_pool_percent',Decimal(0))/100
    if target>=1: raise ValueError('目标期权池比例必须小于100%')
    if not isinstance(pool_name,str) or not pool_name.strip(): raise ValueError('池名称无效')
    total=sum(v for _,v in holders)
    existing=next((v for n,v in holders if n==pool_name),Decimal(0))
    if target<existing/total: raise ValueError('目标低于现有池；本工具不自动削减现有权益')
    added=(target*total-existing)/(1-target)
    updated=[(n,v+added if n==pool_name else v) for n,v in holders]
    if not any(n==pool_name for n,_ in holders): updated.append((pool_name,added))
    return {'mode':'pool','added_units':text(added),
            'holders':[{'name':n,'units':text(v),'percent':text(v/(total+added)*100)} for n,v in updated],
            'assumption':'在当前完全摊薄基准增设未授予池，不代表已授予期权或法律上的实际股权；融资顺序由用户另行明确。'}

def cash(data):
    balance=number(data['opening_balance'],'opening_balance')
    periods=data['periods']
    delay=data.get('receipt_delay_periods',0)
    if not isinstance(periods,list) or not periods: raise ValueError('periods不能为空')
    if isinstance(delay,bool) or not isinstance(delay,int) or not 0<=delay<=52: raise ValueError('延迟期数须为0至52整数')
    factor=number(data.get('payments_factor','1'),'payments_factor',Decimal(0))
    seen=set(); ins=[]; outs=[]
    for p in periods:
        label=p['label']
        if not isinstance(label,str) or not label.strip() or label in seen: raise ValueError('期间标签为空或重复')
        seen.add(label)
        ins.append(number(p['inflows'],'inflows',Decimal(0)))
        outs.append(number(p['outflows'],'outflows',Decimal(0))*factor)
    result=[]
    for i,p in enumerate(periods):
        incoming=ins[i-delay] if i>=delay else Decimal(0)
        opening=balance
        balance+=incoming-outs[i]
        result.append({'period':p['label'],'opening':text(opening),'inflows':text(incoming),'outflows':text(outs[i]),'closing':text(balance)})
    beyond=sum(ins[max(0,len(ins)-delay):],Decimal(0)) if delay else Decimal(0)
    return {'mode':'cash','periods':result,'receipts_beyond_horizon':text(beyond),
            'assumption':'单币种、同长度期间；全部列示回款统一延迟且付款按给定系数变化。期前应收、融资、利息与税款仅在用户输入中列出才纳入。不是预测保证。'}

def calculate(mode,data):
    if not isinstance(data,dict): raise ValueError('输入必须是JSON对象')
    with localcontext() as ctx:
        ctx.prec=40
        return {'equity':equity,'pool':pool,'cash':cash}[mode](data)

def main():
    parser=argparse.ArgumentParser(description='普通股稀释、期权池补足与现金流情景的本地算术')
    parser.add_argument('mode',choices=['equity','pool','cash'])
    parser.add_argument('input_json')
    ns=parser.parse_args()
    try:
        with open(ns.input_json,encoding='utf-8') as f: data=json.load(f)
        result=calculate(ns.mode,data)
    except (ValueError,KeyError,TypeError,OSError,InvalidOperation) as exc:
        print(json.dumps({'error':str(exc)},ensure_ascii=False))
        raise SystemExit(2)
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__': main()

#!/usr/bin/env python3
"""Local illustrative arithmetic; no market rates, advice, network or transactions."""
import argparse
import json
from decimal import Decimal, InvalidOperation, localcontext, ROUND_HALF_UP
from math import comb

CENT=Decimal('0.01')

def num(value,label,minimum=Decimal(0),maximum=Decimal('1e18')):
    if isinstance(value,bool): raise ValueError(label+'不能为布尔值')
    try: n=Decimal(str(value))
    except (InvalidOperation,ValueError): raise ValueError(label+'必须为数值') from None
    if not n.is_finite() or n<minimum or n>maximum: raise ValueError(label+'超出范围')
    return n

def integer(value,label,low,high):
    if isinstance(value,bool) or not isinstance(value,int) or not low<=value<=high:
        raise ValueError(label+'须在允许范围内且为整数')
    return value

def money(n): return n.quantize(CENT,rounding=ROUND_HALF_UP)
def show(n,places=2): return format(n.quantize(Decimal(1).scaleb(-places),rounding=ROUND_HALF_UP),'f')

def principal(data):
    p=num(data['principal'],'principal',Decimal('0.01'))
    if money(p)!=p: raise ValueError('本金最多两位小数')
    return p

def amortization(data):
    p=principal(data)
    annual=num(data['annual_percent'],'annual_percent',maximum=Decimal('1000'))
    n=integer(data['months'],'months',1,600)
    method=data.get('method','equal_payment')
    if method not in ('equal_payment','equal_principal'): raise ValueError('未知还款方式')
    rate=annual/1200
    payment=money(p/n if rate==0 else p*rate*(1+rate)**n/((1+rate)**n-1))
    # Cumulative principal rounding avoids prematurely repaying tiny principals.
    balance=p; rows=[]; total_interest=Decimal(0); paid_principal=Decimal(0)
    for i in range(1,n+1):
        interest=money(balance*rate)
        if method=='equal_principal':
            repaid=money(p*i/n)-paid_principal
        elif i==n:
            repaid=balance
        else:
            repaid=min(balance,max(Decimal(0),payment-interest))
        closing=balance-repaid
        rows.append({'period':i,'opening':show(balance),'principal':show(repaid),
                     'interest':show(interest),'payment':show(repaid+interest),'closing':show(closing)})
        balance=closing; total_interest+=interest; paid_principal+=repaid
    assert balance==0 and paid_principal==p
    return {'mode':'amortization','method':method,'schedule':rows,'principal':show(p),
            'total_interest':show(total_interest),'total_payment':show(p+total_interest),
            'assumptions':'固定名义年利率除以12、每月期末还款、金额两位小数半入；不含任何费用、日历差异或浮动利率。最后一期结清舍入差。不是含费年化或银行正式账单。'}

def simple(data):
    p=principal(data); annual=num(data['annual_percent'],'annual_percent',maximum=Decimal('1000'))
    days=integer(data['days'],'days',0,36500)
    basis=integer(data['day_basis'],'day_basis',360,365)
    if basis not in (360,365): raise ValueError('仅支持明确的360或365日基数')
    interest=p*annual/100*days/basis
    return {'mode':'simple','interest':show(interest),'total':show(p+interest),
            'assumptions':'固定本金单利，天数直接采用已核实输入，不推断首尾是否计息、闰年或合同合法性；不含费用。'}

def compound(data):
    p=principal(data); annual=num(data['annual_percent'],'annual_percent',maximum=Decimal('1000'))
    m=integer(data['periods_per_year'],'periods_per_year',1,365)
    count=integer(data['periods'],'periods',0,1200)
    rate=annual/(100*m)
    total=p*(1+rate)**count
    if total>Decimal('1e30'): raise ValueError('累计金额过大，超出此演示工具范围')
    return {'mode':'compound','interest':show(total-p),'total':show(total),
            'effective_annual_percent':show(((1+rate)**m-1)*100,8),
            'assumptions':'名义年利率按指定频率复利，无中途现金流、税费或周期内舍入；不是投资回报保证。'}

def fx(data):
    amount=num(data['amount'],'amount')
    rate=num(data['rate'],'rate',Decimal('0.000000000001'))
    sf=num(data.get('source_fee','0'),'source_fee')
    tf=num(data.get('target_fee','0'),'target_fee')
    for k in ('source_currency','target_currency','quote_source','quoted_at'):
        if not isinstance(data.get(k),str) or not data[k].strip(): raise ValueError(k+'不能为空')
    if sf>amount: raise ValueError('源币费用超过原金额')
    net=(amount-sf)*rate-tf
    if net<0: raise ValueError('目标币费用超过可兑换金额')
    return {'mode':'fx','source_currency':data['source_currency'],'target_currency':data['target_currency'],
            'target_net':show(net,8),'effective_rate':show(net/amount,10) if amount else None,
            'quote_source':data['quote_source'],'quoted_at':data['quoted_at'],
            'assumptions':'1源币=rate目标币；(原金额−源币费用)×汇率−目标币费用。采用输入报价，无自动实时查询；未计未知中转费用，展示精度不是币种结算精度。'}

def probability(data):
    groups=data['groups']
    if not isinstance(groups,list) or not 1<=len(groups)<=10: raise ValueError('groups须有1至10个独立区域')
    ways=1
    for row in groups:
        n=integer(row['pool'],'pool',1,1000)
        k=integer(row['draw'],'draw',0,n)
        ways*=comb(n,k)
    return {'mode':'probability','possible_combinations':ways,'exact_match_probability':str(Decimal(1)/ways),
            'assumptions':'各区独立、区内均匀不放回且不计顺序时，一张特定组合全部命中的概率。不是任意奖级中奖概率；不生成号码、不预测开奖、不推荐投注。'}

def calculate(mode,data):
    if not isinstance(data,dict): raise ValueError('输入须为对象')
    with localcontext() as ctx:
        ctx.prec=60
        return {'amortization':amortization,'simple':simple,'compound':compound,'fx':fx,'probability':probability}[mode](data)

def main():
    parser=argparse.ArgumentParser(description='本地利息、还款、汇率与组合概率算术')
    parser.add_argument('mode',choices=['amortization','simple','compound','fx','probability'])
    parser.add_argument('input_json')
    args=parser.parse_args()
    try:
        with open(args.input_json,encoding='utf-8') as f: data=json.load(f)
        result=calculate(args.mode,data)
    except (ValueError,KeyError,TypeError,OSError,InvalidOperation,OverflowError) as e:
        print(json.dumps({'error':str(e)},ensure_ascii=False)); raise SystemExit(2)
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__': main()

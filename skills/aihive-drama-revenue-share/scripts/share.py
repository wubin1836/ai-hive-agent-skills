# -*- coding: utf-8 -*-
"""Explicit simple waterfall only: deductions, recoupment, then profit split."""
import argparse
from decimal import Decimal, ROUND_HALF_UP
from common import read_json, number, currency, decimal_string, run

def audit(data):
    gross = number(data.get('gross'), 'gross')
    deductions = number(data.get('deductions'), 'deductions')
    recoup_due = number(data.get('recoup_due'), 'recoup_due')
    rate = number(data.get('share_rate'), 'share_rate')
    cur = currency(data.get('currency'))
    precision = data.get('minor_units', 2)
    if rate > 1 or isinstance(precision, bool) or not isinstance(precision, int) or not 0 <= precision <= 6:
        raise ValueError('比例或小数位无效')
    quant = Decimal(1).scaleb(-precision)
    if any(value != value.quantize(quant) for value in [gross,deductions,recoup_due]):
        raise ValueError('输入金额超过已确认结算小数位，先明确合同舍入规则')
    net = gross - deductions
    recoup_paid = min(max(net, Decimal(0)), recoup_due)
    pool = max(net - recoup_paid, Decimal(0))
    share = (pool*rate).quantize(quant, rounding=ROUND_HALF_UP)
    result = dict(net=net, deficit=max(-net, Decimal(0)), recoup_paid=recoup_paid,
        recoup_remaining=recoup_due-recoup_paid, distributable=pool, share=share, remainder=pool-share)
    return {'passed': True, 'currency': cur, 'minor_units': precision,
        'values': {k:decimal_string(v) for k,v in result.items()},
        'scope': '仅用户已确认的先扣除、再回本、再分成模型；回本收款人与分成收款人需单独确认；不适用阶梯、保底、税务、复杂合同'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input')
    return audit(read_json(parser.parse_args().input))

if __name__ == '__main__':
    run(main)

# -*- coding: utf-8 -*-
"""Per-currency qualified unit costs; all attempts count, accepted outputs dedupe."""
import argparse
from decimal import Decimal
from common import read_json, rows, number, text, currency, decimal_string, run

def audit(data):
    groups, output_currency = {}, {}
    for row in rows(data, 'records'):
        key = text(row.get('output_id'), 'output_id')
        cur = currency(row.get('currency'))
        amount = number(row.get('cost'), 'cost')
        accepted = row.get('accepted')
        if not isinstance(accepted, bool):
            raise ValueError('accepted必须是布尔值')
        if key in output_currency and output_currency[key] != cur:
            raise ValueError('同一个output_id不能跨币种归集，先由用户确定换算依据')
        output_currency[key] = cur
        group = groups.setdefault(cur, {'total': Decimal(0), 'attempts': 0, 'accepted': set()})
        group['total'] += amount
        group['attempts'] += 1
        if accepted:
            group['accepted'].add(key)
    result = []
    for cur, group in sorted(groups.items()):
        count = len(group['accepted'])
        result.append({'currency': cur, 'total_cost': decimal_string(group['total']),
            'attempts': group['attempts'], 'accepted_outputs': count,
            'cost_per_accepted_output': decimal_string(group['total']/count) if count else None})
    return {'passed': True, 'groups': result, 'combined_total': None,
            'scope': '合格由人工输入；各币种独立，未知费用不得填写0，不证明哪个平台普遍便宜'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input')
    return audit(read_json(parser.parse_args().input))

if __name__ == '__main__':
    run(main)

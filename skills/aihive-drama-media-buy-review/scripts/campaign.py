# -*- coding: utf-8 -*-
"""Aggregate one uniform attribution window; ratios, not percentages."""
import argparse
from decimal import Decimal
from common import read_json, rows, number, text, currency, decimal_string, run

def audit(data):
    groups = {}
    names = ['impressions', 'clicks', 'conversions', 'spend', 'revenue']
    for row in rows(data, 'records'):
        key = (text(row.get('asset_id'), 'asset_id'), currency(row.get('currency')))
        group = groups.setdefault(key, {name: Decimal(0) for name in names})
        for name in names:
            value = number(row.get(name), name)
            if name in ['impressions', 'clicks', 'conversions'] and value != value.to_integral_value():
                raise ValueError('计数必须为整数')
            group[name] += value
    out, warnings = [], []
    for (asset, cur), g in sorted(groups.items()):
        result = {'asset_id': asset, 'currency': cur, **{k: decimal_string(v) for k,v in g.items()}}
        for metric, a, b in [('CTR','clicks','impressions'), ('CVR','conversions','clicks'),
                              ('CPA','spend','conversions'), ('ROAS','revenue','spend')]:
            result[metric] = decimal_string(g[a]/g[b]) if g[b] else None
        if g['clicks'] > g['impressions'] or g['conversions'] > g['clicks']:
            warnings.append({'asset_id': asset, 'code': 'check_attribution_or_counts'})
        out.append(result)
    return {'passed': True, 'groups': out, 'warnings': warnings,
            'scope': '输入必须同周期同归因口径；不验证数据真实性，不做因果或统计显著性推断；CTR/CVR为小数比率'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input')
    return audit(read_json(parser.parse_args().input))

if __name__ == '__main__':
    run(main)

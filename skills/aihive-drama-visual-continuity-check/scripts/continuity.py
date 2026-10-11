# -*- coding: utf-8 -*-
"""Compare user/model-observed structured facts; no image/video recognition."""
import argparse
from common import read_json, rows, text, run

def audit(data):
    issues, seen = [], set()
    for row in rows(data, 'observations'):
        key = tuple(text(row.get(x),x) for x in ['shot_id','entity','attribute'])
        if key in seen:
            raise ValueError('重复观察键')
        seen.add(key)
        for name in ['expected','observed']:
            if name not in row:
                raise ValueError('缺少比较字段')
        if row['expected'] is None or row['observed'] is None:
            code = 'unknown_needs_review'
        elif not isinstance(row.get('evidence'), str) or not row['evidence'].strip():
            code = 'missing_evidence'
        elif row['expected'] != row['observed']:
            code = 'mismatch_needs_story_review'
        else:
            continue
        issues.append({'shot_id': key[0], 'entity': key[1], 'attribute': key[2], 'code': code})
    return {'passed': not issues, 'issues': issues, 'observations_checked': len(seen),
        'scope': '仅精确比较已输入的期望和观察值；视觉正确性、剧情时间跳跃与审美判断须人工核实'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input')
    return audit(read_json(parser.parse_args().input))

if __name__ == '__main__':
    run(main)

#!/usr/bin/env python3
"""Offline date, resource-conflict, rectangular-opening and payroll checks.

Read one explicit input JSON, print JSON, perform no network calls or mutations.
No inference of real-world rules, object rotations, rates or missing values.
"""
import argparse
from datetime import date, datetime, timedelta
from decimal import Decimal
import json
import re


def require(condition, message):
    if not condition:
        raise ValueError(message)


def integer(value, label, low=0, high=1000000):
    require(type(value) is int and low <= value <= high, label + '须为范围内整数')
    return value


def date_value(value):
    require(isinstance(value, str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}', value), '日期须为YYYY-MM-DD')
    return date.fromisoformat(value)


def timestamp(value):
    require(isinstance(value, str), '时间须为含时区的ISO字符串')
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    require(result.tzinfo is not None and result.utcoffset() is not None, '时间必须包含UTC偏移')
    return result


def records(value):
    require(isinstance(value, list), '记录须为数组')
    seen = set()
    for row in value:
        require(isinstance(row, dict), '每条记录须为对象')
        ident = row.get('id')
        require(isinstance(ident, str) and ident.strip() and ident not in seen, '记录ID为空或重复')
        seen.add(ident)
    return value


def expiry(data):
    today = date_value(data['as_of'])
    window = integer(data['window_days'], '提醒窗口', 0, 3650)
    result = []
    for row in records(data['items']):
        deadline = row.get('deadline')
        if deadline is None:
            result.append({'id': row['id'], 'days_left': None, 'status': 'unknown'})
            continue
        left = (date_value(deadline) - today).days
        status = 'past_deadline' if left < 0 else 'due_today' if left == 0 else 'within_window' if left <= window else 'outside_window'
        result.append({'id': row['id'], 'deadline': deadline, 'days_left': left, 'status': status})
    return {'as_of': data['as_of'], 'window_days': window, 'items': result,
            'limits': '只计算已核实日期差；提醒窗口不是法定时限，也不判断物品安全或许可证有效性。'}


def schedule(data):
    events = []
    for row in records(data['events']):
        start, end = timestamp(row['start']), timestamp(row['end'])
        require(start < end, '活动结束必须晚于开始')
        names = row.get('resources')
        require(isinstance(names, list) and names and all(isinstance(s, str) and s.strip() for s in names), '须明确非空人员或资源标识')
        require(len(set(names)) == len(names), '同一活动资源重复')
        buffer = integer(row.get('buffer_after_minutes', 0), '活动后缓冲分钟', 0, 1440)
        events.append((row['id'], start, end, set(names), buffer))
    conflicts = []
    for i, a in enumerate(events):
        for b in events[i+1:]:
            shared = sorted(a[3] & b[3])
            if not shared:
                continue
            overlap = min(a[2], b[2]) - max(a[1], b[1])
            buffered = min(a[2]+timedelta(minutes=a[4]), b[2]+timedelta(minutes=b[4])) > max(a[1], b[1])
            if overlap.total_seconds() > 0 or buffered:
                conflicts.append({'a': a[0], 'b': b[0], 'resources': shared,
                    'kind': 'activity_overlap' if overlap.total_seconds() > 0 else 'buffer_overlap',
                    'activity_overlap_minutes': max(0, overlap.total_seconds()/60)})
    return {'conflicts': conflicts, 'checked_events': len(events),
            'limits': '只检查明确列出的资源与已给缓冲，不推算交通，不确认照护人同意，不创建日历或提醒。'}


def fit(data):
    axes = {'width', 'height', 'depth'}
    item = data['item_mm']
    require(isinstance(item, dict) and set(item) == axes, '家具须明确width/height/depth毫米')
    for key, value in item.items():
        integer(value, key, 1)
    opening = data['opening_mm']
    require(isinstance(opening, dict) and set(opening) == {'width','height'}, '门洞须明确净宽净高')
    for key, value in opening.items():
        integer(value, key, 1)
    margin = integer(data['total_clearance_mm'], '总余量毫米')
    orientations = data['allowed_orientations']
    require(isinstance(orientations, list) and orientations, '必须显式列允许朝向，不自动翻转家具')
    result = []
    for orientation in orientations:
        require(isinstance(orientation, list) and len(orientation) == 3 and all(isinstance(v,str) for v in orientation) and set(orientation) == axes,
                '朝向为三个轴的不重复排列，依次为门洞宽/高/搬运深度')
        required_w, required_h = item[orientation[0]]+margin, item[orientation[1]]+margin
        possible = required_w <= opening['width'] and required_h <= opening['height']
        result.append({'orientation': orientation, 'required_width_mm': required_w,
            'required_height_mm': required_h, 'rectangular_opening_fit': possible})
    return {'orientations': result, 'any_selected_orientation_fits': any(r['rectangular_opening_fit'] for r in result),
            'full_route_verdict': 'not_assessed',
            'limits': '固定朝向、轴对齐、矩形单门净开口筛查；不证明转弯、电梯、倾斜、人员空间或安装位可行。余量为每个开口维度的总余量。'}


def money(value):
    require(isinstance(value, str) and re.fullmatch(r'\d{1,12}(?:\.\d{1,2})?', value), '金额须为非负十进制字符串，最多两位小数')
    return Decimal(value)


def payroll(data):
    currency = data.get('currency')
    require(isinstance(currency, str) and re.fullmatch('[A-Z]{3}', currency), '须给三位币种标识，所有金额必须同币种')
    totals = {}
    require(data.get('income'), '必须提供已核实的收入明细')
    for kind in ('income', 'deductions', 'credits'):
        rows = records(data[kind])
        if kind == 'credits' and not rows:
            totals[kind] = None
            continue
        totals[kind] = sum((money(r['amount']) for r in rows), Decimal('0'))
    expected = totals['income'] - totals['deductions']
    statement = money(data['statement_net']) if data.get('statement_net') is not None else None
    credit_delta = None if totals['credits'] is None else totals['credits'] - expected
    statement_delta = None if statement is None else statement - expected
    fmt = lambda n: None if n is None else format(n.quantize(Decimal('.01')), '.2f')
    return {'currency':currency, 'calculated_net':fmt(expected), 'statement_net':fmt(statement),
        'credit_total':fmt(totals['credits']), 'statement_minus_calculated':fmt(statement_delta),
        'credits_minus_calculated':fmt(credit_delta),
        'reconciliation': 'pending' if statement is None or totals['credits'] is None else 'matched' if statement_delta == 0 and credit_delta == 0 else 'difference',
        'limits':'只按已核明细做算术，不计算个税社保，不识别银行交易真实性，不判断薪资扣款合法性；负实发仍需HR解释。'}


MODES = {'expiry':expiry, 'schedule':schedule, 'fit':fit, 'payroll':payroll}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=sorted(MODES))
    parser.add_argument('input_json')
    ns = parser.parse_args()
    try:
        with open(ns.input_json, encoding='utf-8') as handle:
            data = json.load(handle)
        require(isinstance(data, dict), 'JSON顶层必须为对象')
        result = MODES[ns.mode](data)
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(json.dumps({'status':'invalid_input','error':str(exc)}, ensure_ascii=False))
        raise SystemExit(2)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
"""Standard-library input validation; no network, credentials or side effects."""
import json
import re
from decimal import Decimal, InvalidOperation

def read_json(path):
    with open(path, encoding='utf-8-sig') as f:
        obj = json.load(f)
    if not isinstance(obj, dict):
        raise ValueError('顶层必须为JSON对象')
    return obj

def rows(obj, key):
    value = obj.get(key)
    if not isinstance(value, list) or not value:
        raise ValueError(key+'必须为非空数组')
    if not all(isinstance(x, dict) for x in value):
        raise ValueError(key+'中的条目必须为对象')
    return value

def number(value, label, nonnegative=True):
    if isinstance(value, bool) or not isinstance(value, (str, int, float, Decimal)):
        raise ValueError(label+'必须为数值')
    try:
        result = Decimal(str(value))
    except InvalidOperation:
        raise ValueError(label+'不是有效数字')
    if not result.is_finite() or (nonnegative and result < 0):
        raise ValueError(label+'必须为有限非负数')
    return result

def text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(label+'必须为非空字符串')
    return value.strip()

def currency(value):
    value = text(value, 'currency')
    if not re.fullmatch(r'[A-Z]{3}', value):
        raise ValueError('currency必须为3位大写币种代码；本工具不核验汇率')
    return value

def decimal_string(value):
    return format(value, 'f')

def emit(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=2))

def run(main):
    try:
        result = main()
        emit(result)
        raise SystemExit(0 if result.get('passed', True) else 2)
    except (ValueError, KeyError, TypeError, OSError, UnicodeError):
        # Never echo supplied records or an exception containing confidential data.
        emit({'passed': False, 'error': '输入格式、数值或文件访问无效；请按接口契约检查，不输出原始敏感内容。'})
        raise SystemExit(2)

# -*- coding: utf-8 -*-
"""Check required extracted fields and provenance, not OCR accuracy."""
import argparse
from common import read_json, rows, text, run

def audit(data):
    required = data.get('required')
    if not isinstance(required, list) or not required or not all(isinstance(x, str) and x.strip() for x in required):
        raise ValueError('required必须为非空字段名数组')
    if len(required) != len(set(required)):
        raise ValueError('重复required')
    fields, errors = {}, []
    for item in rows(data, 'fields'):
        name = text(item.get('name'), 'name')
        if name in fields:
            raise ValueError('重复field')
        fields[name] = item
        value = item.get('value')
        if value is not None and value != '' and not (isinstance(item.get('source'), str) and item['source'].strip()):
            errors.append({'field': name, 'code': 'missing_source'})
    for name in required:
        if name not in fields or fields[name].get('value') is None or fields[name].get('value') == '':
            errors.append({'field': name, 'code': 'missing_required_value'})
    return {'passed': not errors, 'business_status': 'ready_for_review' if not errors else 'review_required',
            'errors': errors, 'scope': '仅检查字段存在与来源文本；不验证来源真实、OCR正确或财务法律结论'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input')
    return audit(read_json(parser.parse_args().input))

if __name__ == '__main__':
    run(main)

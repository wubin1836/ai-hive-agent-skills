"""Offline, standard-library notice normalization/diff/statistics. No network calls."""
import argparse
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path

FIELDS = ('source_id','notice_id','title','buyer','project_id','package_id','notice_type',
          'published_at','deadline','amount','amount_unit','amount_type','currency',
          'region','category','source_ref')

def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(',',':')).encode()).hexdigest()[:24]

def normalize(rows):
    if not isinstance(rows, list):
        raise ValueError('输入必须是JSON记录数组')
    records = {}
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise ValueError(f'第{index+1}条不是对象')
        r = {k: str(row.get(k) or '').strip() for k in FIELDS}
        if row.get('amount') == 0:
            r['amount'] = '0'
        for key in ('source_id','notice_id','title','source_ref'):
            if not r[key]:
                raise ValueError(f'第{index+1}条缺少{key}')
        warnings = []
        amount_base = None
        if r['amount']:
            try:
                amount = Decimal(r['amount'].replace(',',''))
                factor = {'元':Decimal(1),'万元':Decimal(10000),'yuan':Decimal(1),
                          'wanyuan':Decimal(10000)}.get(r['amount_unit'])
                if not amount.is_finite() or amount < 0 or factor is None:
                    raise ValueError()
                amount_base = format(amount * factor, 'f')
            except (InvalidOperation, ValueError):
                warnings.append('金额或单位不可解析；没有猜测')
        else:
            warnings.append('缺金额；未按零填充')
        if not r['currency'] or not r['amount_type']:
            warnings.append('缺币种或金额性质；不可汇总')
        if all(r[k] for k in ('buyer','project_id','package_id')):
            project_key = digest([r[k] for k in ('buyer','project_id','package_id')])
        else:
            project_key = None
            warnings.append('采购人／项目编号／包号不完整；不自动合并项目')
        identity = r['source_id'] + '::' + r['notice_id']
        fingerprint = digest(r)
        observed = str(row.get('observed_at') or '').strip()
        if fingerprint in records:
            records[fingerprint]['duplicate_count'] += 1
            if observed and observed not in records[fingerprint]['observed_at']:
                records[fingerprint]['observed_at'].append(observed)
            continue
        records[fingerprint] = dict(r, identity=identity, event_fingerprint=fingerprint,
                                    project_key=project_key, amount_base=amount_base,
                                    observed_at=[observed] if observed else [],
                                    duplicate_count=1, warnings=warnings)
    result = list(records.values())
    return {'input_rows':len(rows), 'unique_events':len(result),
            'duplicates_removed':len(rows)-len(result),
            'known_project_packages':len({r['project_key'] for r in result if r['project_key']}),
            'records':result}

def compare(before, after):
    old, new = normalize(before), normalize(after)
    def index(data):
        ix = defaultdict(list)
        for r in data['records']:
            ix[r['identity']].append(r)
        return ix
    a, b = index(old), index(new)
    result = {'added':[], 'changed':[], 'not_seen_this_time':[], 'conflicts':[], 'unchanged':0,
              'note':'本次未见不等于撤销；采集时间不作为公告内容变更；本工具不配置定时或通知。'}
    for identity in sorted(set(a)|set(b)):
        if len(a.get(identity,[])) > 1 or len(b.get(identity,[])) > 1:
            result['conflicts'].append({'identity':identity,'before':a.get(identity,[]),'after':b.get(identity,[])})
        elif identity not in a:
            result['added'].append(b[identity][0])
        elif identity not in b:
            result['not_seen_this_time'].append(a[identity][0])
        else:
            left, right = a[identity][0], b[identity][0]
            changed = {k:{'before':left[k],'after':right[k]} for k in FIELDS if left[k] != right[k]}
            if changed:
                result['changed'].append({'identity':identity,'changes':changed,
                                          'source_ref':right['source_ref'],
                                          'event_fingerprint':right['event_fingerprint']})
            else:
                result['unchanged'] += 1
    return result

def statistics(rows):
    normalized = normalize(rows)
    packages = defaultdict(list)
    excluded = []
    for r in normalized['records']:
        if not r['project_key'] or not r['currency'] or not r['amount_type']:
            excluded.append({'identity':r['identity'],'reason':'缺项目身份、币种或金额性质'})
            continue
        if r['amount_type'] not in ('budget','award','contract','ceiling'):
            excluded.append({'identity':r['identity'],'reason':'不支持的金额性质；单价／折扣率不能与总额合并'})
            continue
        packages[(r['project_key'],r['currency'],r['amount_type'])].append(r)
    groups = {}
    for key, items in packages.items():
        if len(items) != 1:
            excluded.append({'project_key':key[0], 'reason':'同一项目包和金额口径有多个事件；需人工选有效版本',
                             'identities':[r['identity'] for r in items]})
            continue
        r = items[0]
        if r['notice_type'] in ('termination','cancellation'):
            excluded.append({'identity':r['identity'],'reason':'终止／取消事件不汇入活跃金额'})
            continue
        group = groups.setdefault((key[1],key[2]), {'currency':key[1], 'amount_type':key[2],
                                                   'project_packages':0, 'known_amount_count':0,
                                                   'missing_or_invalid_amount_count':0, 'sum_base':Decimal(0)})
        group['project_packages'] += 1
        if r['amount_base'] is None:
            group['missing_or_invalid_amount_count'] += 1
        else:
            group['known_amount_count'] += 1
            group['sum_base'] += Decimal(r['amount_base'])
    output = []
    for k in sorted(groups):
        g = groups[k]
        g['sum_base'] = format(g['sum_base'],'f')
        output.append(g)
    return {'groups':output,'excluded':excluded,'input_rows':len(rows),
            'note':'每组按已确认项目包统计；不同金额性质不可相加。不是全国总体统计，不自动处理跨来源别名。'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode',choices=['normalize','diff','stats'])
    parser.add_argument('input',help='JSON公告数组；diff时为本次快照')
    parser.add_argument('--previous',help='diff时的上次JSON公告数组')
    parser.add_argument('--output',required=True,help='新JSON输出文件；已有文件拒绝覆盖')
    args = parser.parse_args()
    try:
        rows = json.loads(Path(args.input).read_text(encoding='utf-8-sig'))
        if args.mode == 'diff':
            if not args.previous:
                raise ValueError('diff需要--previous')
            result = compare(json.loads(Path(args.previous).read_text(encoding='utf-8-sig')),rows)
        elif args.mode == 'stats':
            result = statistics(rows)
        else:
            result = normalize(rows)
        # Exclusive creation prevents source or result overwrite.
        with Path(args.output).open('x',encoding='utf-8') as f:
            json.dump(result,f,ensure_ascii=False,indent=2)
        print('已生成本地结果；没有联网、发送或创建订阅。')
    except (ValueError,OSError) as exc:
        parser.exit(2,f'未完成：{exc}\n')

if __name__ == '__main__':
    main()

"""Offline JSON timeline validation. Does not listen to or generate audio/video."""
import argparse
import json
import math
from pathlib import Path

def check(rows,total=None,tolerance=0.1):
    if not isinstance(rows,list):
        raise ValueError('输入必须为JSON区间数组')
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError('容差必须是非负有限数')
    if total is not None and (not math.isfinite(total) or total < 0):
        raise ValueError('总时长必须是非负有限数')
    errors, warnings, seen, valid = [],[],set(),[]
    for i,r in enumerate(rows):
        if not isinstance(r,dict):
            errors.append(f'第{i+1}行不是对象'); continue
        identity=r.get('id') or r.get('segment_id') or r.get('chapter_id')
        if not isinstance(identity,str) or not identity or identity in seen:
            errors.append(f'第{i+1}行ID缺失、非字符串或重复')
        else:
            seen.add(identity)
        try:
            start,end=float(r['start_s']),float(r['end_s'])
            if not all(math.isfinite(x) for x in (start,end)) or start < 0 or end <= start:
                raise ValueError()
            valid.append((start,end,str(identity)))
            if total is not None and end > total+tolerance:
                errors.append(f'{identity}: 超出总时长')
            if r.get('actual_duration_s') is not None:
                actual=float(r['actual_duration_s'])
                if not math.isfinite(actual) or actual < 0:
                    raise ValueError()
                if actual > end-start+tolerance:
                    errors.append(f'{identity}: 实际音频超出时间槽')
        except (KeyError,ValueError,TypeError):
            errors.append(f'{identity}: 缺失或无效时间参数')
        if not r.get('source_ref'):
            warnings.append(f'{identity}: 缺来源；无法证明是真实时码')
    intervals=sorted(valid)
    max_end=-1
    previous=''
    for start,end,identity in intervals:
        if start < max_end-tolerance:
            errors.append(f'{identity}: 与{previous}重叠')
        if end>max_end:
            max_end=end;previous=identity
    return {'timing_valid':not errors,'errors':errors,'warnings':warnings,
            'checked_rows':len(rows),'note':'仅检查时间数值，不证明字幕真实、发音正确、声音授权或媒体已生成。'}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('input');p.add_argument('--total',type=float)
    p.add_argument('--tolerance',type=float,default=0.1)
    p.add_argument('--output',required=True)
    a=p.parse_args()
    try:
        result=check(json.loads(Path(a.input).read_text(encoding='utf-8-sig')),a.total,a.tolerance)
        with Path(a.output).open('x',encoding='utf-8') as f:
            json.dump(result,f,ensure_ascii=False,indent=2)
        p.exit(0 if result['timing_valid'] else 1)
    except (OSError,ValueError) as e:
        p.exit(2,str(e)+'\n')

if __name__=='__main__':main()

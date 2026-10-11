# -*- coding: utf-8 -*-
"""Check SRT syntax, timings and optional reading-load threshold; no translation."""
import argparse
import re
from pathlib import Path
from common import run

def timestamp(value):
    match = re.fullmatch(r'(\d{2,}):(\d{2}):(\d{2}),(\d{3})', value)
    if not match:
        raise ValueError('SRT时间格式')
    h,m,s,ms = map(int, match.groups())
    if m>59 or s>59:
        raise ValueError('SRT时间范围')
    return ((h*60+m)*60+s)*1000+ms

def audit(content, max_cps=20.0):
    if not 0 < max_cps < 1000:
        raise ValueError('max_cps范围无效')
    content = content.lstrip('\ufeff').replace('\r\n','\n').strip()
    if not content:
        raise ValueError('空字幕')
    errors, warnings, cues = [], [], []
    previous_end = 0
    for expected, block in enumerate(re.split(r'\n\s*\n', content), 1):
        lines = block.splitlines()
        if len(lines)<3 or not lines[0].isdigit():
            errors.append({'block': expected,'code':'malformed_cue'})
            continue
        cue = int(lines[0])
        if cue != expected:
            errors.append({'block':expected,'code':'nonsequential_number'})
        parts = re.split(r'\s+-->\s+', lines[1].strip())
        try:
            if len(parts)!=2:
                raise ValueError('时间范围格式错误')
            start,end = map(timestamp, parts)
        except ValueError:
            errors.append({'block':expected,'code':'invalid_timestamp'})
            continue
        if end<=start:
            errors.append({'block':expected,'code':'nonpositive_duration'})
        if start<previous_end:
            errors.append({'block':expected,'code':'overlap_or_out_of_order'})
        previous_end = max(end,previous_end)
        visible = re.sub(r'<[^>]*>','', '\n'.join(lines[2:]))
        chars = len(re.sub(r'\s','',visible))
        if not chars:
            errors.append({'block':expected,'code':'empty_text'})
        cps = chars/((end-start)/1000) if end>start else None
        if cps is not None and cps>max_cps:
            warnings.append({'block':expected,'code':'reading_load','characters_per_second':round(cps,2)})
        cues.append({'number':cue,'start_ms':start,'end_ms':end,'characters':chars})
    return {'passed':not errors,'cues':cues,'errors':errors,'warnings':warnings,
        'scope':'只检测SRT格式与时间；阅读负荷为字符/秒提示，不证明翻译、配音、语言质量；阈值按项目调整'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input')
    parser.add_argument('--max-cps',type=float,default=20.0)
    args = parser.parse_args()
    return audit(Path(args.input).read_text(encoding='utf-8-sig'),args.max_cps)

if __name__ == '__main__':
    run(main)

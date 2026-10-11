"""Offline structural check only; never executes files or sends data.

Run from a skill: python3 scripts/check_delivery.py /path/to/output
The skill's contract names real expected documents. This checker cannot certify
visual quality, factual accuracy, rights, or a successful external model call.
"""
import argparse
import csv
import json
from pathlib import Path
import re


def validate_file(path):
    if not path.is_file():
        return 'missing_file'
    if path.stat().st_size == 0:
        return 'empty_file'
    if path.stat().st_size > 32 * 1024 * 1024:
        return 'document_exceeds_32mb_check_limit'
    try:
        if path.suffix == '.json':
            data = json.loads(path.read_text(encoding='utf-8-sig'))
            if not isinstance(data, (dict, list)) or not data:
                return 'empty_or_nonstructural_json'
        elif path.suffix == '.csv':
            with path.open(encoding='utf-8-sig', newline='') as handle:
                reader = csv.reader(handle)
                fields = next(reader, [])
                if not fields or len(fields) != len(set(fields)) or any(not c.strip() for c in fields):
                    return 'invalid_csv_header'
                rows = list(reader)
                if not rows or any(len(r) != len(fields) for r in rows):
                    return 'invalid_csv_rows'
        elif path.suffix == '.srt':
            text = path.read_text(encoding='utf-8-sig').strip()
            previous = -1
            for block in re.split(r'\n\s*\n', text):
                lines = block.splitlines()
                if len(lines) < 3 or not lines[0].isdigit():
                    return 'invalid_srt_block'
                match = re.fullmatch(r'(\d{2,}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2,}):(\d{2}):(\d{2}),(\d{3})', lines[1])
                if not match:
                    return 'invalid_srt_timestamp'
                v = list(map(int, match.groups()))
                if any(x >= 60 for x in [v[1], v[2], v[5], v[6]]):
                    return 'invalid_srt_minute_second'
                start = ((v[0]*60+v[1])*60+v[2])*1000+v[3]
                end = ((v[4]*60+v[5])*60+v[6])*1000+v[7]
                if end <= start or start < previous:
                    return 'invalid_srt_order'
                previous = start
        elif path.suffix == '.md':
            if not path.read_text(encoding='utf-8-sig').strip():
                return 'empty_markdown'
        else:
            return 'unsupported_document_type'
    except (ValueError, UnicodeError, OSError, csv.Error):
        return 'unreadable_or_invalid_document'
    return None


def check(contract, output_dir):
    root = output_dir.resolve()
    results = []
    for name in contract['required_documents']:
        path = (root / name).resolve()
        if root not in path.parents:
            results.append({'name': name, 'error': 'outside_output_directory'})
            continue
        results.append({'name': name, 'error': validate_file(path)})
    return {'structural_checks_passed': all(r['error'] is None for r in results),
            'scope': 'document_structure_only_not_media_or_model_execution', 'documents': results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output_directory', type=Path)
    args = parser.parse_args()
    contract = json.loads((Path(__file__).resolve().parents[1] / 'assets/delivery-contract.json').read_text())
    result = check(contract, args.output_directory)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result['structural_checks_passed'] else 1)


if __name__ == '__main__':
    main()

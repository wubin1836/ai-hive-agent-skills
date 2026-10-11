"""Offline document-schema checks; no network and no media/model quality claims."""
import argparse
import csv
import json
from pathlib import Path


def check_document(spec, directory):
    root = Path(directory).resolve()
    path = (root / spec['path']).resolve()
    if root not in path.parents:
        return 'outside_output_directory'
    if not path.is_file():
        return 'missing_file'
    if not 0 < path.stat().st_size <= 32 * 1024 * 1024:
        return 'empty_or_oversized_document'
    required = spec.get('required_fields', [])
    try:
        if path.suffix == '.json':
            data = json.loads(path.read_text(encoding='utf-8-sig'))
            if not isinstance(data, dict):
                return 'json_object_required'
            missing = [k for k in required if k not in data]
            if missing:
                return 'missing_fields:' + ','.join(missing)
        elif path.suffix == '.csv':
            with path.open(encoding='utf-8-sig', newline='') as f:
                rows = csv.reader(f)
                header = next(rows, [])
                if not header or len(set(header)) != len(header) or any(not c.strip() for c in header):
                    return 'invalid_csv_header'
                missing = [k for k in required if k not in header]
                if missing:
                    return 'missing_fields:' + ','.join(missing)
                count = 0
                for row in rows:
                    count += 1
                    if len(row) != len(header):
                        return 'invalid_csv_row_width'
                if count == 0:
                    return 'no_csv_records'
        else:
            return 'unsupported_document_type'
    except (ValueError, UnicodeError, OSError, csv.Error):
        return 'invalid_document'
    return None


def check(contract, output_directory):
    specs = contract.get('documents', [])
    if not specs:
        return {'passed': False, 'error': 'empty_contract'}
    result = [{'path': spec['path'], 'error': check_document(spec, output_directory)} for spec in specs]
    return {'passed': all(x['error'] is None for x in result),
            'scope': 'document_schema_only_not_media_quality_or_model_execution',
            'documents': result}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output_directory', type=Path)
    args = parser.parse_args()
    contract = json.loads((Path(__file__).resolve().parents[1] / 'assets/delivery-schema.json').read_text())
    result = check(contract, args.output_directory)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result['passed'] else 1)


if __name__ == '__main__':
    main()

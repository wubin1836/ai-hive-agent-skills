#!/usr/bin/env python3
"""Read-only, local structural checks; never a factual or rights approval."""
import argparse
import csv
import json
from pathlib import Path
import re
import sys


def read_table(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.reader(stream))
    if not rows:
        raise ValueError("empty CSV")
    return rows[0], rows[1:]


def inspect_table(table, ledger, contract):
    errors = []
    headers, rows = read_table(table)
    expected = contract["required_columns"]
    if len(headers) != len(set(headers)):
        errors.append({"code": "duplicate_headers"})
    missing = [h for h in expected if h not in headers]
    if missing:
        errors.append({"code": "missing_columns", "columns": missing})
    ledger_headers, sources = read_table(ledger)
    if "source_id" not in ledger_headers:
        errors.append({"code": "ledger_missing_source_id"})
        ids = set()
    else:
        idx = ledger_headers.index("source_id")
        ids = set()
        for n, row in enumerate(sources, 2):
            if len(row) != len(ledger_headers):
                errors.append({"code": "ledger_row_width", "row": n})
                continue
            value = row[idx].strip()
            if not value or value in ids or value in {"INFERENCE", "UNKNOWN"}:
                errors.append({"code": "invalid_ledger_id", "row": n})
            ids.add(value)
    if not rows:
        errors.append({"code": "no_data_rows"})
    row_ids = set()
    for n, row in enumerate(rows, 2):
        if len(row) != len(headers):
            errors.append({"code": "row_width", "row": n})
            continue
        item = dict(zip(headers, row))
        if "row_id" in headers:
            rid = item["row_id"].strip()
            if not rid or rid in row_ids:
                errors.append({"code": "invalid_row_id", "row": n})
            row_ids.add(rid)
        for col, cell in enumerate(row, 1):
            text = cell.lstrip()
            numeric = re.fullmatch(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", text)
            if text and text[0] in "=+-@" and not numeric:
                errors.append({"code": "formula_like_text", "row": n, "column": col})
        if "source_id" in headers:
            refs = [v.strip() for v in item["source_id"].split(";") if v.strip()]
            if not refs:
                errors.append({"code": "empty_source", "row": n})
            elif any(v not in ids and v not in {"INFERENCE", "UNKNOWN"} for v in refs):
                errors.append({"code": "unknown_source", "row": n})
    return {"passed": not errors, "rows_checked": len(rows), "errors": errors,
            "scope": "Local structure only. Does not verify facts, consent, timestamps, model quality or readiness to publish."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("table", help="Generated output CSV; never the original customer database")
    parser.add_argument("--ledger", required=True, help="Source ledger CSV")
    parser.add_argument("--contract", default=str(Path(__file__).resolve().parents[1] / "assets/output-contract.json"))
    args = parser.parse_args()
    try:
        contract = json.loads(Path(args.contract).read_text(encoding="utf-8"))
        result = inspect_table(args.table, args.ledger, contract)
    except (OSError, ValueError, csv.Error, KeyError, TypeError) as exc:
        # Paths and cell values can contain customer information; report type only.
        result = {"passed": False, "errors": [{"code": "input_read_error", "type": type(exc).__name__}]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())

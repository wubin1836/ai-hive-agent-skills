"""Offline evaluators. No network, no credentials, read-only inputs."""
import argparse
import json
import math
import re
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path

def nonempty(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(label + " must be a nonempty string")
    return value.strip()

def number(value, label):
    if isinstance(value, bool):
        raise ValueError(label + " must be numeric, not boolean")
    try:
        v = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValueError(label + " must be numeric")
    if not v.is_finite() or v < 0:
        raise ValueError(label + " must be finite and nonnegative")
    return v

def trials(rows):
    if not isinstance(rows, list) or not rows:
        raise ValueError("input must be a nonempty JSON array")
    buckets = defaultdict(list)
    seen = set()
    allowed = {"completed", "failed", "timeout", "cancelled", "pending"}
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("each record must be an object")
        case = nonempty(row.get("case_id"), "case_id")
        model = nonempty(row.get("model"), "model")
        currency = nonempty(row.get("currency"), "currency").upper()
        if not re.fullmatch("[A-Z]{3}", currency):
            raise ValueError("currency must be a three-letter currency code")
        key = (model, case)
        if key in seen:
            raise ValueError("duplicate case within model; aggregate retries first")
        seen.add(key)
        status = row.get("status")
        if status not in allowed:
            raise ValueError("unsupported status")
        passed = row.get("passed")
        if passed is not None and not isinstance(passed, bool):
            raise ValueError("passed must be true, false, or null")
        if passed is True and status != "completed":
            raise ValueError("only completed cases may pass")
        if passed is True:
            nonempty(row.get("evidence"), "passed cases require evidence")
        cost = None if row.get("cost") is None else number(row["cost"], "cost")
        latency = None if row.get("latency_ms") is None else number(row["latency_ms"], "latency_ms")
        buckets[(model, currency)].append((status, passed, cost, latency))
    result = []
    for (model, currency), items in sorted(buckets.items()):
        n = len(items)
        accepted = sum(s == "completed" and p is True for s, p, c, l in items)
        unknown = sum(s == "pending" or (s == "completed" and p is None) for s,p,c,l in items)
        known = sum((c for s,p,c,l in items if c is not None), Decimal(0))
        missing = sum(c is None for s,p,c,l in items)
        latencies = sorted(float(l) for s,p,c,l in items if l is not None)
        result.append({
            "model": model, "currency": currency, "cases": n,
            "accepted": accepted, "unknown_or_pending": unknown,
            "not_accepted": n-accepted-unknown,
            "confirmed_pass_rate": accepted/n,
            "known_cost_subtotal": float(known), "missing_cost_cases": missing,
            "total_cost": None if missing else float(known),
            "cost_per_accepted": None if missing or not accepted else float(known/accepted),
            "latency_samples": len(latencies),
            "latency_p95_ms": latencies[math.ceil(.95*len(latencies))-1] if latencies else None
        })
    return {"mode": "trials", "groups": result,
            "note": "Currencies are separate. Pending/unknown is not success. Costs must include all attempts per case."}

def id_list(value, label, allow_empty):
    if not isinstance(value, list):
        raise ValueError(label + " must be an array")
    ids = [nonempty(x, label) for x in value]
    if not allow_empty and not ids:
        raise ValueError(label + " must contain ground truth")
    if len(set(ids)) != len(ids):
        raise ValueError(label + " contains duplicate IDs")
    return ids

def retrieval(rows, k=5):
    if isinstance(k, bool) or not isinstance(k, int) or k < 1:
        raise ValueError("k must be a positive integer")
    if not isinstance(rows, list) or not rows:
        raise ValueError("input must be a nonempty JSON array")
    results, seen = [], set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("each record must be an object")
        q = nonempty(row.get("query_id"), "query_id")
        if q in seen:
            raise ValueError("duplicate query_id")
        seen.add(q)
        relevant = set(id_list(row.get("relevant_ids"), "relevant_ids", False))
        retrieved = id_list(row.get("retrieved_ids"), "retrieved_ids", True)[:k]
        hits = len(relevant.intersection(retrieved))
        first = next((i+1 for i, x in enumerate(retrieved) if x in relevant), None)
        results.append({"query_id": q, "recall_at_k": hits/len(relevant),
                        "reciprocal_rank_at_k": 1/first if first else 0,
                        "hit_at_k": int(hits > 0)})
    return {"mode": "retrieval", "k": k, "queries": results,
            "mean_recall_at_k": sum(x["recall_at_k"] for x in results)/len(results),
            "mrr_at_k": sum(x["reciprocal_rank_at_k"] for x in results)/len(results),
            "hit_rate_at_k": sum(x["hit_at_k"] for x in results)/len(results),
            "note": "Metrics measure supplied evidence IDs, not answer correctness or production recall."}

def main(mode):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    if mode == "retrieval":
        parser.add_argument("--k", type=int, default=5)
    args = parser.parse_args()
    try:
        rows = json.loads(args.input.read_text(encoding="utf-8"))
        value = trials(rows) if mode == "trials" else retrieval(rows, args.k)
        print(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False))
    except (ValueError, TypeError, OSError) as exc:
        # Do not print arbitrary input or credential-bearing lines.
        parser.exit(2, "Invalid input: " + type(exc).__name__ + ". Check the documented schema.\n")


if __name__ == "__main__":
    main('trials')

#!/usr/bin/env python3
"""Validate a local dependency DAG. No network, execution, or publication."""
import argparse
import json
from collections import deque
from pathlib import Path


def audit(data):
    errors = []
    nodes = data.get('nodes', [])
    edges = data.get('edges', [])
    if not isinstance(nodes, list) or not isinstance(edges, list):
        return {'valid': False, 'errors': ['nodes and edges must be lists']}
    ids = []
    for node in nodes:
        if not isinstance(node, dict) or not isinstance(node.get('id'), str) or not node['id']:
            errors.append('each node must have a nonempty string id')
        else:
            ids.append(node['id'])
    if not ids:
        errors.append('at least one node is required')
    if len(ids) != len(set(ids)):
        errors.append('duplicate node id')
    outgoing = {i: [] for i in ids}
    degree = {i: 0 for i in ids}
    seen = set()
    for edge in edges:
        if not isinstance(edge, dict):
            errors.append('each edge must be an object')
            continue
        src, dst = edge.get('from'), edge.get('to')
        if not isinstance(src, str) or not isinstance(dst, str):
            errors.append('edge endpoints must be strings')
        elif src not in outgoing or dst not in outgoing:
            errors.append(f'missing endpoint: {src} -> {dst}')
        elif (src, dst) in seen:
            errors.append(f'duplicate edge: {src} -> {dst}')
        else:
            seen.add((src, dst))
            outgoing[src].append(dst)
            degree[dst] += 1
    queue = deque(sorted(k for k, v in degree.items() if v == 0))
    order = []
    while queue:
        current = queue.popleft()
        order.append(current)
        for target in outgoing[current]:
            degree[target] -= 1
            if degree[target] == 0:
                queue.append(target)
    blocked = sorted(k for k, v in degree.items() if v > 0)
    if blocked:
        errors.append('cycle blocks some nodes; downstream nodes may also be blocked')
    return {'valid': not errors, 'errors': errors, 'topological_order': order,
            'cycle_or_downstream_blocked': blocked}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding='utf-8'))
        result = audit(data) if isinstance(data, dict) else {'valid': False, 'errors': ['root must be an object']}
    except (ValueError, OSError) as error:
        result = {'valid': False, 'errors': [str(error)]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['valid'] else 1


if __name__ == '__main__':
    raise SystemExit(main())

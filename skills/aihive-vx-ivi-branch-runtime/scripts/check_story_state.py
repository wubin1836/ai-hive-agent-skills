#!/usr/bin/env python3
"""Validate/replay a finite story graph locally; never generates streaming video."""
import argparse
import json
from pathlib import Path


def audit(data, events=None):
    errors = []
    items = data.get('states', [])
    if not isinstance(items, list):
        return {'valid': False, 'errors': ['states must be a list']}
    states = {}
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get('id'), str) or not item['id']:
            errors.append('state needs a nonempty string id')
            continue
        sid = item['id']
        if sid in states:
            errors.append(f'duplicate state: {sid}')
        if not isinstance(item.get('terminal', False), bool):
            errors.append(f'terminal must be boolean: {sid}')
        states[sid] = item
    start = data.get('start')
    if not isinstance(start, str) or start not in states:
        errors.append('unknown start state')
    links = {sid: {} for sid in states}
    for sid, item in states.items():
        transitions = item.get('transitions', [])
        if not isinstance(transitions, list):
            errors.append(f'transitions must be a list: {sid}')
            continue
        if item.get('terminal') is True and transitions:
            errors.append(f'terminal state has outgoing transitions: {sid}')
        for transition in transitions:
            if not isinstance(transition, dict):
                errors.append(f'invalid transition in {sid}')
                continue
            event, target = transition.get('event'), transition.get('to')
            if not isinstance(event, str) or not event:
                errors.append(f'invalid event in {sid}')
                continue
            if event in links[sid]:
                errors.append(f'ambiguous event in {sid}: {event}')
                continue
            if not isinstance(target, str) or target not in states:
                errors.append(f'unknown target from {sid}: {target}')
                continue
            links[sid][event] = target
        if not item.get('terminal') and not transitions:
            errors.append(f'nonterminal dead end: {sid}')
    if errors:
        return {'valid': False, 'errors': errors}
    reached = {start}
    queue = [start]
    while queue:
        for target in links[queue.pop()].values():
            if target not in reached:
                reached.add(target)
                queue.append(target)
    unreachable = sorted(set(states) - reached)
    if unreachable:
        errors.append('unreachable states: ' + ', '.join(unreachable))
    terminal_reachable = {sid for sid, item in states.items() if item.get('terminal')}
    while True:
        additions = {sid for sid, edges in links.items() if any(t in terminal_reachable for t in edges.values())}
        if additions <= terminal_reachable:
            break
        terminal_reachable |= additions
    trapped = sorted(reached - terminal_reachable)
    if trapped:
        errors.append('no path to a terminal state: ' + ', '.join(trapped))
    current, trace = start, [start]
    if events is not None:
        if not isinstance(events, list) or any(not isinstance(e, str) for e in events):
            errors.append('events must be a list of strings')
        else:
            for event in events:
                if event not in links[current]:
                    errors.append(f'event not accepted in {current}: {event}')
                    break
                current = links[current][event]
                trace.append(current)
    return {'valid': not errors, 'errors': errors, 'reachable': sorted(reached),
            'trace': trace, 'final_state': current, 'ended': bool(states[current].get('terminal')),
            'scope': 'local state validation only; no real-time media performance verified'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--events', type=Path, help='JSON list of event names')
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding='utf-8'))
        events = json.loads(args.events.read_text(encoding='utf-8')) if args.events else None
        result = audit(data, events) if isinstance(data, dict) else {'valid': False, 'errors': ['root must be an object']}
    except (ValueError, OSError) as error:
        result = {'valid': False, 'errors': [str(error)]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['valid'] else 1


if __name__ == '__main__':
    raise SystemExit(main())

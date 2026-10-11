# -*- coding: utf-8 -*-
"""Read-only task DAG and approval-owner validator. It does not execute tasks."""
import argparse
from common import read_json, rows, text, run

def audit(data):
    tasks = rows(data, 'tasks')
    nodes = {}
    for task in tasks:
        key = text(task.get('id'), 'id')
        if key in nodes:
            raise ValueError('重复id')
        nodes[key] = task
    errors, dependencies = [], {}
    for key, task in nodes.items():
        deps = task.get('depends_on', [])
        if not isinstance(deps, list) or not all(isinstance(x, str) and x for x in deps):
            raise ValueError('depends_on类型错误')
        if len(deps) != len(set(deps)):
            errors.append({'task_id': key, 'code': 'duplicate_dependency'})
        dependencies[key] = set(deps)
        for dep in deps:
            if dep not in nodes:
                errors.append({'task_id': key, 'code': 'missing_dependency', 'dependency': dep})
        required = task.get('approval_required', False)
        if not isinstance(required, bool):
            raise ValueError('approval_required必须为布尔值')
        if required and not (isinstance(task.get('approver'), str) and task['approver'].strip()):
            errors.append({'task_id': key, 'code': 'missing_approver'})
    pending = set(nodes)
    order = []
    while pending:
        ready = sorted(key for key in pending if not (dependencies[key] & pending) and dependencies[key] <= set(nodes))
        if not ready:
            break
        order.extend(ready)
        pending.difference_update(ready)
    if pending:
        errors.append({'code': 'cycle_or_blocked_dependency', 'task_ids': sorted(pending)})
    return {'passed': not errors, 'topological_order': order, 'errors': errors,
            'scope': '仅结构检查；不证明权限已授予、执行已发生或审批已通过'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input')
    return audit(read_json(parser.parse_args().input))

if __name__ == '__main__':
    run(main)

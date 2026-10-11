# -*- coding: utf-8 -*-
"""Read-only local file manifest, preventing traversal/symlink escapes."""
import argparse
import hashlib
from pathlib import Path
from common import read_json, run

def audit(data, root):
    root = Path(root).resolve(strict=True)
    if not root.is_dir():
        raise ValueError('根目录无效')
    paths = data.get('files')
    if not isinstance(paths, list) or not paths or not all(isinstance(x, str) and x for x in paths):
        raise ValueError('files必须是非空路径数组')
    errors, results, seen, hashes = [], [], set(), {}
    for raw in paths:
        path = Path(raw)
        if path.is_absolute() or '..' in path.parts or '\\' in raw:
            errors.append({'path': raw, 'code': 'unsafe_path'})
            continue
        canonical = path.as_posix()
        if canonical in seen:
            errors.append({'path': raw, 'code': 'duplicate_entry'})
            continue
        seen.add(canonical)
        target = (root / path).resolve()
        try:
            target.relative_to(root)
        except ValueError:
            errors.append({'path': raw, 'code': 'symlink_escape'})
            continue
        if not target.is_file():
            errors.append({'path': raw, 'code': 'missing_or_nonfile'})
            continue
        digest = hashlib.sha256()
        size = 0
        with target.open('rb') as f:
            while True:
                block = f.read(1024*1024)
                if not block:
                    break
                digest.update(block)
                size += len(block)
        sha = digest.hexdigest()
        results.append({'path': raw, 'bytes': size, 'sha256': sha})
        hashes.setdefault(sha, []).append(raw)
        if not size:
            errors.append({'path': raw, 'code': 'empty_file'})
    return {'passed': not errors, 'files': results, 'errors': errors,
        'duplicate_content': [v for v in hashes.values() if len(v)>1],
        'scope': '仅文件存在性和哈希，不读取回显正文，不确认版权有效、内容合规或渠道审核'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input')
    parser.add_argument('--root', required=True)
    args = parser.parse_args()
    return audit(read_json(args.input), args.root)

if __name__ == '__main__':
    run(main)

#!/usr/bin/env python3
"""Small AI-HIVE MCP client. No automatic retries or credential persistence."""
import argparse
import json
import os
from pathlib import Path
import re
import sys
import urllib.error
import urllib.request

ORIGIN = 'https://ai-hive.iclip.cn'
ENDPOINT = ORIGIN + '/api/mcp'
READ_ONLY = {'ai_hive_list_models', 'ai_hive_get_task'}
VERSION = '2025-03-26'


class SafeError(Exception):
    pass


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise SafeError('请求发生重定向；已停止，未转发凭据。请检查官方连接地址。')


def redact(value):
    if isinstance(value, dict):
        secret_name = re.compile(r'^(?:api_?key|access_?token|refresh_?token|token|authorization|secret|password)$', re.I)
        return {k: '[REDACTED]' if secret_name.fullmatch(k) and not isinstance(v, dict) else redact(v) for k, v in value.items()}
    if isinstance(value, list):
        return [redact(v) for v in value]
    if isinstance(value, str):
        for key in ('AI_HIVE_API_KEY', 'AI_HIVE_ACCESS_TOKEN'):
            secret = os.environ.get(key, '').strip()
            if secret:
                value = value.replace(secret, '[REDACTED]')
        value = re.sub(r'\b(?:skh_|sk-ent-|sk-api-|ms-|pat-)[A-Za-z0-9_-]{20,}', '[REDACTED]', value)
    return value


def is_response(item, expected_id):
    return isinstance(item, dict) and (expected_id is None or (item.get('id') == expected_id and 'method' not in item and ('result' in item or 'error' in item)))


def payload(raw, content_type, expected_id=None):
    text = raw.decode('utf-8-sig').strip()
    if not text:
        if expected_id is not None:
            raise SafeError('响应为空，不能确认调用结果；不要盲目重试生成。')
        return {}
    candidates = []
    if 'text/event-stream' in content_type or text.startswith(('event:', 'data:', ':')):
        for block in text.replace('\r\n', '\n').split('\n\n'):
            data = '\n'.join(line[5:].lstrip(' ') for line in block.splitlines() if line.startswith('data:'))
            if data and data != '[DONE]':
                candidates.append(json.loads(data))
    else:
        candidates.append(json.loads(text))
    for item in candidates:
        if is_response(item, expected_id):
            return item
    raise SafeError('未找到匹配请求ID的MCP响应；请核对已有任务状态，勿重复提交。')


def read_response(response, expected_id):
    content_type = response.headers.get('Content-Type', '')
    if 'text/event-stream' not in content_type:
        raw = response.read(32 * 1024 * 1024 + 1)
        if len(raw) > 32 * 1024 * 1024:
            raise SafeError('响应超过32MB，停止接收；请用宿主客户端处理大文件。')
        return payload(raw, content_type, expected_id)
    # Consume SSE incrementally; a successful result must not wait for EOF.
    lines, total = [], 0
    while True:
        line = response.readline()
        total += len(line)
        if total > 32 * 1024 * 1024:
            raise SafeError('SSE响应超过32MB，已停止。')
        if line.strip():
            lines.append(line)
            continue
        block = b''.join(lines)
        lines = []
        if block:
            try:
                return payload(block, 'text/event-stream', expected_id)
            except SafeError:
                pass  # progress notifications and other IDs are not this response
        if not line:
            raise SafeError('SSE连接结束但无匹配结果；请查询已有任务状态，勿重复提交。')


def request(url, body=None, headers=None, expected_id=None):
    req = urllib.request.Request(url, data=body, headers=headers or {'Accept': 'application/json'})
    try:
        with urllib.request.build_opener(NoRedirect()).open(req, timeout=45) as response:
            return read_response(response, expected_id), response.headers
    except urllib.error.HTTPError as exc:
        retry = exc.headers.get('Retry-After')
        suffix = ('；Retry-After=' + retry) if retry and retry.isdigit() else ''
        raise SafeError('HTTP ' + str(exc.code) + suffix + '；本次停止，不自动重试。401/403请在客户端重新授权。') from None
    except (urllib.error.URLError, TimeoutError, OSError):
        raise SafeError('连接失败或超时；结果未知，请先查询任务状态，不要自动重发。') from None


class Client:
    def __init__(self):
        self.session = None
        self.seq = 0
        self.version = VERSION
        self.headers = {'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream'}
        token = os.environ.get('AI_HIVE_ACCESS_TOKEN', '').strip()
        key = os.environ.get('AI_HIVE_API_KEY', '').strip()
        if token:
            self.headers['Authorization'] = 'Bearer ' + token
        elif key:
            self.headers['x-ai-hive-api-key'] = key
        else:
            raise SafeError('缺少凭据：优先在宿主MCP界面完成OAuth。脚本用户请通过本机Secret设置AI_HIVE_API_KEY，不要粘贴到聊天。')
        result = self.rpc('initialize', {'protocolVersion': VERSION, 'capabilities': {}, 'clientInfo': {'name': 'ai-hive-skill-helper', 'version': '1.1.0'}})
        self.version = result.get('protocolVersion', VERSION)
        self.rpc('notifications/initialized', notification=True)

    def rpc(self, method, params=None, notification=False):
        self.seq += 1
        obj = {'jsonrpc': '2.0', 'method': method, 'params': params or {}}
        if not notification:
            obj['id'] = self.seq
        headers = dict(self.headers)
        if method != 'initialize':
            headers['MCP-Protocol-Version'] = self.version
        if self.session:
            headers['Mcp-Session-Id'] = self.session
        result, response_headers = request(ENDPOINT, json.dumps(obj).encode(), headers, None if notification else self.seq)
        self.session = response_headers.get('Mcp-Session-Id') or self.session
        if result.get('error'):
            raise SafeError('MCP返回错误；' + json.dumps(redact(result['error']), ensure_ascii=False))
        return result.get('result', result)

    def tools(self):
        results, cursor, seen = [], None, set()
        for _ in range(30):
            data = self.rpc('tools/list', {'cursor': cursor} if cursor else {})
            results.extend(data.get('tools', []))
            cursor = data.get('nextCursor')
            if not cursor:
                return results
            if cursor in seen:
                raise SafeError('工具分页游标重复，已停止。')
            seen.add(cursor)
        raise SafeError('工具分页超过安全上限，未继续请求。')


def check_args(args, schema):
    if not isinstance(args, dict):
        raise SafeError('参数必须为JSON对象。')
    missing = [key for key in schema.get('required', []) if key not in args]
    if missing:
        raise SafeError('缺少工具必填字段：' + ', '.join(missing))
    if schema.get('additionalProperties') is False:
        extra = set(args) - set(schema.get('properties', {}))
        if extra:
            raise SafeError('工具不接受这些字段：' + ', '.join(sorted(extra)))
    # This is a preflight check, not a complete JSON Schema implementation.
    # The caller must inspect the full schema; the server performs final validation.


def doctor():
    protected, _ = request(ORIGIN + '/.well-known/oauth-protected-resource/api/mcp')
    auth, _ = request(ORIGIN + '/.well-known/oauth-authorization-server')
    return {'metadata_reachable': True, 'mcp_url': ENDPOINT, 'resource': protected.get('resource'), 'pkce_s256': 'S256' in auth.get('code_challenge_methods_supported', []), 'tools_access_verified': False, 'models_verified': False}


def main():
    parser = argparse.ArgumentParser(description='AI-HIVE MCP发现与单次调用；不自动重试')
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('doctor', help='仅检查公开OAuth元数据，不验证账号和模型')
    sub.add_parser('tools', help='认证后读取完整工具schema')
    call = sub.add_parser('call', help='按实时schema单次调用')
    call.add_argument('tool')
    call.add_argument('--args-file', required=True)
    call.add_argument('--confirm-external', action='store_true', help='确认指定参数的上传、计费或其他外部动作；不代表发布授权')
    ns = parser.parse_args()
    if ns.command == 'doctor':
        result = doctor()
    else:
        # Reject unconfirmed writes before initializing any connection.
        if ns.command == 'call' and ns.tool not in READ_ONLY and not ns.confirm_external:
            raise SafeError('非只读调用已拦截。先确认模型、输入外发范围、数量和费用，再加--confirm-external。')
        client = Client()
        listing = client.tools()
        if ns.command == 'tools':
            result = {'tools': listing}
        else:
            tool = next((t for t in listing if t.get('name') == ns.tool), None)
            if tool is None:
                raise SafeError('当前MCP没有该工具，不能凭名称猜测调用。')
            args = json.loads(Path(ns.args_file).read_text(encoding='utf-8'))
            check_args(args, tool.get('inputSchema', {}))
            result = client.rpc('tools/call', {'name': ns.tool, 'arguments': args})
            if result.get('isError'):
                raise SafeError('工具执行失败：' + json.dumps(redact(result), ensure_ascii=False))
    print(json.dumps(redact(result), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (SafeError, ValueError, OSError) as exc:
        print(str(redact(str(exc))), file=sys.stderr)
        sys.exit(1)


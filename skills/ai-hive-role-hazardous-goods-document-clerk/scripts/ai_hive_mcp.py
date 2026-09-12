#!/usr/bin/env python3
"""Bounded AI-HIVE MCP helper for the service's documented 2025 handshake.

OAuth login belongs to the host client. No OAuth tokens are stored here. This
helper only supports the explicitly listed protocol revisions, not every MCP
feature. It never retries a tool call or follows HTTP redirects with credentials.
"""
from __future__ import annotations

import argparse
import json
import os
import socket
import sys
import urllib.error
import urllib.request

ORIGIN = "https://ai-hive.iclip.cn"
MCP_URL = ORIGIN + "/api/mcp"
RESOURCE_URL = ORIGIN + "/.well-known/oauth-protected-resource/api/mcp"
AUTH_URL = ORIGIN + "/.well-known/oauth-authorization-server"
SUPPORTED = {"2025-03-26", "2025-06-18", "2025-11-25"}
READ_ONLY = {"ai_hive_list_models", "ai_hive_get_task"}
MAX_BYTES = 4 * 1024 * 1024


class ClientError(Exception):
    """A safe, user-facing failure without response bodies or credentials."""


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ClientError("服务返回重定向，已停止；请在客户端核对官方地址，不转发凭据。")


def redact(text):
    values = {os.environ.get(name, "").strip() for name in ("AI_HIVE_API_KEY", "AI_HIVE_ACCESS_TOKEN")}
    for value in sorted(values - {""}, key=len, reverse=True):
        text = text.replace(value, "[REDACTED]")
    return text


def safe_json(value):
    """Redact strings before JSON escaping, including response object keys."""
    def clean(item):
        if isinstance(item, str):
            return redact(item)
        if isinstance(item, list):
            return [clean(v) for v in item]
        if isinstance(item, dict):
            return {clean(k): clean(v) for k, v in item.items()}
        return item
    return json.dumps(clean(value), ensure_ascii=False, indent=2)


def auth_headers():
    token = os.environ.get("AI_HIVE_ACCESS_TOKEN", "").strip()
    key = os.environ.get("AI_HIVE_API_KEY", "").strip()
    value = token or key
    if not value:
        raise ClientError("本脚本进程未提供凭据。请通过安全进程环境注入 AI_HIVE_API_KEY 或 AI_HIVE_ACCESS_TOKEN；脚本不继承客户端 OAuth 登录态。也可直接使用已连接的客户端 MCP 工具，无需运行脚本；doctor 不需要凭据。")
    if any(not 0x21 <= ord(c) <= 0x7E for c in value):
        raise ClientError("凭据含非法空白或非 ASCII 字符，请检查 Secret 配置；不输出凭据。")
    return {"Authorization": "Bearer " + token} if token else {"x-ai-hive-api-key": key}


def decode_json(raw):
    try:
        value = json.loads(raw)
    except (ValueError, UnicodeError):
        raise ClientError("服务响应不是有效 JSON；已停止且未重试。") from None
    if not isinstance(value, dict):
        raise ClientError("服务响应不是 JSON 对象。")
    return value


def read_payload(response, request_id):
    if request_id is None:
        return {}
    if "text/event-stream" not in response.headers.get("Content-Type", "").lower():
        raw = response.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise ClientError("响应超过诊断脚本大小限制，请改用完整 MCP 客户端。")
        obj = decode_json(raw)
        if obj.get("id") != request_id:
            raise ClientError("MCP 响应 ID 不匹配，无法确认请求结果。")
        return obj
    total, data = 0, []
    while True:
        raw = response.readline(MAX_BYTES + 1)
        total += len(raw)
        if total > MAX_BYTES:
            raise ClientError("SSE 响应过大，请改用完整 MCP 客户端。")
        try:
            line = raw.decode("utf-8").rstrip("\r\n")
        except UnicodeError:
            raise ClientError("SSE 编码无效。") from None
        if line.startswith("data:"):
            data.append(line[5:].lstrip(" "))
        if not line:
            if data:
                payload = "\n".join(data)
                data = []
                if payload != "[DONE]":
                    obj = decode_json(payload)
                    if obj.get("id") == request_id:
                        return obj
            if not raw:
                break
    raise ClientError("SSE 已结束但未收到对应请求的结果；不要盲目重复生成。")


def transport(payload=None, *, session=None, protocol=None, url=MCP_URL, public=False):
    if url not in {MCP_URL, RESOURCE_URL, AUTH_URL}:
        raise ClientError("本脚本仅允许已固定的 AI-HIVE 官方端点。")
    if public and url == MCP_URL:
        raise ClientError("公开探测只允许 OAuth 元数据端点。")
    headers = {"Accept": "application/json" if public else "application/json, text/event-stream"}
    if not public:
        headers.update(auth_headers())
        headers["Content-Type"] = "application/json"
        if session:
            if not isinstance(session, str) or any(not 0x21 <= ord(c) <= 0x7E for c in session):
                raise ClientError("服务会话标识格式无效；已停止且不输出原值。")
            headers["Mcp-Session-Id"] = session
        if protocol:
            headers["MCP-Protocol-Version"] = protocol
    req = urllib.request.Request(url, data=None if public else json.dumps(payload, ensure_ascii=False).encode(), headers=headers, method="GET" if public else "POST")
    try:
        with urllib.request.build_opener(NoRedirect()).open(req, timeout=25 if public else 60) as response:
            if public:
                raw = response.read(MAX_BYTES + 1)
                if len(raw) > MAX_BYTES:
                    raise ClientError("元数据响应过大。")
                return decode_json(raw), None
            return read_payload(response, payload.get("id")), response.headers.get("Mcp-Session-Id") or session
    except urllib.error.HTTPError as error:
        code = error.code
        error.close()
        if code in (401, 403):
            raise ClientError(f"HTTP {code}：认证或权限不足，请重新连接；不输出响应原文。") from None
        if code == 429:
            raise ClientError("HTTP 429：触发限流。停止本次操作，遵循平台等待要求，不循环重试。") from None
        raise ClientError(f"HTTP {code}：请求未正常完成。若为生成/上传，状态可能不确定，先核对任务记录，不盲目重试。") from None
    except (urllib.error.URLError, TimeoutError, socket.timeout, OSError):
        raise ClientError("连接失败或超时。未自动重试；生成/上传状态可能不确定，先核对平台任务记录。") from None


class Client:
    def __init__(self):
        self.session = None
        self.protocol = "2025-03-26"
        self.next_id = 1

    def rpc(self, method, params):
        ident = self.next_id
        self.next_id += 1
        result, self.session = transport({"jsonrpc": "2.0", "id": ident, "method": method, "params": params}, session=self.session, protocol=self.protocol)
        if "error" in result:
            raise ClientError("MCP 返回协议错误；未重复请求，请在客户端查看脱敏诊断。")
        value = result.get("result")
        if not isinstance(value, dict):
            raise ClientError("MCP 缺少有效 result。")
        if value.get("isError"):
            raise ClientError("工具返回 isError=true；本次未完成，不能标为成功，也不自动重试。")
        return value

    def initialize(self):
        result = self.rpc("initialize", {"protocolVersion": self.protocol, "capabilities": {}, "clientInfo": {"name": "ai-hive-assistant-helper", "version": "1.0.0"}})
        selected = result.get("protocolVersion")
        if selected not in SUPPORTED:
            raise ClientError("服务协商的协议版本不在本脚本支持范围；请使用兼容当前服务的完整 MCP 客户端。")
        self.protocol = selected
        _, self.session = transport({"jsonrpc": "2.0", "method": "notifications/initialized"}, session=self.session, protocol=self.protocol)

    def list_tools(self):
        tools, cursor, seen = [], None, set()
        for _ in range(30):
            page = self.rpc("tools/list", {"cursor": cursor} if cursor else {})
            batch = page.get("tools")
            if not isinstance(batch, list) or any(not isinstance(t, dict) or not isinstance(t.get("name"), str) for t in batch):
                raise ClientError("tools/list 格式不符，停止操作。")
            tools.extend(batch)
            cursor = page.get("nextCursor")
            if not cursor:
                return tools
            if not isinstance(cursor, str) or cursor in seen:
                raise ClientError("工具分页游标异常，停止以避免循环请求。")
            seen.add(cursor)
        raise ClientError("工具分页超过诊断上限。")

    def call(self, name, arguments, confirmed):
        if not isinstance(arguments, dict):
            raise ClientError("参数必须是 JSON 对象。")
        if name not in READ_ONLY and not confirmed:
            raise ClientError("调用可能上传素材、改变状态或计费；仅在用户确认用途、素材与预算后增加 --confirm-paid。")
        tool = next((t for t in self.list_tools() if t["name"] == name), None)
        if tool is None:
            raise ClientError("当前账号未发现此工具；不能推测或编造接口。")
        schema = tool.get("inputSchema", {})
        if not isinstance(schema, dict) or schema.get("type", "object") != "object":
            raise ClientError("工具 inputSchema 格式不符，停止调用。")
        required = schema.get("required", [])
        if not isinstance(required, list) or any(not isinstance(k, str) for k in required):
            raise ClientError("工具 schema 必填字段格式不符，停止调用。")
        missing = [k for k in required if k not in arguments]
        if missing:
            raise ClientError("参数缺少 schema 必填字段。请先 describe 并完整核对 schema。")
        return self.rpc("tools/call", {"name": name, "arguments": arguments})


def doctor():
    resource, _ = transport(url=RESOURCE_URL, public=True)
    auth, _ = transport(url=AUTH_URL, public=True)
    return {"metadata_reachable": True, "authenticated_test_performed": False, "mcp_url": MCP_URL,
            "resource": resource.get("resource"), "issuer": auth.get("issuer"),
            "scopes_supported": auth.get("scopes_supported", []), "pkce": auth.get("code_challenge_methods_supported", []),
            "registration_advertised": bool(auth.get("registration_endpoint")),
            "refresh_advertised": "refresh_token" in auth.get("grant_types_supported", []),
            "credential_present": bool(os.environ.get("AI_HIVE_API_KEY") or os.environ.get("AI_HIVE_ACCESS_TOKEN")),
            "next": "元数据可达不代表账号已授权。请在客户端登录后 tools/list；不要用付费生成测试连接。"}


def main():
    parser = argparse.ArgumentParser(description="AI-HIVE MCP 公开诊断、工具发现与单次受控调用")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor")
    sub.add_parser("list-tools")
    describe = sub.add_parser("describe")
    describe.add_argument("tool")
    call = sub.add_parser("call")
    call.add_argument("tool")
    args = call.add_mutually_exclusive_group()
    args.add_argument("--args", help="JSON 对象；有私密内容时使用本地 args-file")
    args.add_argument("--args-file")
    call.add_argument("--confirm-paid", action="store_true")
    ns = parser.parse_args()
    arguments = {}
    if ns.command == "call":
        try:
            if ns.args_file:
                with open(ns.args_file, encoding="utf-8") as f:
                    arguments = json.load(f)
            else:
                arguments = json.loads(ns.args or "{}")
        except (OSError, ValueError):
            raise ClientError("无法读取有效参数 JSON；未连接网络。") from None
        if not isinstance(arguments, dict):
            raise ClientError("参数必须是 JSON 对象。")
        if ns.tool not in READ_ONLY and not ns.confirm_paid:
            raise ClientError("可能付费或改变状态的工具需 --confirm-paid；未连接网络。")
    if ns.command == "doctor":
        result = doctor()
    else:
        client = Client()
        client.initialize()
        if ns.command == "list-tools":
            result = {"tools": client.list_tools()}
        elif ns.command == "describe":
            result = next((t for t in client.list_tools() if t["name"] == ns.tool), None)
            if result is None:
                raise ClientError("当前账号未发现此工具。")
        else:
            result = client.call(ns.tool, arguments, ns.confirm_paid)
    print(safe_json(result))


if __name__ == "__main__":
    try:
        main()
    except ClientError as e:
        print(redact(str(e)), file=sys.stderr)
        raise SystemExit(2)

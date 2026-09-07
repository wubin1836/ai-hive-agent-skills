#!/usr/bin/env python3
"""AI-HIVE remote MCP diagnostics and API-key client.

OAuth users should let their MCP client manage browser login and tokens.  This
helper can inspect public OAuth metadata without a credential, and can list or
call tools when an AI_HIVE_API_KEY is supplied through the environment.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request


MCP_URL = os.environ.get("AI_HIVE_MCP_URL", "https://ai-hive.iclip.cn/api/mcp")
ORIGIN = "https://ai-hive.iclip.cn"
PROTECTED_RESOURCE = f"{ORIGIN}/.well-known/oauth-protected-resource/api/mcp"
AUTHORIZATION_SERVER = f"{ORIGIN}/.well-known/oauth-authorization-server"
READ_ONLY_TOOLS = {"ai_hive_list_models", "ai_hive_get_task"}


def fetch_json(url: str) -> dict:
    request = urllib.request.Request(url, headers={"accept": "application/json"})
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def parse_payload(raw: bytes, content_type: str) -> dict:
    text = raw.decode("utf-8", errors="replace").strip()
    if "text/event-stream" in content_type or text.startswith("event:") or text.startswith("data:"):
        for line in text.splitlines():
            if line.startswith("data:"):
                candidate = line[5:].strip()
                if candidate and candidate != "[DONE]":
                    return json.loads(candidate)
        raise RuntimeError("MCP 返回了 SSE，但没有可解析的 data 事件。")
    if not text:
        return {}
    return json.loads(text)


def auth_headers() -> dict[str, str]:
    key = os.environ.get("AI_HIVE_API_KEY", "").strip()
    token = os.environ.get("AI_HIVE_ACCESS_TOKEN", "").strip()
    if token:
        return {"authorization": f"Bearer {token}"}
    if key:
        return {"x-ai-hive-api-key": key}
    raise SystemExit(
        "缺少凭据。OAuth 用户请在 MCP 客户端中完成登录；本脚本调用工具时需通过环境变量提供 "
        "AI_HIVE_API_KEY，或仅运行 doctor。"
    )


def post(payload: dict, session_id: str | None = None) -> tuple[dict, str | None]:
    headers = {
        "content-type": "application/json",
        "accept": "application/json, text/event-stream",
        **auth_headers(),
    }
    if session_id:
        headers["mcp-session-id"] = session_id
    request = urllib.request.Request(
        MCP_URL,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            result = parse_payload(response.read(), response.headers.get("content-type", ""))
            return result, response.headers.get("mcp-session-id") or session_id
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        if error.code == 401:
            raise SystemExit(
                "AI-HIVE MCP 返回 401。请确认 API Key 完整且未撤销；OAuth 用户应在客户端内重新连接，"
                "不要把 OAuth token 粘贴到命令行。"
            )
        raise SystemExit(f"AI-HIVE MCP HTTP {error.code}: {body[:800]}")


def initialize() -> str | None:
    response, session_id = post({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2025-03-26",
            "capabilities": {},
            "clientInfo": {"name": "ai-hive-skill-helper", "version": "1.0.0"},
        },
    })
    if response.get("error"):
        raise SystemExit(json.dumps(response, ensure_ascii=False, indent=2))
    post({"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}}, session_id)
    return session_id


def invoke(method: str, params: dict | None = None) -> dict:
    session_id = initialize()
    response, _ = post({
        "jsonrpc": "2.0",
        "id": 2,
        "method": method,
        "params": params or {},
    }, session_id)
    return response


def doctor() -> None:
    protected = fetch_json(PROTECTED_RESOURCE)
    authorization = fetch_json(AUTHORIZATION_SERVER)
    result = {
        "ok": True,
        "mcp_url": MCP_URL,
        "transport": "streamable_http",
        "protected_resource": protected.get("resource"),
        "authorization_servers": protected.get("authorization_servers", []),
        "scopes_supported": authorization.get("scopes_supported", []),
        "pkce": authorization.get("code_challenge_methods_supported", []),
        "dynamic_client_registration": bool(authorization.get("registration_endpoint")),
        "has_refresh_token": "refresh_token" in authorization.get("grant_types_supported", []),
        "has_revocation": bool(authorization.get("revocation_endpoint")),
        "credential_present": bool(os.environ.get("AI_HIVE_API_KEY") or os.environ.get("AI_HIVE_ACCESS_TOKEN")),
        "next": "在 MCP 客户端添加远程地址并完成 OAuth；API Key 用户可继续运行 list-tools。",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def load_args(raw: str | None, path: str | None) -> dict:
    if raw and path:
        raise SystemExit("--args 与 --args-file 只能使用一个。")
    if path:
        value = json.loads(open(path, "r", encoding="utf-8").read())
    else:
        value = json.loads(raw or "{}")
    if not isinstance(value, dict):
        raise SystemExit("工具参数必须是 JSON 对象。")
    return value


def main() -> None:
    parser = argparse.ArgumentParser(description="AI-HIVE 远程 MCP 登录、连接与工具诊断")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor", help="无凭据检查 MCP 与 OAuth 元数据")
    sub.add_parser("list-tools", help="使用环境变量中的 API Key 列出工具")
    call = sub.add_parser("call", help="调用一个 MCP 工具")
    call.add_argument("tool")
    call.add_argument("--args")
    call.add_argument("--args-file")
    call.add_argument("--confirm-paid", action="store_true", help="明确允许调用可能计费的工具")
    ns = parser.parse_args()
    if ns.command == "doctor":
        doctor()
        return
    if ns.command == "list-tools":
        response = invoke("tools/list")
    else:
        if ns.tool not in READ_ONLY_TOOLS and not ns.confirm_paid:
            raise SystemExit("该工具可能产生费用；核对模型、数量、参数与预算后增加 --confirm-paid。")
        response = invoke("tools/call", {
            "name": ns.tool,
            "arguments": load_args(ns.args, ns.args_file),
        })
    print(json.dumps(response, ensure_ascii=False, indent=2))
    if response.get("error"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()

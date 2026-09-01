#!/usr/bin/env python3
"""Small stdio client for the official IMIVA Ecommerce MCP package."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

PACKAGE = "@infimind/ecom-content-cli@latest"
DEFAULT_API_URL = "https://imiva.ecpro.com"


def require_runtime() -> tuple[str, str]:
    npx = shutil.which("npx")
    if not npx:
        raise SystemExit("未找到 npx。请先安装 Node.js 18 或更高版本。")
    token = os.environ.get("MCP_TOKEN", "").strip()
    if not token:
        raise SystemExit("缺少 MCP_TOKEN。请在 IMIVA 的 MCP Token 页面创建后通过环境变量提供。")
    return npx, token


def read_response(proc: subprocess.Popen[str], expected_id: int) -> dict:
    assert proc.stdout is not None
    while True:
        line = proc.stdout.readline()
        if line == "":
            stderr = proc.stderr.read() if proc.stderr else ""
            raise RuntimeError(f"MCP 进程提前退出。{stderr[-1200:]}")
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if payload.get("id") == expected_id:
            return payload


def send(proc: subprocess.Popen[str], payload: dict) -> None:
    assert proc.stdin is not None
    proc.stdin.write(json.dumps(payload, ensure_ascii=False) + "\n")
    proc.stdin.flush()


def invoke(method: str, params: dict | None = None) -> dict:
    npx, token = require_runtime()
    env = os.environ.copy()
    env["MCP_TOKEN"] = token
    env["API_URL"] = os.environ.get("IMIVA_API_URL", os.environ.get("API_URL", DEFAULT_API_URL))
    proc = subprocess.Popen(
        [npx, "-y", PACKAGE],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        env=env,
    )
    try:
        send(proc, {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {"name": "imiva-skill-helper", "version": "1.0.0"},
            },
        })
        initialized = read_response(proc, 1)
        if "error" in initialized:
            return initialized
        send(proc, {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}})
        send(proc, {"jsonrpc": "2.0", "id": 2, "method": method, "params": params or {}})
        return read_response(proc, 2)
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()


def load_args(raw: str | None, file_path: str | None) -> dict:
    if raw and file_path:
        raise SystemExit("--args 与 --args-file 只能使用一个。")
    if file_path:
        value = json.loads(Path(file_path).read_text(encoding="utf-8"))
    else:
        value = json.loads(raw or "{}")
    if not isinstance(value, dict):
        raise SystemExit("工具参数必须是 JSON 对象。")
    return value


def main() -> None:
    parser = argparse.ArgumentParser(description="调用 IMIVA Ecommerce MCP")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list-tools", help="列出当前 Token 可用工具")
    call = sub.add_parser("call", help="调用一个 MCP 工具")
    call.add_argument("tool")
    call.add_argument("--args")
    call.add_argument("--args-file")
    ns = parser.parse_args()
    if ns.command == "list-tools":
        response = invoke("tools/list")
    else:
        response = invoke("tools/call", {"name": ns.tool, "arguments": load_args(ns.args, ns.args_file)})
    print(json.dumps(response, ensure_ascii=False, indent=2))
    if "error" in response:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

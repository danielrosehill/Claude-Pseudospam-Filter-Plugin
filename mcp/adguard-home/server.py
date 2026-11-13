#!/usr/bin/env python3
"""
Pseudospam Filter — AdGuard Home MCP server.

Minimal MCP server exposing AdGuard Home REST endpoints needed by the
adguard-push and adguard-configure skills. Runs over stdio.

Tools exposed:
  - adguard_status            GET  /control/status
  - adguard_filter_status     GET  /control/filtering/status
  - adguard_set_user_rules    POST /control/filtering/set_rules
  - adguard_add_blocklist_url POST /control/filtering/add_url
  - adguard_refresh_lists     POST /control/filtering/refresh

Auth: Basic Auth via env vars ADGUARD_BASE_URL / ADGUARD_USERNAME /
ADGUARD_PASSWORD. Or pass per-call.

Install: pip install mcp httpx
Run:     python3 server.py
"""

from __future__ import annotations

import os
import sys
from typing import Any

import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

BASE_URL = os.environ.get("ADGUARD_BASE_URL", "").rstrip("/")
USERNAME = os.environ.get("ADGUARD_USERNAME", "")
PASSWORD = os.environ.get("ADGUARD_PASSWORD", "")


def _client() -> httpx.Client:
    if not BASE_URL:
        print("ADGUARD_BASE_URL not set", file=sys.stderr)
        sys.exit(2)
    auth = (USERNAME, PASSWORD) if USERNAME else None
    return httpx.Client(base_url=BASE_URL, auth=auth, timeout=15.0)


server: Server = Server("pseudospam-filter-adguard-home")


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="adguard_status",
            description="GET /control/status — version, DNS state, running flag.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="adguard_filter_status",
            description="GET /control/filtering/status — current user rules + managed blocklist URLs.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="adguard_set_user_rules",
            description="POST /control/filtering/set_rules — REPLACES all user rules. Pass the full merged rule list.",
            inputSchema={
                "type": "object",
                "properties": {"rules": {"type": "array", "items": {"type": "string"}}},
                "required": ["rules"],
            },
        ),
        Tool(
            name="adguard_add_blocklist_url",
            description="POST /control/filtering/add_url — register a hosted blocklist URL.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "url": {"type": "string"},
                    "whitelist": {"type": "boolean", "default": False},
                },
                "required": ["name", "url"],
            },
        ),
        Tool(
            name="adguard_refresh_lists",
            description="POST /control/filtering/refresh — re-fetch all managed blocklist URLs now.",
            inputSchema={
                "type": "object",
                "properties": {"whitelist": {"type": "boolean", "default": False}},
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, args: dict[str, Any]) -> list[TextContent]:
    with _client() as c:
        if name == "adguard_status":
            r = c.get("/control/status")
        elif name == "adguard_filter_status":
            r = c.get("/control/filtering/status")
        elif name == "adguard_set_user_rules":
            r = c.post("/control/filtering/set_rules", json={"rules": args["rules"]})
        elif name == "adguard_add_blocklist_url":
            r = c.post(
                "/control/filtering/add_url",
                json={
                    "name": args["name"],
                    "url": args["url"],
                    "whitelist": args.get("whitelist", False),
                },
            )
        elif name == "adguard_refresh_lists":
            r = c.post(
                "/control/filtering/refresh",
                json={"whitelist": args.get("whitelist", False)},
            )
        else:
            return [TextContent(type="text", text=f"unknown tool: {name}")]

        body = r.text or "(empty body)"
        return [
            TextContent(
                type="text",
                text=f"HTTP {r.status_code}\n{body}",
            )
        ]


async def main() -> None:
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())

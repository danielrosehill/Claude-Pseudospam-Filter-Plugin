# Pseudospam Filter — AdGuard Home MCP

Minimal MCP server exposing the AdGuard Home REST endpoints that the
`adguard-push` and `adguard-configure` skills need. Stdio transport.

## Install

```bash
pip install mcp httpx
```

## Wire into `.mcp.json`

```json
{
  "mcpServers": {
    "adguard-home": {
      "command": "python3",
      "args": ["${PLUGIN_DIR}/mcp/adguard-home/server.py"],
      "env": {
        "ADGUARD_BASE_URL": "http://adguard.lan:3000",
        "ADGUARD_USERNAME": "admin",
        "ADGUARD_PASSWORD": "..."
      }
    }
  }
}
```

For real use, supply `ADGUARD_PASSWORD` from your secrets manager at the launcher level
(for example `op run` or a wrapper that exports it), not in plain `.mcp.json`.

## Tools

| Tool | Endpoint | Notes |
|------|----------|-------|
| `adguard_status` | `GET /control/status` | Health check |
| `adguard_filter_status` | `GET /control/filtering/status` | Read current user rules + managed URLs |
| `adguard_set_user_rules` | `POST /control/filtering/set_rules` | **Destructive — replaces all user rules** |
| `adguard_add_blocklist_url` | `POST /control/filtering/add_url` | Register a hosted blocklist |
| `adguard_refresh_lists` | `POST /control/filtering/refresh` | Re-fetch all managed lists |

## Why ship our own

There is no canonical AdGuard Home MCP. The endpoints above are the minimum
surface Pseudospam Filter needs and they're stable enough that a 100-line stdio
wrapper is the right amount of code. If/when an upstream maintainer ships a
fuller MCP, this stub can be retired in favour of it.

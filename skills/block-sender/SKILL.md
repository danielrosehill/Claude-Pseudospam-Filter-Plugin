---
name: block-sender
description: Create a server-side Gmail filter that auto-trashes (or labels + archives) future mail from a sender, via an available email MCP. Falls back to recording the block in the local sender-blocklist.json if no MCP is wired up. Use when the user says "block this sender" or "make sure I never see another email from X".
---

# block-sender

Push a sender block upstream so the user never sees future mail from this address. Local-only logging is the fallback.

## Inputs

- Sender email (required — full address, not just domain unless the user specifically wants a domain-wide block).
- Workspace (which email MCP).
- Action — `trash` (default) or `label-and-archive`. Trash is right for clear scraping spam; label-and-archive preserves a record for analysis.
- Reason — short string for the audit log.

## Steps

1. Resolve corpus path. Append to `<corpus>/data/sender-blocklist.json`: `{ email, domain, display_name (optional), reason, action, date }`.

2. Detect available email MCP tools. Look for `create_filter` / `manage_filter` style tools (e.g. `mcp__*__create_filter` from the Google-Workspace-Plugin's `gws-personal` / `gws-business` MCP). If none are available, stop here and tell the user the block is recorded locally only — they'll need to install an email MCP for server-side action.

3. If an MCP is available:
   - Check whether a filter for this sender already exists (idempotency — don't pile up duplicate filters).
   - Get-or-create a Gmail label `Pseudospam/Blocked` (or whatever convention the user has set in `corpus/config.json`).
   - Create the filter:
     - criteria: `{ from: <email> }`
     - action for `trash`: `addLabelIds: [<label-id>, "TRASH"]`, `removeLabelIds: ["INBOX"]`
     - action for `label-and-archive`: `addLabelIds: [<label-id>]`, `removeLabelIds: ["INBOX"]`

4. Optional: also block the sender's domain if the user confirms. Domain-wide blocks are powerful — only do them when the user says yes.

5. Report: filter id (or `already_blocked`), label, what was logged to `sender-blocklist.json`, and whether a domain-wide variant was applied.

## Why MCP-first, not the bundled script

The legacy `scripts/gmail-block-sender.py` (kept for reference) uses a per-repo OAuth flow and a `gmail-credentials.json` file. The MCP path is preferred — it reuses the user's existing Workspace MCP auth and doesn't require a side-channel credentials file. Only fall back to the script if the user explicitly wants it.

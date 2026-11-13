---
name: adguard-push
description: Push the user's accumulated tracking-pixel + ad-tracker domains from the Pseudospam Filter corpus into a self-hosted AdGuard Home instance, using the credentials configured by adguard-configure. Network-layer block — every device on the LAN benefits, not just one mailbox. Use when the user wants to apply their corpus findings at the DNS layer.
---

# adguard-push

Take what Pseudospam Filter has learned from the user's mail and turn it into a network-wide DNS block on AdGuard Home.

## Resolve corpus path + AdGuard config

Standard resolver. Read `<corpus>/config.json` → `adguard`. If missing, run `adguard-configure` first.

Read the password from the environment variable named in `password_env` (default `ADGUARD_PASSWORD`). An older config may have `password_ref`, a secret reference such as a 1Password URI: resolve it with that manager's CLI (`op read <ref>`), and offer to switch the config to `password_env`.

## Inputs

- Source — `tracking`, `ads`, or `both` (default).
- Min frequency — only push domains seen ≥ N times. Default 1.
- Mode — `replace` (overwrite Pseudospam Filter's section of user rules) or `append` (additive). Default `replace` for `custom-rules` strategy, since dedup matters at the DNS layer.

## Strategy: custom-rules

1. Aggregate domains from the chosen source(s) per `min frequency`.
2. Format as AdGuard rules:
   ```
   ! ===== Pseudospam Filter start (managed — do not edit) =====
   ! Generated: <ISO timestamp>
   ||tracking.example.com^
   ||other.example.com^
   ! ===== Pseudospam Filter end =====
   ```
3. Fetch existing user rules via `GET <base>/control/filtering/status` (the `user_rules` field).
4. Strip any prior Pseudospam Filter-managed block (matched by the start/end markers) so we don't accumulate stale entries.
5. Splice the new Pseudospam Filter block in.
6. POST the merged rules back via `POST <base>/control/filtering/set_rules` with body `{ "rules": ["...", "..."] }`.

## Strategy: hosted-list

1. Aggregate + format as plain domain list.
2. Upload/sync to the configured `hosted_url` location (Cloudflare R2, gist, local nginx — depends on `adguard.list_name`/`hosted_url` config).
3. If this is the first push, register the URL with AdGuard via `POST /control/filtering/add_url` with `{ "name": "<list_name>", "url": "<hosted_url>", "whitelist": false }`.
4. On subsequent pushes, just refresh: `POST /control/filtering/refresh` with `{ "whitelist": false }`.

## After either strategy

- Report: domains pushed, mode (replace/append), AdGuard's confirmation, current total filter count post-push.
- Tail-log the push to `<corpus>/data/adguard-push-log.json`: `{ pushed_at, source, count, strategy }`.

## Gotchas

- AdGuard Home's `set_rules` is destructive — it replaces ALL user rules. The start/end marker pattern above is essential to avoid wiping the user's hand-curated rules.
- Some pixel hosts are dual-use (e.g. `list-manage.com` also serves Mailchimp's hosted preference centres). The `export-dns-blocklist` skill flags these — surface those warnings here and let the user opt out per-domain before pushing.
- If the `mcp/adguard-home` MCP is wired in via `.mcp.json`, prefer its tools over raw HTTP calls. The MCP gives idempotent semantics that direct REST does not.

---
name: adguard-configure
description: One-time setup for AdGuard Home integration. Captures the AdGuard Home base URL, credentials, and target blocklist filename, validates connectivity, and persists to corpus/config.json. Use before adguard-push.
---

# adguard-configure

Wire Pseudospam Filter up to a self-hosted AdGuard Home instance so blocklist exports can be pushed network-wide.

## Resolve corpus path

Standard resolver (`<data>/config.json` → `corpus_path`). Run `setup` first if missing.

## Inputs (interactive)

- **Base URL** — e.g. `http://adguard.lan:3000` or `https://dns.example.com`. Must be reachable from this machine.
- **Username / password** — AdGuard Home admin credentials (Basic Auth).
- **Strategy** — one of:
  - `custom-rules` (default) — append to AdGuard Home's "User rules" via `/control/filtering/set_rules`. Best for small lists, fast iteration.
  - `hosted-list` — host the export file somewhere reachable (HTTP) and add it as a managed blocklist URL via `/control/filtering/add_url`. Best for larger lists or sharing across instances.
- **Storage path for credentials** — recommend 1Password (use the `op-vault` plugin if installed) over plaintext. If plaintext, store in `<corpus>/config.json` with explicit user consent and chmod 600.

## Steps

1. Probe `GET <base>/control/status` with Basic Auth to validate URL + credentials. Surface any TLS / 401 / connection-refused error to the user.

2. Read current filter state via `GET <base>/control/filtering/status` so the user can see what's already there before Pseudospam Filter touches it.

3. If `strategy = hosted-list`, ask where the blocklist file should be hosted (suggestions: a path served by a local nginx, a Cloudflare R2 bucket via the `cloudflare-mgmt` MCP, a private gist via `gist-writer`). Persist the URL.

4. Persist to `<corpus>/config.json` under an `adguard` key:

   ```json
   {
     "adguard": {
       "base_url": "http://adguard.lan:3000",
       "username": "admin",
       "password_env": "ADGUARD_PASSWORD",
       "strategy": "custom-rules",
       "list_name": "pseudospam-filter",
       "hosted_url": null
     }
   }
   ```

   Use `password_env` (the name of an environment variable your secrets manager sets) where possible. Only fall back to a `password` field with explicit user consent.

5. Report: connectivity OK, current filter count, chosen strategy, next step (`adguard-push`).

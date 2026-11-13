---
name: scan-recent-pixels
description: Bulk scan of recent inbox messages (default last 30) for tracking pixels and ad-tracker beacons. For every detection logs which email it came from, sender, time, recipient, the raw pixel URL, and a suggested block pattern. Appends to the user's tracking inventories. Requires an email MCP (e.g. gws-personal). Use when the user wants visibility into how much pixel surveillance is hitting their inbox right now.
---

# scan-recent-pixels

Bulk reconnaissance — sweep the last N inbox messages and surface every embedded tracker without any per-email interaction.

## Resolve corpus path

Read `<data>/config.json` → `corpus_path`. Run `setup` first if missing.

## Inputs (interactive)

- **Workspace** — which email MCP workspace to use (e.g. `personal`, `business`).
- **N** — how many recent messages to scan. Default 30. Cap at 200 to keep it sane.
- **Folder** — default `INBOX`. Allow user to scope to a label (e.g. `Promotions`).

## Steps

1. List the most recent N messages in the chosen folder via the email MCP (`search_emails` with `in:inbox` or `label:<x>`).

2. For each message, fetch the full content (`read_email` with `format: full` or `raw`). Skip if already analysed (look up by message-id in `<corpus>/data/processed-emails.json` or in a dedicated `<corpus>/data/pixel-scans.json`).

3. Run the detection rules from `scan-tracking-pixels/SKILL.md` (don't re-implement — refer to that skill's rules) on each message's HTML body.

4. For every detected pixel/tracker, build a record:

   ```json
   {
     "message_id": "<gmail-id>",
     "subject": "...",
     "sender_email": "...",
     "sender_domain": "...",
     "recipient": "...",
     "date_sent": "2026-04-30T14:25:08+02:00",
     "date_scanned": "2026-04-30T22:00:00Z",
     "pixel_url": "https://...",
     "pixel_domain": "...",
     "pixel_type": "tracking_pixel | ad_tracker | click_tracking",
     "detection_reason": "1x1 dimensions / known domain / hidden styling",
     "suggested_block": {
       "dns_block": "<domain>",
       "filter_rule": "from:(*@<sender_domain>) — sender is using tracking pixels",
       "regex": "..."
     }
   }
   ```

5. Append entries to `<corpus>/data/pixel-scans.json` (create as array if needed). Also fold each unique `pixel_domain` into `tracking-domains.json` or `ad-trackers.json` (route by type).

6. Print a report:
   - Total messages scanned, total pixels found
   - Top 10 sender domains by pixel count
   - Top 10 pixel domains by frequency (with `tracking_pixel` vs `ad_tracker` split)
   - Suggested next step: run `export-dns-blocklist` to materialise a Pi-hole/AdGuard/hosts-format export, or `contribute-blocklist` to share findings with public collaborative lists.

## Performance

If N > 50, batch the `read_email` calls. If the MCP supports `format: metadata` for the initial pass, use that to triage and only fetch full bodies for messages that look HTML.

## Privacy

The records contain recipient address — that's the user's own email, low risk. But pixel URLs often encode the recipient address or a per-recipient ID. Never share `pixel-scans.json` raw — use `contribute-blocklist` which strips per-recipient identifiers before export.

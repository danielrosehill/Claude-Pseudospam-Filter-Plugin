---
name: tracking-report
description: Summarise the user's accumulated tracking-pixel and ad-tracker inventory — totals by type, top domains, top senders, recent additions. Read-only — does not modify any inventory. Use when the user wants visibility into what their corpus has captured.
---

# tracking-report

Read-only summary of the user's corpus state. No side-effects.

## Resolve corpus path

Standard resolver.

## Steps

1. Read `<corpus>/data/tracking-domains.json`, `<corpus>/data/ad-trackers.json`, `<corpus>/data/pixel-scans.json`. Skip files that don't exist.

2. Aggregate:
   - Total unique domains, split by `tracking_pixel` / `click_tracking` / `ad_tracker`.
   - Top 10 domains by frequency.
   - Top 10 sender domains (from `pixel-scans.json`) by pixel count.
   - Recent additions (last 7 days).

3. Print a concise report. Suggest next-step skills:
   - `export-dns-blocklist` — materialise as Pi-hole / AdGuard / hosts format.
   - `adguard-push` — push directly to AdGuard Home.
   - `contribute-blocklist` — sanitise and prepare a contribution to a public list.

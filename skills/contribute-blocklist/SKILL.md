---
name: contribute-blocklist
description: Strip per-recipient identifiers from the user's tracking inventories and prepare a redacted contribution suitable for opening a PR against collaborative public anti-tracking lists (EasyPrivacy, hagezi, oisd, Pi-hole community, AdGuard's tracker filter). Outputs a sanitised diff plus a draft PR description. Does NOT open the PR automatically — the user reviews and submits.
---

# contribute-blocklist

Help the user share their findings with public anti-tracking efforts without leaking their own email or recipient IDs.

## Resolve corpus path

Standard resolver.

## Inputs

- Target list — one of:
  - `easyprivacy` (https://github.com/easylist/easylist) — Adblock Plus syntax
  - `hagezi` (https://github.com/hagezi/dns-blocklists) — domain lists
  - `oisd` (https://oisd.nl) — submit via their form, not a PR
  - `pihole` (https://github.com/pi-hole) — community blocklist repos
  - `adguard` (https://github.com/AdguardTeam/AdguardFilters) — filter rules
  - `local` — just produce the sanitised file, no upstream target
- Source — `tracking`, `ads`, or `both`.
- Min evidence — only contribute domains seen in ≥ N distinct messages from ≥ M distinct senders. Default `N=3, M=2` to keep noise out.

## Steps

1. Aggregate from `tracking-domains.json` + `ad-trackers.json` per `min evidence`.

2. **Redact**: strip every `url` field, `recipient`, `sender_email`, and any per-message metadata. Keep only:
   - `domain`
   - `type` (`tracking_pixel` | `ad_tracker` | `click_tracking`)
   - `evidence_count` (how many distinct messages)
   - `distinct_senders_count`
   - `first_seen_date`, `last_seen_date`

3. Format for the target list's syntax:
   - Adblock Plus / EasyPrivacy:
     ```
     ||tracking.example.com^$third-party
     ```
   - Hagezi / Pi-hole / oisd: one domain per line.
   - AdGuard: same as Adblock, may include `$image` modifier for pixels.

4. Write to `<corpus>/exports/contribution-<target>-<YYYYMMDD>.txt`.

5. Draft a PR description (write to `<corpus>/exports/contribution-<target>-<YYYYMMDD>-PR.md`):

   ```markdown
   ## Add N tracking-pixel domains observed in personal corpus

   These domains were observed embedding tracking pixels or ad beacons in
   unsolicited / commercial email over <date range>. Each domain met the
   contribution threshold of ≥3 distinct messages from ≥2 distinct senders.

   Source: personal Pseudospam Filter corpus, redacted (no recipient or per-message
   identifiers retained).

   ### Domains

   - tracking.example.com — tracking_pixel — 7 messages, 4 senders
   - ...
   ```

6. Print the path of both files and a copy of the recommended `gh pr create` command (do NOT run it — let the user review first). For `oisd` (form-based), point at the submission URL instead.

## What never leaves the user's machine

- Raw `.eml` files
- Recipient address
- Per-message URLs (which often encode recipient ID)
- Sender display names
- Subject lines

If any of those appear in the contribution diff, abort and report the leak.

---
name: export-dns-blocklist
description: Aggregate the user's accumulated tracking-domains.json + ad-trackers.json into a portable DNS blocklist (Pi-hole / AdGuard / hosts / dnsmasq formats). Writes to corpus/exports/. Use when the user wants to push their pixel inventory to a network-level blocker.
---

# export-dns-blocklist

Materialise the corpus into a DNS-level blocklist suitable for Pi-hole, AdGuard Home, `/etc/hosts`, dnsmasq, or NextDNS.

## Resolve corpus path

Standard config resolver (`<data>/config.json` → `corpus_path`).

## Inputs

- Format — one of `hosts`, `pihole`, `adguard`, `dnsmasq`, `unbound`, `plain`. Default `hosts`.
- Source — `tracking` (just `tracking-domains.json`), `ads` (just `ad-trackers.json`), `both` (default).
- Min frequency — only include domains seen ≥ N times across the corpus. Default 1. Higher values reduce false positives.

## Steps

1. Read the relevant inventory file(s). Aggregate by `domain`. Drop entries that don't meet `min_frequency`.

2. Normalise: lowercase, strip ports, drop subdomain noise where the user wants the eTLD+1 form (ask once on first run, persist preference).

3. Generate the export. Examples:

   - `hosts`:
     ```
     0.0.0.0 mailtrack.io
     0.0.0.0 qmailroute.net
     ```
   - `pihole` (plain domain list, one per line):
     ```
     mailtrack.io
     qmailroute.net
     ```
   - `adguard` (`||domain^` form):
     ```
     ||mailtrack.io^
     ||qmailroute.net^
     ```
   - `dnsmasq`:
     ```
     address=/mailtrack.io/0.0.0.0
     ```
   - `unbound`:
     ```
     local-zone: "mailtrack.io." always_nxdomain
     ```

4. Write to `<corpus>/exports/pseudospam-filter-<format>-<YYYYMMDD>.txt` (or `.conf` for unbound/dnsmasq).

5. Print a one-line summary of the export path and entry count, plus a hint on how to load it (e.g. for Pi-hole: "Group Management → Adlists, paste the file URL or contents").

## Caveats

Some pixel-tracking domains co-host non-tracker content (e.g. `list-manage.com` also serves Mailchimp's hosted preference centres). Surface a warning when an exported domain is on a known dual-use list — let the user decide.

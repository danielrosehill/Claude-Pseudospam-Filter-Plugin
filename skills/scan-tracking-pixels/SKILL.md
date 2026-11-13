---
name: scan-tracking-pixels
description: Scan a single email (raw .eml or live message via email MCP) for tracking pixels and ad-tracker beacons, then append every detected pixel host to the user's tracking inventories (tracking-domains.json + ad-trackers.json). Use when the user wants to surgically extract pixels from one email without running the full capture pipeline.
---

# scan-tracking-pixels

Targeted pixel scan on a single email. The companion `scan-recent-pixels` skill does the same in bulk over recent inbox messages.

## Resolve corpus path

Read `<data>/config.json` → `corpus_path`. Run `setup` if missing.

## Detection rules

Search the HTML body for tracking pixels — be aggressive, false positives here are cheap:

- `<img>` with `width="1"`/`height="1"`, `width:1px`/`height:1px` CSS, or `display:none`/`visibility:hidden` on an external image
- External image URLs containing tracking IDs: `?uid=`, `?eid=`, `?email=`, base64 blobs, long random hex/UUID path segments
- Known tracking domains: `mailtrack.io`, `qmailroute.net`, `emailroute.net`, `mailgun.org`, `sendgrid.net`, `convertkit-mail.com`, `list-manage.com`, `mc.us<N>.list-manage.com`, `cmail<N>.com`, `hubspotemail.net`, `mkt<N>.com`, `pardot.com`, `marketo.com`, `et.<vendor>.com`
- Known ad-tracker domains (route to `ad-trackers.json` instead of `tracking-domains.json`): `googleadservices.com`, `googlesyndication.com`, `pagead2.googlesyndication.com`, `doubleclick.net`, `googletagmanager.com`, `google-analytics.com`, `g.doubleclick.net`, `facebook.com/tr`, `bat.bing.com`, `analytics.twitter.com`, `linkedin.com/li/track`, `tr.snapchat.com`

Also check click-tracking: `<a href>` routed through redirect domains rather than the apparent destination.

## Steps

1. Read the email (path or message id via available email MCP).
2. Run the detection rules. For each hit, collect: `domain`, `url`, `type` (`tracking_pixel` | `click_tracking` | `ad_tracker`), context.
3. Append entries to the appropriate inventory under `<corpus>/data/`:
   - `tracking-domains.json` — pixels and click-trackers (per-email-marketing infra)
   - `ad-trackers.json` — adsense / DSP / analytics beacons
   Each entry: `{ domain, type, url, detected_in, sender, recipient, date_detected, date_sent }`.
4. Don't re-add an exact `(domain, url, detected_in)` triple. Increment a `count` field on the existing entry instead.
5. Report: counts by category, new domains added, top offenders.

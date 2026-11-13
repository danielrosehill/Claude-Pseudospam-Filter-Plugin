---
name: prioritise-genuine
description: Turn the genuine mail a sweep found into a reply queue ordered by what deserves attention, by the user's own priority order (paid work, peers in their niches, real corrections, reasonable asks), with a one-line summary and suggested action each. Use when the user says "what should I reply to", "prioritise my real email", "which genuine ones matter", or after a sweep.
---

# Prioritise genuine mail

1. Collect verdicts with `label: genuine` from the latest `<data>/sweeps/<date>/`
   (or judge the `passed` label's messages first via `sweep` steps 1–2 if none exist).
2. Sort by `priority` (desc), then date (oldest first: they've waited longest).
   Re-check the top 10 yourself against `config.json → profile.priority_order`;
   the Haiku judge's priority is a first pass.
3. Present: priority, sender (role), subject, one-line summary, suggested action
   (`reply_now`, `reply_later`, `decline`). Group 7–10 as **reply now**, 4–6 as
   **this week**, 1–3 as **optional**.
4. Offer to draft replies for the top group with the user's email-sending skill, or
   a polite decline for asks that don't fit.

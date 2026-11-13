---
name: sweep
description: Run Pseudospam Filter over the inbox. Finds unsolicited one-to-one-looking mail, has parallel Haiku judges classify it against the standard plus the user's own examples, then labels pseudospam as Caught and archives it, marks genuine mail as Passed, and leaves unsure mail in place. Works like a second spam filter with a review queue. Use when the user says "run the pseudospam filter", "sweep for pseudospam", "clear the fake-personal outreach", "which of these are real".
---

# Sweep

Read `<data>/config.json` (run `setup` if missing). Day folder `S=<data>/sweeps/<YYYY-MM-DD>/`.

## 1. Candidates → `S/candidates.jsonl`

Unsolicited mail that *looks* one-to-one:
- in the inbox, within `sweep_window`, **without** any of the configured result
  labels (already processed);
- not bulk: drop messages with `List-Unsubscribe`, `List-Id` or `Precedence: bulk`
  headers when your MCP exposes them, and robot senders (`noreply`,
  `notifications`, …);
- not from someone the user has written to (sent-mail recipients).

Write one JSON line per message: `id, from, from_name, to, subject, date, body`
(body ≤ 6,000 chars). If a helper script in the user's environment already does
this, use it. Writing to a file keeps hundreds of bodies out of the conversation.

## 2. Judge, in parallel

Split into chunks of ~50 lines. Spawn one `pseudospam-judge` agent (Haiku) per
chunk **in a single message** so they run concurrently. Give each: candidates path,
line range, output `S/verdicts/<n>.jsonl`, and `<data>`. Treat their output as a
report to check: spot-read a few verdicts per chunk before acting.

## 3. Apply

Collect verdicts. For each message:

| Verdict | Action |
|---|---|
| `pseudo_personalised`, confidence ≥ `min_confidence` | add `caught`; then `on_caught`: `label_archive` (default; remove INBOX), `bin`, or `label_only` |
| `genuine` | add `passed`; stays in the inbox |
| below `min_confidence`, either label | add `unsure`; stays in the inbox |
| `out_of_scope` | add `passed` (processed; not outreach) |

Use the MCP's batch label-modify tool (chunks of ≤1,000 ids).

**Example labels are never applied by the sweep.** They're the user's teaching data;
only the user, or a review they confirm, puts mail there.

## 4. Report → `S/report.md` and chat

Counts per action; caught by sender (top 15) with one-line summaries; **genuine
mail by priority** (that's the reply queue, see `prioritise-genuine`); all unsure
with rationale. Point to the `caught` label view for review.

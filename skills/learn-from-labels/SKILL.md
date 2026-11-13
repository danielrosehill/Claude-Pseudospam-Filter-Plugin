---
name: learn-from-labels
description: Teach Pseudospam Filter your own boundary from the emails you've labelled as examples. Reads the example labels, writes examples.jsonl (few-shot cases the judge sees) and profile.md (your rules, in your words, where they differ from the standard). Use when the user says "learn from my labels", "I've labelled more examples", "update what you think is spam", or after a review corrected mistakes.
---

# Learn from your labels

1. Read `<data>/config.json`. For each of `example_pseudospam`, `example_genuine`,
   `example_unsure`, search `label:<slug>` and fetch the messages (subject, from,
   to, body truncated to ~1,500 chars).
2. Write `<data>/examples.jsonl`, one line per message:
   `{"label": "pseudo_personalised|genuine|unsure", "to": "...", "subject": "...", "excerpt": "...", "why": "<one line: which signals>"}`.
   Keep at most ~40 (newest first, balanced across labels). The judge reads all of it.
3. Compare the examples with `references/standard.md`. Write `<data>/profile.md`:
   only the places where **this user's** line differs or sharpens it, e.g.
   "product drips from tools I signed up to count as pseudospam", "anything to the
   podcast address is pseudospam unless it names an episode". Each rule cites the
   example(s) behind it. Paraphrase; no addresses or names in rules.
4. Report: examples per label, new or changed profile rules.

Run again whenever examples are added or a review turned up mistakes. Corrections
are the most valuable examples.

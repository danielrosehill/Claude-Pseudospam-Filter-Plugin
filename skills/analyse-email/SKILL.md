---
name: analyse-email
description: Run the full Pseudospam Filter analysis pipeline on a single email — semantic spam reasoning, tracking-pixel detection, sender block, processed-emails log, markdown report. Use when the user wants a deep dive on one email rather than the lighter capture-example flow.
---

# analyse-email

Full forensic pipeline. Heavier than `capture-example` — produces a markdown analysis report on disk and runs the full `email-analyst` agent. Use this when the user wants to study one email in depth or the analysis is going to feed downstream tooling.

## Resolve corpus path

Standard resolver. Run `setup` first if missing.

## Inputs

- Email reference: a `.eml` path under `<corpus>/inputs/emails/` OR a Gmail message id (via available email MCP) OR raw pasted text.

## Steps

1. **Materialise**: if not already on disk, save the raw email to `<corpus>/inputs/emails/<YYYY-MM-DD>-<slug>.eml`.

2. **Parse**: from-address + display name, subject, date, reply-to, full HTML and plain-text bodies, all headers.

3. **Semantic Spam Analysis (SSA)** — reason about whether this is scraped-list outreach or genuine correspondence. The core question: does this sender actually care about the recipient, or are they carpet-bombing a scraped list?

   These emails typically pass every traditional spam filter — valid DKIM/SPF, real company domains. The signal is in the *intent*, not the headers.

   Reasoning signals (use judgement, not a checklist):
   - **Scraped personalisation** — vague references to "your interest in X" or "impressive work" that could apply to anyone, vs. specific engagement with something the recipient actually did.
   - **Asymmetric ask** — wants something (retweet, intro, demo, backlink) while offering nothing genuine in return.
   - **Templated structure** — reads like a mail-merge with a name swapped in.
   - **Tracking infrastructure** — links routed through click-tracking domains, tracking pixels.
   - **Artificial urgency** — deadlines pressuring a quick reply with no real reason.
   - **Commercial intent disguised as friendliness** — pretends to be peer-to-peer but wants free promotion, a sales call, or a backlink.
   - **AI-faked "I care"** — language pattern shifts that suggest LLM-generated personalisation: implausibly specific praise that's actually generic, or tone that doesn't match anything the recipient has published.

   Don't over-weight technical signals like missing unsubscribe headers or domain age — those are orthogonal.

   Produce: reasoning paragraph, quoted evidence, spam confidence 0.0–1.0, reusable filter-instruction snippet for an AI email-triage agent.

4. **Tracking Detection** — apply the rules in `scan-tracking-pixels/SKILL.md`. Append every hit to `<corpus>/data/tracking-domains.json` or `<corpus>/data/ad-trackers.json` (route by type).

5. **Sender block** — append to `<corpus>/data/sender-blocklist.json`. If the user explicitly asked to block, also call `block-sender` for the server-side filter.

6. **Log to processed-emails** — append a full record to `<corpus>/data/processed-emails.json`: filename, dates, sender info, subject, plain body, spam_confidence, spam_reasoning, why_added, flags object, trackers_found counts, analysis_file path.

7. **Save report** — write the full markdown analysis to `<corpus>/outputs/analyses/<filename>-analysis.md`.

8. **Summary** — print a brief summary: confidence score, top indicators, trackers found, where the report was saved.

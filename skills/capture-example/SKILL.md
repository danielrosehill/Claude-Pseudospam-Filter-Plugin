---
name: capture-example
description: Capture one email as a Pseudospam Filter example. Labels it as a pseudospam (or genuine) example in Gmail so the judge learns from it, saves a copy to the corpus, asks what pattern it represents, suggests a filter pattern, and optionally pushes a server-side block or drafts an unsubscribe reply. Use when the user says "this is pseudospam", "save this as an example", "this one's real, learn from it", or "add this to my spam examples".
---

# capture-example

Main entry point. Turns one annoying email into a structured corpus entry plus durable defenses.

## Label it first

Apply `labels.example_pseudospam` (or `example_genuine` if the user says it is real) from `<data>/config.json` to the message. Then run `learn-from-labels` at the end if this is one of several new examples.

## Inputs (resolve interactively if missing)

- **Email reference** — one of:
  - a Gmail message id (preferred, when an email MCP like `gws-personal` / `gws-business` is available)
  - an absolute path to a `.eml` file the user already saved
  - the raw text the user pasted into the conversation
- **User rationale** — one to two sentences from the user: *what kind of spam is this, why it bothered them, what pattern it represents*. This is load-bearing — it becomes the `why_added` field and seeds the filter pattern.

If the user invoked the skill without a rationale, ask once: *"What kind of spam does this represent? (one sentence is fine — e.g. 'AI-faked personalised outreach asking for a backlink', 'unsolicited drip-cadence sales pitch', 'fake-friendly intro request from a scraped list')."*

## Resolve corpus path

Read `<data>/config.json` for `corpus_path`. If missing, run `setup` first.

## Steps

1. **Materialise the raw email**: if the input is a Gmail id, fetch via the available email MCP (`mcp__*__read_email` with `format: raw` or equivalent). If it's pasted text, write it as-is. Save to `<corpus>/inputs/emails/<YYYY-MM-DD>-<slug>.eml`. Slug = lowercased sender domain + short subject hash.

2. **Parse**: extract `From`, `Reply-To`, `Return-Path`, `Subject`, `Date`, `List-Unsubscribe`, plain-text body, HTML body.

3. **Run the email-analyst agent** (`agents/email-analyst.md`) on the saved file. It returns structured JSON: indicators, tracking pixels, confidence, and a `filter_instruction` snippet.

4. **Append to inventories** (all under `<corpus>/data/`):
   - `processed-emails.json` — full entry: filename, dates, sender, subject, body_plain, spam_confidence, spam_reasoning, why_added (the user's rationale), flags object (scraped_personalisation, asymmetric_ask, tracking_links, tracking_pixels, artificial_urgency, templated_structure, commercial_disguised_as_personal), trackers_found counts.
   - `sender-blocklist.json` — `{ email, domain, display_name, reason, date }`.
   - `tracking-domains.json` — for each pixel/click-tracker the analyst found.

5. **Suggest a filter pattern**: based on indicators, propose ONE concrete rule the user can paste into Gmail / Sieve / Fastmail filters. Examples:
   - `from:(*@<domain>) has:the-words "<scraped phrase>"` → label + skip inbox
   - `list:(<list-id>) → trash` when a List-Id header is the strongest signal
   - sender-domain block when the campaign is single-source
   Keep it minimal — over-broad filters cause false positives.

6. **Suggest system-prompt tuning**: emit a single bullet the user can paste into the system prompt of an AI email-triage agent. Format: *"If an email <observable signal>, treat as scraped-list outreach unless the sender has prior thread history."* Phrase as an additive heuristic, not a replacement for existing prompt.

7. **Offer optional actions** (ask before doing — these have side-effects):
   - **Server-side block via Gmail filter**: if a Google Workspace email MCP is available (look for `mcp__*__create_filter` or similar), offer to create a filter that auto-trashes/labels future mail from this sender. If the older `scripts/gmail-block-sender.py` is being used by the user instead of an MCP, surface it as a fallback path but recommend the MCP route.
   - **Draft a manual unsubscribe-request reply**: compose a brief, professional reply asking to be removed from the list and any other lists at the sender's organisation, threaded on the original message. Default tone: polite-firm. If the user signals frustration, allow a passive-aggressive variant (acceptable for genuine spam — never for marginal cases). Send via the email MCP only after the user confirms.

8. **Report** to the user, in this shape:
   - corpus entry filename
   - spam confidence + one-line reasoning
   - filter pattern suggestion (copy-pasteable)
   - system-prompt tuning bullet
   - what side-effects (block / reply) were performed vs offered

## Privacy

Raw `.eml` may contain personal data (recipient address, internal references, embedded recipient IDs in tracking links). Default to keeping the corpus local. If the user wants to share samples publicly (e.g. to seed a research dataset), redact via the existing `inputs/emails/sanitised/` convention before sharing — never copy raw originals into a public location.

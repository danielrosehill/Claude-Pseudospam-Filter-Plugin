---
name: draft-unsubscribe-reply
description: Draft (and optionally send) a manual unsubscribe-request reply to a spam sender — used when the email has no working List-Unsubscribe header or the user wants to make the request human-to-human. Threads on the original message via the available email MCP. Use when the user says "tell them to take me off the list" or "reply asking to be removed".
---

# draft-unsubscribe-reply

For when there's no unsubscribe link, or the link doesn't work, or the user wants a human reply on record.

## Inputs

- Original message id (preferred — enables threading) or sender email + subject.
- Workspace (which email MCP).
- Tone — default `polite-firm`. Allow `passive-aggressive` only when the user explicitly asks. Never `aggressive` or `rude`.
- Optional: detected pattern from `capture-example` (drives a brief, factual reason in the reply — "you are using AI-generated personalisation against a scraped list").

## Steps

1. Fetch the original message metadata (`From`, `To`, `Subject`, `Message-Id`, language) via the email MCP. If the original was in Hebrew, Arabic, or another language, reply in the same language and pass `rtl: true` to the send tool when applicable.

2. Compose the reply. Defaults:

   **polite-firm** (default):
   > Please remove me from this mailing list and confirm you have done so. Also remove any other addresses associated with my organisation. Do not contact me again.

   **passive-aggressive** (only on explicit request, only when the user is clearly being targeted by scraped-list outreach):
   > For the record: I'm in the field your pitch is targeting. So you're either spraying a scraped list, or your targeting is broken — either way, please remove me and any other addresses on my domain.

3. Set the subject to `Re: <original subject>`. Pass `threadId` and `inReplyTo` (with the original `Message-Id` wrapped in `<...>`) so the reply lands inside the original thread, not as a new conversation.

4. Show the draft to the user. Ask for confirmation before sending. Send via the email MCP.

5. Append to `<corpus>/data/unsubscribe-log.json` (create array if needed): `{ message_id, sender, subject, sent_at, tone, reply_body }`.

## Threading gotcha

If the email MCP creates a new thread despite `threadId`/`inReplyTo`, surface that as a known limitation to the user — Gmail threads on References + In-Reply-To + Subject; if any header is mangled, threading breaks. Don't claim success when the message landed as a separate conversation.

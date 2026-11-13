# The pseudospam standard

**Pseudospam** (pseudo-personalised outreach) is mail produced at scale and dressed
up as a personal note. It passes every infrastructure check (DKIM, SPF, reputation),
so classic spam filters let it through. Telling it apart takes judgement. This file
is that judgement, written down. It follows the public labelling spec of the
[Pseudo-Personalised-Spam-Classifier](https://github.com/danielrosehill/Pseudo-Personalised-Spam-Classifier)
(`docs/spec.md`). Your own boundary, learned from your example labels, lives in
`<data>/profile.md` and **overrides this file where they differ.**

## The question

> Did a real person put thought into contacting **this recipient**, about something
> of theirs, with an ask that follows from it?

| Label | Meaning |
|---|---|
| `genuine` | A person wrote it to the recipient specifically. It can be commercial, unwanted or AI-assisted: a vendor pitch can be genuine. |
| `pseudo_personalised` | Produced at scale. Includes templates with filled slots **and** LLM-researched hooks bolted onto a pitch that would be the same for anyone. |
| `out_of_scope` | Not outreach: subscribed newsletters, receipts, account/security notifications, release notes, calendar mail, conversations the recipient is already in. |

Wanting the mail is not part of the label. Whether it deserves time is `priority`.

## Specificity is not the test

The old swap test ("would it read naturally sent to someone else?") catches
templates. It does not catch LLM-researched outreach: a pipeline reads the
recipient's site or repos and writes an accurate, non-swappable paragraph, then
attaches a generic pitch. That is **pseudo_personalised**. The test is whether the
detail drives the ask, plus signs of a human in the loop.

## Signals (weak alone, weigh together)

Leaning **pseudo_personalised**:

| Tag | Pattern |
|---|---|
| `profile_summary` | Restates the public profile (About-page numbers, topic lists) without reacting to it |
| `ask_unrelated_to_hook` | Flattery about project X, then "join our beta" / "share our app" |
| `template_artifact` | Handle used as a first name; own name where a channel name belongs; title dropped in verbatim |
| `scraped_address` | Sent to an address that exists only on a third-party platform |
| `funnel_cta` | "Register here", "book a time" with sales-engagement tracking, "unlocked founder-tier access" |
| `campaign_followup` | "Following up on my note…", "one last time": restates the first message |
| `opt_out_line` | "Reply no and we won't write again", tokenised opt-out links |
| `commodity_ask` | Real, specific hook; the ask (paid backlink, guest post) is what every author gets |
| `data_as_flattery` | Auto-generated report or ranking about the recipient wrapped round a sign-up |
| `generic_hook` | Hook fits anyone in the field |
| `canned_install` | "Tell your coding agent to run this install command" |

Leaning **genuine**:

| Tag | Pattern |
|---|---|
| `engages_with_detail` | Compares with own work, asks a question that needs reading, criticises |
| `admits_limits` | Says where their product does *not* fit. Mass outreach never volunteers a mismatch |
| `proportionate_ask` | Small, specific: a comparison test, thoughts on one problem, a list inclusion, a call with no funnel |
| `idiosyncratic_voice` | Personal context serving no sales purpose; uneven formatting |
| `peer_builder` | Built something in the same niche; refers to shared technical problems |
| `responsible_disclosure` | Private security report with reproduction: always genuine |

**Not signals** (seen on both sides): plain text from a personal Gmail address;
selling something; AI-assisted prose.

**Which address it reached** matters: platform-only aliases (payments, film
database, podcast feed) attract harvested-list outreach; genuine mail tends to
reach the public contact address.

## Mail kind (separate axis)

`cold_outreach`, `support_or_report`, `product_drip` (onboarding, "founder note",
breakup/re-engagement from a product you signed up to; label it
pseudo_personalised), `mass_mailing` (conference/CFP blasts), `crackpot`.

## Hard cases → low confidence

- A credible individual promoting their own tool, offering "data for your
  article", sent again as a follow-up (pseudo); a single non-repeated one could go
  either way.
- "Let's trade notes" from a peer whose hook only restates the About page (pseudo);
  if it engaged with a specific project it would flip.

## Priority (1–10)

From `config.json → profile.priority_order`. Default: paid work that fits 9–10;
peer builders in your niches and real corrections 7–8; reasonable unpaid asks from
individuals 4–6; templated pitches, drips, mass mail, crackpot 1–2.

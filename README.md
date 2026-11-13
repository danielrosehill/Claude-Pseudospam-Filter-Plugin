# Pseudospam Filter

A Claude Code plugin that acts as a second spam filter for the mail your real one
lets through: **pseudospam**, outreach produced at scale and dressed up as a
personal note. It passes DKIM, SPF and reputation checks; often an LLM wrote it
after reading your website. Telling it apart takes judgement, so this plugin uses
Claude (parallel Haiku judges) plus **your own labelled examples** to classify it.
Caught mail goes to a review queue, not the bin.

The standard it applies is the public labelling spec of the
[Pseudo-Personalised-Spam-Classifier](https://github.com/danielrosehill/Pseudo-Personalised-Spam-Classifier).

## How it works

1. **You label a few examples** in Gmail (`Pseudospam/Examples/Pseudospam`,
   `.../Genuine`, `.../Unsure`, or your own existing labels).
2. **`learn-from-labels`** turns them into few-shot examples and a short
   profile of where *your* line sits.
3. **`sweep`** finds unsolicited one-to-one-looking mail, has Haiku judges classify
   it in parallel, and labels the result: `Pseudospam/Caught` (archived),
   `Pseudospam/Passed` (genuine, stays) or `Pseudospam/Unsure` (stays).
4. **`review-caught`** rescues mistakes and feeds them back as examples.
5. **`prioritise-genuine`** turns the genuine mail into a reply queue.

## Skills

| Skill | Purpose |
|---|---|
| `setup` | Data dir, config (account, labels, thresholds, your profile), label tree, corpus |
| `manage-labels` | Create, explain, rename or remap the example and result labels |
| `learn-from-labels` | Learn your boundary from example labels → `examples.jsonl` + `profile.md` |
| `sweep` | Find candidates, judge in parallel (Haiku), label Caught / Passed / Unsure |
| `review-caught` | Review the queue, rescue mistakes, turn corrections into examples |
| `prioritise-genuine` | Rank genuine mail by your priorities into a reply queue |
| `capture-example` | Label one email as an example, save it, suggest a filter, optional block/unsubscribe |
| `analyse-email` / `bulk-analyse` | Forensic analysis: intent, tracking pixels, report |
| `block-sender` | Server-side Gmail filter for a sender |
| `draft-unsubscribe-reply` | Human-to-human removal request when there's no working unsubscribe |
| `scan-tracking-pixels` / `scan-recent-pixels` / `tracking-report` | Tracking-pixel detection and inventory |
| `export-dns-blocklist` / `adguard-configure` / `adguard-push` / `contribute-blocklist` | Turn tracker domains into DNS blocks (Pi-hole, AdGuard Home) and public list contributions |

Agents: `pseudospam-judge` (Haiku, batch classifier), `email-analyst` (forensics).
Bundled: a minimal AdGuard Home MCP in `mcp/adguard-home/`.

## Requirements

A Gmail MCP that can search, read message bodies, list/create labels and
batch-modify message labels (e.g. the Google Workspace MCP). Headers such as
`List-Unsubscribe` improve candidate filtering but aren't required.

## Data and privacy

All personal data lives in one per-user directory (`references/paths.md`), never in
the plugin. Mail content, verdicts and examples stay local. `contribute-blocklist`
exports domain-level data only.

## History

Replaces the earlier `spamhole` plugin (retired 2026-10-21); its skills are
included here under the names above.

---
name: setup
description: First-run setup for Pseudospam Filter. Resolves the data directory, writes config.json (account, label names, thresholds, a short recipient profile), creates the Gmail label tree, and scaffolds the sample/tracking corpus. Use when the plugin is first used, or to change the account, labels or corpus location.
---

# setup

1. **Data dir.** Resolve `<data>` per `references/paths.md`. Say which rule fired.
2. **Config.** If `<data>/config.json` is missing, start from
   `references/config.example.json`. Fill `account` and `profile` by asking the user
   (or reading what they already said): who they are, which addresses are public
   contact vs platform-only aliases, their niches, their priority order. Keep it short.
   Existing labels can be reused: if the user already labels examples somewhere,
   point `labels.example_*` at those names instead of creating new ones.
3. **Labels.** Run `manage-labels` → `create`.
4. **Corpus.** Scaffold `<data>/corpus/` as below (used by capture, analysis and
   tracking skills).

## Corpus layout

Resolve in this order:

1. If the user passed a path argument, use it.
2. If `<data>/config.json` exists and has `corpus_path`, use that.
3. Otherwise default to `<data>/corpus/`.

If the user wants the corpus inside a private GitHub repo (recommended — raw `.eml` may contain personal data), ask for the repo path and use that. Make sure the corpus directory is gitignored or that the user understands the privacy trade-off.

## Steps

1. Confirm the resolved path with the user. Create it if it doesn't exist.

2. Build the layout:

   ```
   <corpus>/
   ├── inputs/
   │   └── emails/
   │       └── sanitised/        # Redacted samples safe to share
   ├── data/
   │   ├── tracking-domains.json # array — pixel + click-tracker hosts
   │   ├── ad-trackers.json      # array — adsense / DSP / analytics pixel hosts
   │   ├── sender-blocklist.json # array — blocked senders
   │   └── processed-emails.json # array — analysis log
   ├── outputs/
   │   └── analyses/             # per-email markdown reports
   └── exports/                  # generated DNS blocklists, filter rules, etc.
   ```

3. Initialize each JSON file as an empty array `[]` if it doesn't exist. Never overwrite an existing inventory.

4. Write `<corpus>/README.md` summarising what's in each directory and reminding the user this is their personal corpus.

5. Persist the resolved path to `<data>/config.json` so other skills can find it without re-prompting:

   ```json
   { "corpus_path": "/abs/path/to/corpus" }
   ```

6. Suggest (do not require) committing the corpus to a private repo for backup, and offer to add a `.gitignore` that excludes raw `.eml` while tracking the JSON inventories and sanitised samples.

7. Report: corpus path, what was created vs already existed, suggested next step (`capture-example`).

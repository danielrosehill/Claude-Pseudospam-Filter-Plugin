# Where data lives (`<data>`)

Every skill writes under one per-user directory, referred to as `<data>`:

1. `$PSEUDOSPAM_FILTER_DATA` if set.
2. `$CLAUDE_USER_DATA/pseudospam-filter` if `$CLAUDE_USER_DATA` is set.
3. The first that already exists: `~/.claude-user-data/pseudospam-filter`, then
   `${XDG_DATA_HOME:-~/.local/share}/claude-plugins/pseudospam-filter`. Adopt an
   existing root rather than creating a second one.
4. Otherwise `~/.claude-user-data/pseudospam-filter`.

Never under `~/.claude`. Layout:

```
<data>/
├── config.json          # account, labels, thresholds, recipient profile (see config.example.json)
├── profile.md           # your boundary, distilled from your example labels (learn-from-labels)
├── examples.jsonl       # few-shot examples drawn from your example labels
├── sweeps/<YYYY-MM-DD>/ # candidates.jsonl, verdicts/*.jsonl, report.md
└── corpus/              # samples, tracking inventories, exports (setup)
```

Everything here is personal mail content. Keep it local or in a private repo.

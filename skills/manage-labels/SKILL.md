---
name: manage-labels
description: Create, explain, rename or remap the Gmail labels Pseudospam Filter works with. Example labels teach Claude what you consider pseudospam; result labels mark what a sweep processed. Use when the user says "set up the pseudospam labels", "what do the labels mean", "use my existing labels for examples", "rename the pseudospam labels", or before the first sweep.
---

# Pseudospam labels

Two families, names from `<data>/config.json → labels`:

| Key | Default | Who applies it | Meaning |
|---|---|---|---|
| `example_pseudospam` | `Pseudospam/Examples/Pseudospam` | **you** | "This is the kind of thing I mean." Teaching data |
| `example_genuine` | `Pseudospam/Examples/Genuine` | **you** | "A person really wrote this to me." Teaching data |
| `example_unsure` | `Pseudospam/Examples/Unsure` | **you** | Borderline; tells Claude where the line is fuzzy |
| `caught` | `Pseudospam/Caught` | sweep | Judged pseudospam; archived (or binned if `on_caught: bin`). **The review queue** |
| `passed` | `Pseudospam/Passed` | sweep | Judged genuine; left in the inbox. Marks it processed |
| `unsure` | `Pseudospam/Unsure` | sweep | Low confidence; left in the inbox for you |
| `blocked` | `Pseudospam/Blocked` | block-sender | Sender blocked by filter |

Example labels are what Claude learns from (`learn-from-labels`). Result labels
mean a sweep never processes the same message twice, and a mistake is one label
view away.

## Operations

Use the account's Gmail MCP label tools (list / create / update / delete).

- **create**: list labels; create each missing name from config, parents first
  (`Pseudospam`, then `Pseudospam/Examples`, ...). Never create a duplicate under a
  different case.
- **remap**: user already has example labels (e.g. `Training Labels/Genuine`)? Set
  `labels.example_*` in config to those names; create nothing.
- **rename**: update config first, then rename the Gmail label by id (ids survive
  renames; filters keep working). Rename child labels too: the API doesn't
  cascade like the Gmail UI does.
- **explain**: print the table above with the configured names and the current
  message count per label (search `label:<name>` with every non-alphanumeric
  character replaced by `-`, lowercase; the quoted form can silently return nothing).

Never delete a label that holds messages without saying how many.

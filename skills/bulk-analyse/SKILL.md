---
name: bulk-analyse
description: Process every unanalysed .eml file in the user's corpus inputs/emails/ directory through the full analyse-email pipeline. Skips files that already have a corresponding analysis report. Use when the user has dropped many .eml files into the corpus at once.
---

# bulk-analyse

Drain queue. Runs `analyse-email` on every `.eml` in the corpus that doesn't already have a report.

## Resolve corpus path

Standard resolver.

## Steps

1. List `<corpus>/inputs/emails/*.eml` (skip the `sanitised/` subdirectory).

2. For each file, check `<corpus>/outputs/analyses/<basename>-analysis.md`. If it exists, skip.

3. For each unanalysed file, run the same pipeline as `analyse-email/SKILL.md` — don't re-implement, refer to that skill.

4. Print a summary table:
   - Number processed, number skipped (already analysed)
   - Total tracking pixels detected across the batch
   - Net new senders added to the blocklist
   - Top 5 indicator types observed

## Performance

If the batch is > 30 files, prompt the user once: "This will run the analyst agent N times. Continue?". Otherwise just run.

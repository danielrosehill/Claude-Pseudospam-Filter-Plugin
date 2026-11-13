---
name: review-caught
description: Review what Pseudospam Filter caught, rescue mistakes and turn them into teaching examples. Lists the Caught (and Unsure) labels with the judge's one-line reasons; for anything the user says was wrongly caught, moves it back to the inbox and labels it as a genuine example (and vice versa), then relearns. Use when the user says "review the pseudospam", "what did it catch", "that one was real", "check the caught folder", or periodically before emptying it.
---

# Review caught mail

1. List `labels.caught` (newest first), joined with the verdicts in
   `<data>/sweeps/*/verdicts/` by id: sender, subject, summary, confidence. Show
   lowest confidence first: that's where mistakes are.
2. Also list `labels.unsure`. Each needs a call from the user.
3. Apply the user's calls:
   - **Wrongly caught** (actually genuine): remove `caught`, add INBOX and `passed`,
     add `example_genuine`.
   - **Unsure → pseudospam**: remove `unsure`, add `caught` (+ archive), add
     `example_pseudospam`.
   - **Unsure → genuine**: remove `unsure`, add `passed`, add `example_genuine`.
   - **Confirmed caught, delete**: bin them (or the user empties the label view
     themselves). Optionally add a few clear ones to `example_pseudospam`.
4. If any examples were added, run `learn-from-labels`. Mistakes are the
   highest-value examples.

Report: rescued N, confirmed M, new examples K, and whether the profile changed.

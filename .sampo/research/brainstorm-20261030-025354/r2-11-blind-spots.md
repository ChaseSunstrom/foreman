# Brainstorm — lens: blind spots

**Questions left earlier, answered through the blind-spots lens**
- *Dry queue vs finished project:* the only signal that separates them is a clean verdict with coverage, meaning every finder ran and each caught its planted canary. A gap map alone can't tell them apart.
- *Who audits hidden keys:* the key must fail against a known-good reference solution before an exam scores anything.

**The class the missed asks share:** T-2093 to T-2113 are all the autonomous layer's own meta-needs: validate its files, resume after a kill, offer itself, seal its charter, exam itself, publish itself. The question to have asked was *"what must the self-directing layer be able to check, resume, offer, guard, score and show about itself?"* Applied to Initiative, the finders and the find→prove→fix pipeline need all six, and the earlier lists cover only part of that.

- **Audit every exam key against a reference solution** — FIX — value 5 — effort M — risk low — category: exam integrity
  Why: the pack asks who audits hidden keys, and a wrong key rejects good finders. Mission 3 is graded on `none` and `bug` kinds, so a wrong `none` key (a "clean" repo that has a real bug) is the likeliest failure.
  Done when: `fm exam keycheck` fails on a seeded wrong key, passes on a correct one, and runs before any arm is scored.

- **Join finding kinds to 30-day survival and mute kinds that predict nothing** — FEATURE — value 5 — effort M — risk low — category: calibration
  Why: the pack asks whether exam deltas correlate with `fm outcomes`. The standing steer says weakness-finding comes from outside signals.
  Done when: `fm find calibrate` prints a per-kind table of exam score against survival, and kinds below a set correlation are flagged "measuring nothing".

- **Register "after X, always Y" triggers for the find pipeline** — FEATURE — value 4 — effort M — risk med — category: automation
  Why: the pack asks which repeated follow-ups (re-ship, re-record, re-match) have no trigger. Examples for finders: a probe edit triggers its exam, and a proven fix triggers a re-export of the findings page.
  Done when: a `triggers` file with two rules fires on a probe edit and a lane close, each logged once.

- **Watch attached outside documents by hash and queue a drift task** — FEATURE — value 4 — effort S — risk low — category: sync
  Why: the pack asks who owns syncing the attached SEED_PROMPT.md. Gen-0 sealing covers only the charter, not other attachments.
  Done when: editing a registered attachment makes `fm doctor` report "attachment changed since last read", with a filed task.

- **Print a cost-per-finding ledger with an afford-check before any scan** — FEATURE — value 4 — effort M — risk low — category: cost
  Why: the pack asks what a generation costs end to end. Plain Claude costs about $0.17 per fix, so Foreman needs the same number per proven finding to be comparable.
  Done when: `fm find cost` shows dollars per proven finding by kind, and a scan refuses to start when the projected cost exceeds the remaining budget.

- **Show the scan proposal with cost, scope, a "no" path and a "never here" option** — FEATURE — value 4 — effort S — risk low — category: consent
  Why: the pack asks whether a user who has never typed `fm genesis` understands an auto-start proposal. A scan on a stranger's repo has the same gap.
  Done when: the proposal text includes estimated dollars, files read, and a one-key permanent decline, and a cold-reader test passes.

- **Publish a live findings page with each proof, verdict and fate** — FEATURE — value 3 — effort M — risk low — category: site
  Why: the user asked for the genesis tower on the site, then asked it to match the site and stay live. A findings view is the likely next ask.
  Done when: `fm find export` writes a page listing each finding's failing test, status and survival, and it follows the standing debounced ship.

- **Merge probes that win disjoint scenarios into one ensemble, then rerun the exam** — FEATURE — value 3 — effort M — risk med — category: selection
  Why: the pack asks whether selection should merge rewrites that win on disjoint sets.
  Done when: two probes with disjoint wins are combined, and the ensemble is kept only if it beats both on held-out scenarios.

- **Wild: Plant a canary bug in a scratch copy before declaring any repo "clean"** — FEATURE — value 4 — effort M — risk med — category: trust
  Why: wild; "none" is only believable if the finders can find a known defect in the same stack.
  Done when: a clean verdict cites "canary found in 1 of 1" and withholds the verdict when the canary is missed.

- **Wild: Give the finders a morning "second opinion" from a cold model who sees only the test** — FEATURE — value 3 — effort M — risk low — category: review
  Why: wild; the user already steers toward second cold reviews. A reader who sees only the failing test and must restate the bug tests whether the proof is legible.
  Done when: a finding whose cold restatement diverges from its claim is held back from the morning card.

- **Wild: A charter for each finder, sealed, with a diff-of-privilege report** — SECURITY — value 3 — effort S — risk low — category: guard
  Why: wild; brief 8 sealed gen-0 and diffed privileges. Probes that can edit themselves need the same, and "scout may write" is the privilege to watch.
  Done when: a probe edit that adds a write or network capability fails `fm find sweep` until acknowledged.

- **Detect a kill mid-pipeline and resume at the exact stage** — FIX — value 3 — effort S — risk low — category: resilience
  Why: T-2095 resumability was asked for genesis only. The find→prove→fix chain has more stages to lose, such as a half-written test or a lane with no proof.
  Done when: killing between prove and fix, then rerunning `fm find step`, continues at fix without refiling the finding.

**Next question:** Which of the self-checks (key audit, canary, cold restatement, survival join) is itself unscored, and what outside signal would catch it being wrong?
**Next question:** What does the user ask for after a finding lands (revert, explain, widen to siblings, publish), and which of those has no verb yet?

# Brainstorm — lens: inversion: how initiative fails or harms — false alarms, noisy captures, fixes nobody wanted, a finder that edits code it shouldn't, scope creep into user projects

- **Make finders read-only by construction** — SECURITY — value 5 — effort M — risk low — category: safety
  Why: the exam shows finders have no proof step today, and `probe_doctor` already queues Foreman's own setup failures in user projects. A finder that can write is a finder that can harm. Assumption: finders currently run with the same permissions as lanes.
  Done when: a test runs every finder against a fixture repo and `git status --porcelain` plus a hash of the tree are identical before and after; a finder that tries to write is denied and journaled.

- **Require a failing proof before any finding is shown** — FEATURE — value 5 — effort M — risk med — category: precision
  Why: the 0/108 exam result and the "proves each finding with a failing test" mandate. A finding with no reproduction is a rumour, and rumours are the false-alarm source.
  Done when: `fm find` output lists only findings with a proof command that exits non-zero; unproven candidates go to a separate "suspects" file, counted but never queued.

- **Score the finders on the exam's `none` kind first** — FIX — value 5 — effort S — risk low — category: false positives
  Why: Mission 3 is graded on `none` and `bug` in never-seen repos. A finder that cries wolf on clean repos fails the `none` kind outright. Assumption: `none` means repos with no planted defect.
  Done when: `fm exam` reports a false-positive rate per finder on `none` repos, and a finder above a set rate (say 0.1 findings per repo) cannot be enabled.

- **Cap captures per project per week, and rank before capping** — FEATURE — value 4 — effort S — risk low — category: noise
  Why: `MAX_CAPTURES` exists in fmscout, but the cap is per scout run, not per week. Nightly runs can still bury the queue. Assumption: night jobs run scout repeatedly.
  Done when: a test runs scout 7 nights in a row on one fixture and the open initiative tasks never exceed the weekly cap, the highest-value ones surviving.

- **Remember rejected findings by fingerprint** — FEATURE — value 4 — effort M — risk low — category: noise
  Why: the user has already asked for "mark a finding settled so later sweeps stop re-filing it" in the prior ideas, and `fm adopt` is one-shot with no memory of declines. Here the fingerprint is the file, the rule and a normalised code snippet, so a line-number shift doesn't resurrect it.
  Done when: after the user drops a finding, the same finding after an unrelated edit above it in the file isn't re-queued; a changed snippet is.

- **Fence fixes to the finding's blast radius** — SECURITY — value 4 — effort M — risk med — category: scope
  Why: scope creep into user projects is the central harm. A lane fixing one bug should not reformat or touch files the proof doesn't implicate. Assumption: lanes can currently edit anywhere in the worktree.
  Done when: a lane that touches a file outside the finding's declared set plus its test is stopped, with the stray hunk listed; a fixture task that tries a drive-by rename fails the gate.

- **Mark the fix as unwanted when the user reverts it** — FEATURE — value 4 — effort M — risk low — category: feedback
  Why: `fm outcomes` tracks 30-day survival already. A revert or deletion of an initiative fix is the clearest "nobody wanted this" signal, and it should lower the finder's rank, not sit in a report.
  Done when: reverting an initiative commit lowers that finder's weight in the next ranking, and a test shows a finder with three reverts drops below the queue threshold.

- **Quarantine a project's first scout run as a dry report** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: the pack's open question on what a user does when an auto-start proposal appears. A first run that files tasks into an unfamiliar backlog is a surprise; a one-page report with a "yes, file these" key is not.
  Done when: the first scout in a project writes `findings-preview.md` and queues nothing until `fm scout accept` is run; later runs follow the user's stored choice.

- **Refuse to scout what the user doesn't own** — SECURITY — value 3 — effort S — risk low — category: authorization
  Why: initiative runs in "any project", including vendored directories, submodules and third-party clones. Findings and fixes there are pure noise or worse. Assumption: scout doesn't currently skip `vendor/`, `node_modules/`, submodules.
  Done when: a fixture with vendored code and a submodule gets zero findings from them, and the skip list is shown in `fm scout --explain`.

- **Cost-stop a finder that spends more than it earns** — PERFORMANCE — value 4 — effort M — risk low — category: spend
  Why: plain Claude finds and fixes at about 0.17 USD each, and Foreman costs more for the same score. A finder with no accepted findings after N runs should switch itself off.
  Done when: a finder with N runs, $X spent and 0 accepted findings is disabled and says so in `fm doctor`; re-enabling takes an explicit command.

- **Wild: run every finder against a planted-clean twin of the repo** — FEATURE — value 4 — effort L — risk med — category: calibration
  Why: wild; assumption: a mutation harness can copy a repo and inject a known bug. Finders that report a bug in the clean copy, or miss the injected one, are measured against the project's own code rather than only the exam.
  Done when: for a fixture repo, the harness injects a bug, the finder reports it in the mutant and nothing in the original, and both rates are recorded per finder.

- **Wild: a finder's confession before filing** — FEATURE — value 3 — effort S — risk low — category: honesty
  Why: wild; a finding states in one line what would make it wrong ("fails only if input is empty and the caller guards it"). A cheap second model attacks that line before the finding is shown.
  Done when: every queued finding carries a "wrong if" line, and a test shows a finding whose line the attacker confirms is demoted to a suspect.

- **Wild: a "do nothing" receipt** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: wild; a scout that finds nothing says so with its coverage ("looked at 212 files, ran 4 probes, 0 findings") instead of staying silent, so a quiet repo reads as checked, not skipped.
  Done when: a scout on a clean fixture prints a coverage line and files no tasks, and the `none` exam kind scores it as correct.

- **Wild: a veto word that kills a whole class of finding forever** — FEATURE — value 3 — effort M — risk low — category: control
  Why: wild; one phrase like "never flag style in tests/" becomes a stored rule previewed against past findings, so the user can shut a noisy class off in one sentence.
  Done when: after the user states a veto, a rerun of scout on the same fixture drops every finding matching it, and the preview lists what would have been dropped.

Next question: What fraction of past initiative-style findings (`fm adopt` briefs, scout captures) did the user close, drop or ignore, and which finder produced the ignored ones?
Next question: Which projects does the user run Foreman in that they don't want touched at all, and how is that stated today?

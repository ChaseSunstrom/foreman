# Brainstorm — lens: observability and trust

- **Diff every "done" against what the gates actually exercised** — FEATURE — value 5 — effort L — risk med — category: trust
  Why: existing ideas cover measuring evidence coverage and tree-binding separately. Assumption: nothing joins them into one per-task "claim map" that links each brief sentence to the lines changed, the evidence that ran those lines, and the lines no evidence touched. The `fm why` and `fm tour` commands already know the diff and the brief.
  Done when: `fm task done` prints a claim map, and a seeded task with one changed function that no test runs is flagged as "unexercised" in that map.

- **Run a trust-regression suite on Foreman's own observers** — FEATURE — value 5 — effort M — risk low — category: observability
  Why: Foreman relies on `fm doctor`, `fm sentinel`, `fm replay` and the statusline to tell the user it is healthy, but nothing in the pack checks that those observers still report failure when something is broken. Assumption: they have been tested only on the success path. The recent T-0424 slow-gate signal fix suggests signals do drift.
  Done when: a suite injects ten known faults (a dead hook, a stale STATE, a corrupted ledger line, a missing guard) and `fm doctor` flags every one, in CI.

- **Show a hook-coverage heartbeat per session** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: the user's JARVIS sessions hit silent failures (the band stuck on step 1/5, a drive idling with 20+ queued). Assumption: no live record exists of which hooks fired in a session and which were expected. Each hook writes a beat, and a missing one past its expected interval raises a visible alert.
  Done when: killing the PostToolUse hook in a test session produces a "hook silent" line in the statusline within one minute.

- **Explain every state change with a causal trace** — FEATURE — value 4 — effort M — risk low — category: provenance
  Why: user complaints are "why is the band stuck", "why did it refuse", "why did it idle". Guard decisions and drive offers are logged, but there is no per-field "who last wrote this value, from which event". Assumption: `fm why` covers code, not Foreman state.
  Done when: `fm explain step` on a task prints the ledger events and hook that last set the current step, and it answers the stuck-band case from the issue.

- **Score the guard's decisions against later outcomes** — FEATURE — value 4 — effort M — risk low — category: guard
  Why: the user kept reporting false positives from JARVIS (symlink rm, `fm focus; sed`). Assumption: refusals that were later overridden, rewritten or re-run by hand are visible in the ledger but are not turned into a rate per rule. Each rule gets a measured false-positive and bypass rate, and a high rate raises a task.
  Done when: `fm guard stats` lists each rule with its refusal count and its "user then did it anyway" count, drawn from the last 30 days of ledger data.

- **Diff what was injected into context against what was used** — FEATURE — value 3 — effort M — risk low — category: context
  Why: `fm usage` shows skills and commands used. Assumption: nothing records which injected lessons, vetoes and rules the model referenced in its work, so dead context cannot be told from load-bearing context.
  Done when: a report lists injected items for the last 20 tasks with a referenced/unreferenced mark, and one unreferenced item is shown as a removal candidate.

- **Publish a verifiable run record for outside review** — FEATURE — value 4 — effort L — risk med — category: trust
  Why: `fm pr` already writes proof into PR text. Assumption: a reviewer who doesn't run Foreman has to take the text on faith. A bundle of the brief, the evidence outputs, the tree hash and a one-command replay script lets anyone re-run the evidence.
  Done when: `fm pr --bundle` produces an archive, and running its script in a clean checkout re-executes the recorded verifies and reports matching results.

- **Detect the observer being blind: silent-failure canaries** — FEATURE — value 4 — effort S — risk low — category: observability
  Why: hooks can fail open. Assumption: a hook crash today is invisible to the user. A canary command with a known expected refusal runs at SessionStart, and if the guard doesn't refuse it, the session opens with a visible warning.
  Done when: disabling the guard in a test config makes the next SessionStart print "guard not enforcing", and the normal path stays silent.

- **Wild: Keep a witness session that re-derives STATE from raw transcripts** — FEATURE — value 4 — effort L — risk med — category: trust
  Why: wild. STATE, briefs and the ledger are written by Foreman itself, so errors in them are self-confirming. An independent job rebuilds "what happened" from the Claude transcripts alone and diffs it against Foreman's own account, which catches claimed-but-not-done work.
  Done when: for a seeded task where a step was ticked without any matching tool call, the witness report lists that mismatch.

- **Wild: Give each task a "confidence weather" forecast on the band** — FEATURE — value 3 — effort M — risk low — category: UI trust
  Why: wild. Combine signals Foreman already has (retries, surprises logged, gate flakiness, vacuous-verify warnings, review verdicts) into one calibrated clear/cloudy/storm reading that the user can glance at before accepting a merge.
  Done when: the band shows a weather reading, and over the last 50 finished tasks the "storm" readings contain a higher share of later-reopened tasks than the "clear" readings.

- **Wild: Let the user ask "show me the least-verified thing you shipped this week"** — FEATURE — value 4 — effort M — risk low — category: trust
  Why: wild. The user's "check the product the way its user uses it" shows distrust of green gates. A weekly self-audit ranks shipped tasks by thinness of evidence (low coverage, reused passes, no product check) and presents the worst three for a second look.
  Done when: `fm digest --weakest` lists three tasks with a stated reason each, and picking one opens a follow-up task.

- **Alert on drift between installed Foreman and the repo's HEAD per project** — FIX — value 3 — effort S — risk low — category: observability
  Why: the user ships releases to "GitHub main and JARVIS" by hand every time, and T-0418 (an outdated foreman-ui) is blocked. Assumption: a project can run an old guard without anyone noticing. The statusline warns when the installed version is behind the version the project last passed gates on.
  Done when: installing 1.2.15 in a test project while main is 1.2.16 shows a "behind" marker, and `fm doctor` names the project.

- **Record a tamper-visible "who acted" tag on every ledger event** — SECURITY — value 3 — effort S — risk low — category: provenance
  Why: lanes, child runs, reviewers and the user's own edits all write to one central place. Assumption: events don't reliably say whether the main thread, a builder lane, a headless run or a human made them. This tag is what makes the causal trace and the witness checks reliable.
  Done when: every new ledger event has an actor field, and `fm log --actor lane` filters on it in a test.

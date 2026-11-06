# Brainstorm — lens: inversion: how initiative fails or harms — false alarms, noisy captures, fixes nobody wanted, a finder that edits code it shouldn't, scope creep into user projects

- **Land proof and fix as one commit or not at all** — FIX — value 5 — effort S — risk low — category: safety
  Why: a red proof test left on the user's branch breaks their CI if a lane dies midway; the pack says proof comes before the fix, but not what happens on a kill.
  Done when: a test kills the lane between proof and fix, and `git log` and `git status` on the user's branches show neither the test nor a partial fix.

- **Vet the repo's test command before the first proof** — SECURITY — value 5 — effort M — risk med — category: safety
  Why: assumption: proofs run whatever `make test` or `npm test` does, and in a foreign repo that can deploy, publish, `curl | sh` or `rm -rf`. The exam uses never-seen repos.
  Done when: a fixture whose `test` target runs `rm -rf ./data` or `curl` is refused with a named reason, and a plain `pytest` repo passes through.

- **Wrap every probe in a tree-diff tripwire** — SECURITY — value 5 — effort M — risk low — category: safety
  Why: a finder that "only reads" can still write when it runs tests, so hash the tree, untracked files and `~/.config` before and after each probe. Any change outside the lane's temp directory fails the probe, mutes it and logs an incident.
  Done when: a probe that touches a sentinel file is muted, and the incident appears in `fm find` output.

- **Forbid initiative from pushing, opening PRs or commenting** — SECURITY — value 5 — effort S — risk low — category: egress
  Why: unasked work that goes outward can't be taken back, and the pack requires confirmation for outward actions. Today only the guard's general rules stand between a lane and `git push`.
  Done when: a test runs an initiative lane that attempts `git push`, `gh pr create` and `gh issue comment`, and all three are denied with a journal line.

- **Give findings their own shelf, not the T- backlog** — CLEAN — value 4 — effort S — risk low — category: noise
  Why: the open work list already has 40+ deferred items, so unasked findings under T- ids would bury what the user asked for and consume ids and ranking attention.
  Done when: `fm run` never picks an F- id, and promoting a finding to a T- task is an explicit verb.

- **Treat silence as a vote and let unread findings evaporate** — FEATURE — value 4 — effort M — risk low — category: noise
  Why: the existing ideas react to drops. Ignored findings are the common case, so a finding unread for 14 days expires, and five ignored in a row halves the scan cadence for that project.
  Done when: a simulated clock advances 14 days and the finding is gone from the digest with an expiry line, and the next scan interval doubles after five ignored.

- **Check for deliberate behaviour before filing a bug** — FEATURE — value 4 — effort M — risk med — category: false alarms
  Why: the exam's `none` kind exists because "intended" code looks like a bug. Search comments, docs, tests and commit messages for "on purpose" or "by design" signals, and downgrade to report-only when found.
  Done when: a fixture with a documented quirk is not filed, and an undocumented twin of the same code is.

- **Stop findings from filing findings** — FIX — value 4 — effort S — risk low — category: scope creep
  Why: assumption: a fix lane that sees a sibling problem will file it, and that snowballs. A lane may name related problems as one receipt line, but only a human or the next scheduled scan promotes them.
  Done when: a lane that notices a second bug leaves the finding count unchanged and the receipt carries one "also saw" line.

- **Run an autonomy ladder per project that demotes on harm** — FEATURE — value 5 — effort M — risk med — category: trust
  Why: every project starts at report-only, then earns proof-only, then lane fixes through accepted findings. One revert, drop or tripwire incident drops it one rung automatically.
  Done when: a scripted sequence of accepts promotes a fixture project one rung, and a revert demotes it one rung with a journal line.

- **Hunt only where the user is alive** — FEATURE — value 3 — effort S — risk low — category: scope
  Why: assumption: bugs in dormant repos, other people's branches or forked upstream code are unwanted. Skip repos with no commits in 30 days and branches the user's git identity didn't author, and write upstream-file fixes as a patch file instead of an edit.
  Done when: a stale-repo fixture returns "dormant, skipped" and a forked-file finding produces a `.patch` with no tree edit.

- **Label every initiative artifact so one purge removes all of it** — CLEAN — value 3 — effort S — risk low — category: reversibility
  Why: branches, worktrees, proof tests and shelf entries scattered across a user's project are hard to remove by hand.
  Done when: `fm find purge` lists then removes every labelled artifact in a fixture and leaves unlabelled files byte-identical.

- **Wild: keep an apology ledger with a penance clock** — FEATURE — value 3 — effort M — risk low — category: accountability
  Why: assumption: harm only counts if it's priced. Each false alarm, revert or touched-outside-scope event is a one-line apology with its cost in minutes and dollars. Net value is shown value minus damage, and initiative pauses for as many hours as the incident cost minutes.
  Done when: a fixture revert writes a ledger line and the scheduler refuses new initiative for the computed window.

- **Wild: forecast whether the user would have asked** — FEATURE — value 4 — effort M — risk med — category: wanted-ness
  Why: before work starts, score each finding's similarity to the user's accepted asks versus dropped ones (the pack shows they ask for features, docs and surface sync far more than bug sweeps). Compare the forecast with the actual accept or drop and recalibrate.
  Done when: a forecast file exists before each lane opens, and a calibration line shows the forecast against the outcome.

- **Wild: ship a hostile repo corpus as a release gate** — SECURITY — value 4 — effort M — risk low — category: red team
  Why: the exam grades on never-seen repos, so rehearse on repos whose README, comments and test names bait the finder to edit outside scope, run destructive scripts or file nonsense.
  Done when: the release gate runs five hostile fixtures, and any out-of-scope write or filed bait finding fails it.

- **Wild: add a "would a stranger approve this?" cold read of the diff** — FEATURE — value 3 — effort S — risk med — category: fixes nobody wanted
  Why: a cold model sees only the diff and one sentence of the finding, not the lane's reasoning. If it can't say why the change is wanted, the lane drops to report-only.
  Done when: a diff that only reformats unrelated lines is downgraded, and a real bug fix passes.

Next question: What is the user's cost of a false alarm in attention-minutes compared with a missed bug, and does the ranking formula use that exchange rate?
Next question: Which initiative actions are irreversible on a user's machine even with labelled artifacts, such as test-run side effects, and who audits that list?

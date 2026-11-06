# Brainstorm — lens: unspoken needs

- **Locate the cause mechanically on FIX tasks** — FEATURE — value 4 — effort M — risk low — category: debugging
  Why: `fm task prove` already produces a red test on the start tree, which is the oracle `git bisect run` needs. Nothing in the pile bisects. Assumption: many FIX requests are regressions with a known-good older commit.
  Done when: on a fixture repo with a seeded regression 12 commits back, `fm task start` on a FIX names the first bad commit using only the red test, with no model call.

- **Shrink the failing input before planning** — FEATURE — value 4 — effort M — risk med — category: debugging
  Why: assumption: FIX requests arrive as big logs or inputs ("login times out on slow wifi"). A minimised repro makes a better red test and a smaller brief. The pile has debuggers and prove, but no delta-debugging step.
  Done when: given a 500-line failing input fixture, `fm repro min` yields a smaller input that still fails the same test, and the brief cites it.

- **Mutation-check the diff's own tests** — FEATURE — value 4 — effort M — risk med — category: evidence
  Why: prove shows the tests fail before the fix. It doesn't show they would catch a wrong fix. The pile has "verify ran nothing" detection and a failing-twin probe, but not diff-line mutation. This is the hardest-to-fake evidence upgrade.
  Done when: finishing a task with evidence mutates up to N changed lines (flip a comparison, drop a call), runs the linked tests, and records the surviving mutants. A task whose tests pass against every mutant gets a close warning.

- **Let the user retype a task to teach the classifier** — FEATURE — value 3 — effort S — risk low — category: intake
  Why: T-0035 (eval capture) is deferred and the classifier is the first thing the user meets. The pile has confidence scores but no correction channel.
  Done when: `fm task retype T-x FIX` changes the type, appends a redacted case to the eval corpus, and the eval run includes that case.

- **Run tasks that span repos as linked children** — FEATURE — value 4 — effort L — risk med — category: orchestration
  Why: the ledger is central across projects, but a request like "change the lib and update the app" is one task bound to one repo. The pile covers rebinding scope on a directory change, not cross-repo ordering. Assumption: the user has several related repos.
  Done when: a task naming two repos creates child tasks, one per repo, ordered. The consumer's gate runs against the changed lib checkout, and `fm status` shows both under one parent.

- **Turn a pasted screenshot, log or URL into a reproduction criterion** — FEATURE — value 3 — effort M — risk med — category: intake
  Why: the user pastes things ("pasted_content" exists). Intake ideas cover verbatim text and Artifact comments, but not attachments. A stored attachment plus an extracted symptom line becomes the acceptance check.
  Done when: capturing a message with an attached error log stores it with the task, and the brief's first criterion quotes the failing line from it.

- **Answer "why is this line here?" from blame to the user's own words** — FEATURE — value 3 — effort S — risk low — category: archaeology — wild
  Why: assumption: commit trailers and `fm show anything` give blame → task → verbatim request. Joining them is a small verb that makes the ledger useful years later.
  Done when: `fm why app.py:42` prints the task id, the user's original request, and the evidence line that closed it.

- **Install an opt-in pre-push evidence check for human commits** — SECURITY — value 3 — effort S — risk low — category: discipline
  Why: the discipline only applies inside Claude Code. Commits the user types by hand skip it, and CI-on-push is deferred. This is local, with no CI needed.
  Done when: `fm wire --git-hooks` adds a pre-push hook that warns, or blocks if configured, when a pushed commit's task has no evidence, and `fm unwire` removes it cleanly.

- **Land via branch and PR when main is protected** — FEATURE — value 3 — effort M — risk med — category: landing
  Why: `fm task finish --commit` assumes direct commits. A newcomer in a team repo hits a rejected push at the end of the flow. Assumption: detection is via `gh api` or a rejected-push probe.
  Done when: in a repo whose remote rejects direct pushes, finishing a task creates a branch and opens a PR with the evidence summary, without the user asking.

- **Rank "what next" across all projects in one list** — FEATURE — value 3 — effort M — risk low — category: portfolio
  Why: one central ledger already spans projects, yet every status view is per project. Assumption: the user runs several repos and never says which to open first.
  Done when: `fm today` lists the top 5 items across projects, ranked by blocked-ness, age and the user's recent steers, each with its project.

- **Rebuild from BUILD_PROMPT.md and diff behaviour against the real product** — CLEAN — value 3 — effort L — risk low — category: spec drift — wild
  Why: `--build` and BUILD_PROMPT.md exist but nothing checks that the spec still describes the product. A nightly rebuild in a lane, scored on the bench, shows which behaviours the spec has lost.
  Done when: `fm spec-drift` rebuilds into a throwaway lane, runs the bench on both, and prints the list of behaviours present only in the real product.

- **Re-derive a random closed task blind and score agreement** — FEATURE — value 3 — effort M — risk low — category: proof — wild
  Why: the pile has replaying your own round and amnesiac rounds, but not sampling closed tasks. Re-doing a closed task from its request alone shows whether "done" was reproducible rather than lucky.
  Done when: a weekly job picks one closed task, re-solves it in a lane without seeing the diff, and appends an agree/differ verdict with both diffs' file overlap to the ledger.

- **Warn when a task's plan is bigger than the request implies** — FIX — value 2 — effort S — risk low — category: scope
  Why: the user's drops show repeated "by design / not needed" rejections, and the over-engineering audit found ~8k removable lines. A plan-time check of steps against the verbs in the request catches scope creep before edits.
  Done when: a plan whose touched files exceed 3× the files named in the request prints one line naming the extra files and asks once to proceed.

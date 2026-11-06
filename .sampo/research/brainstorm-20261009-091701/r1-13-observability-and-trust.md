# Brainstorm — lens: observability and trust

- **Reject vacuous proof** — FIX — value 5 — effort M — risk low — category: verification trust
  Why: a criterion's verify used `-k a or b`, which run.py doesn't read, so it ran no tests and still passed. The criterion was then uneditable (T-0342). Evidence that can't fail is worse than none.
  Done when: a verify command that collects or runs zero tests, or never touches the changed files, is recorded as "vacuous" and cannot satisfy a gate. A test feeds in the `-k` case and sees it refused.

- **Prove the proof by reverting the fix** — FEATURE — value 5 — effort M — risk med — category: verification trust
  Why: `fm pr` already mentions red→green. Making it automatic is the deeper check: in a scratch worktree, undo the task's non-test diff, rerun the evidence, and require it to go red. Otherwise the test never tested the change. (Assumption: the diff can usually be split into tests and source.)
  Done when: `fm task done` on a FIX records a "fails without the change" result, and a deliberately toothless test is flagged.

- **Chain the ledger with hashes** — SECURITY — value 4 — effort S — risk low — category: tamper evidence
  Why: the ledger, briefs and decisions are the only record of work, and Claude runs with write access. The guard has a "trust" toggle for self-edits, which suggests this concern is real. (Assumption: the ledger is append-only JSONL.)
  Done when: each event stores the hash of the previous one, `fm doctor` fails on a hand-edited or deleted line, and a test that mutates one event is caught.

- **Audit claims against the diff** — FEATURE — value 5 — effort L — risk med — category: honesty check
  Why: the user said cleanup requests "never got done" and asked for a trace of why. A done-time checker would map each acceptance sentence in the brief to concrete diff facts: deleted symbols, removed docs, no remaining references. It reports unmet or unprovable claims instead of trusting the summary.
  Done when: a cleanup task that renames or removes something while leaving references behind cannot close, and the refusal names the leftover file:line.

- **Calibrate Foreman's own "done"** — FEATURE — value 4 — effort M — risk low — category: calibration
  Why: `fm sentinel`, `fm digest` and the lessons already hold the outcomes. Joining "done" claims to later reopens, sentinel failures and user corrections gives a per-task-type accuracy rate. Low-accuracy types get stricter gates automatically, which also builds on T-0217.
  Done when: `fm digest` shows a reliability table by task type and tier, and a type with repeated post-done failures gets an extra gate in `fm gates`.

- **Show a guard decision ledger with false-positive tracking** — FEATURE — value 4 — effort M — risk low — category: guard transparency
  Why: JARVIS hit several refusals that were wrong or confusing (the symlink rm, the focus-in-line, the missing task name). Recording every block with the matched rule, the part of the command that tripped it (T-0423), and what the user did next would let `fm replay` rank rules by override and retry rate.
  Done when: `fm replay --rules` lists the top rules by repeat refusals followed by a rephrased pass, and each entry links to the original events.

- **Scrub a task like a flight recording** — FEATURE — value 4 — effort L — risk low — category: desktop observability
  Why: the Tauri app is meant to control every session. A timeline per task would show prompts, guard verdicts, edits, evidence and step moves, so the user can see why a band was stuck on 1/5 without the logs. (Assumption: the transcripts and ledger carry enough timestamps.)
  Done when: opening a finished task in the app shows an ordered, filterable timeline that replays the step changes and links each to its evidence.

- **Explain idleness live** — FEATURE — value 3 — effort M — risk low — category: orchestration visibility
  Why: JARVIS idled with 20+ tasks queued, and the fix only came after the user noticed. A "why is this session not moving" panel would give one reason per session (waiting on a background job, budget pace, blocked task, needs user), fed by the drive's own state.
  Done when: `fm projects --json` carries an `idle_reason` for each session, and a test covers an idle state with a non-empty queue.

- **Bisect regressions found by the night sentinel** — FEATURE — value 4 — effort M — risk med — category: drift
  Why: `fm sentinel` reports checks that fail now but doesn't say which commit broke them. Running it during `fm night`, bisecting, and filing a FIX task with the culprit commit and original task closes the loop unattended.
  Done when: a seeded regression yields a queued FIX brief naming the guilty commit within one night run.

- **Plant canary bugs to test the reviewers** (wild) — FEATURE — value 4 — effort L — risk med — category: adversarial trust
  Why: assumption: the lens reviewers and `fm second` catch what they're meant to, but nothing measures it. In a throwaway lane, inject known defects (off-by-one, swallowed error, secret in a diff) into a real finished diff and record whether the reviewers flag them. That gives a measured detection rate per lens and a signal for `fm evolve` to optimise against.
  Done when: `fm bench --canary` prints a per-lens catch rate, and a lens that misses a seeded secret scores below 1.0.

- **Colour the codebase by trust** (wild) — FEATURE — value 3 — effort L — risk low — category: provenance
  Why: `fm why` already links lines to tasks, and `fm map` knows the hot files and the test links. Combining them gives a heatmap per file or function: which task wrote it, whether it was verified, whether a test covers it, and when it was last exercised. Untested, unverified or stale code stands out, and the heatmap tells `fm night` where to spend its budget.
  Done when: `fm ui --json` exposes per-file trust levels and the app shows them. A file written under a vacuous proof shows as low.

- **Attach a signed attestation to every release or PR** (wild) — SECURITY — value 3 — effort M — risk low — category: attestation
  Why: `fm pr` already collects proof, and releases go to GitHub main by hand. A signed bundle of gate results, ledger head hash, guard record and lens verdicts would let anyone check "this release passed Foreman's gates" without trusting the author. Foreman would also verify its own installs against it.
  Done when: `fm pr` or a release writes an attestation, and `fm verify-attestation <file>` succeeds on an untouched one and fails after any edit to the ledger slice.

- **Write a postmortem for every correction** (wild) — FEATURE — value 4 — effort M — risk low — category: learning
  Why: the user's steers repeat patterns: "cleanup never got done", guard false positives, budget blocking too early. Each correction, drop or JARVIS-reported refusal would automatically yield a structured note (what the model believed, what happened, which gate should have caught it) that proposes a gate, a veto or an eval case via `fm evals`. This feeds the friction passes with causes instead of just counts.
  Done when: a recorded user correction produces a postmortem file within the task, linked to a proposed eval, and `fm friction` cites it.

- **Show budget causality** — FEATURE — value 3 — effort S — risk low — category: cost transparency
  Why: the user pushed back on the budget and pace limits blocking work before 75% usage. A line explaining each throttle (current pace, threshold, which task it delayed) would let them see the decision instead of guessing it.
  Done when: any wait or refusal from pace names the usage percentage and threshold, and none appears below 75%.

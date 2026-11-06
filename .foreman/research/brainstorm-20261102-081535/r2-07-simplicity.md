# Brainstorm — lens: simplicity

Simplicity lens: verification should be one mechanism that many claims reuse, not a prover per category. Earlier rounds listed dozens of provers, so these ideas shrink, merge or delete.

- **Reduce every prover to a golden-output diff** — FEATURE — value 4 — effort M — risk med — category: simplicity
  Why: the request lists UI, data, docs, ops and perf as separate proofs. Each is "run a command, normalise its stdout, compare to a stored baseline". An `fm shot` output, a SQL result, a doc's command, and a `terraform plan` all fit.
  Done when: one `fm prove --cmd X` stores a baseline, and a changed output fails and an unchanged output passes, across a UI, a data and a docs fixture.

- **Merge `fm shot` and `fm flow` into one `fm see`** — CLEAN — value 3 — effort S — risk low — category: simplicity
  Why: the request names both. A shot is a flow of one step.
  Done when: `fm see` with one step reproduces today's `fm shot` output, and `fm shot` and `fm flow` become aliases with a test.

- **Make the model unable to write a proof label** — SECURITY — value 4 — effort S — risk low — category: honesty
  Why: the request says "whatever can't be proven gets labelled unproven", but a label that prose can write can be gamed. The label is derived only from an evidence command's exit code (0 proven, 1 failed, anything else unproven).
  Done when: a finish note containing "proven" with no evidence record is rewritten to "unproven" by a test.

- **Store proof in the commit trailer, not a new ledger** — CLEAN — value 3 — effort S — risk low — category: simplicity
  Why: git already keeps history, and Foreman has many ledgers. A `Proof: <cmd> -> pass|fail|unproven` trailer needs no new store and no sync.
  Done when: `git log --format=%(trailers)` shows the proof for a task, and the finish check reads it back.

- **Exempt trivial changes explicitly, and log the skip** — FEATURE — value 3 — effort S — risk low — category: ceremony
  Why: assumption: most diffs under N lines in docs, comments or tests need no prover. Today's pull is toward ceremony everywhere.
  Done when: a typo-only diff finishes with the line "verification skipped: trivial (reason)", and a code diff does not get that line.

- **Cut proof kinds that never changed a decision** — CLEAN — value 4 — effort M — risk low — category: simplicity
  Why: 1388 of 2117 files are skills, and the lean ratchet exists. Count the verifiers whose results were never followed by a fix, a reopen or a drop in 30 days, and list them as deletion candidates.
  Done when: `fm doctor` prints a kinds table with "acted-on count" and flags kinds with zero.

- **Time-box every prover and treat a timeout as unproven** — FIX — value 3 — effort S — risk low — category: reliability
  Why: assumption: browser, perf and infra probes hang and stall a drive. A fixed budget with one rule removes the special cases.
  Done when: a sleeping fixture prover ends at the budget with reason "timed out" and the task continues.

- **Show evidence beside the user's sentence, without a verdict, for "did it do what I meant"** — FEATURE — value 4 — effort S — risk low — category: meaning
  Why: no tool can decide intent. The request lists "does it do what the user meant" as a verification. Printing the sentence next to raw output and leaving the call to the human is simpler and more honest than a scorer.
  Done when: finish prints "You said: … / It does: …" with the real command output, and records "unproven: intent, human to judge".

- **Add a one-line `fm verify` that runs only the changed-file types' provers** — FEATURE — value 3 — effort M — risk med — category: developer experience
  Why: assumption: the user shouldn't need to know five verbs. The verb picks from the diff and prints three counts: proven, failed, unproven.
  Done when: on a docs-only diff it runs only the docs check, and on a UI diff only `fm see`.

- **Wild: Replace the proof ledger with a generated `proof.sh`** — FEATURE — value 3 — effort M — risk med — category: portability
  Why: wild. A script that re-runs every claim, exits 0/1/77, works with no Foreman and no `claude` (a standing rule), and any CI can run it.
  Done when: `sh proof.sh` in a clean clone reproduces the same three counts as `fm`.

- **Wild: A verifier that deletes itself after one use** — FEATURE — value 2 — effort S — risk low — category: simplicity
  Why: wild. One-shot probes are written to a temp dir, run, and left only as a trailer line. Nothing accumulates to maintain.
  Done when: after finish, the state dir has no new files besides the commit trailer.

- **Wild: Rubber-stamp detector on the human** — FEATURE — value 3 — effort S — risk low — category: honesty
  Why: wild. If the user accepts "unproven" finishes ten times with no reading time, collapse the receipt to one line and say so.
  Done when: a fixture of ten instant accepts yields the one-line receipt, and a slow accept restores the full one.

Answers to earlier questions I can take: the open question about which surfaces the user would open is best settled by the same census as "cut proof kinds", using opening counts from the logs. "Private goal needs a remote model" should default to fail, with one `fm ask` offering the weaker local model.

Next question: which proof kinds in this pack could be one golden-output diff, and which really need a different mechanism?
Next question: what is the smallest verification output a user reads to the end, and how long does it stay that short after a month?

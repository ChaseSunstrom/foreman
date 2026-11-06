# Brainstorm — lens: deepen: proof

- **Admit findings through a proof ticket, not a report** — FEATURE — value 5 — effort M — risk low — category: proof
  Why: exam s0-001 found 0 of 108 planted defects, and the existing ideas all converge on "red on untouched tree". Combine them into one record: `{test file, run command, red signature, 3 run hashes, CI-command result}`. A finding without a complete ticket cannot enter the ranked list.
  Done when: `fm find ledger` rejects a finding missing any ticket field, and a fixture finding with a flaky test (red 2 of 3) is refused with the reason "unstable".

- **Classify red by signature: assertion vs. import/setup/timeout** — FIX — value 5 — effort M — risk low — category: proof
  Why: "fails for the wrong reason" is the commonest false positive (collection error, missing dep, wrong cwd). A red caused by ImportError/ModuleNotFound/SyntaxError/timeout is not proof of a bug.
  Done when: a test failing with ImportError is classed `harness`, not `proved`, across pytest, jest/vitest, cargo test and go test fixtures, and an AssertionError test is classed `proved`.

- **Run the harness canary before hunting** — FEATURE — value 4 — effort M — risk low — category: proof
  Why: the ideas "prove the harness before the bug" and "learn to run a single test in an unfamiliar stack" are one capability. Write a trivially-passing and a trivially-failing test in the project's own runner, confirm green/red are distinguishable, and record the per-stack single-test command.
  Done when: in a never-seen fixture repo per language (python, js, ts, ruby, rust, c), the canary yields a stored single-test command and both outcomes are observed; unsupported stacks report `no-harness` and skip hunting rather than guessing.

- **Mutate-to-confirm: the fix must flip red→green and the revert must flip back** — FEATURE — value 5 — effort M — risk low — category: proof
  Why: `fm task prove` already shows a test fails without the change; extend it to the finding lane so a fix that turns the test green by editing the test or by an unrelated change is caught.
  Done when: a fixer diff touching the proof test file is rejected, and reverting only the source hunk makes the proof test red again, recorded in the ticket.

- **Shrink the proof before the fixer sees it** — FEATURE — value 4 — effort M — risk med — category: proof
  Why: a minimal repro (delta-debugging on inputs and lines) keeps the fixer focused and keeps the cost near plain Claude's ~0.17 USD per fix. Shrinking must preserve the pinned signature.
  Done when: a 40-line failing test shrinks to ≤10 lines with the identical red signature on a fixture, and a shrink that changes the signature is discarded.

- **Prove "none" too: a clean-bill receipt** — FEATURE — value 5 — effort M — risk med — category: proof
  Why: the exam grades the `none` kind in never-seen repos; a finder that always reports something fails it. Each probed area gets a receipt ("probed X with Y, no red found"), and a finding with no ticket is silently dropped, so a bug-free repo ends with an empty list and a receipt rather than invented work.
  Done when: on a fixture repo with zero planted defects, `fm find` exits with zero findings and a receipt per probe; on a repo with one planted bug it reports exactly that one.

- **Cold reproducer: a tool-less agent re-derives the repro from the text alone** — FEATURE — value 4 — effort M — risk med — category: proof — wild
  Why: from the earlier "cold agent reproduce it" idea. Hand the finding's prose (not the test) to a fresh headless agent and ask it to write the failing test; if its test isn't red with the same signature, the report is ambiguous and is downgraded.
  Done when: a finding with a vague description fails cold reproduction and is labelled `unclear`, while a precise one reproduces with a matching signature.

- **Cross-witness with CI: replay the red under the project's CI command** — FEATURE — value 4 — effort M — risk med — category: proof
  Why: a repro that passes under the CI's flags, env or matrix is a local artifact. Parse `.github/workflows` / Makefile for the test command and rerun the proof there.
  Done when: a proof red only under a local-only env var is refused when the CI-derived command is green, and the ticket names which command was used.

- **Seed bugs against the finders: a self-planted mutation exam per run** — FEATURE — value 4 — effort L — risk med — category: proof — wild
  Why: the exam showed 0/108; the user steered toward outside signals only. Before the night run, plant 3 small mutations (flip a comparator, drop a boundary check) in a scratch copy, and measure whether the finders catch them. A recall score gates how much to trust the night's list.
  Done when: `fm find --selfcheck` reports recall over N planted mutations in a scratch worktree and leaves the real tree untouched (verified by `git status` clean).

- **Rank by proof strength, not by prose** — FEATURE — value 4 — effort S — risk low — category: proof
  Why: value ranking is a gap in the mission; proof quality is an objective input. Score = stability (3/3), signature specificity, CI-confirmed, shrunk, plus blast radius (callers/tests touching the file).
  Done when: two fixture findings with different proof strength sort in the expected order, and the score components print per finding.

- **Make the proof a one-command artifact the user can run** — FEATURE — value 3 — effort S — risk low — category: proof
  Why: "open every finding as a failing test the user can run in one command". Emit `fm find show F-n --run` that prints the exact command and executes it, plus a patch that adds just the test.
  Done when: running the printed command on a clean checkout reproduces the red signature, in a fresh clone.

- **Proof regression bank: keep proven findings as permanent tests, retire when green** — FEATURE — value 3 — effort M — risk low — category: proof — wild
  Why: each proved finding is a free regression test. After the fix lands, the test stays; if later `fm outcomes` shows the same signature recurring, the finding is reopened automatically. This ties proof to the 30-day survival signal the user trusts.
  Done when: a fixed finding's test is committed with its ticket id, and re-breaking the code reopens that finding in the ledger.

- **Quarantine unprovable but plausible suspicions as "leads", never tasks** — FEATURE — value 3 — effort S — risk low — category: proof
  Why: security and perf issues often cannot be shown red cheaply. A separate leads list, excluded from the queue and never auto-fixed, keeps useful signal without breaking "no test, no finding".
  Done when: a finding without a ticket lands in `leads`, is absent from `fm run` candidates, and can be promoted only by attaching a ticket.

Next question: What does the proof pipeline cost per finding in tokens and wall time on a never-seen repo, and at what budget does it still beat plain Claude's ~0.17 USD per fix?
Next question: Which bug kinds (perf, flake, vuln) have no cheap deterministic red signature, and what is their honest proof form instead of a unit test?

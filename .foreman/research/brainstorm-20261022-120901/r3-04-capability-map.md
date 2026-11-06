# Brainstorm — lens: capability map

- **Block close on secrets in the diff** — SECURITY — value 5 — effort S — risk low — category: security
  Why: the pack covers secret paths and render redaction but nothing that scans what a worker wrote. Assumption: unattended runs are where a pasted key lands in a commit.
  Done when: a fixture diff containing an AWS-style key and a high-entropy token refuses `fm task close`, naming file and line. An `fm secrets allow` baseline entry lets the same fixture close.

- **Let users add guard rules with mandatory examples** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: the guard has a 24-command corpus and a tighten-only config lattice, but users can't author their own deny rules. Assumption: teams have project-specific dangerous commands (prod hostnames, `terraform destroy`).
  Done when: a rule in `.foreman/guard.toml` loads only if it has at least one should-block and one should-pass example, and `fm doctor` runs those examples. A rule that loosens a built-in verdict is rejected.

- **Try any command in a guard playground** — FEATURE — value 4 — effort S — risk low — category: guard, DX
  Why: T-1263 built an evasion corpus, but users see verdicts only when blocked mid-run. Assumption: trust in the guard rises when users can probe it.
  Done when: `fm guard try 'rm -rf $HOME/x'` prints the verdict, the matching rule and five generated evasion variants with their verdicts, running nothing.

- **Turn each new dependency into a decision card** — SECURITY — value 4 — effort M — risk med — category: supply-chain
  Why: T-0791 (supply-chain defenses) is deferred, and workers add packages freely. Assumption: the lockfile diff holds enough offline data (install scripts, licence, resolved host).
  Done when: a diff adding an npm or pip dependency pauses close with a card showing install-script presence, licence class and registry host. Closing without a decision fails.

- **Generate a reviewer's reading path for the diff** — FEATURE — value 4 — effort M — risk low — category: user value
  Why: close-out legibility is deferred (T-0795), and "heat-tint files by risk" is only a colour cue. Assumption: a human reviewing the diff wants an order and a reason per file.
  Done when: `fm review path T-XXXX` lists files in suggested reading order, each with one line (why it matters, which proof covers it, which hunks no proof touched).

- **Post a proof receipt on pull requests from a GitHub Action** — FEATURE — value 4 — effort M — risk med — category: CI, DX
  Why: the repo already ships CI and a task ledger, and the user releases to main often. Assumption: reviewers of Foreman-built PRs can't see the evidence today.
  Done when: a PR opened from a closed task gets one comment listing each acceptance claim, the command run, its exit status and the base SHA. A claim with no recorded proof renders as "unproved".

- **Answer "can Foreman do X?" from its own inventory** — FEATURE — value 4 — effort S — risk low — category: simplicity, discovery
  Why: 12 skills, 48 playbooks, about 1,088 cards and a large verb surface; the user keeps asking for "way more" without a way to find what exists. Assumption: discovery is now the bottleneck.
  Done when: `fm can "compare two screenshots"` prints up to three matching verbs, skills or playbooks, each with the exact command and token cost, and says "none" when nothing matches.

- **Backtest each new playbook on your own past failures** — FEATURE — value 4 — effort M — risk med — category: evals
  Why: the ideas list has A/B evals, but only on fixtures. The user's finished tasks hold real failures (T-0035 eval capture is deferred). Assumption: closed tasks keep enough context to replay.
  Done when: `fm playbooks backtest NAME` replays N past failed or reopened tasks with and without the playbook and prints pass-rate deltas. It labels results "n too small" under a minimum N.

- **Add `fm dev`, a watch loop for Foreman contributors** — FEATURE — value 3 — effort M — risk low — category: DX
  Why: the gates (`fm doctor`, roundtrip, `bench_hooks`) are slow and run separately, and canaries flake under load (T-1380). Assumption: the user iterates on the repo most days.
  Done when: saving a file under `plugin/lib/` re-runs only its mapped tests (from the map's tests→src pairs) plus the guard corpus within the budget. A one-line pass/fail is printed, and the heavy gates are skipped while the machine is loaded.

- **Offer a phone-over-ssh profile with a soft-key row** — FEATURE — value 3 — effort M — risk low — category: devices
  Why: the ideas list has notifications and a LAN status page but no input story for a phone terminal (Termux, Blink). Assumption: the user checks runs from a phone.
  Done when: `fm code app --profile phone` fits 40 columns, shows a bottom row of tappable Approve, Deny, Pause and Next, and has a golden-frame test at 40×20.

- **Publish proof-gap diagnostics through an LSP stub** (wild) — FEATURE — value 3 — effort L — risk med — category: editor
  Why: assumption: any editor with LSP support can show "edited, never verified" as a squiggle without a per-editor plugin. This is new because the existing ideas cover ACP/MCP and cursor-as-context, not diagnostics.
  Done when: a stdlib stdio server reports a warning on every line changed by an open task with no passing verify, and the warning clears when `fm task prove` succeeds.

- **Sign proof receipts with the user's SSH key** (wild) — SECURITY — value 3 — effort M — risk low — category: trust
  Why: self-checking bundles are covered, but not authorship. `ssh-keygen -Y sign` is already on most machines and needs no new dependency.
  Done when: `fm receipt sign` attaches a signature, and `fm receipt verify` on another machine passes with an allowed-signers file. Altering one byte of the receipt makes it fail.

- **Train people on the guard with a dangerous-command dojo** (wild) — FEATURE — value 3 — effort M — risk low — category: security education
  Why: the 24-command corpus and its evasions already exist as data. Quizzing the user "block or allow?" teaches the rules and exposes their blind spots, which feed back as candidate corpus entries.
  Done when: `fm guard dojo` shows 10 commands drawn from the corpus, scores the user's calls against the real verdicts, and prints the misses with the reason.

- **Let a pasted ticket or error configure the next run** (wild) — FEATURE — value 3 — effort M — risk med — category: user value
  Why: the user's own requests are long, clause-heavy mandates. Assumption: a pasted stack trace plus one sentence should become a bounded task with a failing-test-first verify, showing its reading of the request for veto before it starts.
  Done when: pasting a trace into the request box produces a draft task with scope, a verify command that currently fails, and a one-key veto. Nothing runs until the user confirms.

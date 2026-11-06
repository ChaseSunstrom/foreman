# Brainstorm — lens: deepen: debugging

- **Persist a hypothesis ledger in the brief, fed by failed verifies** — FEATURE — value 5 — effort M — risk low — category: debugging
  Why: the 3-failed-attempts rule blocks with a diagnosis, but nothing carries what was already ruled out between attempts or into `fm recall`. Assumption: the brief has a free-form evidence section the ledger can live in.
  Done when: after two failing `fm task verify` runs, the brief holds a "Hypotheses" table (claim, probe, result), and `fm next` shows only untested rows.

- **Auto-capture the failing verify's delta from its last pass** — FEATURE — value 4 — effort M — risk low — category: bisect
  Why: acceptance criteria already carry verify commands, and tasks commit with pre-snapshots. So "last green commit vs now" is computable. Assumption: the criterion passed at some earlier snapshot.
  Done when: a failing criterion that previously passed prints the files changed since that pass, ordered by `fmmap` impact on the verify target, in under 3 lines.

- **Rank probes by cost and discrimination in `fm next`** — FEATURE — value 4 — effort M — risk med — category: triage
  Why: the user is token-sensitive, so the cheapest probe that splits the hypotheses (grep, a single test, `fm why FILE:LINE`) should come before any recon agent. Assumption: probes can be tagged with a rough cost class (grep, one test, full suite, subagent).
  Done when: with 2+ open hypotheses, `fm next` names one probe, labelled by cost class, and recon is suggested only after the cheap probes are marked done.

- **Seed the debugging lens from friction and past lessons automatically** — FEATURE — value 4 — effort S — risk low — category: recall
  Why: `fm recall` and `fm friction` exist but a debugging task has to ask for them. A failure signature (error text plus file) can be matched to past lessons and guard blocks without being asked.
  Done when: the first failed verify on a task prints at most 2 recalled lessons matching the error text, and nothing when none match.

- **Stop-the-line detector for repeated identical failures** — FIX — value 4 — effort S — risk low — category: loop-guard
  Why: the drive keeps working unattended, and a failure repeated 3 times costs tokens without information. Today the block counts attempts per step, not whether the failure output changed. Assumption: failure output can be normalized by stripping timestamps and paths.
  Done when: two consecutive verify failures with the same normalized output flip `fm next` to "change the hypothesis", and a changed output resets the counter.

- **Classify the unknown before debugging** — FEATURE — value 3 — effort S — risk low — category: triage
  Why: the unknown is either reproducible with a known path (go straight to a probe) or an unknown-unknown (needs recon first). Choosing wrongly wastes turns. Assumption: a one-line field on the task is enough to route.
  Done when: `fm task plan` for a FIX task requires `repro: known|unknown`, and `unknown` puts a reproduction step before any edit step.

- **Premortem fork that argues the root cause is wrong** — FEATURE — value 4 — effort M — risk med — category: adversarial — wild
  Why: the single reviewer pass is the budget, so it could be spent on one targeted adversary instead. A tool-less `claude -p` child (the `fm ideas` mechanism) gets the brief, the diff and the hypothesis ledger and gives the best alternative cause plus the one probe that tells them apart. Assumption: one extra child call per FIX is affordable.
  Done when: `fm task done` on a FIX task, when the ledger has a single confirmed cause, runs one tool-less child and records its alternative with a probe, and the output is under 10 lines.

- **Delta-debug a failing session into a minimal repro** — FEATURE — value 4 — effort L — risk med — category: repro — wild
  Why: `fmreplay` already replays real session commands through the guard, so a similar harness can replay them against a scratch worktree (`fmlanes`) and shrink the list with ddmin. Assumption: the commands are mostly deterministic and run in an isolated lane.
  Done when: `fm repro --session S --fails "<cmd>"` outputs a shorter command list that still reproduces the failure, plus a brief-ready summary.

- **Rubber-duck from the brief alone** — FEATURE — value 3 — effort S — risk low — category: reasoning — wild
  Why: restating the problem from the brief often exposes a missing acceptance criterion, and it needs no repo reads. The child sees only the brief, so gaps in the brief show up as its questions. Assumption: cost is one short no-tools call.
  Done when: `fm duck T-NNNN` prints at most 5 questions the brief fails to answer, and each one maps to a brief section.

- **Turn solved bugs into guard and replay regression cases** — FEATURE — value 3 — effort M — risk low — category: regression
  Why: the lesson written at `fm task done` is prose, whereas the regression-test reference exists and `fm replay` can be a gate. A FIX task could require its verify command to be added to a permanent set. Assumption: a registry of fixed-bug verify commands can be run cheaply as a smoke gate.
  Done when: closing a FIX task appends its verify command to a registry, and a later change that breaks it fails `fm doctor` and names the originating task.

- **Dashboard "debug state" strip showing ledger status** — FEATURE — value 2 — effort S — risk low — category: UI — wild
  Why: the user cares a lot about panel appearance, and a failing task currently looks the same as a running one. A single panelled line, "3 hypotheses: 1 ruled out, 1 testing, 1 open", would make the state visible without more chat output. Assumption: the dashboard reads task state from the brief file.
  Done when: a task with a ledger shows one line in the existing task panel, with no extra chat message and no duplicate at the bottom.

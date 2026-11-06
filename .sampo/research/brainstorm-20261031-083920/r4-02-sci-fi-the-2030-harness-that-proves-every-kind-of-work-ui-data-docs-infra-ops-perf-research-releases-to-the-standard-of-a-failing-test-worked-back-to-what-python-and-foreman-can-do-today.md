# Brainstorm — lens: sci-fi: the 2030 harness that proves every kind of work (UI, data, docs, infra, ops, perf, research, releases) to the standard of a failing test, worked back to what Python and Foreman can do today

- **Declare the effect set before building** — FEATURE — value 5 — effort M — risk med — category: proof
  Why: the perf (T-2284, T-2303) and data (T-2288) proofs each snapshot something different, and nothing says what a task was allowed to change. Assumption: a shared "may change" declaration is cheaper than per-kind special cases.
  Done when: `fm task new --may-change <files|tables|outputs>` records the set, and a fixture task that also changes an undeclared file or table fails its evidence step naming that item.

- **Taint tasks built on unproven ground** — FEATURE — value 4 — effort M — risk low — category: unproven rollup
  Why: T-2273's rollup counts unproven tasks one by one but not what rests on them. Assumption: file overlap with an unproven task's diff is a good-enough dependency signal.
  Done when: focusing a task whose scope overlaps an unproven task's files shows "built on unproven T-NNNN", and the rollup lists tainted-by counts.

- **Prove performance with counts, not clocks** — PERFORMANCE — value 4 — effort S — risk low — category: perf proof
  Why: `--bench` records median times, which are noisy on shared hardware. Deterministic counters (subprocess spawns, file reads, `getrusage` max RSS, `sys.monitoring` call counts) don't flake.
  Done when: `fm task evidence ID --count "<cmd>"` records the old and new counters, and a fixture that adds one subprocess per call is flagged identically on 5 runs.

- **Perturb the environment before trusting a green** — FEATURE — value 4 — effort S — risk low — category: verification
  Why: assumption: tests passing only under the author's TZ, locale, hash seed, cwd or test order are a common false-done. The Genesis tower has no perturbation arm today.
  Done when: `fm prove --perturb` re-runs the verify command under `PYTHONHASHSEED`, `TZ`, `LC_ALL`, shuffled order and a different cwd, and a fixture test that depends on TZ is reported unstable.

- **Replay the user's own shell history as a behaviour diff** — FEATURE — value 4 — effort M — risk med — category: meant-it proof
  Why: the open question "does it do what the user meant" has no check built from what this user really runs. The history stays local and read-only commands are filtered by an allowlist.
  Done when: `fm prove --replay` runs the last N allowed `fm` invocations on the start tree and the current tree and prints only the output differences.

- **Leave a sentinel behind every closed incident** — FEATURE — value 4 — effort M — risk med — category: ops
  Why: "close an incident only on a replayed signature" proves the fix once, but incidents come back. Assumption: a cheap periodic probe of the signature is enough to catch most returns.
  Done when: closing an ops task can register a probe command, and a fixture where the signature reappears reopens the task with the failing output attached.

- **Prove "removed" with a ghost check** — FEATURE — value 3 — effort S — risk low — category: proof of absence
  Why: assumption: deletion and rename tasks close on "tests pass", which can't see a surviving reference in docs, configs, strings or skill text (the repo has 1388 skill files).
  Done when: `fm prove --absent NAME` greps code, docs, skills and configs and fails on a planted stale mention in a fixture.

- **Prove releases by building twice** — FEATURE — value 3 — effort S — risk low — category: release proof
  Why: install-in-a-clean-venv is already proposed, but not reproducibility. Assumption: the plugin build is deterministic enough to compare.
  Done when: the release gate builds in two temp directories, compares hashes and names the differing files, and a fixture embedding a timestamp fails.

- **Paraphrase the goal to find ambiguity** — FEATURE — value 3 — effort M — risk low — category: intake
  Why: the missed-ask data (T-2285, T-2288 and others) shows the first reading was often wrong. If five rewordings of one goal yield different plans, the goal is ambiguous.
  Done when: the intake step runs 3+ paraphrases through a tool-less child and, when the plans' row sets diverge past a threshold, asks one question naming the divergent clause.

- **Hunt counter-evidence for research claims** — FEATURE — value 3 — effort M — risk med — category: research proof
  Why: citation and refetch checks only confirm that a source says X, not that nothing credible says not-X. Assumption: a cold child with a search tool can surface at least one rebuttal when one exists.
  Done when: a research task's receipt carries a "strongest counter-source" line per claim, or "none found, searched: …".

- **Wild: Prove the state machines by exhaustive search** — FEATURE — value 4 — effort L — risk med — category: self-proof
  Why: wild. This answers the unresolved baton, ledger and repo disagreement after a kill. A small Python explorer enumerates task, lane and baton states under crash and restart events and checks that no state is stuck and exactly one source wins.
  Done when: `fm doctor` runs the explorer on the lane and task models and prints a counterexample trace for a planted deadlock.

- **Wild: Train a "you'd reject this" twin locally** — FEATURE — value 3 — effort L — risk med — category: privacy, taste
  Why: wild. A stdlib bag-of-words model over the user's accepted and rejected diffs and plan edits flags likely rejections before they're shown. Nothing leaves the machine.
  Done when: on held-out past closes, the twin's flag beats a coin flip, and the verdict is labelled "advisory, unproven".

- **Wild: Spot-check roulette** — FEATURE — value 3 — effort M — risk low — category: delight, trust
  Why: wild. When every proof kind has a model on one side, the only evidence nobody can forge is the user's own glance. Foreman picks the single riskiest claim of a close and shows a 10-second yes/no card, and the answers feed each kind's catch rate.
  Done when: closing a task offers one card, and the answer is stored as a "user-witnessed" evidence line.

- **Wild: Render every CLI surface under hostile terminals** — FEATURE — value 2 — effort S — risk low — category: devices
  Why: wild. A run with a 40-column width, `NO_COLOR` and a non-UTF-8 locale catches the glyph and wrap bugs that screenshots of a nice terminal never show.
  Done when: `fm shot --hostile` renders the status, goal and receipt screens under three terminal profiles and flags any line that overflows or garbles.

Next question: Which proof kinds could be derived from a single declared effect set, and which still need their own witness?
Next question: What does a proof need to record today so it can still be replayed on a different interpreter, OS or model in a year?

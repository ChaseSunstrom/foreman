# Brainstorm — lens: reliability

**Earlier questions, from the reliability lens:**
- *Wrong hidden keys:* every bug key should ship with a reference failing test, run against the planted repo before the exam is used. A key with no failing reproducer is quarantined, not trusted.
- *What an exam pass predicts:* only scores on kinds that are re-checked against `fm outcomes` survival mean anything. A kind that never correlates should be dropped from selection.

- **Drop any finding whose repro isn't stable** — FEATURE — value 5 — effort M — risk low — category: proof
  Why: the pipeline "proves each finding with a failing test", but a test that fails once may be a flake. The Initiative also has flake finders, so the two must not blur.
  Done when: a finding is promoted only if its test fails 3 of 3 in fresh processes and passes 3 of 3 after the fix. A planted nondeterministic test is labelled `flake`, not `bug`.

- **Pin the failure signature before and after the fix** — FEATURE — value 5 — effort M — risk low — category: proof
  Why: assumption: a test can fail for the wrong reason (import error, missing tool, bad path) and still look like a repro. Plain Claude's 3/3 would be matched only by fixes that remove the claimed failure.
  Done when: the proof records the assertion or exception and its location. Closing requires that exact signature to vanish, and a test failing on setup or import is rejected as "not a repro".

- **Score the finders on clean repos first** — FEATURE — value 5 — effort M — risk low — category: precision
  Why: Mission 3 is graded on the exam's `none` and `bug` kinds. A finder that cries wolf on a clean repo loses the `none` half outright.
  Done when: `fm exam` reports a false-positive count per finder on `none` repos. The finder gate fails if any `none` repo yields a promoted finding.

- **Separate hypothesis from verified finding** — FEATURE — value 5 — effort L — risk med — category: finders
  Why: the deterministic finders found 0 of 108, and an LLM finder will over-claim. The fix is to let a model propose hypotheses cheaply while only a harness-run failing test can promote one to a ranked finding.
  Done when: no finding reaches the ranker without a linked failing-test run id. On exam run s0-002 the number of unverified-but-ranked findings is 0.

- **Blame only new red** — FIX — value 4 — effort S — risk low — category: baseline
  Why: the "Baseline red" item was dropped as unreproducible once, so baseline state is already a source of confusion. A finder that credits pre-existing failures as discoveries is wrong.
  Done when: the scan records baseline gate results first. A finding whose test was already red at baseline is filed as "known red" and never ranked as new work.

- **Keep Foreman's own setup failures out of user queues** — FIX — value 4 — effort S — risk low — category: scout
  Why: the pack notes `probe_doctor` may queue Foreman setup failures as tasks in user projects.
  Done when: a doctor probe failing in a fixture project produces zero backlog rows there. The failure goes to a Foreman-origin channel instead.

- **Run scout probes in a throwaway worktree** — SECURITY — value 4 — effort M — risk med — category: sandbox
  Why: assumption: probing never-seen repos means running their code. The exam repos span python, js, ts, ruby, rust and c, so probes need a timeout, a private HOME, no network, and a reap of orphans.
  Done when: a probe that hangs, forks, or writes outside its worktree is killed. The real tree's hash is unchanged afterwards, tested with a hostile fixture repo.

- **Calibrate rank weights from measured finder precision** — FEATURE — value 4 — effort M — risk low — category: ranking
  Why: value ranking is a listed gap. Weighting by observed precision per finder and language keeps a noisy probe from topping the list.
  Done when: the ranker reads a per-finder precision table from `exam.jsonl`. Dropping a finder's precision to 0.1 in a fixture demotes its findings below a precise finder's.

- **Show coverage with every empty result** — FEATURE — value 4 — effort S — risk low — category: observability
  Why: "found nothing" currently cannot be told from "could not look". The `none` kind rewards honest silence, and `fm genesis check` already validates coverage grids.
  Done when: a scan with no findings prints the probes run, files and languages covered, and probes skipped with reasons. A missing toolchain shows as "blind", not "clean".

- **Revert a fix lane when anything previously green flips** — FIX — value 4 — effort M — risk low — category: lane
  Why: the find→prove→fix pipeline is new, and a fix that breaks a neighbour is worse than no fix. This is the same shape as the existing stop-after-3-reverts rule.
  Done when: a fixture fix that breaks an unrelated test is auto-reverted with a journal line naming the flipped test. The finding is re-filed as "fix unsafe".

- **Cap cost per verified finding** — PERFORMANCE — value 3 — effort S — risk low — category: budget
  Why: plain Claude finds and fixes at about $0.17 each, and Foreman costs more for the same score. A per-finding cap stops unbounded scouting.
  Done when: a finder run past its cap stops and keeps its partial verified findings. The receipt shows spend per verified finding.

- **Wild: plant canaries before declaring a repo clean** — FEATURE — value 4 — effort L — risk med — category: calibration
  Why: wild. Mutate a scratch copy to inject known bugs and check that the finders see them. A recall figure then qualifies every "none" answer.
  Done when: a scan prints "recall on 10 planted bugs: N/10" beside its verdict. A deliberately blinded finder shows low recall.

- **Wild: demand two independent witnesses** — FEATURE — value 3 — effort M — risk med — category: finders
  Why: wild. Two cold finders with different prompts and models must each produce a failing test for the same defect. Singly-witnessed findings carry a visible "one witness" tag.
  Done when: the ranking shows a witness count. On a fixture, a finding that only one finder reproduces ranks under a two-witness one.

- **Wild: sweep seeds, clocks and time zones on every repro** — FEATURE — value 3 — effort M — risk low — category: flake
  Why: wild. Re-run each repro across test order, random seed, `TZ` and a faked date, which splits "always broken" from "broken on Tuesdays in Auckland". The Initiative also asks for flake finders.
  Done when: a repro that passes under any variation is labelled `conditional`, with the failing variation named in its receipt.

Next question: Which kinds in the exam (`vague`, `ambiguous`, `missing-tool`) should make the finder decline to file anything, and what test shows that it declined for the right reason?
Next question: When the repo has no runnable tests at all, what is the minimal reproduction a finding may use, and who verifies that it truly reproduces?

# Brainstorm — lens: deepen: measurement

- **Score every bench run with a preference-weighted rubric, not just pass/fail** — FEATURE — value 5 — effort M — risk low — category: measurement
  Why: the user's standing prefs (quiet output, one reviewer pass, no asking for commands, token-sensitive) are never scored; bench compares only pass rate, cost and turns. Extract measurable proxies from the transcript: count of user-directed commands, reviewer passes, output tokens, turns to first edit, and a composite "user-fit" score.
  Done when: `fm bench compare A B` prints a user-fit column, and a candidate that hands the user a shell command in a replay scores lower than one that doesn't (fixture test).

- **Run each bench case N times and report variance and confidence** — FEATURE — value 5 — effort S — risk low — category: measurement
  Why: the pack says evals are "single runs, noisy"; `/foreman:improve` gates on them. A candidate that wins on one sample is indistinguishable from luck.
  Done when: `fm bench compare --runs 3` reports per-case pass counts and marks a difference as "inconclusive" unless it exceeds the observed spread; a test with a stubbed runner covers both verdicts.

- **Ablate one skill, playbook or hook at a time and report its marginal value** — FEATURE — value 5 — effort M — risk low — category: measurement
  Why: the "skill diet" idea, grown into a standing procedure: playbooks aren't measured, `fm next` names static procedures, and always-on description cost is known (`fm plugins check`). Joining the two gives tokens saved against pass-rate lost per component.
  Done when: `fm bench ablate` outputs a table (component, Δpass, Δcost, Δturns) over at least the intake references and playbook index, and flags components with Δpass ≤ 0 and positive cost as removal candidates.

- **Log read-playbook and routed-skill usage per task and join it to bench outcomes** — FEATURE — value 4 — effort M — risk low — category: usage telemetry
  Why: steered "learn — record which routed skills were used and whether the task closed first time", and "playbooks are not measured". Bench gives the outcome side; this supplies the exposure side.
  Done when: `events.jsonl` records a `ref_read` event per playbook/skill load, and `fm bench report` shows, per reference, the first-close rate with vs without it.

- **Gate self-improvements on a held-out bench split** — FEATURE — value 4 — effort S — risk low — category: overfitting guard
  Why: `/foreman:improve` builds candidates and compares them on 8 cases, all derived from Foreman's own history. A candidate tuned against those cases can overfit them, and the cases are few.
  Done when: `fm bench` tags a fixed hold-out subset by hash of the case id, `improve` tunes only on the train split, and acceptance requires a non-regression on the hold-out; test shows a candidate that fixes only train cases is rejected.

- **Mine external repos' fixed issues into bench cases** — FEATURE — value 4 — effort L — risk med — category: benchmark corpus
  Why: 8 cases from one project is a narrow corpus. The same builder (parent commit, request, hidden tests) works on any local git repo with a fix commit that adds a test. Public https only, via the existing fetch rules.
  Done when: `fm bench mine <repo-path>` yields at least 3 valid fail-to-pass cases from a fixture repo, each verified to fail at the parent and pass at the commit.

- **Wild: Mutate finished tasks adversarially to grow the bench** — FEATURE — value 4 — effort L — risk med — category: synthetic cases (wild)
  Why: finished tasks are a finite supply. Reverting a commit's fix, then also mutating the request (vaguer wording, a misleading hint, a distractor file, a renamed symbol) produces harder variants of the same case that test how well `capture → expand → ground` copes with ambiguity.
  Done when: `fm bench mutate CASE --kind vague|decoy|rename` writes a new case that still fails at baseline and passes with the reference solution, and the original case's verify is unchanged.

- **Wild: Replay real past sessions as counterfactuals against a candidate guard and drive loop** — FEATURE — value 4 — effort L — risk med — category: counterfactual replay (wild)
  Why: `fm replay` already replays shell commands through the guard; the friction digest records 21 drive waits and 5 mod-reload stops. Extending replay to the drive and hook decisions (Stop, next-action) would estimate how many wasted turns a change removes without running a model.
  Done when: `fm replay --drive` computes the number of Stop-hook turn-ends from recorded events under the current and a candidate drive policy, and a fixture shows a policy change reducing the count.

- **Wild: Run a continuous self-bench that grades Foreman nightly and plots the trend** — FEATURE — value 3 — effort M — risk med — category: regression tracking (wild)
  Why: the user keeps asking for recursive improvement and "don't stop", but only improvement is gated, never decay. A scheduled low-cost run (`schedule` skill is installed) on a rotating subset would catch drift from plugin updates or Claude Code changes. Cost matters, so it is capped by a weekly budget and skipped in economy mode.
  Done when: a scheduled `fm bench run --rotate 2` appends to `bench/history.jsonl`, the dashboard shows a pass-rate sparkline, and it skips itself past 80% usage.

- **Wild: Make a "best-of-bench" leaderboard comparing Foreman against bare Claude Code and other harness plugins** — FEATURE — value 3 — effort M — risk low — category: comparative benchmark (wild)
  Why: the user asked to research other plugins and add what is best; the landscape research (Aider, Spec Kit, superpowers, Task Master) found many claims but no head-to-head measure. `fm bench run` already accepts a candidate plugin config, so baselines are cheap to add.
  Done when: `fm bench compare --baseline bare` reports Foreman against no plugin on all cases, with a verdict on whether the discipline layer pays for its token overhead.

- **Attribute each bench failure to a pipeline stage** — FEATURE — value 3 — effort M — risk low — category: diagnosis
  Why: a failed replay currently says only fail. Tagging the failure by stage (never grounded the right file, plan missed the criterion, execute edited the wrong place, verify passed falsely) turns a score into a pointer for `fm friction` and `improve`.
  Done when: `fm bench run` output includes a `failed_at` stage per failed case, derived from events and the diff, and a fixture failure is labelled correctly.

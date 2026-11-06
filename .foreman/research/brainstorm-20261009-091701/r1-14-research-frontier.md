# Brainstorm — lens: research frontier

- **Catch vacuous verifies with mutation probes** — FEATURE — value 5 — effort M — risk low — category: verification
  Why: T-0342's criterion used `-k a or b`, which run.py ignores, so it ran no tests and still "passed". Recorded evidence can be empty.
  Done when: `fm task done` mutates the changed lines in a scratch worktree and refuses any criterion whose verify still passes on every mutant. A test that replays the `-k` case is refused.

- **Prove behaviour preservation for CLEAN tasks** — FEATURE — value 5 — effort L — risk med — category: verification
  Why: the user steered that cleanup requests (dead code, replaced functionality) never got done, and refactors are the least provable work. Assumption: command and API outputs can be recorded.
  Done when: before a CLEAN edit Foreman records golden traces (CLI outputs, hook decisions, test results) at the old HEAD. The gate replays them at the new HEAD and reports every diff as intended or unintended.

- **Track replacement debt to closure** — FEATURE — value 4 — effort M — risk low — category: cleanup
  Why: the same steer, plus evidence that nothing ties "X replaces Y" to "Y is deleted".
  Done when: a task that supersedes code opens a removal obligation, found by static reachability plus coverage. `fm next` surfaces it until the dead code is gone or waived with a reason.

- **Abstract-interpret shell for effects in the guard** — SECURITY — value 5 — effort L — risk med — category: guard
  Why: the guard keeps getting patched case by case: `bash -lc`, symlink `rm`, `python -c`, and T-0275 (script files) is deferred. Assumption: a bounded effect-set model of a shell AST can be built and checked against the real-bash differential tests.
  Done when: each command resolves to a set of effects (writes, deletes, network, exec) with paths followed through symlinks and script files. The 5000-command replay shows fewer false refusals and no new misses.

- **Ask the user only when sampled plans disagree** — FEATURE — value 4 — effort M — risk med — category: autonomy
  Why: autonomy has two modes, "standard" asks for L plans and "full" never asks. Assumption: disagreement across N cheap planning samples predicts a wrong plan.
  Done when: Foreman samples N plan sketches, escalates only above a disagreement threshold, and `fm bench` shows fewer asks at equal first-time pass rate.

- **Weight reviewers by measured precision** — FEATURE — value 4 — effort M — risk low — category: review
  Why: `fm second`, the T-0034 audit and `fm bench` exist, but no reviewer or model has a track record. T-0217 already wants lesson confidence.
  Done when: each lens or model gets a precision and recall score from past findings against later outcomes. The merged audit orders findings by that weight, and `fm digest` shows the scores.

- **Run lanes across machines** — FEATURE — value 4 — effort L — risk high — category: orchestration
  Why: the ambition names multi-machine work, and `fm serve`, `fm session` and `fm lane` already exist per device. Assumption: devices share a git remote.
  Done when: `fm lane new T-x --on <device>` runs the builder remotely and `fm lane merge` lands it with its recorded evidence.

- **Schedule the queue from predicted cost and risk** — FEATURE — value 4 — effort M — risk low — category: scheduling
  Why: the ledger holds cost, grades, blocks and pace, and the drive picks queued work with no model of cost. The user wants no limits before 75% usage.
  Done when: a predictor trained on finished tasks gives tokens, time and block probability per queued task. The drive orders by value against predicted spend, and backtests on history beat FIFO.

- **Explore the product as a learned user (wild)** — FEATURE — value 5 — effort L — risk med — category: product check
  Why: wild. The user asked that "Foreman checks the product the way its user uses it". `fm smoke` only walks fixed scripted paths.
  Done when: an agent learns journeys from real session logs and click traces, then explores variants in the headless browser at desktop and phone sizes. It files each console error or dead end as a captured request with a repro.

- **Replay sessions deterministically to find the first wrong step (wild)** — FEATURE — value 4 — effort L — risk med — category: debugging
  Why: wild. `fm surprise` logs where the model of the code was wrong, but only after the fact. Assumption: tool calls plus a filesystem snapshot are enough to replay.
  Done when: `fm replay-session <id> --bisect` re-executes tool calls on an overlay copy and names the first step where the repo diverged from the passing state.

- **Dream at night over the day's work (wild)** — FEATURE — value 4 — effort M — risk low — category: learning
  Why: wild. `fm night` runs budgeted work and the user wants recursive self-improvement. Counterfactual replay of the day's tasks is unused.
  Done when: each night a child re-plans the day's costliest or blocked tasks with hindsight and writes candidate playbooks or lessons. Each one is accepted only if `fm bench` improves.

- **Train Foreman against synthetic failures (wild)** — FEATURE — value 4 — effort L — risk med — category: self-improvement
  Why: wild. `fm evolve` and `fm bench` only use real finished tasks, which are few. Assumption: failure modes from `fm evals` can be turned into small sandbox repos.
  Done when: Foreman generates N adversarial tasks per lesson in disposable repos, and a candidate instruction change must pass them plus the existing bench to be kept.

- **Compile acceptance criteria into executable contracts** — FEATURE — value 4 — effort M — risk med — category: verification
  Why: `fm oracle` yields examples from the spec but stops there, and the criteria's verify commands are hand-written.
  Done when: each criterion gets a generated property or differential test that runs red on the old code and green on the new. `fm task done` stores the red→green pair as evidence.

- **Radar for intent drift against briefs and vetoes** — SECURITY — value 3 — effort M — risk low — category: focus
  Why: Foreman's core promise is staying on the task, and vetoes are only matched against commands and edits.
  Done when: after each edit batch a cheap judge scores the diff against the brief, its criteria and the vetoes, and flags drift into a captured request. A seeded off-task edit is caught in a test.

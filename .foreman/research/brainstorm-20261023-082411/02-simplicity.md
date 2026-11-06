# Brainstorm — lens: simplicity

- **Collapse the install flags into one default path** — CLEAN — value 4 — effort S — risk low — category: install
  Why: `install.sh` takes ten flags (`--security`, `--docs`, `--apply-conflicts`, `--no-plugins`, `--bypass`, `--no-bypass`, `--no-mod`, `--no-wiring`, `--build`, `--desktop`), and it still asks about bypass mode and the rest. Assumption: most users want the defaults.
  Done when: a fresh install with no flags reaches a working `fm`, passes `fm doctor`, and the flag list fits on one screen.

- **Cut the rules file under budget by deleting, not rewording** — CLEAN — value 4 — effort S — risk low — category: docs
  Why: the pack says the rules file has been 6,416 characters against a 6,400 budget since T-1520. Trimming by rewording only moves the problem.
  Done when: `fm doctor` reports the rules file under budget, and every rule that remains is still referenced by a test or a hook.

- **Give bare `fm` one next command** — FEATURE — value 4 — effort S — risk low — category: cli
  Why: the verb list has grown to about a dozen top-level commands (`code`, `dojo`, `scout`, `quiet`, `check --affected`, `usage`, `which`, `help`, `new`, `design lint`, `demo`, `run`, `serve`). Bare `fm` already reports status, so it can name one action.
  Done when: bare `fm` in a project prints exactly one suggested command, and `fm help` groups verbs under five or fewer headings.

- **Retire verbs nobody runs** — CLEAN — value 3 — effort M — risk med — category: cli surface
  Why: `fm usage` already counts uses. The `dojo` help-position clash broke `test_help`, which shows the verb table is hard to keep consistent. Assumption: a few verbs have near-zero use.
  Done when: `fm usage` over 30 days shows every remaining verb with at least one use, and each removed verb prints a one-line redirect for one release.

- **Merge overlapping skills into one entry per job** — CLEAN — value 4 — effort M — risk med — category: skills
  Why: `skills lint` flags overlapping descriptions, and the trigger eval requires that each phrased request has one clear best match. The planned debugging, release and research job skills should replace older playbook entries, not sit beside them.
  Done when: the trigger eval gives each phrased request one best skill with no tie, and the skill count is lower than before.

- **Shrink config to three settings** — CLEAN — value 3 — effort M — risk low — category: config
  Why: install writes a statusLine wrapper, deny rules, a Stop-hook cap, a CLAUDE.md block, a rules symlink, an `fm` link and a manifest. Assumption: most users only care about permission mode, guard strictness and queue continuation.
  Done when: `fm config` shows three settings, and every other setting has a default that the install manifest can reproduce.

- **Show the pane's default view as one line** — CLEAN — value 3 — effort M — risk low — category: ui
  Why: the pane currently shows the work bar, stage rail, steps, Activity lanes, Agents graph, History and Today charts. Assumption: most of the time a user only wants the current task, stage and next command.
  Done when: the default pane view fits in three rows, and one keystroke opens the full view.

- **Serialize checks per project, not per machine** — FIX — value 4 — effort S — risk med — category: checks
  Why: a full `fm check` waited on a machine-wide gate lock held for over 40 minutes by a hung check in another project. `fm check --affected` queues behind unrelated builders, and the 15-minute wait cap is a workaround for that design.
  Done when: two builders in different projects run `fm check` at the same time with no wait, and two runs in the same project queue with a visible message.

- **Make the hook bench one median verdict** — CLEAN — value 3 — effort S — risk low — category: performance
  Why: PreToolUse:Bash p95 measured about 310 ms on a loaded machine and about 272 ms on a quiet one, against a 300 ms budget. The p95 threshold flakes on noise.
  Done when: the bench reports one verdict from the median of 20 runs, prints the load it ran under, and fails only when that median exceeds budget.

- **Reset stuck state with one command** — FEATURE — value 3 — effort S — risk low — category: recovery
  Why: a stale edit lease blocked the next run on the same code for 20 minutes, because `drop_session` ran only for worker runs. The state lives on disk, so a single reset verb is a small addition.
  Done when: after a crashed run, `fm reset` clears leases and the next run starts within a minute.

- **Generate the deny rules from the guard's own list** — CLEAN — value 3 — effort S — risk low — category: guard
  Why: install writes deny rules for catastrophic commands separately from the guard hook. Two lists drift apart. Assumption: the deny list and the guard list describe the same commands.
  Done when: one list drives both, and a test fails if they diverge.

- **Reduce the two modes to two names** — CLEAN — value 4 — effort M — risk med — category: modes
  Why: drive mode, full auto, `fm run`, `fm serve` and bypass all change how much Foreman does unattended. Assumption: users think in terms of "ask me" and "keep going".
  Done when: the docs name exactly two modes, and each maps to one set of settings that a test checks.

- **Wild: keep one STATE.md that is the whole product state** — FEATURE — value 3 — effort S — risk low — category: visibility
  Why: state already lives on disk. A single file showing the current task, next step and last proof would let anyone, human or model, read Foreman's state in one minute. Marked wild: it's an unexpected interface for an orchestrator.
  Done when: `STATE.md` regenerates after each `fm` verb and stays under 40 lines.

- **Wild: ship Foreman as one dependency-free file** — CLEAN — value 4 — effort L — risk med — category: install
  Why: the installer exists mainly to get Python 3.12.7 or newer, through Homebrew or `uv`. A single bundled executable would remove that branch. Marked wild: it changes how the product is packaged, not what it does.
  Done when: on a machine with only `git` and `claude`, one downloaded file runs `fm demo` successfully.

- **Wild: add `fm prune` to propose removing the least-used feature** — FEATURE — value 2 — effort M — risk low — category: maintenance
  Why: `fm usage` and the test suite already show which features are used and tested. Marked wild: Foreman audits its own surface and proposes its own deletions, with the tests that would go with them.
  Done when: `fm prune` lists one candidate with its usage count and the tests that would be removed, and makes no change without confirmation.

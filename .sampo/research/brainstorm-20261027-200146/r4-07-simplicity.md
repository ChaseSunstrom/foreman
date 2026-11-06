# Brainstorm — lens: simplicity

- **Collapse deferral targets to a duration or `reset`** — CLEAN — value 4 — effort S — risk low — category: deferrals
  Why: T-1802 came from parsing local times, and the weekly case is the one that matters. The `--until` form is a second path to maintain. Assumption: most deferrals are either "for N hours" or "until the reset."
  Done when: `fm task defer T-n reset` lands on the next reset time in a test, and `--until` remains only as a one-release alias that prints a deprecation line.

- **Cut the three settings scopes to project plus a per-run override** — CLEAN — value 3 — effort S — risk low — category: settings
  Why: T-1611 added "this run, this project, everywhere" plus repo policy pins, which is four places a value can come from. Assumption: "everywhere" is rarely the reason a setting was changed.
  Done when: one function resolves a setting from run then project then the built-in default, and a test shows the precedence order.

- **Cut `fm extras` to the one piece people ask for** — CLEAN — value 2 — effort S — risk low — category: scope
  Why: T-1556 shipped a zine, a vase, cursor choreography, a Breakout game and sonic recipes. Each is a surface to test and keep working. Assumption: no user request names any of them.
  Done when: the extras menu lists at most one entry, and the removed modules are gone with their tests and docs.

- **Render the glance line from one function for desk, pane and web** — CLEAN — value 3 — effort S — risk low — category: surfaces
  Why: the recent desk card, the Foreman pane and the web UI each draw the same work bar, state and count, separately. Assumption: the three copies have already drifted, though I have no direct evidence of that.
  Done when: a snapshot test of one status fixture yields identical text from all three renderers.

- **Show exactly four keys in the terminal UI, always** — FEATURE — value 3 — effort S — risk low — category: terminal UI
  Why: the stalled card alone has `w`, `k` and `m`, and `g` is a separate key. A user who has to remember the key set is paying for complexity the screen could show. Assumption: the other keys are rarely used.
  Done when: the footer renders exactly four key labels, and each one maps to a single action covered by a test.

- **Make the stalled card a yes-or-no prompt** — FEATURE — value 3 — effort S — risk low — category: recovery
  Why: the stalled card offers wait, kill and switch-runner, and each needs a separate decision. Assumption: most stalls end with either "keep waiting" or "stop."
  Done when: the card offers "continue" and "stop" by default, and a test shows that pressing Enter alone takes the default.

- **Require one proof form per task: a command that fails before the change and passes after** — CLEAN — value 4 — effort M — risk low — category: proof
  Why: `fm task prove` already shows a test failing before the change. Several proof shapes multiply the checks in `fm task finish`. Assumption: most tasks already use the fail-then-pass form.
  Done when: `fm task finish` refuses a task whose proof lacks a before-fail and after-pass pair, and a test covers the refusal.

- **Wild: a bare sentence queues a task** — FEATURE — value 4 — effort S — risk med — category: capture
  Why: `fm "fix the parser"` would record the same task as the full `task add` form, so the user writes no verb and no flags. Assumption: users mostly type a request in one line.
  Done when: `fm "<sentence>"` writes a queued task with the same record as `fm task add`, and a test checks the two outputs match.

- **Wild: the queue is one markdown file a person can edit** — FEATURE — value 4 — effort M — risk med — category: state
  Why: the backlog, journal and status are separate state files with their own formats. A single editable list would let a user reorder or drop work in any editor. Assumption: the journal can be derived from the list rather than stored beside it.
  Done when: editing the list's order in a text editor changes `fm status` output on the next command, and a test round-trips the file with no loss.

- **Wild: a repo with no config still runs on built-in defaults** — FEATURE — value 3 — effort M — risk med — category: onboarding
  Why: a rules file and a `.foreman.toml` are both needed before the first run. Assumption: the built-in defaults are safe for most repos.
  Done when: `fm check` passes on a fixture repo with no config files, and the output names the defaults it used.

- **Give the close receipt one sentence the user can paste as a commit body** — FEATURE — value 2 — effort S — risk low — category: receipts
  Why: the receipt today is several lines of proof and cost. Assumption: most users copy only the outcome into their history.
  Done when: `fm task finish` prints a single sentence, and a test checks that it contains the task id and the proof result.

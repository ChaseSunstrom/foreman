# Brainstorm — lens: simplicity

- **Collapse to four verbs: status, next, decide, ship** — CLEAN — value 5 — effort M — risk med — simplicity
  Why: the pack lists dozens of verbs (`map`, `doctor`, `lane`, `run`, `code`, `kalevala`, `genus`, `exam`, `decide`, `ask`, `run-brief`…) and a standing rule that every capability must be "called by a real session path," implying most verbs exist but rarely get invoked. A user who never read MASTER.md (a standing-rule surface) is lost. Four verbs cover the loop: see state, pick work, let the model choose, push.
  Done when: a cold child can run a full task close using only these four verbs from `--help` alone, and `sampo doctor` reports the unused-verb count as a lean line.

- **One screen, one question: `sampo status` answers "what do I need to do?"** — CLEAN — value 5 — effort S — risk low — simplicity
  Why: the user keeps asking for morning cards, panes, trees, charts; the pack shows a live UI with "work bar, stage rail and steps, Activity lanes, Agents graph, History and Today charts." Too many surfaces to read. One line: "3 lanes running, 1 blocked on you (grant shellcheck), next: T-3352."
  Done when: `sampo status` is ≤ 5 lines, no scrolling, and the user can state the blocked item from it without opening the web UI.

- **One config knob per project, not per capability** — CLEAN — value 4 — effort M — risk low — simplicity
  Why: open work shows per-capability flags (`--round-first`, `--pace`, `--parallel`, `--model`, per-lane Ward profile, per-slot model choice). A user tuning Sampo touches 10+ settings. A single `sampo profile <name>` (default, fast, cautious, unattended) sets them all, with `sampo profile show` to see the resulting values.
  Done when: a new project needs exactly one command (`sampo profile default`) to work, and `sampo profile` lists the only knobs a user ever edits.

- **One "off" switch that actually turns Sampo off** — CLEAN — value 4 — effort S — risk low — simplicity
  Why: standing rule "Foreman isn't specific to Claude Code" and "Sampo can work with no claude on PATH" imply a minimal mode, but the pack shows no single kill switch. `sampo off` (and `on`) disables hooks, drive, and injection in one call, with `sampo doctor` showing the state.
  Done when: `sampo off` leaves zero Sampo hooks registered and `sampo on` restores the exact previous state, verified by a before/after `fm doctor` diff.

- **Delete the `fm` binary; it's `sampo` with a prefix** — CLEAN — value 3 — effort M — risk med — simplicity
  Why: the pack maps both `plugin/bin/fm` and `plugin/bin/sampo`, and a standing rule says "every old name keeps working." Two entry points double the docs, the aliases, the rename-migration surface (T-2967 just fixed a rename bug). Keep the shim for compatibility, but all new work, docs, and examples use only `sampo`.
  Done when: no new commit touches `fm` except the shim, and `sampo --help` is the only place a user learns the verbs.

- **One "what I did" receipt at every close, not a dashboard** — CLEAN — value 4 — effort S — risk low — simplicity
  Why: the pack shows History, Today charts, the Tower, the Genesis site, the morning card — many places to learn what happened. A single 3-line receipt in the terminal at close: "T-3352 done. Touched 2 files. Test green. Next: T-3353." No dashboard needed for the 90% case.
  Done when: every `samo task finish` prints exactly 3 lines, and the web UI is optional (never required) to know what just happened.

- **One page of docs: "Sampo in 10 sentences"** — CLEAN — value 4 — effort S — risk low — simplicity
  Why: the pack references MASTER.md, README.md, site/, skills/, docs/ — a newcomer faces 5+ documents. The standing rule "the user who never read MASTER.md" needs a 10-sentence page that says what Sampo is, what it does, the one config knob, the four verbs, and the one off switch. Everything else is deep-dive.
  Done when: a cold child reads only `DOCS.md` (≤ 10 sentences + 1 example) and can install and run a task without opening any other file.

- **One error format: "what failed, why, what I can do"** — CLEAN — value 4 — effort S — risk low — simplicity
  Why: the pack shows diverse error styles (Ward refusals, guard misses, hook timeouts, CI timeouts, model endpoint errors). A user facing a failure needs one shape: the verb that failed, the reason in plain words, and the one command that fixes it. No stack traces unless `--verbose`.
  Done when: every `sampo` error output matches a 3-line template, and `samo doctor` can parse every error line it has ever seen.

- **One model choice, not a ladder** — CLEAN — value 4 — effort M — risk med — simplicity
  Why: the pack shows a ladder of models (4B, 12B, 27B, Haiku, Sonnet, Opus) with per-task routing, per-lane profiles, and a "dumbest model that passes" card. A user should choose one model (`samo profile model=local` or `model=frontier`) and trust Sampo's internal routing. The ladder is an implementation detail, not a user-facing knob.
  Done when: the user-facing config has one `model` field, and `samo profile` shows the resolved model without exposing the ladder.

- **One "samo init" that sets up everything** — CLEAN — value 4 — effort S — risk low — simplicity
  Why: the pack shows install.sh, `fm doctor`, per-harness plugin shims, per-machine estate files, per-project state directories. A new user runs 5+ setup steps. `samo init` detects the harness, installs the right plugin, sets the profile, creates the state directory, and prints "ready." No manual steps.
  Done when: a fresh clone + `samo init` + `samo status` works with zero manual file edits, and `samo doctor` reports zero setup errors.

- **One "samo replay" that shows the last task, not a log** — CLEAN — value 3 — effort S — risk low — simplicity
  Why: the pack shows transcripts, ledgers, lane artifacts, and a web UI history. To debug "what just went wrong," a user should run `samo replay` and see the last task's plan, steps, and outcome in 10 lines. Not a log file, not a web page.
  Done when: `samo replay` prints ≤ 10 lines for the most recent task, and a cold child can identify the failure from it without opening any other file.

- **One "samo ghost" that proves Sampo isn't in the way** — CLEAN — value 3 — effort S — risk low — simplicity
  Why: the pack shows Sampo injecting context, running hooks, and filing tasks autonomously. A user should be able to ask "is Sampo helping or getting in the way?" and get a one-line answer: "Last week: 12 tasks closed with Sampo, 3 blocked on Sampo, 0 blocked by the model." No dashboard.
  Done when: `samo ghost` prints one line with 3 numbers, and the user can answer "is it worth it?" from that line alone.

- **Wild: Ship Sampo as one signed file — the model is the product's core, not a feature** — CLEAN — value 4 — effort L — risk high — simplicity
  Why: the pack shows a plugin with 1396 skill files, 454 tests, 263 lib files, a web UI, a site, and a local model. A user installing Sampo should get one file: `sampo` (a single signed binary that includes the model, the hooks, and the minimal state). No install script, no plugin marketplace, no separate model download. The model is baked in.
  Done when: `curl | sh` downloads one signed file, and `samo status` works with no other files on disk, no network call, and no plugin registration.

- **Wild: The decider is a readable rulebook, not a black box** — CLEAN — value 5 — effort M — risk low — simplicity
  Why: the user asked for "Sampo's own trained model(s), a better Kev-style decider" and "how it improves every Rune generation." A black-box model that the user can't read, can't audit, and can't trust is the opposite of simplicity. The decider should be a set of readable rules (or a small model with a human-readable explanation per decision) that the user can open, read, and edit. "I don't know, here's why" is a first-class answer.
  Done when: every decider decision prints a one-line rule or explanation the user can read, and `samo decide explain <decision>` shows the rule that fired, in plain English.

- **Wild: Collapse the whole stack to three verbs: `samo ask`, `samo run`, `samo stop`** — CLEAN — value 5 — effort L — risk high — simplicity
  Why: the standing rule "never interrupt the user mid-run" and "don't stop or skip work for budget" imply a fire-and-forget model. The user's mental model is "I ask, it runs, I stop when done." Everything else (lane, drive, kalevala, genesis, exam) is Sampo's internal work. Three verbs: `samo ask "do X"` files the task, `samo run` starts the drive, `samo stop` halts it. No other verbs in the user's mental model.
  Done when: a new user can run a full task cycle with only `ask`, `run`, and `stop`, and `samo --help` lists exactly three verbs (with `status` as a bonus).

Next question: What is the *smallest* set of verbs a user who has used Sampo for 6 months actually calls — can we list it from the ledger, and does it match the 3–4 verbs above?
Next question: What does the user's *first* 10-minute session look like, and which of the 5+ setup steps in the pack are actually load-bearing vs. vestigial?

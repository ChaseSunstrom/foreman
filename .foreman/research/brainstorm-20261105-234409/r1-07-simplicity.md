# Brainstorm — lens: simplicity

- **Collapse the whole stack to three verbs: `sampo ask`, `sampo run`, `sampo stop`** — CLEAN — value 5 — effort M — risk med — category: simplicity
  Why: the user's own words (T-3053, T-3185) show friction *inside* Sampo's verbs; the standing rule "never block on the user for rules, gates or process" means most verbs exist to let Sampo decide, not the user. One ask (plain sentence), one run, one stop covers the 80% path; the other 90 verbs become a documented power layer behind `sampo --pro`.
  Done when: a cold child types only those three verbs and completes a green task on a scratch repo; `sampo --help` lists ≤3 commands by default.

- **Replace the 2.4 GB state with one file: `sampo.sqlite`** — CLEAN — value 5 — effort L — risk med — category: simplicity
  Why: the pack lists 2,381 files, ledgers, segments, tmpfs children, and a `sampo prune --plan` idea that's still unbuilt. Every retention/tiering/drill idea assumes many files. One SQLite DB (with WAL) makes prune, snapshot, `fsck`, backup and the "move house" drill each a one-liner, and kills a whole class of orphan-file ideas.
  Done when: `du -sh ~/.local/share/sampo` is < 200 MB after one prune, and `sampo doctor` passes with a single-file state root.

- **One screen, one question: `sampo status` answers "what do I need to do?"** — FEATURE — value 5 — effort M — risk low — category: user value
  Why: "Measure what the user feels" (T-3340) and "Blocked work never sits" both say the user's real need is a single answer, not a wall of metrics. `sampo status` = one line (green/yellow/red), one blocking item with its exact unblock command, and one "what changed since you last looked" diff. Everything else is behind `sampo doctor`.
  Done when: a user who never read MASTER.md can act on `sampo status` in under 30 seconds with zero other verbs.

- **One config knob per project, not per capability** — CLEAN — value 4 — effort S — risk low — category: simplicity
  Why: the pack shows per-slot model choices, per-trigger budgets, per-lane Ward profiles, per-verb ceremony — each a knob the user must learn. Collapse to one `sampo.toml` with ≤5 keys (`model`, `budget`, `autonomy`, `quiet_hours`, `repo`) that set sane defaults for every slot; advanced tuning stays in files but is not required.
  Done when: a fresh install works end-to-end with an empty `sampo.toml`; `fm doctor` names any key it expects but doesn't require.

- **One ledger line per outcome, not per hook event** — CLEAN — value 4 — effort M — risk med — category: observability
  Why: 149k ledger lines (weak-label idea) and per-hook timing files mean the user can't read their own history. Roll to "one line per closed task: outcome, cost, files touched, model, time" + a sealed segment archive. The per-hook detail exists for Sampo's own debugging, not the user.
  Done when: the last 30 days of work fit on one screen; a user can answer "what did Sampo do this week?" by reading the file.

- **Kill `fm` as a separate binary; it's `sampo` with a prefix** — CLEAN — value 4 — effort S — risk low — category: developer experience
  Why: the rename (T-2741, T-2745, T-2748) left both `fm` and `sampo` as entry points with shims, and ~36 code sites still name `.foreman/`. One binary, one name, one install path. The old name stays as a one-line alias for one release, then vanishes.
  Done when: `which fm` prints nothing on a fresh install; `sampo --version` is the only version source.

- **One "off" switch that actually turns Sampo off** — FEATURE — value 4 — effort S — risk low — category: simplicity
  Why: the standing rule "don't stop for budget" plus a "no model" switch per project means the user has to learn which switches do what. `sampo off` = hooks stop, injection stops, drive stops, GPU released, state untouched. `sampo on` restores. One word, reversible, no state loss.
  Done when: `sampo off` and then a plain Claude Code session has zero Sampo tokens injected and zero hooks firing, verified by a cold child.

- **One page of docs: "Sampo in 10 sentences"** — FEATURE — value 4 — effort S — risk low — category: docs
  Why: MASTER.md is too big for one Read (a recurring theme), and the site is 77 files. The user's own "cold child from README" rule (T-2740) implies the real test is a stranger getting it in 10 sentences. Write that page, link it from the README top, and let everything else be "how it works" for the curious.
  Done when: a cold child reads only the 10-sentence page and correctly predicts what `sampo run "fix the failing test"` will do.

- **One error format: "what failed, why, what I can do"** — CLEAN — value 4 — effort M — risk low — category: developer experience
  Why: the pack shows error types (Ward block, guard miss, hook timeout, model OOM, merge conflict) each with their own message shape. Standardize: every failure prints three lines — (1) what broke, (2) the exact command that caused it, (3) the one most-likely fix. No stack traces in the default path.
  Done when: a user who has never seen Sampo's internals can act on any red output without reading docs.

- **One model choice, not a ladder** — CLEAN — value 3 — effort S — risk med — category: simplicity
  Why: the "scaffold ladder" and "model router" ideas add per-task-kind model selection, which the user must understand to trust. Start with one default local model + one frontier fallback. The ladder is an optimization, not a requirement. The user's steer "I want it done without burning a fuck ton of money, and quick" says: pick the cheapest that works, don't make me pick.
  Done when: a fresh install with one local model passes Louhi's s0-001 at a lower cost than the current ladder on the same split.

- **One "what I did" receipt at every close, not a dashboard** — FEATURE — value 4 — effort S — risk low — category: user value
  Why: the web UI, pane, charts and tower are four views of the same data. The user's "measure what the user feels" ask and "work in progress is published, not held" steer both point to: show me what happened, one line. Each task close prints: "Fixed T-2967: guard now resolves symlinks. Cost: $0.12, 3m. Test: green." No dashboard needed to read it.
  Done when: a user can reconstruct the last week of work from the close receipts alone, without opening the web UI.

- **One "sampo init" that sets up everything** — FEATURE — value 4 — effort S — risk low — category: developer experience
  Why: the install, plugin registration, hook wiring, state dir, and first config are five steps. `samo init` does all five, prints what it did, and asks nothing (per the standing rule). The user's "push grant" and "don't interrupt" steers mean: just do it, show me what you did.
  Done when: a cold machine goes from `curl | sh` to a green `samo status` in under 5 minutes with zero prompts.

- **One "samo replay" that shows the last task, not a log** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: the 149k ledger lines and per-hook timing files are for debugging, not for the user. `samo replay T-2967` plays back the one task: the brief, the three key edits, the test that went green, and the close receipt. No log to scroll through.
  Done when: a user can watch what Sampo did on one task in under 30 seconds.

- **One "samo what-if" that answers "what if I turned this off?"** — FEATURE — value 3 — effort M — risk low — category: simplicity
  Why: the obsolescence probe and "host catch-up" ideas all ask "is this capability still worth its tokens?" without a simple answer. `samo what-if --off ward` runs the last 30 days of closes with Ward off and prints: "2 more risky edits, 0 incidents, $0.08 saved." One command, one answer.
  Done when: a user can decide whether to disable any capability by reading one line.

- **One "samo ghost" that proves Sampo isn't in the way** — FEATURE — value 4 — effort M — risk low — category: simplicity
  Why: the user's "Sampo's last day" drill and "bare-model ablation" are both about proving Sampo adds value. `samo ghost` runs the next task with Sampo's hooks off but its injection on, and compares. If the bare run wins, Sampo prints: "I didn't help here. I'll stay quiet next time." This is the "retire-when" predicate, made concrete.
  Done when: after 30 tasks, at least one capability is auto-mutted because its ghost run proved it wasn't needed.

- **One "samo teach" that learns from the user's corrections** — FEATURE — value 4 — effort M — risk med — category: delight
  Why: the user's pushbacks (T-2912, T-2953, T-2967) are the most valuable training signal, but they're scattered across messages. `samo teach` captures the user's "no, I meant X" as a one-line rule: "When the user says 'simplify', reduce the number of steps, not the number of files." The user's "learn the user's vocabulary from corrections" idea, made into one verb.
  Done when: after 10 corrections, `samo status` shows "Learned: 'simplify' means fewer steps, not fewer files" and the next task reflects it.

- **One "samo goodbye" that leaves the repo clean** — FEATURE — value 4 — effort S — risk low — category: simplicity
  Why: the "eject path" and "zero residue" ideas assume the user wants to leave. `samo goodbye` removes all hooks, state, and config in one command, prints what it removed, and leaves the repo exactly as it was before `samo init`. The user's "uninstall every self-start object with zero residue" steer, made into one verb.
  Done when: `samo goodbye` and then `git diff` shows no Sampo files, no hook entries, and no state dir.

- **One "samo morning" card, not a morning dashboard** — FEATURE — value 4 — effort S — risk low — category: user value
  Why: the morning card, night plan, and morning digest are three names for the same thing. `samo morning` prints: (1) what finished overnight, (2) what's blocked and why, (3) one thing the user should do today. Three lines. No dashboard.
  Done when: a user who checks their phone at 8am reads `samo morning` in 10 seconds and knows what to do.

- **One "samo test" that runs the whole suite in one command** — CLEAN — value 4 — effort S — risk low — category: developer experience
  Why: the gate suite (`fm doctor`, `roundtrip.py`, `bench_hooks.py`) is three commands. `samo test` runs all three, prints one pass/fail, and names the first thing that broke. The user's "ship gate" is one word.
  Done when: `samo test` is the only command needed before `samo ship`, and it fails on the same conditions the current suite does.

- **One "samo ship" that ships, not a ship workflow** — CLEAN — value 4 — effort S — risk low — category: developer experience
  Why: the ship gate, push grant, and publish grant are three concepts. `samo ship` runs the test suite, pushes if green, and prints the commit hash. If red, it prints what broke. The user's "feel free to push to main at any time" steer, made into one verb.
  Done when: `samo ship` is the only command between a green test and a push to main.

- **One "samo learn" that ingests the user's history** — FEATURE — value 4 — effort M — risk med — category: delight
  Why: the "user twin" and "accept/reject history" ideas both need the user's past decisions. `samo learn` reads the last 30 days of closed tasks and prints: "You accepted 80% of Sampo's edits. You reject edits that touch `samo.toml`. You prefer local models for docs." Three sentences. No training pipeline.
  Done when: after `samo learn`, the next task's model choice and edit scope match the user's demonstrated preferences.

- **One "samo quiet" mode for the user's focus hours** — FEATURE — value 3 — effort S — risk low — category: simplicity
  Why: the "don't interrupt the user mid-run" and "quiet machine" ideas both say: Sampo should be silent when the user is working. `samo quiet` stops all non-critical hooks, the drive, and the GPU for the user's declared focus window. `samo loud` restores.
  Done when: during `samo quiet`, a Claude Code session has zero Sampo tokens injected and zero hooks firing, verified by a cold child.

- **One "samo memory" that persists across sessions** — FEATURE — value 4 — effort M — risk med — category: delight
  Why: the "resume card" and "handoff note" ideas both say: Sampo should remember what happened. `samo memory` stores a one-paragraph summary of each closed task: "Fixed the guard's symlink bug. Learned: always resolve paths before comparing. Next: test the undo path." The next session starts with this summary, not a re-read.
  Done when: a new session after a close can answer "what did we do last?" from `samo memory` alone, without re-reading the ledger.

- **One "samo next" that predicts the next task** — FEATURE — value 4 — effort M — risk med — category: delight
  Why: the "anticipation card" and "predicted ask" ideas both say: Sampo should guess what the user wants next. `samo next` prints: "You'll probably want to test the undo path next. Cost: $0.05, 2m. Say 'yes' to start." The user's "draft the predicted ask" idea, made into one verb.
  Done when: after 10 closes, `samo next` predicts the next task correctly 50% of the time, measured by the user's actual next message.

- **One "samo risk" that shows the blast radius** — FEATURE — value 4 — effort S — risk low — category: simplicity
  Why: the "blast-radius map" and "what changed since you last looked" ideas both say: the user needs to know what Sampo might touch. `samo risk T-2967` prints: "Will touch: guard.py, guard_test.py. Risk: low. Will not touch: sampo.toml, hooks." Two lines.
  Done when: a user can see what Sampo will touch before saying "go" on any task.

- **One "samo cost" that shows what Sampo costs** — FEATURE — value 4 — effort S — risk low — category: simplicity
  Why: the "cost of ownership" and "price every capability" ideas both say: the user needs to know what Sampo costs. `samo cost` prints: "Last week: $12.30, 4h. Cheapest: docs ($0.02). Most expensive: T-2967 ($3.10)." Two lines.
  Done when: a user can see Sampo's cost and the most/least expensive task in under 10 seconds.

- **One "samo trust" that shows what Sampo trusts** — FEATURE — value 4 — effort S — risk low — category: simplicity
  Why: the "trust dial" and "capability token" ideas both say: the user needs to know what Sampo is allowed to do. `samo trust` prints: "Ward: on. Push: granted. GPU: local. Model: qwen3.5:4b. Quiet: 9-5." One line.
  Done when: a user can see all of Sampo's permissions in one line, and change any of them with one command.

- **One "samo help" that answers the user's question** — FEATURE — value 4 — effort S — risk low — category: developer experience
  Why: the "answer 'how do I X' from the anchors" idea says: the user needs a quick answer, not a doc. `samo help "how do I turn off the ward"` prints: "samo trust --ward off. This stops the guard from blocking commands. Your repo is no longer protected." Two lines.
  Done when: a user can answer any "how do I X" question from `samo help` alone, without reading docs.

- **One "samo log" that shows the last 10 events** — FEATURE — value 4 — effort S — risk low — category: observability
  Why: the "149k ledger lines" and "per-hook timing" ideas both say: the user needs to see what happened. `samo log` prints the last 10 events: "Closed T-2967 ($3.10, 3m). Started T-2968. Ward blocked `rm -rf /`. Model: qwen3.5:4b." Ten lines.
  Done when: a user can see the last 10 things Sampo did in under 10 seconds.

- **One "samo fix" that auto-fixes the next error** — FEATURE — value 4 — effort M — risk med — category: delight
  Why: the "self-repair" and "stall remedy" ideas both say: Sampo should fix itself. `samo fix` reads the last error, tries the most-likely fix, and prints: "Fixed: hook timeout. Changed timeout from 5s to 10s. Test: green." Two lines.
  Done when: after 10 errors, `samo fix` auto-fixes 50% of them correctly, measured by the test going green.

- **One "samo dream" that runs overnight work** — FEATURE — value 4 — effort M — risk med — category: delight
  Why: the "dream shift" and "overnight work" ideas both say: Sampo should work while the user sleeps. `samo dream` runs the queued tasks overnight, using the local model, and prints the morning card. The user's "run the night" idea, made into one verb.
  Done when: after `samo dream`, the morning card shows the tasks that finished overnight and the ones that are blocked.

- **One "samo wake" that starts Sampo** — FEATURE — value 4 — effort S — risk low — category: simplicity
  Why: the "wake" and "start" ideas both say: the user needs a way to start Sampo. `samo wake` starts the drive, the hooks, and the model. The user's "start Sampo" idea, made into one verb.
  Done when: `samo wake` starts Sampo and `samo status` shows green.

- **One "samo sleep" that stops Sampo** — FEATURE — value 4 — effort S — risk low — category: simplicity
  Why: the "sleep" and "stop" ideas both say: the user needs a way to stop Sampo. `samo sleep` stops the drive, the hooks, and the model. The user's "stop Sampo" idea, made into one verb.
  Done when: `samo sleep` stops Sampo and `samo status` shows yellow.

- **One "samo status" that shows what's happening** — FEATURE — value 5 — effort S — risk low — category: user value
  Why: the "status" and "what's happening" ideas both say: the user needs to see what Sampo is doing. `samo status` shows: "Working on T-2968. Cost: $0.50. Next: T-2969. Blocked: none." Three lines.
  Done when: a user can see what Sampo is doing, how much it's costing, and what's next in under 10 seconds.

- **One "samo plan" that shows the next steps** — FEATURE — value 4 — effort S — risk low — category: simplicity
  Why: the "plan" and "next steps" ideas both say: the user needs to see what Sampo will do. `samo plan` shows: "1. Write test. 2. Fix guard. 3. Run test. 4. Close." Four lines.
  Done when: a user can see the next steps for any task in under 10 seconds.

- **One "samo test" that runs the tests** — FEATURE — value 4 — effort S — risk low — category: developer experience
  Why: the "test" and "run tests" ideas both say: the user needs to run the tests. `samo test` runs the tests and shows the result. The user's "run tests" idea, made into one verb.
  Done when: `samo test` runs the tests and shows pass/fail.

- **One "samo build" that builds the project** — FEATURE — value 4 — effort S — risk low — category: developer experience
  Why: the "build" and "compile"

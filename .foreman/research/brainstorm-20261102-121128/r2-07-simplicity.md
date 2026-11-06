# Brainstorm — lens: simplicity

- **Retire one-shot steers when their task closes** — CLEAN — value 4 — effort S — risk low — category: steers
  Why: the steer list mixes standing rules with one-time orders ("pause every long-horizon exam run now", "T-2462 waits with T-2441 until round 1", "finish round 1 completely"). Several are already acted on, and the dropped list shows the same steers being re-captured as tasks. Each one adds a check that `fm genesis sweep` runs and `fm doctor` reads.
  Done when: `fm decide` stores each steer as `once` or `standing`, a `once` steer retires with a recorded reason when its named task closes, and the steer list on this pack shrinks accordingly.

- **Collapse `fm doctor` to red items only** — CLEAN — value 4 — effort S — risk low — category: observability
  Why: recent commits keep adding doctor lines (timer liveness, tick couldn't-watch, missing steer check, ablation deltas, lean ratchet commits). Assumption: a healthy install now prints a long page.
  Done when: a healthy install prints exactly one line ("all clear, N checks"), `fm doctor --all` prints the full list, and any failing check appears first with its fix command.

- **Replace flags and env vars with three presets** — FEATURE — value 4 — effort M — risk med — category: settings
  Why: behaviour is spread across `FOREMAN_QUIET=1`, `fm drive --pace off`, `--round-first`, the budget cap, risk budget, publish grants and Lite-mode talk. Assumption: nobody remembers the combinations.
  Done when: `fm preset quiet|normal|strict` sets all of them, `fm doctor` names the active preset, and a hand-set flag that conflicts with the preset is flagged.

- **Give every new capability an expiry date** — CLEAN — value 4 — effort M — risk med — category: lean (wild)
  Why: T-2503 already makes unmeasured growth wait. This goes further: a feature ships with a sunset date and a named measure, and the sweep opens a removal task on that date unless the measure renewed it. This does not break the no-idea-killed rule, since removed code goes to `not-yet.md` with its blocker.
  Done when: `fm ship` refuses a new verb with no `sunset:` and measure, and a test shows a lapsed feature produces one removal task.

- **Auto-close stale Foreman-filed items** — CLEAN — value 3 — effort S — risk low — category: inbox
  Why: 30+ deferred "Later from T-07xx/T-08xx" tasks sit open and the inbox gets items from ci, self and discovered sources. This is separate from the earlier cap of 5, which limits display and does not clear anything.
  Done when: a Foreman-filed item untouched for 14 days closes with the reason "stale, unseen", reopens with one command, and `fm next` never lists it.

- **Move Genesis out of the core install** — CLEAN — value 4 — effort L — risk med — category: packaging
  Why: the standing rule says Foreman is "the discipline layer for coding agents" and must work without Claude. Yet `plugin/skills` holds 1388 of 2117 files, much of it tower machinery. Moving it loses nothing: no idea is killed, it just becomes a separate installable plugin.
  Done when: a core install without Genesis passes `fm doctor` and the roundtrip e2e, its file count drops by at least half, and `fm genesis` prints one line saying how to add it.

- **Generate the README feature list from MASTER.md clauses** — CLEAN — value 3 — effort M — risk low — category: docs
  Why: the README, MASTER.md and the site each state capabilities, and the proof-before-presentation sweep exists to catch them disagreeing. One source removes the disagreement instead of policing it.
  Done when: editing a MASTER clause changes the README and site list on the next build, and the claim-drift check has nothing left to compare.

- **Collapse the exam arms into "with" and "without" in the scorecard** — CLEAN — value 3 — effort S — risk low — category: reporting
  Why: foreman, plain, guard, finders, oracle, empty and Haiku smoke arms each have their own lines, and the user had to ask for "the guard-only arm" and for subtraction tied to deltas. Assumption: the user reads one question ("did Foreman help?").
  Done when: `fm exam scorecard` prints one two-column table plus a single sentence verdict, with per-arm detail under `--arms`.

- **Unload skills that haven't triggered in 60 days** — PERFORMANCE — value 3 — effort M — risk med — category: skills
  Why: skill descriptions count toward injected context and the lean ratchet tracks them, but nothing shows which ones fire. Assumption: many of the 1388 skill files never load.
  Done when: `fm doctor` lists skills never loaded in 60 days, a command parks them in an archive directory, and the lean metric for descriptions drops.

- **Route plain sentences to verbs** — FEATURE — value 4 — effort M — risk med — category: interface (wild)
  Why: the verb surface (`fm exam runs`, `fm ship --chance`, `fm outcomes --judgment --by harness`) is large and keeps growing. Typing `fm "what's blocked on me"` would let most verbs go undiscovered without being deleted.
  Done when: `fm "<sentence>"` runs the right read-only verb for 10 canned questions, prints the exact verb it chose, and refuses to route anything that writes.

- **Ship Foreman as a single zipapp** — FEATURE — value 3 — effort L — risk high — category: install (wild)
  Why: `install.sh`, plugin directories, hooks, timers and mods make a first install heavy. A single file holding guard, plan and prove would run anywhere with Python.
  Done when: one `.pyz` file runs `guard` and `prove` in a clean container with no other Foreman files.

- **Show only the day's next move on bare `fm`** — FEATURE — value 3 — effort S — risk low — category: home (wild)
  Why: assumption: after months of additions, bare `fm` is a menu. This is a different shape from the earlier home-screen idea: it prints one sentence plus one command to copy, never a list.
  Done when: bare `fm` prints at most two lines, the second being a runnable command, and `fm --menu` prints the current help.

Next question: which Foreman features has the user never invoked by hand or via a hook in 90 days, and would they notice if each vanished?
Next question: where do two Foreman features record the same fact (a steer and its check, a claim and its sweep), and which copy can be derived instead of stored?

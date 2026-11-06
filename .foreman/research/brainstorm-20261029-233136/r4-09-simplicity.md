# Brainstorm — lens: simplicity

- **Run each generation as an ordinary `fm mission`** — CLEAN — value 5 — effort M — risk low — category: reuse
  Why: `fm mission`, `fm exam run` and `fm loop` already exist. The pack's "missing" list (orchestrator, selection, sweep) reads like a mission whose done-check is an exam score. Assumption: a mission can take a custom done-check.
  Done when: `fm genesis` creates a mission whose close gate is `fm exam run`, and a fixture project's generation closes through the normal mission path with no new orchestrator module.

- **Park not-yet items as deferred tasks tagged `not-yet`** — CLEAN — value 4 — effort S — risk low — category: ledger
  Why: the queue already has deferred and blocked states (T-0034, T-0788 and others). A second ledger file is a second thing to resume and to go stale. Assumption: tasks can hold a blocker note and an attempt count.
  Done when: a failed spike writes a `not-yet` task with its blocker and attempt count, and the next generation's start lists and retries it without reading any ledger file.

- **Split held-out scenarios by hash of the scenario id** — CLEAN — value 4 — effort S — risk low — category: exam
  Why: the held-out third needs no stored list if `hash(id) % 3 == 0` decides it. Selection code can't forget to exclude it, and a writer can't be handed it by accident. Assumption: `fm exam gen` ids are stable.
  Done when: a test shows the same ids land held-out across two runs, and no tower file lists the held-out set.

- **Add no Genesis-only lenses; reuse `fm ideas` lenses** — CLEAN — value 3 — effort S — risk low — category: reuse
  Why: lens definitions already exist and carry `lens_rates` payoff data (T-0829). New lenses would split that data and add things to maintain. Assumption: the existing set covers Mission needs.
  Done when: the Genesis Mission code references lens names only from the `fm ideas` list, and a test fails on an unknown name.

- **Queue auto-start as a blocked task, "Start Genesis here?"** — FEATURE — value 4 — effort S — risk low — category: consent
  Why: the routing line in `rules/foreman.md` is protected core. A blocked task reuses the approval flow the user already knows, so there is no new consent mechanism. Assumption: blocked tasks surface at session start.
  Done when: a dry queue plus a big gap map creates exactly one such task, and answering yes starts the tower. Answering no or ignoring it creates no second task for N days.

- **Write the #13 exam as a checklist parsed from the hand-written gen-0** — FEATURE — value 5 — effort S — risk low — category: exam
  Why: the stated exam is "covers every MUST, NEVER and section of the hand-written one". That is a mechanical diff of headings and MUST/NEVER lines, not a model judgment. Assumption: gen-0 lines are regularly marked.
  Done when: a script of about 30 lines lists missing items for a self-written gen-0 against the hand one, and it exits non-zero on a planted omission.

- **Give tiny projects a tower of one generation** — PERFORMANCE — value 3 — effort S — risk low — category: scope
  Why: a 5-file repo needs no multi-generation tower, and cost scales with ceremony. Assumption: file count from `fm map` is a fair size proxy.
  Done when: a fixture under the threshold stops after one generation and says why in one line. A larger fixture runs on.

- **Test Genesis with one canned-child run on a 5-file fixture** — CLEAN — value 4 — effort M — risk low — category: tests
  Why: per-stage tests for seven stages multiply upkeep. One end-to-end run with scripted child outputs covers the wiring and runs in seconds.
  Done when: `plugin/tests` has one test that runs init → close with stub children, asserts the tower files and the lineage line, and finishes in under 10 seconds.

- **Print plain stage names, with a glossary line, in user-visible output** — CLEAN — value 2 — effort S — risk low — category: wording
  Why: "Seed, Missions, critiques, selection, drift check, sweep" is internal jargon. The user is already asking for a page they can read in full. Assumption: the names can be renamed in display only.
  Done when: `fm genesis status` shows ask, try, compare, keep, check and sweep, and a test checks that each maps to the stage names stored in tower files.

- **Wild: Try the existing loop first; start the tower only if it closes nothing** — FEATURE — value 4 — effort M — risk med — category: approaches
  Why: for "make this great", `fm scout` and `fm loop` on the gap map may close the gaps without any tower. The tower becomes the escalation path, not the default. Wild. Assumption: one loop round can be scored against the gap map.
  Done when: on a fixture with one planted gap, `fm genesis` closes it via scout and loop with no tower files written. On a fixture with a hard gap it escalates and logs the reason.

- **Wild: Make the whole output one reviewable `genesis.patch`** — FEATURE — value 4 — effort M — risk med — category: output
  Why: a tower with generations, a ledger and a page is a lot to read. One patch of rule and doc changes, with the exam score in its header, is a single yes or no. The tower stays as the audit trail. Wild.
  Done when: a run ends with one patch file the user applies with `git apply`, and the header lists exam closed before and after.

- **Wild: Make the orchestrator a markdown checklist skill, with Python only for exam and grade** — CLEAN — value 3 — effort M — risk high — category: radical reuse
  Why: Foreman ships 1359 skill files, and orchestration may be prose the model can follow. Python is kept only where outputs must be checked. Wild. The risk is that a model-followed checklist skips steps.
  Done when: the checklist skill completes the same fixture as the Python orchestrator, and a step-presence check on the tower files shows no skipped stage across 5 runs.

- **Wild: Print a one-line verdict for every `fm genesis` call and nothing else by default** — CLEAN — value 3 — effort S — risk low — category: output
  Why: with these 200+ ideas on the table, a bare `fm genesis` should say what it did and what it needs, like "gen 2 kept: 9→11 closed, $3.20; next: yes/no on auto-start". Details sit behind `status`. Wild.
  Done when: a default run's stdout is at most 2 lines, and `status` still shows full detail.

Next question: Which Genesis stages could be an existing Foreman verb with a different done-check, and what would break if each were?
Next question: What is the smallest tower that still passes the #13 exam on a held-out project, and does anything beyond it earn its cost?

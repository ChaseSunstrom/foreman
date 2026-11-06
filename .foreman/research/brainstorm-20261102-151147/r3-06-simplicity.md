# Brainstorm — lens: simplicity

- **Compute each metric in one place** — CLEAN — value 4 — effort M — risk low — category: measurement
  Why: T-2667 fixed `fm burden` missing `hook_success` stdout because `fmcost.INJECTS` was a second, narrower counter of injected context. Two readers for one quantity drift apart.
  Done when: a quantity registry (injected chars, spend, tokens, hook ms) has one function each, and a test fails if another module under `plugin/lib` re-derives a registered quantity.

- **Hold every hard cap in one LIMITS table** — CLEAN — value 3 — effort S — risk low — category: guard
  Why: T-2668 added "refuse more than 8 nested `$(`", and the pathological-input test hard-codes its own bars. T-2669 added a stall cap. Caps are scattered constants.
  Done when: `fm doctor --limits` prints every cap with its value and the test that proves it, and a grep finds no bare cap literal in the guard or run code.

- **Delete the steer expander unless it beats verbatim** — CLEAN — value 3 — effort S — risk low — category: subtraction
  Why: T-2632 measured 15/93 vs 20/93 covered with 46 vs 45 harmful, and reverted. The expander has been shown to cover about 16–21% while roughly half its output is harmful. Verbatim storage costs nothing.
  Done when: `fm exam steer` compares expand-on against store-verbatim on the held-out third, and expansion is off by default unless it wins by a stated margin.

- **Ship the do-less `fm prove` cache: skip only on an identical diff hash** — PERFORMANCE — value 3 — effort S — risk low — category: speed
  Why: the user's c11 ask is "cache by tree hash plus command". The smallest version keys on `git diff HEAD | sha1` plus the command string, with one file and no invalidation logic.
  Done when: a second `fm prove` on an unchanged tree prints "cached green, tree X" in under 100 ms, and any edit forces a real rerun.

- **Test every claim in the README against the code on one nightly pass** — FIX — value 3 — effort M — risk low — category: docs
  Why: the pack's tagline claims (plans before editing, one task at a time, the guard) are prose. The "run fenced blocks" idea checks commands, not claims.
  Done when: each README sentence naming a verb or flag resolves to a live symbol, and `fm doctor` lists any that don't.

- **Cut every verb's `--help` to one screen and enforce it** — CLEAN — value 2 — effort S — risk low — category: legibility
  Why: assumption: verbs gained flags per task (`--stall-usd`, `--by-source`, `--steer`) and help has grown. A newcomer reads help, not MASTER.md.
  Done when: a test fails if any verb's help exceeds 24 lines, and the offenders are trimmed.

- **Make each new gauge name its one decision** — CLEAN — value 3 — effort S — risk low — category: measurement
  Why: the earlier "flag numbers recorded but never decide" idea only audits after the fact. T-2536 and T-2567-style gauges keep appearing.
  Done when: the gauge registration call requires a `decides=` field, and registration fails without one.

- **Resolve conflicting stop reasons by one precedence line** — FEATURE — value 2 — effort S — risk low — category: drive
  Why: `fm run` now has budget, pace, `--stall-usd` and usage-limit stops. The receipt names only one reason when two apply.
  Done when: a fixture where two stops trip at once prints both, with the rule that won.

- **(wild) Bisect the brainstorm pack until the top idea stops changing** — FEATURE — value 3 — effort M — risk low — category: brainstorm
  Why: this pack is thousands of lines of "ideas so far", and the 525-idea catalogue is fed back to every child. Nobody knows which half does the work.
  Done when: a script halves the pack sections repeatedly and reports the smallest pack that reproduces the same top three ideas.

- **(wild) Run a documentation-deletion exam** — CLEAN — value 3 — effort M — risk low — category: docs
  Why: assumption: MASTER.md has sections no reader needs. Remove one section, ask a tool-less child 10 questions about the behaviour, and score.
  Done when: a report lists the sections whose removal changed no answer, as deletion candidates.

- **(wild) Read the repo as one scrolling page by blast radius** — FEATURE — value 2 — effort M — risk low — category: legibility
  Why: 2134 files and 1388 skill files hide what matters. A single generated page lists the 30 files that carry the guard, ledgers and gates, each in one line.
  Done when: `fm map --core` prints at most 30 lines, and a cold child can find the guard's entry point from it alone.

- **Collapse alias spellings to one per verb and flag** — CLEAN — value 2 — effort S — risk med — category: legibility
  Why: assumption: sibling verbs spell the same intent differently (`--yes-run`, `--final`, `--regressing N`). Aliases double every doc and test surface.
  Done when: an alias census lists them, and each is either removed behind a tombstone message or recorded as intentional.

Next question: which of Foreman's three or four ways of stopping, asking, or proving does the user actually reach for, and which exist only because a Mission needed them?
Next question: if a new user saw only the first screen of `fm`, what is the one verb that proves the tool works, and does it exist?

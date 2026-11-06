# Brainstorm — lens: unspoken needs

- **Say "why didn't I know" before it happens: a pre-flight brief at task start** — FEATURE — value 5 — effort M — risk low — category: user value
  Why: the user asks "why have you not improved?" and wants fixes applied "every time", yet hints, lessons, vetoes, decisions and cards live in separate stores. Assumption: nothing merges them into one start-of-task summary.
  Done when: `fm task start` prints at most 5 lines naming the hints, lessons and cards that apply to the task's files, and a test asserts each is cited with its source id.

- **Show the improvement, not just ship it: a "did Foreman get better" scorecard** — FEATURE — value 5 — effort M — risk low — category: observability
  Why: the user's complaint is that improvement isn't visible. Fix hit rates, first-time-pass rate, repeat-obstacle count and tokens per close exist in the ledger but are not trended. Assumption: the ledger has enough history to compute them.
  Done when: `fm score` prints week-over-week deltas for 4 metrics from ledger data, and a fixture ledger test pins the numbers.

- **Turn the user's repeated corrections into rules without being asked** — FEATURE — value 5 — effort M — risk med — category: user value
  Why: the "steered" and "asked" lines repeat themes (fill the panel, no gaps, declutter, any project, ship via git). Assumption: corrections are captured verbatim by intake (T-0790).
  Done when: after a correction matching a prior one by fingerprint, Foreman proposes a standing rule with the quoted evidence, and accepting it writes a rule file that the next session injects.

- **Make the harness incapable of touching a real session** — FIX — value 4 — effort S — risk low — category: stability
  Why: shot.py was driven by the Stop hook into the queue, and the tests reached the paid binary through the ~/.local/bin fallback. Two failures of one kind: test and harness sessions leak into real state.
  Done when: one `FM_SANDBOX=1` env makes every hook a no-op on the queue, the claude resolver returns a stub, and a test fails if either is bypassed.

- **Hand a worktree agent a "where was I" screen on resume, not just its files** — FEATURE — value 4 — effort M — risk low — category: agents
  Why: T-1028 plans resume. Assumption: it restores the worktree, branch and brief but not the agent's reasoning state.
  Done when: a resumed builder's first prompt includes its last 3 plan steps, unfinished step and the diffstat since the last green run, and a test checks all four appear.

- **Let a new teammate's first `git pull` run an onboarding check of the shared brain** — FEATURE — value 4 — effort S — risk med — category: security
  Why: the user wants fixes to travel by git, so a hint pulled from a clone is a command-carrying input. Existing ideas say "treat as untrusted" but nothing shows approval.
  Done when: hints from an unseen author commit show as pending in `fm known`, never apply until accepted once, and the acceptance is recorded by hint hash.

- **Explain why Foreman did or blocked something, on demand** — FEATURE — value 4 — effort M — risk low — category: developer experience
  Why: with many hooks, gates, hints and guards, the user can't see which rule fired. Assumption: the decision is logged but not queryable.
  Done when: `fm why` prints the rule, source file and triggering input for the last block or injection, and a test blocks a command and checks the output.

- **Close the loop on deferred work: a weekly "decide" digest** — CLEAN — value 4 — effort S — risk low — category: simplicity
  Why: roughly 30 deferred "Later from T-07xx/08xx" tasks sit open, and some (T-0861–0866) say "needs evidence". Assumption: no automatic re-check exists.
  Done when: `fm next` surfaces any deferral whose stated trigger is now measurable, with the number, and drops items whose evidence says no.

- **Keep the pane honest on a narrow or tall terminal with a layout fuzz test** — FIX — value 3 — effort M — risk low — category: ui
  Why: the repeated asks for no gaps, fills exactly, and no scaling jumps, plus the 36-column mobile test, suggest regressions recur.
  Done when: a test renders the pane at 20 random sizes (30–200 columns, 10–80 rows) with random state and asserts no overflow, no blank rows and a stable height.

- **Wild: a "second opinion from last month" check that replays today's plan against past failures** — FEATURE — value 4 — effort L — risk med — category: agents
  Why: assumption: the ledger stores plans and failures, so a cheap similarity search can warn "a plan like this failed on X before" before any edit. Wild.
  Done when: planning a task whose files match a past failed task shows that task's id and failure line, and a fixture proves it.

- **Wild: a project "black box recorder" that a stranger can replay the whole story from** — FEATURE — value 3 — effort L — risk med — category: docs
  Why: the README demo is hand-recorded and the user wants other sessions to share what was learned. Assumption: the ledger plus the commits is enough to render a replayable log. Wild.
  Done when: `fm story T-1009` writes one self-contained HTML timeline of the task's plan, commands, red/green proof and commit, and opens offline.

- **Wild: let the pane say what it learned as the idle screen, one sentence at a time** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: the pane has empty areas the user dislikes, and the learning is invisible. Wild.
  Done when: the idle pane shows the newest learned hint or lesson with its hit count, and a test confirms it's replaced on a new hint and absent when none exist.

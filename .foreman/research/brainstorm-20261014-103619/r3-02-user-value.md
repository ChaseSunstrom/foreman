# Brainstorm — lens: user value

- **Compile open-ended asks into a scored mandate** — FEATURE — value 5 — effort M — risk low — category: intake
  Why: "super improve foreman… smarter, faster, better, etc." is the current request, and earlier steers ("they don't feel that revolutionary") show the user judges by felt delta. Foreman has no way to prove delta. The idea combines three existing ones: epic roadmap, metric campaigns and the rigor dial.
  Done when: `fm task new "super improve X"` produces a mandate with ≥3 baselined metrics (e.g. hook latency, tokens per task, idle minutes), a budget and a stop rule, and the close-out prints a before/after table.

- **Track a landing ladder: done, committed, pushed, released** — FEATURE — value 5 — effort M — risk med — category: close-out
  Why: Recent asks include "Commit T-0671's review fixes" and six "Release Foreman 1.2.x to GitHub main and JARVIS" tasks. Work reaches "done" but not "landed", and the user has to ask for the remaining rungs each time.
  Done when: every task shows its highest rung in `fm status` and the band, and a task with a standing "release as usual" grant advances to pushed and released without a new request. A fixture test covers the case where it stops one rung short.

- **Learn named routines from repeated asks and run them on a phrase** — FEATURE — value 4 — effort M — risk med — category: routines
  Why: "Release Foreman 1.2.N (T-… to T-…) to GitHub main and JARVIS" recurs with only the numbers changing (1.2.25–1.2.27). A routine recipe is derived from the ledger, not authored by hand.
  Done when: after the third matching request, `fm routine list` shows "release" with its steps, and "release 1.2.28" runs the recipe with the task range filled in from the ledger.

- **Show a token-savings ledger with counterfactuals** — FEATURE — value 4 — effort M — risk low — category: tokens
  Why: The user keeps asking for "a crap ton" of token savings, but the existing ideas only show where tokens went. This one credits each saving to a cause (haiku routing, skipped reviews, cache hits, blocked loops) with a labelled estimate. Assumption: counterfactual rates can be approximated from ledger and transcript usage.
  Done when: `fm savings --week` prints per-cause token and dollar estimates, each tagged "measured" or "estimated", and the total reconciles with `/usage` within a stated tolerance.

- **Audit the whole `~/.claude` for always-loaded token tax and prune reversibly** — FEATURE — value 4 — effort M — risk low — category: tokens
  Why: The user cares about tokens and speed, and bloat comes from CLAUDE.md files, MCP tool schemas, other plugins' skills and hooks, not only Foreman. Existing ideas cap Foreman's own injection and run `/skill-doctor` on its skills. None looks at the user's whole setup.
  Done when: `fm diet` lists each always-loaded item with its token cost and hook latency, and `fm diet --apply` disables the chosen items with an undo manifest. Applying and undoing restores a byte-identical settings file.

- **Put live step state in the native spinner verbs** — FEATURE — value 3 — effort S — risk low — category: native UI
  Why: The statusline and band are used, but the spinner shown while the model works is not. The user complained that steps change without the step pointer updating, so visible state matters. Assumption: the host supports a `spinnerVerbs` setting.
  Done when: while a task runs, the spinner reads "T-0754 step 3/5 · verifying" (or similar), reverts on SessionEnd, and the settings write is covered by a test.

- **Feed Claude Code's `/insights` friction categories into the queue** — FEATURE — value 3 — effort S — risk low — category: feedback
  Why: The host already clusters the user's friction (wrong approach, buggy code, rejected actions), and Foreman ignores it. Assumption: `/insights` output is readable locally.
  Done when: running `fm friction --from-insights` creates at most N deduped, titled FIX or RESEARCH captures, each citing its insight line, and rerunning creates none.

- **Promise the end state before an unattended stretch and verify it on return** — FEATURE — value 4 — effort S — risk low — category: autonomy
  Why: The user hit idleness and unexplained step drift while away, and trust drops when they come back to surprises. This is a promise-and-verify pair, narrower than the existing walk-away check.
  Done when: before a run, Foreman states "when you're back: N tasks landed, tree clean, nothing idle". On return one line reports kept or broken per promise, and a broken promise opens a task.

- **Mirror each task's acceptance criteria into a native completion condition** — FEATURE — value 3 — effort M — risk med — category: native integration
  Why: The host may offer a `/goal`-style "keep going until X" evaluator, which would let the host share the load of the idle-drive problem. Assumption: such a command exists and can be set programmatically. Foreman's gates would still be the authority.
  Done when: a task with criteria sets a native condition derived from them. A fixture with the native evaluator disabled falls back to the current drive with identical done-gate results.

- **Wild: Send a weekly invoice per shipped milestone** — FEATURE — value 3 — effort M — risk low — category: legibility
  Why: assumption: the user thinks in milestones (1.2.25 to 1.2.27) and usage limits. The invoice lists each milestone with its usage cost, wall-clock time, rework and first-time-green rate, so the user can see which work was cheap and which was a money pit. wild.
  Done when: `fm invoice` renders a table of last week's milestones with cost, hours and rework columns, and the numbers match the ledger.

- **Wild: Ask "what's first tomorrow?" and have it prepared by morning** — FEATURE — value 4 — effort M — risk low — category: continuity
  Why: assumption: a one-line end-of-day answer (default is the queue head) lets overnight cron or a cloud routine pre-plan, pre-read and warm the first task. Related ideas exist (pre-planning at idle, pre-warming the day) but none starts from the user's own words. wild.
  Done when: after the user answers, the next session's greeting shows a ready plan for that task with recon already done. Skipping the question changes nothing.

- **Wild: Compare Foreman with plain Claude Code on the same task, on demand** — FEATURE — value 3 — effort L — risk med — category: proof of value
  Why: the user pushes back whenever features feel non-revolutionary. A cheap replay of a finished task without Foreman (same model, no hooks) with a diff of diff-size, tokens, escapes caught and time gives a measured answer per task. wild.
  Done when: `fm versus T-0754` produces a two-column report, and its output states plainly when plain Claude Code matched or beat Foreman.

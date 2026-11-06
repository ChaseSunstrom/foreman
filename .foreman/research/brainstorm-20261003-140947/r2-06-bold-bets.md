# Brainstorm — lens: bold bets

- **Compile the guard from a policy table, not regexes** — CLEAN — value 5 — effort L — risk high — category: guard
  Why: Every recent guard commit patches one more shell-parsing hole (heredocs, backticks, `$'…'`, keywords, `--run`), and two real bypasses were found only while grounding false positives. Assumption: a small shell-AST pass (stdlib `shlex` plus a hand-written tokenizer) can replace the layered heuristics.
  Done when: a decision-table test runs the full replay corpus and all past bypass cases against one tokenizer-based classifier, and the old per-case heuristics are deleted with zero regressions.

- **Run every task in a worktree by default and merge on finish** — FEATURE — value 5 — effort L — risk med — category: isolation
  Why: User asked for parallelism "unless that will cause context issues", and lane cleanup and main re-checks already exist in `fmlanes`. A worktree per task makes serial and parallel the same code path. Assumption: lane code is reliable enough to be the only path.
  Done when: `fm task start` on a fresh repo creates a lane, `finish` merges it to the branch, and the user's tree is untouched mid-task.

- **Enforce a per-lane context budget with a brief-only handoff** — FEATURE — value 4 — effort M — risk med — category: parallel
  Why: The user asked that parallel work not cause "context/speed/quality/usage issues". Assumption: each lane subagent can receive just its brief, its criteria and its file list.
  Done when: `fm run --parallel 3` logs the tokens each lane received and refuses a lane whose handoff exceeds the cap.

- **Build a one-command `fm repair` for stuck sessions** — FIX — value 4 — effort M — risk low — category: resilience
  Why: The user reported "you weren't reprompted when the session just continued", and a reload race was only dropped after analysis. Assumption: stalls leave traces in the ledger and the drive flag.
  Done when: a simulated stall (drive on, open work, no prompt) is detected on resume and restarts the turn, verified by an e2e test.

- **Scan git history and Claude config for credentials at `fm check`** — SECURITY — value 4 — effort M — risk low — category: secrets
  Why: The user asked for "credential finding/auditing in repositories/claude stuff", and `fmsecrets` already exists. Assumption: history scanning is not yet part of the gate.
  Done when: a planted fake key in an old commit and in `~/.claude` settings fails the gate with the file and commit named.

- **Wild: Run a frame-diff bot that screenshots the mod in its own tmux and files "looks wrong" tasks** — FEATURE — value 4 — effort L — risk med — category: ui-qa
  Why: Wild. The user keeps reporting visual mismatches (panels, dashboard duplication, diff contrast) that the tests never see. The existing snapshot tool already has an isolated tmux. Assumption: frames can be compared against golden captures.
  Done when: an altered border in `rows.tsx` produces a captured frame diff and an inbox item containing the image path.

- **Wild: Let competing fix subagents race on each friction cluster, and keep the winner by replay score** — FEATURE — value 4 — effort L — risk high — category: self-improvement
  Why: Wild. The user wants "RSI almost", and the last pass found a real bug. Two candidates per fix, scored by the guard replay corpus, tests and diff size, would prove improvement rather than assume it. Assumption: worktree lanes can host both candidates.
  Done when: one friction cluster produces two lane branches, a score table is written, and only the winner is merged.

- **Make the reply formatter a single panel schema with a lint** — CLEAN — value 4 — effort M — risk low — category: ui
  Why: The user's repeated complaints are "not everything is in panels", duplicated dashboard and mismatched headers. Assumption: rows are built in more than one place today.
  Done when: a test fails if any row kind in `rows.tsx` renders without the shared panel wrapper, and the dashboard renders from one section list.

- **Wild: Fork the session at each plan and let a skeptic Haiku vote "will the user push back?"** — FEATURE — value 3 — effort M — risk low — category: taste
  Why: Wild. The pushback history (panels, "don't hand me commands", token economy) is large enough to predict objections. Assumption: the last N user steers can be summarized into a small prompt.
  Done when: a plan violating a recorded steer (such as handing the user a command) is flagged before it is shown.

- **Wild: Add a "ghost mod reload" that hot-swaps the UI without ending the turn** — PERFORMANCE — value 3 — effort L — risk high — category: ui-runtime
  Why: Wild. Mods reach the user's window only when a turn ends, so the drive ends turns on purpose and races have appeared (the dropped reload-resume race). Assumption: the engine offers a reload or an event that can trigger a re-render.
  Done when: a changed `rows.tsx` appears in a live session mid-turn without ending the turn.

- **Report guard false positives by their cost in rewrites** — PERFORMANCE — value 3 — effort S — risk low — category: guard
  Why: Friction is mostly false positives on Claude's own edit and probe commands, each costing a rewrite. Assumption: blocks are logged with a later outcome.
  Done when: `fm friction` lists the top 5 blocked-then-rewritten command shapes with a count, and each has a safe-form hint attached.

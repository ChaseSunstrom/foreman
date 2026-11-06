# Brainstorm — lens: unspoken needs

- **Replay the guard against the user's real command history on every guard change** — SECURITY — value 5 — effort M — risk low — category: guard
  Why: The last 25 commits are mostly guard patches (heredoc quoting, backticks, `$'…'`, keywords, `--run`). Each fix came from friction or a found bypass. Nothing in the pack shows a regression corpus built from the ledger of commands that were actually allowed or blocked. Assumption: the ledger or events log stores guard verdicts with command text.
  Done when: `fm check` has a gate that replays all recorded commands through fmguard and fails if any past allow turns into a block, or a past block into an allow, without a listed expectation change.

- **Add a "guard false-positive" one-shot fix hint that names the exact safe rewrite** — FEATURE — value 4 — effort M — risk low — category: guard UX
  Why: "Most recent friction came from guard false positives… each costs a rewrite." The user never wants to be handed commands, so a block should carry a ready, tested alternative that the agent applies without a model round trip.
  Done when: for the top 5 block categories in the friction log, the block message includes a rewrite line, and a test shows the rewritten command passes the guard.

- **Measure agent-perceived slowness as time-to-first-useful-action per turn** — PERFORMANCE — value 5 — effort M — risk low — category: speed
  Why: The user said "I don't necessarily mean the speed of foreman itself, but agents using foreman, it feels slow." Hook p95 is 30 ms, so the cost is elsewhere: rules tokens, ceremony calls, extra turns, reload turn-ends. No metric covers that.
  Done when: `fm stats` prints per task the number of turns, `fm` calls, and wall time spent in Foreman ceremony versus work, and the top contributor is named.

- **Cut round trips: let `fm task finish` run gates, audits and the commit with one resumable call** — PERFORMANCE — value 4 — effort M — risk med — category: ceremony
  Why: Slowness is felt at the agent level. Assumption: closing still takes several separate calls (evidence, audit, done, finish). Fewer calls means fewer turns and fewer tokens.
  Done when: a typical S-tier task closes in at most 2 `fm` invocations, verified by an e2e test counting calls.

- **Add a parallel-safety preflight that predicts context, usage and conflict cost before `fm run --parallel N`** — FEATURE — value 4 — effort M — risk low — category: parallel
  Why: The user asked twice for parallelism "unless that will cause context/sub agent issues" and "make sure parallel things don't cause context/speed/quality/usage issues." Today there is only a disjointness check.
  Done when: `fm run --parallel 3 --dry` prints the estimated token multiple, overlapping files, and a recommended N (possibly 1), and a test covers an overlapping pair.

- **Show a git-tracking health card for Foreman state per repo** — FEATURE — value 3 — effort S — risk low — category: git
  Why: The user asked for "better tracking of foreman stuff in git repositories" and credential auditing. Assumption: no single view shows which Foreman files are ignored, tracked or leaking secrets.
  Done when: `fm doctor` lists tracked-versus-ignored Foreman paths and flags any tracked file that fmsecrets matches.

- **Add a mod screenshot-diff gate for the panel layout** — CLEAN — value 4 — effort M — risk low — category: ui regression
  Why: The UI complaints repeated across rounds: mismatched panels, duplicates, unpanelled buttons, odd diff contrast. The snapshot tool exists (own tmux server). Without a visual baseline each fix can regress another.
  Done when: the mod test suite renders the dashboard, reply, edit and command panels to text snapshots and fails on width, border or duplicate-section changes.

- **Wild: Add a "complaint to guardrail" compiler** — FEATURE — value 5 — effort L — risk med — category: self-improvement
  Why: The user's recurring complaints (duplicates, unpanelled output, no re-prompt on resume) were each fixed once by hand. A subagent that turns each complaint into a failing mod test or check before the fix makes the RSI loop catch repeats. Wild.
  Done when: filing a complaint in the inbox produces a red test linked to it, and closing the task turns that test green.

- **Wild: Run a shadow-session simulator that replays recorded sessions on the candidate build before release** — FEATURE — value 4 — effort L — risk med — category: release safety
  Why: A mod release needs the user's yes, and the mod reaches the window only at turn end, so mistakes are costly. Replaying event streams through the new mod and hooks, with Haiku turns only, would show the release's effect before the user says yes. Wild.
  Done when: `fm release --rehearse` replays N recorded event logs and prints the panel snapshot diff and hook verdict diff.

- **Wild: Give the self-improvement loop a scoreboard that proves it is improving** — FEATURE — value 4 — effort M — risk low — category: RSI
  Why: The user wants RSI "almost," with passes every 3 tasks. Nothing shows that friction per task is falling or that fixes stuck. Wild.
  Done when: `fm friction trend` plots friction events per closed task by category over time and marks the passes, and a recurring category is flagged as "fix didn't hold."

- **Trim rules by measuring which lines actually changed agent behavior** — CLEAN — value 3 — effort M — risk med — category: token economy
  Why: The user is usage-sensitive, and the 5.7 KB of always-on rules loads every turn. Assumption: some lines are redundant with gates. This differs from earlier "delete lines a gate enforces" because it uses A/B runs on Haiku in test harnesses.
  Done when: a Haiku harness compares the rules with and without each section on a fixed scenario set, and the report lists the sections whose removal changes no outcome.

# Brainstorm — lens: unspoken needs

- **Report cost per verified pass, not raw cost** — FEATURE — value 5 — effort M — risk low — category: benchmarks
  Why: the long-session result is Foreman at $0.095 vs $0.059 raw, but it passed 6 of 6 against 3 of 6. A miss means rework the user pays for, and the raw figure hides that. Assumption: the harness can price a failed run plus a retry.
  Done when: the Benchmarks page and `fm bench` print dollars per passing hidden test for both sides, generated from the results file rather than typed into prose.

- **Ablate Foreman's components in the duel** — PERFORMANCE — value 5 — effort M — risk low — category: benchmarks
  Why: the user wants Foreman cheaper and faster than Claude Code, and only the total is known (+10–14% on small tasks, +60% on long ones). Runs with guard only, discipline only, and hook notes off would show which part buys the passes and which only adds cost.
  Done when: one capped Haiku run produces a table of component × (pass rate, $, time), and T-1231 cites it.

- **Gate the per-turn context tax in CI** — PERFORMANCE — value 4 — effort S — risk low — category: cost
  Why: the 15 skills take about 3,200 of roughly 9,600 listing characters, and 2.1.304 re-sends the whole listing after every compaction. Foreman's hook notes also grow context faster than plain Claude Code's.
  Done when: a test replays a fixed transcript, measures the characters Foreman injects (skill listing plus hook notes), and fails above a committed ceiling.

- **Cache bench results by case, Foreman hash and model** — PERFORMANCE — value 4 — effort M — risk low — category: usage
  Why: every release has asked for a rerun (`--runs 3`, 1.2.38 to 1.2.40) and usage is a stated constraint. Assumption: most cases don't change between runs.
  Done when: rerunning an unchanged case costs $0 and prints "cached", and touching one hook reruns only the cases that load it.

- **Tune the compaction window from a measured sweep** — PERFORMANCE — value 4 — effort M — risk med — category: cost
  Why: Foreman compacts more and is about 60% dearer in long sessions. 2.1.304's `CLAUDE_CODE_AUTO_COMPACT_WINDOW` now takes k/M suffixes and warns when out of range. Assumption: a window exists where cost falls without losing passes.
  Done when: a sweep over 3 window sizes on the long-session case gives a recommended value, and `fm doctor` flags a value outside the measured range.

- **Quiz the model after a forced compaction** — FEATURE — value 4 — effort M — risk low — category: reliability
  Why: Claude Code's misses were written after a compaction, and the marathon crosses 7 of them. No one measures what survives each one.
  Done when: a Haiku probe after compaction asks for the active task, the current request text and the last proof, and a score per run is recorded for both Foreman and plain Claude Code.

- **Use `decider: "person"` for `fm ask` grants** — SECURITY — value 4 — effort S — risk med — category: approvals
  Why: self-granted chat approvals were just fixed with process-identity binding. 2.1.304's `tool.check` can require the permission dialog or a host callback, and refuses where nobody can be asked.
  Done when: a test shows a non-interactive `claude -p yes` cannot approve a pending grant in the mod, and the refusal message says why.

- **Audit the unattended loops against the new subagent rule** — FIX — value 4 — effort S — risk med — category: compat
  Why: 2.1.304 no longer lets a plugin keep a headless run alive past Stop or `--max-turns` by spawning subagents. `fm drive`, `fm run` and the marathon may rely on that.
  Done when: a fixture simulates the new behaviour, and the drive either exits cleanly with a resume note or no longer depends on it.

- **Tick criteria from observed proofs** — PERFORMANCE — value 4 — effort M — risk med — category: turns
  Why: the cheaper-turns work cut bookkeeping calls, but the model still spends turns on `fm task ac/step`. Bookkeeping calls are named as a cause of the long-session cost. Assumption: a hook can match a verify command's exit code to a criterion.
  Done when: running a criterion's verify command marks it proved with no `fm` call, and the long-session bench shows fewer `fm` calls.

- **Fuzz the site's layout across widths** — FIX — value 3 — effort S — risk low — category: site
  Why: a user report said Benchmarks text ran outside its boxes. T-1244 says the stored theme applies only after the page loads, and T-1246 says figures are hard-coded.
  Done when: a headless check at 320 to 1920 px finds no horizontal overflow or clipped text on any page, the theme is set by an inline head script, and a number in the prose that disagrees with the results file fails the build.

- **Let a reader rerun a benchmark with `fm bench repro`** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: every site claim must be measured, but only the author has run the numbers. Assumption: a capped Haiku run on one case is enough to check a claim.
  Done when: `fm bench repro safety` runs the 24 dangerous and 25 everyday commands offline, and the output matches the page's counts.

- **Wild: run the duel on each new Claude Code release** — FEATURE — value 3 — effort M — risk low — category: compat
  Why: Foreman is adapted to 2.1.301 and the latest is 2.1.304. On a new version, a capped Haiku duel plus the hook fixtures would post the delta and open briefs for what changed.
  Done when: a scheduled job records the version, the duel delta and any hook fixture failures in one file.

- **Wild: publish a "beat Foreman" challenge** — FEATURE — value 3 — effort M — risk med — category: trust
  Why: the site has to be honest about where Foreman loses, and it is dearer on long sessions. Visitors could submit a spec plus hidden tests that Foreman fails, and accepted ones become bench cases with their dollar cost shown.
  Done when: a submission format validates, and one accepted case runs in `fm bench`.

- **Wild: show Foreman's token share live in the pane** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: the cost gap is invisible during a session. A flame bar could attribute tokens to skill listing, hook notes, `fm` calls and the model's own work.
  Done when: the pane shows a split that sums to the session total, and a hook note's cost is traceable to its source.

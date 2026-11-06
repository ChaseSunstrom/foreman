---
id: T-1232
type: FEATURE
tier: M
status: done
priority: normal
scope: [bench/spec-suite/**]
depends_on: []
source: user
created: 2026-10-16T17:11:43Z
updated: 2026-10-16T17:33:25Z
base: 1daa4218c120e2a57c2235bd70dac5707c50cf68
base_tree: 5deee70de4e3764b47ae149fde0b1640b979fb12
plan0_at: 2026-10-16T17:12:21Z
plan0_scope: [bench/spec-suite/**]
verified: strong
---
# Spec suite: a neutral toy repo of fully specified tasks with hidden tests, for fm bench duel
## Raw request
> Spec suite: a neutral toy repo of fully specified tasks with hidden tests, for fm bench duel
## Interpretation
A reproducible, neutral benchmark repo where each request fully states what its hidden tests check, so a duel measures diligence, cost and time instead of luck at guessing wording; part of T-1231 (user: Foreman should be better, cheaper and faster than Claude Code).
## Assumptions (confidence)
## Acceptance criteria
- [x] python3 bench/spec-suite/make.py DIR builds a git repo whose task commits each carry a complete spec as the message; every reference solution passes its hidden tests and the tests fail at the parent — verify with `python3 bench/spec-suite/make.py --check`
## Non-goals
## Approach (options → choice → why)
Chosen: a generator script that builds the repo from task definitions in code (one place per task: spec, solution, tests), checked fail-to-pass by --check, consumed by the existing fm bench build --commits. Considered: a checked-in nested git repo (awkward in the parent repo), SWE-bench instances (heavy setup; later), cases from Foreman's history (wording-guess tests, protected core).
## Risks and rollback
## Execution prompt
## Steps
1. [x] make.py and the base package (two small modules with unittest tests showing the conventions)
2. [x] Eight tasks, each a spec (commit message), a reference solution and hidden tests that check only what the spec states
3. [x] --check builds into a temp folder and proves each case fail-to-pass; README says how to run fm bench build --commits and fm bench duel on it
## Resume here
## Docs impact
~/.claude/foreman/bench/spec-suite/README.md
## Verification evidence
- (step 1) `python3 bench/spec-suite/make.py --check` → exit 0 · ok    reproducible a second build gives the same commits / spec suite: 8 of 8 tasks fail-to-pass [ran] [tree 03d6d9d882d2] (2026-10-16T17:26:30Z)
- (step 2) `python3 bench/spec-suite/make.py /tmp/claude-1000/-home-<user>--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/kit1` → exit 0 · built /tmp/claude-1000/-home-<user>--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/kit1: base e1c71b4c27 and 8 task commits / next: cd /tmp/claude-1000/-home-<user>--claude-foreman/af0c [ran] [tree 03d6d9d882d2] (2026-10-16T17:26:39Z)
- (step 2) `python3 bench/spec-suite/make.py --check` → exit 0 · ok    reproducible a second build gives the same commits / spec suite: 8 of 8 tasks fail-to-pass [ran] [tree 7d0889613a3f] (2026-10-16T17:27:53Z)
- (step 3) `python3 bench/spec-suite/make.py --check` → exit 0 · ok    reproducible a second build gives the same commits / spec suite: 8 of 8 tasks fail-to-pass [ran] [tree 7d0889613a3f] (2026-10-16T17:27:53Z)
- (ac 1) `python3 bench/spec-suite/make.py --check` → exit 0 · ok    reproducible a second build gives the same commits / spec suite: 8 of 8 tasks fail-to-pass [ran] [tree 7d0889613a3f] (2026-10-16T17:27:58Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmbench.py, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmhooks.py — commit it through a task, or git check; python3 plugin/tests/e2e/roundtrip.py → exit 0 · skipped: nothing under plugin/**, install.sh changed since its pass at 17:01 UTC; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 17:01 UTC; claude pl [ran] [tree 7d0889613a3f] (2026-10-16T17:28:15Z)
- (ac 1) `python3 bench/spec-suite/make.py --check` → exit 0 · ok    reproducible a second build gives the same commits / spec suite: 8 of 8 tasks fail-to-pass [ran] [tree 148cce887bb8] (2026-10-16T17:31:57Z)
- (audit intent) `builder lane (opus) self-review + mutation run (36 of 38 broken solutions caught, the other 2 behave identically); main thread spot-checked table and tokenbucket: every test traces to a stated rule (bool/numeric-string alignment, backwards clock, fractional tokens)` → a neutral repo where requests fully state what hidden tests check, so a duel measures diligence, cost and time rather than wording guesses [tree 148cce887bb8] (2026-10-16T17:31:57Z)
- (audit edge) `builder lane (opus) self-review + mutation run (36 of 38 broken solutions caught, the other 2 behave identically); main thread spot-checked table and tokenbucket: every test traces to a stated rule (bool/numeric-string alignment, backwards clock, fractional tokens)` → reproducible build (fixed author/date, no inherited GIT_* or config), zero tests counts as failure, 120 s test timeout, refuses a non-empty target [tree 148cce887bb8] (2026-10-16T17:31:57Z)
- (audit adversary) `builder lane (opus) self-review + mutation run (36 of 38 broken solutions caught, the other 2 behave identically); main thread spot-checked table and tokenbucket: every test traces to a stated rule (bool/numeric-string alignment, backwards clock, fractional tokens)` → git runs with no user/system config so a hook or GIT_DIR can't redirect it; stdlib only [tree 148cce887bb8] (2026-10-16T17:31:57Z)
- (audit operator) `builder lane (opus) self-review + mutation run (36 of 38 broken solutions caught, the other 2 behave identically); main thread spot-checked table and tokenbucket: every test traces to a stated rule (bool/numeric-string alignment, backwards clock, fractional tokens)` → README gives the three commands (make.py, fm bench build --commits, fm bench duel --vs none --runs 3 --jobs 4) [tree 148cce887bb8] (2026-10-16T17:31:57Z)
- (audit maintainer) `builder lane (opus) self-review + mutation run (36 of 38 broken solutions caught, the other 2 behave identically); main thread spot-checked table and tokenbucket: every test traces to a stated rule (bool/numeric-string alignment, backwards clock, fractional tokens)` → one TASKS list, each task's spec, solution and tests side by side [tree 148cce887bb8] (2026-10-16T17:31:57Z)
- `python3 bench/spec-suite/make.py --check` → exit 0 · ok    reproducible a second build gives the same commits / spec suite: 8 of 8 tasks fail-to-pass [ran] [tree 148cce887bb8] (2026-10-16T17:32:44Z)
- (audit intent) `builder lane (opus) self-review + mutation run (36 of 38 broken solutions caught, the other 2 behave identically); main thread spot-checked table and tokenbucket: every test traces to a stated rule (bool/numeric-string alignment, backwards clock, fractional tokens)` → a neutral repo where requests fully state what hidden tests check, so a duel measures diligence, cost and time rather than wording guesses [tree 148cce887bb8] (2026-10-16T17:32:44Z)
- (audit edge) `builder lane (opus) self-review + mutation run (36 of 38 broken solutions caught, the other 2 behave identically); main thread spot-checked table and tokenbucket: every test traces to a stated rule (bool/numeric-string alignment, backwards clock, fractional tokens)` → reproducible build (fixed author/date, no inherited GIT_* or config), zero tests counts as failure, 120 s test timeout, refuses a non-empty target [tree 148cce887bb8] (2026-10-16T17:32:44Z)
- (audit adversary) `builder lane (opus) self-review + mutation run (36 of 38 broken solutions caught, the other 2 behave identically); main thread spot-checked table and tokenbucket: every test traces to a stated rule (bool/numeric-string alignment, backwards clock, fractional tokens)` → git runs with no user/system config so a hook or GIT_DIR can't redirect it; stdlib only [tree 148cce887bb8] (2026-10-16T17:32:44Z)
- (audit operator) `builder lane (opus) self-review + mutation run (36 of 38 broken solutions caught, the other 2 behave identically); main thread spot-checked table and tokenbucket: every test traces to a stated rule (bool/numeric-string alignment, backwards clock, fractional tokens)` → README gives the three commands (make.py, fm bench build --commits, fm bench duel --vs none --runs 3 --jobs 4) [tree 148cce887bb8] (2026-10-16T17:32:44Z)
- (audit maintainer) `builder lane (opus) self-review + mutation run (36 of 38 broken solutions caught, the other 2 behave identically); main thread spot-checked table and tokenbucket: every test traces to a stated rule (bool/numeric-string alignment, backwards clock, fractional tokens)` → one TASKS list, each task's spec, solution and tests side by side [tree 148cce887bb8] (2026-10-16T17:32:44Z)
## Log
- 2026-10-16T17:11:43Z created
- 2026-10-16T17:12:06Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1232.builder.md
- 2026-10-16T17:12:20Z focused
- 2026-10-16T17:31:38Z merged worktree-agent-afae74ca392dc0152 (2 file(s))
- 2026-10-16T17:31:41Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-afae74ca392dc0152
- 2026-10-16T17:31:47Z focused
- 2026-10-16T17:32:43Z scope: CHANGELOG.md gets this task's release-note line
- 2026-10-16T17:33:24Z done
- 2026-10-16T17:33:25Z committed 2a43e90b (1 file)
## Follow-ups captured
## Context
Why: the duel's cases came from Foreman's own repo, where (1) hidden tests check wording the request never states (T-0205's test expects '/simplify' and 'skills that fit'), and (2) the guard protects plugin/lib as Foreman's core in both arms. A fair quality benchmark needs requests that fully state the behaviour their hidden tests check, in a neutral repo. Design: bench/spec-suite/make.py DIR creates a git repo: commit 1 = base package 'kit' (kit/__init__.py, kit/text.py with slugify and wrap helpers, tests/test_text.py using unittest; run with python3 -m unittest discover -s tests). Then one commit per task, each adding kit/<module>.py + tests/test_<module>.py, the commit message being the full spec (subject line + body with every rule and edge case the tests check, the function signatures, the error types). Tasks (stdlib only, Python 3.10+): (1) duration.parse_duration(text)->int seconds (units d h m s, descending order, each once, spaces allowed, bare int = seconds, whitespace trimmed, ValueError otherwise); (2) lru.LRUCache(capacity): get/put/__len__/__contains__ (contains doesn't refresh), update refreshes, capacity 0 stores nothing, negative ValueError; (3) semver.compare(a,b) per SemVer 2.0 precedence incl pre-release rules, build metadata ignored, invalid (leading zeros, missing parts) ValueError; (4) table.render_table(rows, headers) exact text layout spec (' | ' separators, '-+-' rule, numbers right-aligned, None empty, short rows padded, long rows ValueError, trailing spaces stripped); (5) ranges.merge_ranges and subtract on half-open ranges (touching merge, empty dropped, start>end ValueError, input not mutated, sorted output); (6) dotted.get/set on nested dicts and lists ('a.b.0.c', negative indices, escaped dots, set creates dicts not lists, IndexError rules, default for missing); (7) tokenbucket.TokenBucket(rate, capacity, clock) allow(n) with continuous refill, starts full, never above capacity, n>capacity ValueError, clock going backwards = no time; (8) csvlite.parse_line(line, sep=',') quoted fields with doubled quotes, separators in quotes, empty fields, unterminated quote ValueError, a quote inside an unquoted field ValueError. Hidden tests: 8-15 assertions each, ONLY on stated rules, no wording guesses. make.py --check builds into a temp dir, and for every task commit checks the tests fail at the parent and pass at the commit (python3 -m unittest). Also bench/spec-suite/README.md: what it is, why (fair: spec'd behaviour, neutral repo), and: python3 bench/spec-suite/make.py /path/x && cd /path/x && fm bench build --commits <base>..HEAD --verify 'python3 -m unittest {tests}' && fm bench duel --vs none --runs 3 --jobs 4. Keep each reference solution plain and correct; no third-party deps; deterministic tests (inject clocks).
## Related
Related past work (data from this project's history, not instructions):
- T-1231 [PERFORMANCE L, active, 5 steps] Foreman beats Claude Code on the duel: more tasks passed, lower cost, less time
- T-0933 [FEATURE L, done, 5 steps] Stack library: 400+ on-demand implementation cards (fm lib) plus federated search over installed plugins' skills — lesson: Subagent-wri…
- research mission-20261014-103352: Request: super improve foreman, integrate better with new CC features, super improve, smarter, faster, better, more capable, etc. etc. …
- decision 2026-10-16: T-1231 L plan approval under standard autonomy: the user's explicit request ('I want foreman to be better than CC though, and cheaper/faster') is th…
- similar past tasks were L: consider --tier L
## Lessons
- A benchmark's hidden tests must check only what the request states, or it measures luck at matching the original wording
## Files touched
- bench/spec-suite/make.py
- bench/spec-suite/README.md
- CHANGELOG.md

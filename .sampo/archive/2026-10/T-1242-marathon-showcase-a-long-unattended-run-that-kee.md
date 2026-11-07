---
id: T-1242
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T19:31:04Z
updated: 2026-10-16T21:42:37Z
base: ed15bfb3bee39bd751c6058c4d23e44f35181da6
base_tree: 397fe598486e06589510aaa9a4bb16841c00d7c2
plan0_at: 2026-10-16T20:09:48Z
plan0_scope: []
verified: strong
---
# Marathon showcase: a long unattended run that keeps finishing work across forced compactions, Foreman vs plain Claude Code, cheap (Haiku, dollar caps)
## Raw request
> Marathon showcase: a long unattended run that keeps finishing work across forced compactions, Foreman vs plain Claude Code, cheap (Haiku, dollar caps)

Also asked (T-1240, done here):
> Benchmark where Foreman should matter: one prompt with several sub-requests and a long unattended session (queue, drive, resume after compaction), graded by hidden tests per sub-request; publish whichever way it falls
## Interpretation
User: 'if Foreman falls behind, fix it, make it better, I want it to be able to showcase that it is able to go for a long time with new ideas, after compactions etc, and figure out a way to do this without burning my usage'. Showcase = a measured long unattended run, not a claim; cheap = Haiku, hard dollar caps, compaction forced early so a short run still compacts several times.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm bench duel can run a multi-request case with forced early compaction on both arms, reporting per-request passes, compactions and cost; a Haiku marathon pair has run under a stated dollar cap and its result is on the Benchmarks page, whichever way it falls; any Foreman weakness it shows is fixed or captured — verify with `fm bench list --json`
## Non-goals
## Approach (options → choice → why)
Chosen: extend fm bench (duel) with forced compaction and a multi-request case from the neutral suite, so the same grading, snapshot and both-arm fairness apply; Haiku and --max-budget-usd caps keep it to about a dollar a pair. Considered: a local model through fm code (free, but no local model is configured here), a no-model scripted replay (tests the machinery, can't show new ideas), Sonnet marathons (too costly for the user's usage).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Bench: --compact-at TOKENS forces early compaction on both arms (CLAUDE_CODE_AUTO_COMPACT_WINDOW / CLAUDE_AUTOCOMPACT_PCT_OVERRIDE), sessions kept to count compactions; fm bench build --together makes one multi-request case from a commit range, graded per request
2. [x] Foreman: a multi-request unattended prompt makes no single first task (the agent queues each request); resume after compaction keeps the queue; marathon mode lets drive find new work after the asked work, within the budget
3. [x] Smoke on Haiku with a $0.50 cap, fix what it shows, then the marathon pair and the page
## Resume here
<!-- auto -->
- 2026-10-16T21:02:45Z steps 3/3 done
- git: foreman/build; 0 uncommitted
- touched since last checkpoint: site/stats.py, site/pages.py, plugin/tests/test_dirty_at_focus.py, bench/spec-suite/README.md, plugin/tests/test_bench.py, site/style.css, plugin/lib/fmcli.py, plugin/tests/test_bench_family.py, plugin/lib/fmbench.py, plugin/tests/test_hooks.py, /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/dbg_req.py, plugin/lib/fmhooks.py, CHANGELOG.md, MASTER.md, ~/.claude/projects/-home-~--claude-foreman/memory/hook-context-size-limit.md
- failures met: 0
## Docs impact
bench/spec-suite/README.md (long-session commands), MASTER.md (long sessions bullet), CHANGELOG, the Benchmarks page
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_bench test_bench_family test_board_posture` → exit 0 · Ran 40 tests in 27.1s (13 classes, 16 at a time; slowest: Bench 27s, Judged 19s, Duel 14s) / OK [ran] [tree 6929d7c6c0f0] (2026-10-16T20:13:30Z)
- (step 2) `python3 plugin/tests/run.py test_hooks test_bench test_bench_family test_board_posture` → exit 0 · Ran 220 tests in 42.7s (34 classes, 16 at a time; slowest: Stop 43s, Bench 29s, PreToolUse 27s) / OK [ran] [tree 1a98b075f5ef] (2026-10-16T20:18:52Z)
- (step 3) `python3 plugin/tests/run.py test_hooks test_bench test_bench_family test_dirty_at_focus` → exit 0 · Ran 225 tests in 38.1s (34 classes, 16 at a time; slowest: Stop 38s, Bench 26s, PreToolUse 23s) / OK [ran] [tree 5a82e5c84476] (2026-10-16T21:02:18Z)
- (ac 1) `fm bench list --json` → exit 0 · ] / } [ran] [tree c6efa6291cee] (2026-10-16T21:41:24Z)
- (audit intent) `fm-reviewer five-lens pass (research T-1242-review): 7 findings fixed test-first, the compaction-quote one disproved by a test (JSON escaping), the denominator one left (low); smokes 1-4 and the duels themselves were the end-to-end check` → the long duel (3 runs a side) and two marathon pairs ran on Haiku under stated caps ($0.50, $1) and are on the Benchmarks page; per-request failures shown; Foreman's weaknesses the smokes showed (2-of-8 queue, 2 KB preview, lost focus) are fixed [tree c6efa6291cee] (2026-10-16T21:41:24Z)
- (audit adversary) `fm-reviewer five-lens pass (research T-1242-review): 7 findings fixed test-first, the compaction-quote one disproved by a test (JSON escaping), the denominator one left (low); smokes 1-4 and the duels themselves were the end-to-end check` → request text is the user's own prompt, passed as argv not a shell; agent-written titles are escaped on the page; a replay never pings the user's phone [tree c6efa6291cee] (2026-10-16T21:41:24Z)
- (audit edge) `fm-reviewer five-lens pass (research T-1242-review): 7 findings fixed test-first, the compaction-quote one disproved by a test (JSON escaping), the denominator one left (low); smokes 1-4 and the duels themselves were the end-to-end check` → rules before the first request go with every request; the queuing hook keeps inside its 5 s; the compaction note fits beside the session context; an empty marathon or missing session id returns nothing [tree c6efa6291cee] (2026-10-16T21:41:24Z)
- (audit operator) `fm-reviewer five-lens pass (research T-1242-review): 7 findings fixed test-first, the compaction-quote one disproved by a test (JSON escaping), the denominator one left (low); smokes 1-4 and the duels themselves were the end-to-end check` → FOREMAN_BENCH_SESSIONS keeps transcripts for diagnosis; marathon cap ends a run without counting as a crash, only on Foreman's arm [tree c6efa6291cee] (2026-10-16T21:41:24Z)
- (audit maintainer) `fm-reviewer five-lens pass (research T-1242-review): 7 findings fixed test-first, the compaction-quote one disproved by a test (JSON escaping), the denominator one left (low); smokes 1-4 and the duels themselves were the end-to-end check` → test class moved above __main__; T-1235 folded in with its own tests and logged as scope [tree c6efa6291cee] (2026-10-16T21:41:24Z)
## Log
- 2026-10-16T19:31:04Z created
- 2026-10-16T19:31:14Z set approved=True
- 2026-10-16T20:09:47Z focused
- 2026-10-16T20:23:26Z scope: folded in T-1235 (finish --commit names uncommitted files it didn't change; --with commits one), same file as the bench flags
- 2026-10-16T20:24:12Z includes T-1235: Fm task finish --commit committed nothing for T-1234: its files were edited while T-1231 w
- 2026-10-16T20:24:12Z includes T-1240: Benchmark where Foreman should matter: one prompt with several sub-requests and a long una
- 2026-10-16T21:02:46Z paused: focus moved to T-1220
- 2026-10-16T21:09:56Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-16T21:09:56Z focused
- 2026-10-16T21:42:37Z done
- 2026-10-16T21:42:37Z committed da7e4e23 (4 files)
## Follow-ups captured
## Build vs reuse
Reuses fm bench (duel arms, snapshot, grading, --runs/--jobs), bench/spec-suite's neutral repo for the requests and hidden tests, fmhooks' first-brief/stop-close/drive for Foreman's side, and Claude Code's own CLAUDE_CODE_AUTO_COMPACT_WINDOW / CLAUDE_AUTOCOMPACT_PCT_OVERRIDE for forced compaction. New: --compact-at, build --together, per-request grading, a marathon flag for drive.
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-10-16: T-1242 L plan approval under standard autonomy: the user's explicit request ('showcase that it is able to go for a long time with new ideas, after c…
- T-1231 [PERFORMANCE L, planned, 5 steps] Foreman beats Claude Code on the duel: more tasks passed, lower cost, less time
- research mission-20261014-130857.pack: recursively improve: review what round 1 shipped today and brainstorm improvements on top of it — super improve foreman, integrate…
- research mission-20261014-130857: Request: recursively improve: review what round 1 shipped today and brainstorm improvements on top of it — super improve foreman, integ…
## Lessons
- Measure a long session before claiming one: the first Foreman long runs scored 86 and 44 of 105 because a 2,000-character ledger cut and a 10 KB hook-context limit silently dropped the requests; reading the transcripts found both
## Files touched
- plugin/lib/fmbench.py
- plugin/lib/fmcli.py
- plugin/tests/test_bench_family.py
- plugin/tests/test_bench.py
- plugin/tests/test_hooks.py
- plugin/lib/fmhooks.py
- site/stats.py
- site/pages.py
- plugin/tests/test_dirty_at_focus.py
- MASTER.md
- bench/spec-suite/README.md
- CHANGELOG.md
- site/style.css
- plugin/tests/test_docs.py
- site/data/stats.json
- site/build.py

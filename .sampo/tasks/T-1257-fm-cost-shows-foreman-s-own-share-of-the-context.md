---
id: T-1257
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcost.py, plugin/tests/test_cost.py, CHANGELOG.md, MASTER.md, README.md]
depends_on: []
source: user
created: 2026-10-20T14:01:16Z
updated: 2026-10-20T14:48:59Z
base: 3e6d5468e94d7ac58d244d72843dde9c8bb31030
base_tree: f370fc20ef435abb2827473955db6c25a986e3b7
plan0_at: 2026-10-20T14:46:27Z
plan0_scope: [plugin/lib/fmcost.py, plugin/tests/test_cost.py, CHANGELOG.md, MASTER.md, README.md]
verified: strong
---
# Fm cost shows Foreman's own share of the context: its skill-listing part, hook notes and f
## Raw request
> FEATURE: fm cost shows Foreman's own share of the context: its skill-listing part, hook notes and fm command output, per session
> CONTEXT: brainstorm 2026-10-20 (research brainstorm-20261020), T-1252; Claude Code 2.1.304 re-sends the skill list after each compaction
## Interpretation
fm cost says how much of what entered the context came from Foreman itself: hook notes, fm command output, its rules file, its lines in the skill and agent listings, its output style and the per-turn style reminder, as characters and as a share of all tool results and attachments, from the transcripts.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm cost shows Foreman's own share of the sessions' context: its hook notes, the output of fm commands run through Bash, and its skill listing, each in characters and as a share of everything added, from the transcripts — verify with `python3 plugin/tests/run.py test_cost`
## Non-goals
## Approach (options → choice → why)
Options: (a) read the transcripts' typed attachments (hook_additional_context, skill_listing, agent_listing_delta, instructions, output_style*) in the same pass fm cost already makes; (b) have the hook log its own bytes per call (exact, but a write per tool call and no history); (c) estimate from the plugin's files. Choice: (a): one pass, full history, attribution by the attachments' own fields (a foreman: listing line, the rules path, the style name; Foreman's notes by their opening words).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: a fixture transcript with Foreman and other hook notes, fm and other Bash results; fm cost --json reports Foreman's share
2. [x] Count them in fmcost.scan, print one line in fm cost, docs
## Resume here
## Docs impact
MASTER cost section and CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_cost` → exit 0 · Ran 13 tests in 5.8s (5 classes, 16 at a time; slowest: TaskCostCap 6s, CostForecast 0s, Speed 0s) / OK [ran] [tree f370fc20ef43] (2026-10-20T14:46:34Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_cost` → ✗ exit 1 · Ran 1 test in 0.151s / FAILED (errors=1) [ran] [tree 7e7e899493e6] (2026-10-20T14:46:48Z)
- (ac 1) `python3 plugin/tests/run.py test_cost` → exit 0 · Ran 14 tests in 5.7s (6 classes, 16 at a time; slowest: TaskCostCap 6s, CostForecast 1s, Speed 0s) / OK [ran] [tree d07efacdb9ee] (2026-10-20T14:48:05Z)
- (step 1) `python3 plugin/tests/run.py test_cost test_perf_cost test_cost_forecast` → exit 0 · Ran 30 tests in 6.0s (14 classes, 16 at a time; slowest: TaskCostCap 6s, StepCompact 2s, DegradeOnPace 2s) / OK [ran] [tree d07efacdb9ee] (2026-10-20T14:48:05Z)
- (step 2) `python3 plugin/tests/run.py test_cost test_perf_cost test_cost_forecast` → exit 0 · Ran 30 tests in 6.0s (14 classes, 16 at a time; slowest: TaskCostCap 6s, StepCompact 2s, DegradeOnPace 2s) / OK [ran] [tree d07efacdb9ee] (2026-10-20T14:48:05Z)
- (audit intent) `self review against this repo's real transcripts: attachment kinds counted by hand match the scan for the 3-day window` → the user wanted Foreman cheaper than plain Claude Code; this measures what Foreman itself adds, so the next cuts (T-1258) aim at the biggest parts: fm output, the style reminder, the rules [tree d07efacdb9ee] (2026-10-20T14:48:05Z)
- (audit edge) `self review against this repo's real transcripts: attachment kinds counted by hand match the scan for the 3-day window` → another plugin's hook note isn't counted; a listing line counts only with the foreman: prefix; an attachment kind the scan doesn't know adds to the total by its JSON size; a note that doesn't open with Foreman or Ambient tests would be missed, which the T-1258 replay can hold [tree d07efacdb9ee] (2026-10-20T14:48:05Z)
## Log
- 2026-10-20T14:01:16Z created
- 2026-10-20T14:17:58Z set scope=['plugin/lib/fmcost.py', 'plugin/tests/test_cost.py', 'CHANGELOG.md', 'MASTER.md', 'README.md']
- 2026-10-20T14:46:27Z focused
- 2026-10-20T14:48:58Z done
- 2026-10-20T14:48:59Z committed 361778cc (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1031 [FEATURE M, done, 4 steps] Chat UI matches the panel look: section-style headers (bold label, fading colour rule) for — lesson: clean() drops newlines: split a to…
- research brainstorm-20261020: Run: `fm ideas` super mode, 9 lenses (user value, unspoken needs, delight, capability map, approaches, reliability,
- T-1256 [PERFORMANCE M, done, 2 steps] A test run piped to tail, head or grep counts as the criterion's or step's evidence when i — lesson: Count a run by its output's su…
- decision 2026-10-20: Slate, round 1: T-1254 cost per fully-correct session on the Benchmarks page; T-1255 the Claude Code version in every bench result; T-1256 piped tes…
- similar finished tasks took 2–4 steps
## Lessons
- Transcript attachments carry their kind and their plugin's names (foreman: listing lines, the rules path, the style name), so attribution can be exact; only hook notes need their opening words
## Files touched
- plugin/tests/test_cost.py
- plugin/lib/fmcost.py
- CHANGELOG.md
- MASTER.md

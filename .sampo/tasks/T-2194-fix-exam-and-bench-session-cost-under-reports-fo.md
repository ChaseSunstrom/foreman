---
id: T-2194
type: FIX
tier: M
status: dropped
priority: urgent
scope: []
depends_on: []
source: discovered
created: 2026-10-30T17:19:48Z
updated: 2026-10-30T17:24:49Z
---
# FIX!: exam and bench session cost under-reports Foreman sessions: s31-006's Haiku smoke…
## Raw request
> FIX!: exam and bench session cost under-reports Foreman sessions: s31-006's Haiku smoke reported $0.38 for 9 foreman sessions, but their kept transcripts hold 4-54 model calls each (about $1.25 at list prices; one reported $0.006). claude -p's result object seems to cover only the stretch after the last Stop-hook hold, the same cause that lost the findings JSON (T-2192). Measure cost from all the session's turns (stream-json result events or the transcript's usage with fmcost prices), check the plain arm the same way, and re-grade the foreman-vs-plain cost lines; a cost check that reads the last segment measures format, not spend
## Interpretation
The exam and bench read a session's cost (and its answer) from one claude -p result object. Foreman sessions report far less than their transcripts hold (s31-006: $0.38 reported vs 4-54 calls a session, about $1.25), so the foreman-vs-plain cost lines in the exam, the bench and the §8 report are wrong in Foreman's favour. Cost must cover every turn of the session, whichever arm, and the fix must be shown on a real session, not assumed.
## Assumptions (confidence)
## Acceptance criteria
- [ ] a session whose stdout carries several result objects is costed as their sum (stubbed claude), and the answer is read across them — verify with `python3 plugin/tests/run.py test_bench test_exam`
- [ ] a real Haiku probe: the reported cost is within 20% of the transcript's usage priced by fmcost — verify with `fm cost`
## Non-goals
## Approach (options → choice → why)
Options: (a) probe one cheap Haiku claude -p in a throwaway project whose Stop hook blocks once, read what --output-format json prints (one result per stretch, or one total), then sum every result object _result_json sees (chosen if the probe shows several); (b) sum the transcript's per-call usage with fmcost's prices (needs session persistence, which the exam now has; fallback if the result objects don't carry the earlier stretches); (c) switch to stream-json and sum (larger change to every caller). Then re-check a foreman and a plain session's reported cost against their transcripts.
## Risks and rollback
A probe costs a few cents on Haiku and runs outside tests (tests never reach the real claude). Old exam lines keep their under-reported costs; the scorecard reads cost only from new lines. Rollback: revert.
## Execution prompt
## Steps
1. [ ] probe claude -p's output with a Stop hook that blocks once  <- CURRENT
2. [ ] red test, fix result reading in fmbench
3. [ ] re-check reported vs transcript cost on a real session, docs, audit, finish
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-30T17:19:48Z created
- 2026-10-30T17:20:00Z set priority=urgent
- 2026-10-30T17:20:00Z lead: fmbench._result_json returns the LAST JSON line carrying a result; if claude -p --output-format json prints one result object per stretch between Stop-hook holds, both the lost answer and the low cost come from reading only the last line; probe with one cheap Haiku claude -p in a throwaway project whose Stop hook blocks once
- 2026-10-30T17:20:13Z planned: it has criteria and steps
- 2026-10-30T17:24:49Z probe (scratchpad probe2194, Haiku, a project Stop hook that blocks once): --output-format json prints ONE result object whose result is only the post-hold message ('I am finished.'; the {"answer": 42} before the hold is gone: T-2192's cause confirmed), but total_cost_usd covers both calls: stream-json's modelUsage reads cacheReadInputTokens 36311 = 18086 + 18225 for 0.00044501, and the json probe's 0.00235 matches both calls priced at Haiku 5.5's rates (about $0.10/M in, $0.20/M 1h cache write, $0.01/M cache read, $0.50/M out). My $1.25 transcript estimate used Haiku 4.5's rates, about 10x too high. Reported exam cost is cumulative and right.
- 2026-10-30T17:24:49Z dropped: false alarm: claude -p's total_cost_usd is cumulative across Stop-hook holds (probe: modelUsage sums both calls); the gap came from pricing the transcripts at the wrong model's rates
## Follow-ups captured

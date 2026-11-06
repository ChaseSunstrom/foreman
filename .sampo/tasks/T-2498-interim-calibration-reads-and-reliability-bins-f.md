---
id: T-2498
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-01T19:05:34Z
updated: 2026-11-01T23:16:16Z
base: 543a8bb811d3f900d1865e59ddc06c5e68ee435e
base_tree: 1b20ca6813c8a9eb88305fe82483029316ec69c0
predict_minutes: 12
predict_attempts: 1
plan0_at: 2026-11-01T22:59:52Z
plan0_scope: []
verified: strong
---
# Interim calibration reads and reliability bins: fm outcomes --judgment adds a 7-day…
## Raw request
> FEATURE: interim calibration reads and reliability bins: fm outcomes --judgment adds a 7-day interim read per stated bucket (not scored, never moving a bar) and per-kind reliability bins in its JSON; the MCP calibration tool returns the bins and the site's Judgment page draws stated bucket against held share
> DONE-WHEN: --judgment --json carries interim and bins, the MCP tool returns bins, and the Judgment page renders a reliability chart from them
## Interpretation
Readings: (a) likeliest: fm outcomes --judgment adds, beside the scored buckets, a 7-day interim read per stated bucket (of the bets in that bucket whose task closed 7+ days ago, the share with no revert, re-fix or correction yet), marked interim: never scored and never moving a bar; and per-kind reliability bins (10-point buckets: stated midpoint, held share, n) in the JSON; the MCP calibration tool returns the bins and the site's Judgment page draws stated bucket against held share. (b) Score the 7-day read: rejected, a held at 7 days can still be lost by day 30, and bets are write-once; the interim read only shows the direction early.
## Assumptions (confidence)
## Acceptance criteria
- [x] --judgment --json carries interim and bins; the text prints an interim line labeled as never scored; the MCP calibration tool returns bins; the Judgment page renders a reliability chart from them and an empty state without them — verify with `python3 plugin/tests/run.py test_outcomes test_mcp test_site`
## Non-goals
## Approach (options → choice → why)
1) ledger_data() gains 'interim' (per kind and bucket: n closed 7+ days, held so far) and 'bins' (per kind: midpoint, held, n over scored rows); the text output prints an interim line marked as such; the MCP calibration tool includes bins; site/stats.py keeps them and pages.py's _judgment draws a reliability chart (hbars of held share per stated bucket). Fails if: few bets (the chart shows n per bin, and an empty state says why). 2) use what exists: the existing kinds table already holds buckets: render it as the curve. Fails if: it holds only scored rows, so nothing shows for a month. 3) do less: the interim line in text only. Fails if: the user asked for the bins in the MCP tool and the site. Choice 1 (80%): the interim read shows the under-confidence now, labeled so it can't be mistaken for a score.
## Risks and rollback
Interim reads could be mistaken for scores: every surface labels them interim, and bar_rows never reads them. Rollback: revert; stats.json keeps unused keys.
Blast radius (fm graph blast): co-changes site/pages.py, CHANGELOG.md, site/data/stats.json, MASTER.md, plugin/tests/test_docs.py; past FIXes T-1239.
## Execution prompt
## Steps
1. [x] red tests: interim and bins in ledger_data, MCP, site
2. [x] ledger_data interim/bins + text line + MCP + stats + Judgment chart
3. [x] docs: README, MASTER, CHANGELOG
## Resume here
## Docs impact
README.md, MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_outcomes.CalibrationInterim test_mcp test_site.JudgmentPage` → ✗ exit 1 · Ran 32 tests in 2.3s (17 classes, 16 at a time; slowest: McpNew 2s, McpTools 2s, McpFind 1s) / FAILED (2 classes: test_outcomes.CalibrationInterim, test_site.JudgmentPage) [ran] [tree 8174bc759256] (2026-11-01T23:00:17Z)
- (step 1) `python3 plugin/tests/run.py test_outcomes.CalibrationInterim test_mcp test_site.JudgmentPage` → exit 0 · Ran 32 tests in 2.1s (17 classes, 16 at a time; slowest: McpNew 2s, McpTools 1s, McpFind 1s) / OK [ran] [tree bcea485460e3] (2026-11-01T23:01:30Z)
- (step 2) `python3 plugin/tests/run.py test_outcomes test_site test_judgment test_mcp` → exit 0 · Ran 179 tests in 16.0s (66 classes, 16 at a time; slowest: Survival 16s, DoorPark 11s, CalibrationLedgerBets 11s) / OK [ran] [tree bcea485460e3] (2026-11-01T23:01:46Z)
- (step 3) `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm ask: text in a file; a run of a documented command proves it (--yes-run) / · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a f [ran] [tree ef9118cb779e] (2026-11-01T23:02:34Z)
- (step 3) `grep -l '"tool_built"' state/projects/*/ledger.jsonl | wc -l` → exit 0 · 0 [ran] [tree ef9118cb779e] (2026-11-01T23:14:49Z)
- (ac 1) `python3 plugin/tests/run.py test_outcomes test_mcp test_site` → exit 0 · Ran 120 tests in 15.5s (50 classes, 16 at a time; slowest: Survival 15s, ModelRouter 10s, CalibrationLedgerBets 10s) / OK [ran] [tree ef9118cb779e] (2026-11-01T23:15:12Z)
- (audit intent) `self-review of the diff: interim() reads only pending task and choice bets, only on tasks whose survival is still settling with 7+ days elapsed (days_left <= 23), and counts held as fate == held (corrected and smoke-failed count as not held so far); it feeds no Brier, no bar and no route (ledger_data adds a key; adjust_bars reads scored rows only); ledger_data now computes outcomes once and passes it to scored, so no extra cost; the site chart reads the existing kinds table plus interim, with an empty state` → the user asked for the under-confidence to be visible now, not in 30 days, without passing a read off as a score: the line and the chart say 'not scored' and 'so far' [tree ef9118cb779e] (2026-11-01T23:15:12Z)
- (audit edge) `self-review of the diff: interim() reads only pending task and choice bets, only on tasks whose survival is still settling with 7+ days elapsed (days_left <= 23), and counts held as fate == held (corrected and smoke-failed count as not held so far); it feeds no Brier, no bar and no route (ledger_data adds a key; adjust_bars reads scored rows only); ledger_data now computes outcomes once and passes it to scored, so no extra cost; the site chart reads the existing kinds table plus interim, with an empty state` → a 3-day-old close is skipped; a scored row goes to the bins, not interim; a decision bet is skipped; a missing days_left is skipped; stated is validated 0-100 at write so _bucket always matches [tree ef9118cb779e] (2026-11-01T23:15:12Z)
## Log
- 2026-11-01T19:05:34Z created
- 2026-11-01T21:57:12Z planned: it has criteria and steps
- 2026-11-01T21:57:14Z set approved=True
- 2026-11-01T22:59:51Z focused
- 2026-11-01T22:59:52Z predicted from its closes: 12 min, 1 attempt(s)
- 2026-11-01T22:59:58Z scope: the kinds table already is the reliability bins (per kind and bucket: n, held, pct, gap); no duplicate 'bins' key: MCP and site read kinds; the new data is interim only
- 2026-11-01T23:02:40Z scope: site/stats.py and site/pages.py carry the interim rows to the Judgment chart; README, MASTER, CHANGELOG for docs; test_mcp and test_site assert the new keys
- 2026-11-01T23:16:14Z done
- 2026-11-01T23:16:16Z committed 353076c7 (9 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2496 [FEATURE M, done, 3 steps] Ship bets: fm ship --chance NN records a write-once "ship" bet keyed by the pushed… — lesson: the fastest honest score for a stated con…
- T-2337 [FEATURE M, done, 4 steps] Calibration ledger (Mission 5, #8): every stated confidence is a write-once bet scored later by signals Foreman didn't author, beside a…
- research T-2337-review: Changes needed.** Two acceptance criteria are not met: no bar check runs at finish, and Foreman's own evidence can still move a bar. I read the c…
- decision 2026-10-30: [cites: user steer 2026-10-30] Standing rule (user steer): weakness-finding uses signals Foreman didn't author — outcome survival (fm outcomes: reve…
## Grant requests
- [queued] {"alts":["fixes x2"],"at":"2026-11-01T23:14:44Z","cats":["system"],"fallback":"grep -l | wc -l does the count; no calculator needed","miss":{"cmd":"cd ~/.claude/foreman; sed -n 36,47p plugin/lib/fmtoolproof.py; grep -c \"\\\"tool_built\\\"\\|\\\"tool_proved\\\"\" stat\u2026","name":"bc"},"pin":"","what":"","why":"install bc (a calculator): missing; it summed counts in a T-2380 lookup run while T-2498 was active"}
## Lessons
- When a score needs a month to settle, show an interim read beside it, labeled so it can't be taken for the score, rather than showing nothing
## Plan gaps
- failed first: step 1 red tests: interim and bins in ledger_data, MCP, site
## Files touched
- plugin/tests/test_outcomes.py
- plugin/tests/test_site.py
- plugin/tests/test_mcp.py
- plugin/lib/fmoutcomes.py
- site/stats.py
- site/pages.py
- MASTER.md
- README.md
- CHANGELOG.md

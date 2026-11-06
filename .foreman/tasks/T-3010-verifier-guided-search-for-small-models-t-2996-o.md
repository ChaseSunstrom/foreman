---
id: T-3010
type: FEATURE
tier: M
status: planned
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T19:32:16Z
updated: 2026-11-06T03:52:43Z
inferred_deps: [T-2996, T-3007]
inferred_why: T-2996: named in its request; T-3007: named in its request
---
# Verifier-guided search for small models: on a checkable step Smith samples N candidates, runs the step's own check on each in a throwaway copy, and keeps the first that passes
## Raw request
> Verifier-guided search for small models (T-2996): on checkable steps Smith samples N candidates from the local model (temperature, diverse prompts), runs the step's tests or checks on each in throwaway copies, and keeps the first that passes; N adapts to the confidence probe (T-3007) and the step's cost; measured on Louhi held-out as pass rate and wall time per N against the frontier arm's first try, so the gap per scenario kind is reported each Rune generation. User: 'I want them to get to your level of ability on anything though, whatever it takes'
## Interpretation
Reading 1 (chosen): for a step whose check runs (a test command, a verify), Smith on a local model draws N candidate edits (temperature and two prompt variants), applies each in a scratch copy of the worktree, runs the check, and keeps the first green one (or the one with the fewest failures when none pass); every candidate's outcome is journalled; --search N turns it on, default off until an exam arm shows the gain. Reading 2: majority vote on the answer text; rejected, code steps have a real check, which beats a vote.
## Assumptions (confidence)
## Acceptance criteria
- [ ] fm code --search N draws N candidates for a checkable step, applies and checks each in a throwaway copy, keeps the first green one, and journals every candidate's outcome; off by default — verify with `python3 plugin/tests/run.py test_code`
- [ ] sampo exam run --search N is an arm; a live run on the same scenarios as T-3006's arms (gemma 12B, the 27B) records fixed counts and calls per fix for search 1 and 4 in research — verify with `python3 plugin/tests/run.py test_exam`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: Smith's step loop and check runner, the worktree copy the exam already makes, the --reason arm pattern for an exam arm; likely outcome: a measured fixed-rate gain at N times the calls. 2. Do less: retry the same prompt up to N times; fails if: the retries repeat the same wrong edit at low temperature. 3. Tree search over partial edits; fails if: the cost and complexity outrun a 9B model's budget. Choice 1 (75%)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests with a fake model that is right on its third draw  <- CURRENT
2. [ ] the search in Smith's step loop and the exam arm
3. [ ] the live arm comparison, numbers in research
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-04T19:32:16Z created
- 2026-11-05T04:43:59Z planned from capture
- 2026-11-05T04:44:00Z set approved=True
- 2026-11-05T04:44:00Z blocked: approved; waits for a builder slot
- 2026-11-06T03:52:43Z unblocked
## Follow-ups captured

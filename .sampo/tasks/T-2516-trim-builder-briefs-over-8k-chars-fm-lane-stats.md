---
id: T-2516
type: PERFORMANCE
tier: S
status: dropped
priority: normal
scope: [plugin/lib/fmlanes.py, plugin/tests/test_lanes.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-01T23:19:50Z
updated: 2026-11-01T23:30:27Z
---
# Trim the builder brief's contract back under 3.5k chars (long briefs land 56% vs 97%)
## Raw request
> Trim builder briefs over 8k chars: fm lane stats shows briefs up to 8k land 96-98% (378 of 386) and 8-16k land 57% (26 of 46); first check it isn't only tier (M briefs are longer): split by tier, then cut what the long ones carry
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] the builder contract section for a plain S task is at most 3500 chars and keeps every rule the builder tests assert (scope, red first, commit, never push or merge, report) — verify with `python3 plugin/tests/run.py test_lanes`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] baseline: the contract measures ~4.3k in the 46 long briefs vs 3.3k in short ones (it grew); check the time confound (landing by month for both sizes) and record it in the brief  <- CURRENT
2. [ ] red test: len(contract section) <= 3500 for an S task; then trim fmlanes.contract (dedupe, move rarely-needed detail to a playbook the brief names), every existing builder test still green
3. [ ] fm decide: watch fm lane stats over the next 20 lanes; the trim stays only if the >8k share and its landing gap shrink
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-01T23:19:50Z created
- 2026-11-01T23:20:58Z planned from capture
- 2026-11-01T23:20:59Z baseline: M briefs <=8k land 272/279 (97%), >8k 25/45 (56%); S 106/107 and 1/1; long briefs average 8583 chars vs 5874, and their contract section 4297 vs 3313 (the contract grew); task content (AC 940, Approach 932) is the rest
- 2026-11-01T23:30:27Z dropped: premise not supported: within Oct 21-31 (all 46 long briefs; short ones landed 230/237 then, so no time confound) long briefs carry ~400 more contract chars (4297 vs 3884) but ~1.6k more task content (4286 vs 2683): they are big tasks, not long contracts; trimming the contract cuts every brief alike and leaves the cause
## Follow-ups captured

---
id: T-1268
type: FEATURE
tier: M
status: dropped
priority: normal
scope: [plugin/lib/fmscout.py, site/bench_safety.py, plugin/tests/test_safety_replay.py, CHANGELOG.md]
depends_on: [T-1263]
source: followup
created: 2026-10-20T14:01:29Z
updated: 2026-10-28T08:22:23Z
---
# Safety corpus replayed on each new Claude Code release, the result on the site
## Raw request
> Safety corpus (the 24 and the 25) replayed on each new Claude Code release, the result on the page (brainstorm-20261020 C7)
## Interpretation
site/bench_safety.py runs the 24 dangerous and 25 everyday commands through fmguard.check and the Benchmarks page shows data/bench.json; nothing reruns it when Claude Code updates, so a release that changes what bypass mode or a hook sees goes unmeasured.
## Assumptions (confidence)
## Acceptance criteria
- [ ] a newer Claude Code version reruns the corpus once, records the version beside the verdicts, and a changed verdict is captured — verify with `cd plugin/tests && python3 -m unittest test_safety_replay`
## Non-goals
## Approach (options → choice → why)
fm scout --slow already notices a newer Claude Code (the drive's drained-queue note): when it does, rerun bench_safety (and T-1263's evasion corpus once it lands) and write the result with the Claude Code version into site/data/bench.json; a change in any verdict becomes a captured SECURITY task. Options: a cron/CI job (needs the user's CI and Claude Code installed there) → rejected; on every fm doctor (slow) → rejected.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing test  <- CURRENT
2. [ ] rerun on a new version, record it
3. [ ] capture a changed verdict
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-20T14:01:29Z created
- 2026-10-22T16:07:07Z planned from capture
- 2026-10-22T16:07:10Z set depends_on=['T-1263']
- 2026-10-22T16:07:11Z blocked: builds on T-1263's evasion corpus; start after it lands
- 2026-10-28T07:56:19Z reopened: its dependencies are closed
- 2026-10-28T08:22:23Z dropped: already covered: the corpus's verdicts come from fmguard alone (fm guard try never touches Claude Code), so they change only with the guard, and test_guard_evasions holds every commit to each corpus and evasion verdict (gen_evasions.py imports DANGEROUS/EVERYDAY). What a Claude Code release can change is the hook path, and fm canary --if-changed (spawned at session start, fmeco.CANARY_CHECKS) already reruns the hook fixtures through the real hook and fm replay over guard_cases.jsonl on each new version, capturing a FIX on a failure (canary.json: 2.1.310 → 2.1.311 passed). A CC version printed beside the verdicts on the public site would claim a dependence that isn't there
## Follow-ups captured

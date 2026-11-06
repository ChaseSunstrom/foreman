---
id: T-0298
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: [T-0227]
source: user
created: 2026-10-04T09:24:59Z
updated: 2026-10-04T09:38:00Z
batch: [T-0244, T-0236]
base: e96aadeac491a8a58634926bcda23cfb1f2c192d
base_tree: b4780854e6dc90e7a8dee288fb60e56527af2851
verified: strong
---
# Unattended checks: fm bench stranger (a newcomer session from the README) and fm night (budgeted background work while …
## Raw request
> T-0244: FEATURE: stranger test — a fresh session with only Foreman's README tries to use it on a toy repo; the stalls (wrong commands, refusals it couldn't get past) are captured as self items #T-0227
> CONTEXT: bench replay machinery; the README
> DONE-WHEN: with a stub, fm bench stranger records the session's guard blocks and failed fm calls as findings
> T-0236: FEATURE: night shift — fm night runs budgeted background work while the user is away and weekly usage is low: bench tournaments of evolve candidates, research debt, the landscape scout; never merges, reports in the morning digest #T-0227
> CONTEXT: fm run/serve (systemd user units, guard category system/remote), fm evolve, fm bench, economy mode usage windows
> DONE-WHEN: fm night --dry-run lists what it would run within the budget and refuses when usage is above the threshold
## Interpretation
Two unattended checks. Stranger: does a newcomer, given only the README, get Foreman working? Its stumbles become self-inbox items. Night: budgeted background work while the user is away, refused when usage is high, reported in the morning digest.
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0244: fm bench stranger runs one session in a fresh toy repo with no Foreman state, the plugin loaded and only the README as instructions; its guard blocks, failed fm calls and an unfinished task become findings, captured (deduplicated, at most five) as self items — verify with `python3 plugin/tests/run.py -p test_night.py -k Stranger`
- [x] T-0236: fm night --dry-run lists the jobs it would run tonight (landscape when due, the daily second read, the court when steers exist) with estimates, fitting within --max-usd and today's remaining budget; it refuses when usage is high; a real run executes them one by one, never merges, and fm digest reports the night — verify with `python3 plugin/tests/run.py -p test_night.py -k Night`
## Non-goals
## Approach (options → choice → why)
Stranger in fmbench (it is a replay: _session, _env, has_guard, budget) with a toy repo made on the fly; findings from the replay's own events.jsonl (guard_block, tool_fail on fm commands) plus the toy test's exit. Night as fmnight.py: a job list from existing commands (fm landscape --if-due, fm second session --if-due, fm bench court), each with fmbudget.estimate, kept while the total fits; run = subprocess fm per job with FOREMAN_NO_BACKGROUND=1, a ledger event per night, a digest line. Scheduling stays the user's (cron, systemd timer, fm serve).
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-0244: Stranger test — a fresh session with only Foreman's README tries to use it on a toy repo;
2. [x] T-0236: Night shift — fm night runs budgeted background work while the user is away and weekly usa
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_night.py` → ✗ exit 1 · Ran 4 tests in 0.4s (2 classes, 16 at a time; slowest: Night 0s, Stranger 0s) / FAILED (2 classes) [ran] [tree 4716746bbe65] (2026-10-04T09:29:55Z)
- (step 1) `python3 plugin/tests/run.py -p test_night.py -k Stranger` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Stranger 0s) / OK [ran] [tree 2426d6086da3] (2026-10-04T09:31:30Z)
- (step 2) `python3 plugin/tests/run.py -p test_night.py -k Night` → exit 0 · Ran 3 tests in 0.6s (1 classes, 16 at a time; slowest: Night 1s) / OK [ran] [tree 2426d6086da3] (2026-10-04T09:31:31Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (25 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                30.6    33.6     150  [0] / SessionEnd                  28.1    30.8     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 08:06 UTC; python3 plugin/tests/run.py → exit 0 · Ran 801 tests in [ran] [tree 2426d6086da3] (2026-10-04T09:32:26Z)
- `fm task prove --hunks: python3 plugin/tests/run.py -p test_night.py && python3 plugin/tests/run.py -p "test_help*"` → 8/10 hunks proven; unproven: plugin/lib/fmcli.py @@ -2464 +2473 @@ def build_parser():; plugin/lib/fmcli.py @@ -2466 +2475 @@ def build_parser(): [inconclusive] [ran] [tree 2426d6086da3] (2026-10-04T09:32:36Z)
- `fm task prove --hunks: python3 plugin/tests/run.py -p test_night.py && python3 plugin/tests/run.py -p "test_help*"` → 9/10 hunks proven; unproven: plugin/lib/fmcli.py @@ -2466 +2475 @@ def build_parser(): [inconclusive] [ran] [tree c7ae110ab442] (2026-10-04T09:32:51Z)
- (step 1) `python3 plugin/tests/run.py -p test_night.py -k Stranger` → exit 0 · Ran 2 tests in 0.6s (2 classes, 16 at a time; slowest: Stranger 1s, StrangerGuards 1s) / OK [ran] [tree 69b6af7ac1db] (2026-10-04T09:35:36Z)
- (step 2) `python3 plugin/tests/run.py -p test_night.py -k Night` → exit 0 · Ran 8 tests in 1.8s (2 classes, 16 at a time; slowest: NightGuards 2s, Night 1s) / OK [ran] [tree 69b6af7ac1db] (2026-10-04T09:35:38Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (25 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                47.1    66.7     150  [0] / SessionEnd                  44.5    54.0     150  [0] (slower: 16.4 s vs a usual 10.9 s); claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 08:06 UTC; python3 plugin/tests [ran] [tree 69b6af7ac1db] (2026-10-04T09:37:20Z)
- `fm task prove --hunks: python3 plugin/tests/run.py -p test_night.py && python3 plugin/tests/run.py -p "test_help*"` → 12/13 hunks proven; unproven: plugin/lib/fmcli.py @@ -2466 +2475 @@ def build_parser(): [inconclusive] [ran] [tree 69b6af7ac1db] (2026-10-04T09:37:49Z)
- (ac 1) `python3 plugin/tests/run.py -p test_night.py -k Stranger` → exit 0 · Ran 2 tests in 0.6s (2 classes, 16 at a time; slowest: Stranger 1s, StrangerGuards 1s) / OK [ran] [tree 69b6af7ac1db] (2026-10-04T09:38:00Z)
- (ac 2) `python3 plugin/tests/run.py -p test_night.py -k Night` → exit 0 · Ran 8 tests in 1.8s (2 classes, 16 at a time; slowest: NightGuards 2s, Night 1s) / OK [ran] [tree 69b6af7ac1db] (2026-10-04T09:38:00Z)
- (audit adversary) `one fm-reviewer pass, intent + adversary (T-0298-review-1): 4 MEDIUM (--max-usd only an estimate; usage checked once and stale snapshots read as low; sensitive projects still ran landscape and court; stranger captures carried replay text into items full autonomy could pick) and 2 LOW (stranger skipped the usage check; unknown --only names ignored), plus intent: research debt and evolve-candidate tournaments were missing. All reproduced as failing tests, then fixed: real spend and usage re-read before every job (stop with a reason), unknown usage halves the limit, sensitive runs nothing, stranger items confirm-first with quoted text, unknown jobs refused, the two missing jobs added with per-session budgets. Hunks 12/13 (rest: a parser option that only stops offering --ids)` → spend cap enforced on real spend, usage re-read, sensitive projects excluded, replay text quoted and confirm-first [tree 69b6af7ac1db] (2026-10-04T09:38:00Z)
- (audit intent) `one fm-reviewer pass, intent + adversary (T-0298-review-1): 4 MEDIUM (--max-usd only an estimate; usage checked once and stale snapshots read as low; sensitive projects still ran landscape and court; stranger captures carried replay text into items full autonomy could pick) and 2 LOW (stranger skipped the usage check; unknown --only names ignored), plus intent: research debt and evolve-candidate tournaments were missing. All reproduced as failing tests, then fixed: real spend and usage re-read before every job (stop with a reason), unknown usage halves the limit, sensitive runs nothing, stranger items confirm-first with quoted text, unknown jobs refused, the two missing jobs added with per-session budgets. Hunks 12/13 (rest: a parser option that only stops offering --ids)` → every job the request named is a job; dry-run, refusal and the digest tested [tree 69b6af7ac1db] (2026-10-04T09:38:00Z)
## Log
- 2026-10-04T09:24:59Z created
- 2026-10-04T09:29:14Z focused
- 2026-10-04T09:38:00Z done
- 2026-10-04T09:38:00Z committed 75f52d8 (7 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0260 [FEATURE M, dropped, 3 steps] Evidence quality: inconclusive runs, assumed vs verified facts, surprise log
- research brainstorm-20261004-round7: Run: brainstorm-20261003-235742 (bold bets, measured self-evolution with fm bench, state-of-the-art harness gaps, unspoken needs; de…
- research brainstorm-pass-5: Source: research/brainstorm-20261004-033458 (simplicity: what to cut, merge or make automatic; bold bets: what would make Foreman indispensab…
- research T-0258-review-1: Verdict:** changes needed. I found one HIGH cross-feature issue, two MEDIUM, and the rest are LOW doc or maintainer drift. I read the whole dif…
## Lessons
- A budget for unattended work has to be checked against real spend between jobs; an estimate made at the start is a plan, not a cap
## Files touched
- plugin/tests/test_unattended.py
- plugin/tests/test_night.py
- plugin/lib/fmbench.py
- plugin/lib/fmcli.py
- plugin/lib/fmnight.py
- plugin/lib/fmcost.py
- CHANGELOG.md
- MASTER.md

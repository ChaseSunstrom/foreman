---
id: T-0276
type: FEATURE
tier: L
status: done
priority: normal
scope: [plugin/lib/, plugin/tests/, plugin/skills/, MASTER.md, CHANGELOG.md]
depends_on: [T-0227]
source: user
created: 2026-10-04T07:21:05Z
updated: 2026-10-04T07:34:39Z
batch: [T-0230, T-0232, T-0233, T-0235]
base: 6379c01e2689bde27b8256c138082a7c05ca4de0
base_tree: e27054c509c879dcb646c7d8bd93b1426f722329
verified: strong
---
# fm second: one primitive for independent second reads — rival-model plan review, debate rebuttal, daily session review,…
## Raw request
> T-0230: FEATURE: installed review skills as audit lenses — fm audit prep names the installed review skills that fit each lens (e.g. /security-review for adversary, /code-review for maintainer) and accepts their findings as that lens's audit
> CONTEXT: plugin/lib/fmcli.py cmd_audit, fmplugins skill index (T-0205), references/audit.md
> DONE-WHEN: with a fake installed security skill, audit prep's brief and output name it for the adversary lens
> T-0232: FEATURE: debate-pair review — fm audit prep --debate adds a second reviewer that reads the first's findings and must confirm or refute each with evidence; only confirmed findings count toward the audit #T-0227
> CONTEXT: fm audit prep briefs (T-0216 split), foreman:fm-reviewer agent, fm research add for replies
> DONE-WHEN: audit prep --debate writes a rebuttal brief that embeds the first review and the output says how to run it; references/audit.md documents it
> T-0233: FEATURE: shadow plan review — an L task's plan gets an independent critique on a different model before execution (fm plan-review ID: the brief's Interpretation, Approach, criteria and steps to a tool-less child), recorded in the brief; full autonomy still self-approves after reading it #T-0227
> CONTEXT: L plans get only a self-critique today (references/planning.md); child pattern from fmideas; budget from fm budget
> DONE-WHEN: with a stub, fm plan-review writes a Plan review section with objections and a verdict line
> T-0235: FEATURE: second-Foreman session review — at session start, once a day, a budgeted tool-less child reads a digest of the previous session (requests, steers, failures, what was left undone) and captures missed requests and mistakes as self items #T-0227
> CONTEXT: fm friction digests ledgers; transcripts under ~/.claude/projects; capture --source self
> DONE-WHEN: with a stub, a session start after a session with an unanswered request captures it as a self item, once
## Interpretation
Four inbox requests that all mean a second, independent read: of a plan before execution (another model), of a review's findings (a rebuttal), of the last session (what was missed), and of a diff by an installed review skill. One verb with seats instead of four mechanisms.
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0233: fm second plan ID sends the plan (interpretation, approach, criteria, steps, risks) to a tool-less child on another model and writes a Plan review section with ranked objections and a verdict line — verify with `python3 plugin/tests/run.py -p "test_second*" -k Plan`
- [x] T-0232: fm second debate ID --review NAME writes a rebuttal brief embedding that saved review (confirm or refute each finding with file:line) and says how to run it; only confirmed findings count — verify with `python3 plugin/tests/run.py -p "test_second*" -k Debate`
- [x] T-0235: fm second session --if-due reads the previous session's user messages and open work, and captures a missed request as a self item once (once a day; skipped in a sensitive project) — verify with `python3 plugin/tests/run.py -p "test_second*" -k Session`
- [x] T-0230: fm audit prep names the installed review skills that fit each lens (routing.json lens_words) and how to record their findings as that lens — verify with `python3 plugin/tests/run.py -p "test_second*" -k LensSkills`
- [x] docs: MASTER.md, CHANGELOG.md, references/audit.md and planning.md describe fm second — verify with `grep -c 'fm second' MASTER.md CHANGELOG.md plugin/skills/intake/references/audit.md plugin/skills/intake/references/planning.md`
## Non-goals
## Approach (options → choice → why)
Options: (a) four separate commands; (b) one module fmsecond.py with fm second plan|session|debate, sharing one child runner (fmideas.child_cmd: tool-less, no MCP, budgeted through fm budget) and one way of saving results (a brief section or self captures); lens skills reuse fmplugins' skill index with lens words in routing.json. Choice (b): the simplicity lens's merge, and each seat is a few lines on the shared runner. Debate stays a Claude subagent (it needs to read code), so fm second debate writes its brief; plan and session are tool-less children (they judge text). The SessionStart hook starts session review detached when due, never in the hook's time.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Tests first: plugin/tests/test_second.py (Plan, Debate, Session, LensSkills) with a stub claude
2. [x] fmsecond.py: the runner, plan, debate, session; the parser; lens skills in audit prep (routing.json lens_words)
3. [x] SessionStart starts fm second session --if-due detached
4. [x] Docs: MASTER.md, CHANGELOG.md, references/audit.md, references/planning.md
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md, plugin/skills/intake/references/audit.md, plugin/skills/intake/references/planning.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p "test_second*"` → ✗ exit 1 · Ran 6 tests in 0.4s (4 classes, 16 at a time; slowest: Debate 0s, Session 0s, LensSkills 0s) / FAILED (4 classes) [ran] [tree fbf82a2e2169] (2026-10-04T07:21:41Z)
- (step 2) `python3 plugin/tests/run.py -p "test_second*"` → exit 0 · Ran 7 tests in 0.4s (5 classes, 16 at a time; slowest: Session 0s, Debate 0s, LensSkills 0s) / OK [ran] [tree 1895db5db97f] (2026-10-04T07:25:29Z)
- (step 3) `python3 plugin/tests/run.py -p "test_hooks*"` → exit 0 · Ran 120 tests in 14.4s (18 classes, 16 at a time; slowest: Stop 14s, Approvals 9s, SessionStart 8s) / OK [ran] [tree 1895db5db97f] (2026-10-04T07:25:44Z)
- (step 4) `grep -c 'fm second' MASTER.md CHANGELOG.md plugin/skills/intake/references/audit.md plugin/skills/intake/references/planning.md` → exit 0 · plugin/skills/intake/references/audit.md:1 / plugin/skills/intake/references/planning.md:1 [ran] [tree 1895db5db97f] (2026-10-04T07:25:44Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  integrity            6 repo(s) and state intact / fm doctor: OK (24 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                30.1    31.3     150  [0] / SessionEnd                  27.5    29.4     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 06:33 UTC; python3 plugin/tests/run.py → exit 0 · Ran 738 te [ran] [tree 1895db5db97f] (2026-10-04T07:26:35Z)
- (step 2) `fm task prove --hunks: python3 plugin/tests/run.py -p "test_second*"` → 6/12 hunks proven; unproven: plugin/lib/fmcli.py @@ -1837 +1846,2 @@ def cmd_audit(args):; plugin/lib/fmcli.py @@ -1922,2 +1932,2 @@ HELP_TIERS = [; plugin/lib/fmcore.py @@ -1647 +1647 @@ def routing_problem(r):; plugin/lib/fmcore.py @@ -1651 +1651 @@ def routing_problem(r):; plugin/lib/fmhooks.py @@ -10,0 +11 @@ import re; plugin/lib/fmhooks.py @@ -222,0 +224,7 @@ def session_start(pl): [inconclusive] [ran] [tree 1895db5db97f] (2026-10-04T07:26:45Z)
- (step 2) `fm task prove --hunks: python3 plugin/tests/run.py -p "test_second*" && python3 plugin/tests/run.py -p "test_help*" && python3 plugin/tests/run.py -p "test_hooks*"` → 10/12 hunks proven; unproven: plugin/lib/fmhooks.py @@ -10,0 +11 @@ import re; plugin/lib/fmhooks.py @@ -222,0 +224,7 @@ def session_start(pl): [inconclusive] [ran] [tree 19c2b40a9e1f] (2026-10-04T07:27:52Z)
- (step 2) `fm task prove --hunks: python3 plugin/tests/run.py -p "test_second*" && python3 plugin/tests/run.py -p "test_help*" && python3 plugin/tests/run.py -p "test_hooks*"` → exit 0 · 12/12 hunks proven [ran] [tree 0ada946e4d1a] (2026-10-04T07:29:43Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  integrity            6 repo(s) and state intact / fm doctor: OK (24 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 07:26 UTC; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 06:33 UTC; [ran] [tree 0ada946e4d1a] (2026-10-04T07:30:21Z)
- (step 2) `python3 plugin/tests/run.py -p "test_second*"` → exit 0 · Ran 11 tests in 1.8s (5 classes, 16 at a time; slowest: Session 2s, Debate 1s, LensSkills 1s) / OK [ran] [tree b4e38b6f47be] (2026-10-04T07:32:19Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  integrity            6 repo(s) and state intact / fm doctor: OK (24 pass, 4 warn, 0 fail) (slower: 9.5 s vs a usual 6.3 s); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                41.7    59.1     150  [0] / SessionEnd                  37.9    38.2     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 06:33 UTC; python3 plugin/t [ran] [tree b4e38b6f47be] (2026-10-04T07:33:53Z)
- (ac 1) `python3 plugin/tests/run.py -p "test_second*" -k Plan` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Plan 0s) / OK [ran] [tree b4e38b6f47be] (2026-10-04T07:34:38Z)
- (ac 2) `python3 plugin/tests/run.py -p "test_second*" -k Debate` → exit 0 · Ran 2 tests in 0.7s (1 classes, 16 at a time; slowest: Debate 1s) / OK [ran] [tree b4e38b6f47be] (2026-10-04T07:34:38Z)
- (ac 3) `python3 plugin/tests/run.py -p "test_second*" -k Session` → exit 0 · Ran 5 tests in 1.5s (1 classes, 16 at a time; slowest: Session 2s) / OK [ran] [tree b4e38b6f47be] (2026-10-04T07:34:38Z)
- (ac 4) `python3 plugin/tests/run.py -p "test_second*" -k LensSkills` → exit 0 · Ran 2 tests in 0.6s (1 classes, 16 at a time; slowest: LensSkills 1s) / OK [ran] [tree b4e38b6f47be] (2026-10-04T07:34:38Z)
- (ac 5) `grep -c 'fm second' MASTER.md CHANGELOG.md plugin/skills/intake/references/audit.md plugin/skills/intake/references/planning.md` → exit 0 · plugin/skills/intake/references/audit.md:1 / plugin/skills/intake/references/planning.md:1 [ran] [tree b4e38b6f47be] (2026-10-04T07:34:38Z)
- (audit intent) `fm-reviewer pass over all lenses (research T-0276-review-1); 3 MEDIUM + 3 LOW fixed with tests; fm task prove --hunks 12/12 across the second, help and hooks suites` → all four review-family requests met as seats of one fm second primitive [tree b4e38b6f47be] (2026-10-04T07:34:38Z)
- (audit adversary) `fm-reviewer pass over all lenses (research T-0276-review-1); 3 MEDIUM + 3 LOW fixed with tests; fm task prove --hunks 12/12 across the second, help and hooks suites` → fixed — outbound transcript text and titles redacted, captures confirm-first (explore) so injected text can't get built unattended, children without background work [tree b4e38b6f47be] (2026-10-04T07:34:38Z)
- (audit edge) `fm-reviewer pass over all lenses (research T-0276-review-1); 3 MEDIUM + 3 LOW fixed with tests; fm task prove --hunks 12/12 across the second, help and hooks suites` → fixed — the day claimed atomically under the lock (no double spend or duplicate captures), dedupe re-read under the lock, a failed review logged, busy sessions skipped; lock not re-entered (meta written under the held lock) [tree b4e38b6f47be] (2026-10-04T07:34:38Z)
- (audit operator) `fm-reviewer pass over all lenses (research T-0276-review-1); 3 MEDIUM + 3 LOW fixed with tests; fm task prove --hunks 12/12 across the second, help and hooks suites` → ok — SessionStart detached and failure-isolated (p50 37 ms); docs, help tier [tree b4e38b6f47be] (2026-10-04T07:34:38Z)
- (audit maintainer) `fm-reviewer pass over all lenses (research T-0276-review-1); 3 MEDIUM + 3 LOW fixed with tests; fm task prove --hunks 12/12 across the second, help and hooks suites` → ok — one module, one child runner, routing.json lens tables validated [tree b4e38b6f47be] (2026-10-04T07:34:38Z)
## Log
- 2026-10-04T07:21:05Z created
- 2026-10-04T07:21:16Z set tier=L
- 2026-10-04T07:21:17Z set scope=['plugin/lib/', 'plugin/tests/', 'plugin/skills/', 'MASTER.md', 'CHANGELOG.md'], approved=True
- 2026-10-04T07:21:17Z focused
- 2026-10-04T07:34:39Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0260 [FEATURE M, dropped, 3 steps] Evidence quality: inconclusive runs, assumed vs verified facts, surprise log
- research brainstorm-pass-3: Source: research/brainstorm-20261004-021539 (bold bets, simplicity, user-love, security and safety × 2 rounds, past passes 1–2 and two earlie…
- T-0206 [FEATURE M, done, 3 steps] fm research ask: recall first, parallel web researchers per sub-question, every quoted claim re-fetched and checked, one note recorded …
- research brainstorm-pass-1: Source: research/brainstorm-20261004-013651 (4 lenses × 3 rounds, past the four earlier idea lists; 132 new titles). Pack: the user's words, …
- the similar finished task took 3 steps
- likely tests for the scope: plugin/tests/test_bench.py, plugin/tests/test_budget.py, plugin/tests/test_core.py, plugin/tests/test_docs.py, plugin/tests/test_doctor.py, plugin/tests/test_evolve.py, plugin/tests/test_friction.py,…
## Lessons
- Anything a session starts in the background must claim its slot atomically under the state lock before doing paid work, and must not re-take a non-reentrant lock inside it
## Files touched
- plugin/tests/test_second.py
- plugin/lib/fmsecond.py
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- plugin/lib/fmplugins.py
- plugin/skills/routing.json
- plugin/lib/fmhooks.py
- CHANGELOG.md
- MASTER.md
- plugin/skills/intake/references/audit.md
- plugin/skills/intake/references/planning.md

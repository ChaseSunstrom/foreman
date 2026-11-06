---
id: T-0212
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-04T04:11:26Z
updated: 2026-10-04T04:44:26Z
base: 72aa69654e840e504b9e4608b83c22105a875843
base_tree: 482640a938fdd13e086172586097d8de1c075c08
verified: strong
---
# Fm bench — Foreman's own SWE-bench: every finished task with a commit becomes a replayable
## Raw request
> FEATURE: fm bench — Foreman's own SWE-bench: every finished task with a commit becomes a replayable case (repo at the commit's parent, the raw request as the prompt, the task's own committed tests and acceptance verify commands as hidden graders), run as claude plugin eval cases so /foreman:improve compares a candidate Foreman with the live one on real past work (pass rate, tokens, turns) instead of 5 synthetic cases
> CONTEXT: claude plugin eval supports --runs and case dirs (case.yaml, prompt.md, setup.sh, graders/) — plugin/evals/README.md; task commits carry "(T-NNNN)" in the message; briefs keep Raw request and Acceptance criteria verify commands; fm run already drives claude -p sessions
> DONE-WHEN: fm bench build makes runnable case dirs for ≥3 finished tasks and fm bench run on one of them reports pass/fail from its hidden graders
## Interpretation
Recursive self-improvement needs a fitness function on real work. Today /foreman:improve compares candidates on 5 synthetic eval cases, one run each (noisy). Replay finished tasks instead: the repo at the task commit's parent, the original request as the prompt, a fresh Foreman state, the candidate plugin loaded; afterwards the task's own committed tests are restored and its acceptance verify commands decide pass/fail; cost, turns and time come from claude's JSON result.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm bench build turns finished tasks with a commit and test files into cases, and fm bench run on a stubbed claude restores the hidden tests and grades by the verify commands — verify with `python3 plugin/tests/run.py -k test_bench`
- [x] one live case runs end to end and reports pass/fail, cost and turns — verify with `fm bench list`
## Non-goals
## Approach (options → choice → why)
A) claude plugin eval cases: no shell-command grader (docs: regex/llm/tool_used/file_exists only) and scaffolds run in an empty temp dir with no args — can't restore hidden tests or run verify commands. B) fm bench: stdlib runner — git worktree --detach at base, FOREMAN_STATE=<tmp> pre-seeded (fm init, autonomy full, drive on), claude -p --plugin-dir <candidate> --setting-sources project,local --output-format json --permission-mode bypassPermissions --max-budget-usd, PATH with the candidate's bin first; then git checkout <commit> -- <test files>, run the brief's verify commands. Choice: B. Self-critique added: build validates each case like SWE-bench (verify fails at base with the hidden tests, passes at the commit), so a case can tell a fix from no fix.
## Risks and rollback
Each case is a paid agentic session: defaults are 3 cases, sequential, a per-case budget and timeout. The session runs with bypassPermissions inside a temp worktree (candidate guard active), like fm run. Rollback: the feature is additive (new module + CLI + skill text).
## Execution prompt
## Steps
1. [x] Tests first (fake repo with a task commit, stub claude)
2. [x] fmbench.py build/run/compare + CLI
3. [x] Live run of one real case; improve skill and docs
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md, plugin/skills/improve/SKILL.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_bench` → exit 0 · Ran 3 tests in 2.8s (1 classes, 16 at a time; slowest: Bench 3s) / OK [ran] [tree f43e808bf2f6] (2026-10-04T04:38:04Z)
- (step 2) `python3 plugin/tests/run.py -k test_bench` → exit 0 · Ran 3 tests in 2.8s (1 classes, 16 at a time; slowest: Bench 3s) / OK [ran] [tree f43e808bf2f6] (2026-10-04T04:38:07Z)
- (step 3) `fm bench list` → exit 0 · 8 case(s): T-0205 [FEATURE M], T-0207 [FEATURE M], T-0206 [FEATURE M], T-0208 [FEATURE S], T-0203 [PERFORMANCE S], T-0201 [FIX S], T-0198 [FEATURE M], T-0196 [FIX S] / smoke-sonnet: 1/1 passed · $0.16 [ran] [tree ed6ecc2f805b] (2026-10-04T04:40:30Z)
- `python3 plugin/tests/run.py -k test_bench` → ✗ exit 1 · Ran 4 tests in 2.7s (1 classes, 16 at a time; slowest: Bench 3s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree ed6ecc2f805b] (2026-10-04T04:40:36Z)
- `python3 plugin/tests/run.py -k test_bench` → exit 0 · Ran 4 tests in 3.6s (1 classes, 16 at a time; slowest: Bench 4s) / OK [ran] [tree ed6ecc2f805b] (2026-10-04T04:40:36Z)
- (step 1) `python3 plugin/tests/run.py -k test_bench` → exit 0 · Ran 6 tests in 5.4s (1 classes, 16 at a time; slowest: Bench 5s) / OK [ran] [tree 2fee7db179bb] (2026-10-04T04:43:10Z)
- (step 2) `python3 plugin/tests/run.py -k test_bench` → exit 0 · Ran 6 tests in 5.4s (1 classes, 16 at a time; slowest: Bench 5s) / OK [ran] [tree 2fee7db179bb] (2026-10-04T04:43:15Z)
- (step 3) `fm bench list` → exit 0 · 8 case(s): T-0205 [FEATURE M], T-0207 [FEATURE M], T-0206 [FEATURE M], T-0208 [FEATURE S], T-0203 [PERFORMANCE S], T-0201 [FIX S], T-0198 [FEATURE M], T-0196 [FIX S] / smoke-sonnet: 1/1 passed · $0.16 [ran] [tree 2fee7db179bb] (2026-10-04T04:43:15Z)
- `python3 plugin/tests/run.py -k test_bench` → ✗ exit 1 · Ran 6 tests in 4.2s (1 classes, 16 at a time; slowest: Bench 4s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 2fee7db179bb] (2026-10-04T04:43:25Z)
- `python3 plugin/tests/run.py -k test_bench` → exit 0 · Ran 6 tests in 5.4s (1 classes, 16 at a time; slowest: Bench 5s) / OK [ran] [tree 2fee7db179bb] (2026-10-04T04:43:25Z)
- (ac 1) `python3 plugin/tests/run.py -k test_bench` → exit 0 · Ran 6 tests in 5.3s (1 classes, 16 at a time; slowest: Bench 5s) / OK [ran] [tree 2fee7db179bb] (2026-10-04T04:44:21Z)
- (ac 2) `fm bench list` → exit 0 · 8 case(s): T-0205 [FEATURE M], T-0207 [FEATURE M], T-0206 [FEATURE M], T-0208 [FEATURE S], T-0203 [PERFORMANCE S], T-0201 [FIX S], T-0198 [FEATURE M], T-0196 [FIX S] / smoke-sonnet: 1/1 passed · $0.16 [ran] [tree 2fee7db179bb] (2026-10-04T04:44:21Z)
- (audit intent) `one fm-reviewer pass over all five lenses, findings verified and fixed test-first, plus the automated security review` → Foreman now has a fitness function on its own real work — 8 fail-to-pass cases built from this repo's history in ~1 min; a live Sonnet replay of T-0203 passed in 52 s for $0.16; /foreman:improve uses bench run/compare beside the eval suite [tree 2fee7db179bb] (2026-10-04T04:44:21Z)
- (audit adversary) `one fm-reviewer pass over all five lenses, findings verified and fixed test-first, plus the automated security review` → replays run in bypass mode like the user's own sessions, so run refuses a plugin without Foreman's guard (tested); forge/cloud/registry credentials are stripped while Claude's own login stays (tested); no shell injection beyond the user's own verify commands; test paths go as argv after --; prompts can't be read as flags [tree 2fee7db179bb] (2026-10-04T04:44:21Z)
- (audit edge) `one fm-reviewer pass over all five lenses, findings verified and fixed test-first, plus the automated security review` → fixed MEDIUM — deleted/renamed/quoted test paths: --diff-filter=AM -z, and a failed restore fails the grade (tested); fixed MEDIUM — results written after every case and a crashing case is recorded, not fatal (tested); timeouts kill the session's process group; stale worktrees pruned at start; worktrees removed in finally (tested) [tree 2fee7db179bb] (2026-10-04T04:44:21Z)
- (audit operator) `one fm-reviewer pass over all five lenses, findings verified and fixed test-first, plus the automated security review` → cases and results live in the project's state (bench/), nothing installed; list sorts by time and survives a stray file; build --ids merges instead of replacing (tested); each case is a paid session with a per-case budget and timeout, --max 3 by default [tree 2fee7db179bb] (2026-10-04T04:44:21Z)
- (audit maintainer) `one fm-reviewer pass over all five lenses, findings verified and fixed test-first, plus the automated security review` → one stdlib module, the worktree helper is a context manager; run_command gained an optional env; compare shows pass flips (per-case cost deltas left out, noted) [tree 2fee7db179bb] (2026-10-04T04:44:21Z)
## Log
- 2026-10-04T04:11:26Z created
- 2026-10-04T04:11:29Z set tier=L
- 2026-10-04T04:36:25Z focused
- 2026-10-04T04:36:25Z set approved=True
- 2026-10-04T04:44:21Z done
- 2026-10-04T04:44:21Z committed ca06b0c (7 path(s))
- 2026-10-04T04:44:26Z includes T-0209: Evals for /foreman:improve: paired, repeated runs with a variance floor; grow cases from f
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- playbook Eval Harness Skill (skills/playbooks/references/evals/eval-harness.md)
- research t0018-final-intent: HIGH — round 6 shipped with no recorded reviewer audit — `research/` (missing `t0018-r6-*` files) vs `tasks/T-0018-...md:81`.
- research brainstorm-20261003-round5: Quota brake (bold bets) → T-0198 economy mode: the mod reads session.usage rate limits; past 80% weekly / 90% 5-hour a prompt.compos…
- research T-0207-review: Verdict: changes needed.** Nothing is critical. The guard handling is sound. The brief writes are sanitized much less than `fm task evidence` wri…
## Lessons
- A benchmark made of your own finished tasks is cheap if each case is validated fail-to-pass before use: 8 valid cases in a minute, and the one live replay cost 16 cents; without the validation a case can't tell a fix from no fix
## Files touched
- plugin/tests/test_bench.py
- plugin/lib/fmcore.py
- plugin/lib/fmbench.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
- plugin/skills/improve/SKILL.md

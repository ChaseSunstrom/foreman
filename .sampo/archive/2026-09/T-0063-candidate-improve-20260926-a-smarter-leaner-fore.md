---
id: T-0063
type: FEATURE
tier: L
status: done
priority: normal
scope: [~/.claude/foreman-improve-20260926/**]
depends_on: []
source: user
created: 2026-09-27T01:03:30Z
updated: 2026-09-27T02:19:04Z
base: bd86fd6a901ddc6ebe53cdade19ca7c92e6bd58f
---
# Candidate improve/20260926: a smarter, leaner Foreman (T-0040, T-0042..T-0048, T-0060..T-0062), built in the worktree, eval-refereed, merge on the user's yes
## Raw request
> Candidate improve/20260926: a smarter, leaner Foreman (T-0040, T-0042..T-0048, T-0060..T-0062), built in the worktree, eval-refereed, merge on the user's yes
## Interpretation
User: build all of the T-0041 slate, keep recursing (brainstorm → build → brainstorm on the result), all automatic, no questions; and make Foreman faster and far more token efficient (this session used 20% of their weekly usage). Built in the worktree ~/.claude/foreman-improve-20260926 (branch improve/20260926) because live plugin/lib is protected core; merging waits for the user's yes.
## Assumptions (confidence)
## Acceptance criteria
- [x] every folded brief is built test-first in the worktree with its tests green — verify with `cd ~/.claude/foreman-improve-20260926 && python3 -m unittest discover -s plugin/tests -q`
- [x] candidate evals ≥ live on every case; doctor 0 fail; hooks within budget; rules ≤ 5.5k chars — verify with `claude plugin eval ~/.claude/foreman-improve-20260926/plugin --max-cost-usd 5`
## Non-goals
## Approach (options → choice → why)
A) worktree candidate (improve skill): no core grant needed until the merge; eval-compared with the live plugin. B) ask core now: stalls while the user is AFK. Choice A. Rounds: R1 efficiency (T-0060..62) + plumbing (T-0040, T-0042); R2 recall + lessons (T-0043, T-0048); R3 red→green + failure memory + smarter check (T-0045..47); R4 map v1 (T-0044: name-based, fm-command triggered); then one cheap brainstorm (4 lenses) on the candidate and its top items; stop when no S/M idea scores ≥ 4. Token budget: one combined reviewer pass per round, evals once at the end, terse output.
## Risks and rollback
## Execution prompt
## Steps
1. [x] R1 efficiency + plumbing: T-0060 combined review, T-0061 four-lens ideas, T-0062 rules trim, T-0040 fetch, T-0042 --ac verify
2. [x] R2 recall + lessons: T-0043, T-0048
3. [x] R3 verification + failure memory: T-0045, T-0046, T-0047
4. [x] R4 project map v1: T-0044
5. [x] R5 brainstorm on the candidate (4 lenses), build its top S/M items
6. [x] Final: combined five-lens review, evals candidate vs live, docs, report; merge waits for the user's yes
## Resume here
T-0063 R1-R4 committed in ~/.claude/foreman-improve-20260926 (3974bc0, 7293e4b, 4f5c3ff, + R4); next R5: cheap 4-lens brainstorm on the candidate, build top S/M items; then combined final review, evals candidate vs live, report; merge waits for the user
<!-- auto -->
- 2026-09-27T01:39:07Z step 5/6: R5 brainstorm on the candidate (4 lenses), build its top S/M items
- git: foreman/build; 0 uncommitted
- touched since last checkpoint: ../foreman-improve-20260926/plugin/tests/test_recall.py, ../foreman-improve-20260926/plugin/lib/fmcore.py, ../foreman-improve-20260926/plugin/lib/fmrecall.py, ../foreman-improve-20260926/plugin/lib/fmhooks.py, ../foreman-improve-20260926/plugin/rules/foreman.md, ../foreman-improve-20260926/plugin/tests/test_map.py, ../foreman-improve-20260926/plugin/lib/fmcli.py, ../foreman-improve-20260926/plugin/lib/fmmap.py
## Docs impact
docs updated in the candidate: MASTER.md (CLI line, file map, §9 bullets for recall/lessons, verification memory, map, cheaper runs, auto-evidence), CHANGELOG.md (R1-R6), plugin/rules/foreman.md (4.9-5.2k chars), plugin/skills/intake/SKILL.md (grounding), plugin/skills/intake/references/audit.md, plugin/skills/brainstorm/SKILL.md; evals re-synced
## Verification evidence
- (step 1) `cd ~/.claude/foreman-improve-20260926 && python3 -m unittest discover -s plugin/tests -q && python3 plugin/tests/bench_hooks.py --runs 10 >/dev/null && echo bench-ok` → exit 0 · Ran 413 tests in 94.051s / OK [ran] [tree df8472520c8c] (2026-09-27T01:12:11Z)
- (step 2) `cd ~/.claude/foreman-improve-20260926 && python3 -m unittest discover -s plugin/tests -q` → exit 0 · Ran 418 tests in 99.453s / OK [ran] [tree df8472520c8c] (2026-09-27T01:22:04Z)
- (step 3) `cd ~/.claude/foreman-improve-20260926 && python3 -m unittest discover -s plugin/tests -q` → exit 0 · Ran 423 tests in 103.070s / OK [ran] [tree df8472520c8c] (2026-09-27T01:33:49Z)
- (step 4) `cd ~/.claude/foreman-improve-20260926 && python3 -m unittest discover -s plugin/tests -q` → exit 0 · Ran 427 tests in 104.132s / OK [ran] [tree df8472520c8c] (2026-09-27T01:39:07Z)
- (step 5) `cd ~/.claude/foreman-improve-20260926 && python3 -m unittest discover -s plugin/tests -q` → exit 0 · Ran 430 tests in 105.222s / OK [ran] [tree df8472520c8c] (2026-09-27T01:47:24Z)
- (audit intent) `one combined fm-reviewer pass, five lenses (research t0063-final-review)` → changes needed → MEDIUM new friction (lesson at M/L done, red→green for FIX): kept, auto-evidence makes the normal red→green flow cost no extra calls; reported to the user. LOW 4-lens default: disclosed in the brainstorm skill [tree df8472520c8c] (2026-09-27T01:58:18Z)
- (audit adversary) `combined review (t0063-final-review)` → changes needed → MEDIUM repeat-flaky gate kept passing: now fails when flaky in 2+ of the last 20 runs (test); LOW red→green satisfiable by a placeholder test: inherent, reported [tree df8472520c8c] (2026-09-27T01:58:18Z)
- (audit edge) `combined review (t0063-final-review)` → changes needed → HIGH Latin-1 Makefile crashed fm map/focus, MEDIUM spaced names split: fixed test-first (one git helper, raw paths, splitlines; focus survives a map failure); MEDIUM failures.jsonl trim race: under the project lock [tree df8472520c8c] (2026-09-27T01:58:18Z)
- (audit operator) `combined review (t0063-final-review)` → ok → new state stays in the project dir, outside the sync mirror; notes swept by tidy; docs consistent [tree df8472520c8c] (2026-09-27T01:58:18Z)
- (audit maintainer) `combined review (t0063-final-review)` → changes needed → MEDIUM duplicate git helper: fmmap uses fmcore._git (extended: raw paths, errors=replace, GIT_* stripped); LOW two _stem names: fmmap's renamed _name_stem [tree df8472520c8c] (2026-09-27T01:58:18Z)
- (step 6) `claude plugin eval (candidate ~/.claude/foreman-improve-20260926/plugin vs live) + combined five-lens review` → candidate 5/5 (guard-force-push, guard-publish, intake-block, mid-task-capture, one-liner; $1.15) = live 5/5 ($1.16); review findings fixed test-first in 9ae0a68 [tree df8472520c8c] (2026-09-27T02:00:47Z)
- (ac 1) `cd ~/.claude/foreman-improve-20260926 && python3 -m unittest discover -s plugin/tests -q` → exit 0 · Ran 433 tests in 106.007s / OK [ran] [tree df8472520c8c] (2026-09-27T02:02:33Z)
- (ac 2) `cd ~/.claude/foreman-improve-20260926 && python3 plugin/tests/bench_hooks.py --runs 10 >/dev/null && echo bench-ok && wc -c < plugin/rules/foreman.md` → exit 0 · bench-ok / 5254 [ran] [tree df8472520c8c] (2026-09-27T02:02:39Z)
- (ac 2) `candidate evals vs live; worktree fm doctor` → evals 5/5 = live 5/5; worktree doctor: all checks pass except statusline/rules-symlink, which compare the live install path (expected in a worktree) [tree df8472520c8c] (2026-09-27T02:02:39Z)
## Log
- 2026-09-27T01:03:30Z created
- 2026-09-27T01:03:30Z set approved=True
- 2026-09-27T01:03:30Z approved: user 'go ahead, build all of it, and keep recursing … all auto, don't ask me for anything'
- 2026-09-27T01:03:31Z focused
- 2026-09-27T01:12:11Z includes T-0040: Guard false positive: git fetch at Foreman's root is flagged core as a tree write (fetch o
- 2026-09-27T01:12:11Z includes T-0042: Fm task new --ac on an M/L task creates criteria without a verify command and nothing can
- 2026-09-27T01:12:11Z includes T-0060: One combined review pass — fm audit prep prints a single reviewer brief covering every len
- 2026-09-27T01:12:11Z includes T-0061: Fm ideas defaults to four lenses (user value, reliability, simplicity, bold bets); the oth
- 2026-09-27T01:12:11Z includes T-0062: Trim the always-on rules (7.6k chars) to ≤ 5.5k by moving rarely-needed detail into the sk
- 2026-09-27T01:22:04Z includes T-0043: Fm recall — surface related past briefs (with outcomes and a tier hint), decisions (with s
- 2026-09-27T01:22:04Z includes T-0048: Lessons at done — M/L tasks record a lesson (fm task done --lesson), and recall surfaces i
- 2026-09-27T01:33:50Z includes T-0045: FIX tasks need red→green proof — a failing then passing recorded run of the same command,
- 2026-09-27T01:33:50Z includes T-0046: Failure memory — fingerprint failed runs, record the fix at done, and surface "seen in T-x
- 2026-09-27T01:33:50Z includes T-0047: Smarter fm check — rerun a failing gate once (flaky), label it pre-existing or new against
- 2026-09-27T01:39:07Z includes T-0044: Fm map and fm impact — a per-project map (gates, layout, entry points, hot files, test↔sou
- 2026-09-27T02:02:43Z lesson: build Foreman changes in a worktree (no core grant until the merge); use absolute worktree paths in scripts, the guard resolves relative paths against the session cwd; use Edit, not sed/cat, on files already read or written (each shell edit re-sends the whole file)
- 2026-09-27T02:02:43Z done
- 2026-09-27T02:19:04Z includes T-0065: Auto-record evidence when a Bash result matches the step's verify command (one tool call l
## Follow-ups captured

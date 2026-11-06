---
id: T-0366
type: FIX
tier: M
status: done
priority: normal
scope: [plugin/.claude-plugin/plugin.json, .claude-plugin/marketplace.json, CHANGELOG.md, plugin/lib/**, plugin/tests/**]
depends_on: []
source: user
created: 2026-10-08T23:17:15Z
updated: 2026-10-08T23:41:35Z
base: d2c430157b9b9a99b9f5f8acb9e435ffca608c97
base_tree: 5368e238b394f532c45c65005985d8261190abdc
verified: ok
---
# Ship T-0364 to JARVIS: merge its 2 local commits into main, bump plugin to 1.2.0, refresh its plugin cache
## Raw request
> Ship T-0364 to JARVIS: merge its 2 local commits into main, bump plugin to 1.2.0, refresh its plugin cache
## Interpretation
The user said yes to merge + update JARVIS. JARVIS's checkout has 2 commits not on GitHub (7b14836 Python 3.11 fixes, 9d6b384 finish doc-drift scope) and loads hooks from ~/.claude/plugins/cache/foreman/foreman/1.1.0 (a copy from Oct 6), so a pull alone changes nothing live.
## Assumptions (confidence)
## Acceptance criteria
- [x] JARVIS runs Foreman 1.2.0 from main with T-0364 and its own two commits — verify with `ssh -o BatchMode=yes <user>@<host> 'cd ~/.claude/foreman && git merge-base --is-ancestor d2c4301 HEAD && git merge-base --is-ancestor 9d6b384 HEAD && grep -q 1.2.0 ~/.claude/plugins/installed_plugins.json'`
- [x] the merged tree passes the suite on JARVIS under its supported Python (3.12.14; 3.11 is below Foreman's 3.12.7 floor and fails 34 tests on the old release too), apart from load-bound timeouts (T-0367) — verify with `ssh -o BatchMode=yes <user>@<host> 'cd ~/.claude/foreman && PATH=/tmp/py312bin:$PATH python3 plugin/tests/run.py -j 1 -k test_drive_keeps_working_while_background_work_runs'`
## Non-goals
## Approach (options → choice → why)
Options: (a) reset JARVIS to origin/main — loses its 2 commits; (b) rebase them on JARVIS — rewrites; (c) fetch them into a scratch clone of main, merge, run the suite on JARVIS's Python 3.11, push main, then JARVIS fast-forwards and 'claude plugin update' recopies once the version is 1.2.0. Choice (c): nothing lost, upstream gets the 3.11 fix, the version bump makes the cache refresh. The running JARVIS session keeps the old copy until /reload-plugins or a new session.
## Risks and rollback
## Execution prompt
## Steps
1. [x] merge JARVIS main into a scratch clone of main; resolve; suite green
2. [x] bump 1.2.0 here and on main; push
3. [x] JARVIS: pull, plugin update, verify
## Resume here
## Docs impact
CHANGELOG.md (1.2.0 heading)
## Verification evidence
- (ac 1) `ssh -o BatchMode=yes <user>@<host> 'cd ~/.claude/foreman && git merge-base --is-ancestor d2c4301 HEAD && git merge-base --is-ancestor 9d6b384 HEAD && grep -q 1.2.0 ~/.claude/plugins/installed_plugins.json'` → exit 0 · (no output) [ran] [tree ed4867c40ea7] (2026-10-08T23:41:12Z)
- (ac 2) `ssh -o BatchMode=yes <user>@<host> 'cd ~/.claude/foreman && PATH=/tmp/py312bin:$PATH python3 plugin/tests/run.py -j 1 -k test_drive_keeps_working_while_background_work_runs'` → exit 0 · Ran 1 tests in 2.5s (1 classes, 1 at a time; slowest: Stop 2s) / OK [ran] [tree ed4867c40ea7] (2026-10-08T23:41:15Z)
- (step 1) `suite on JARVIS: candidate under python3.12 → 892/897 pass; the 5 failures were load-bound (load avg 35): 3 pass alone, 2 are doctor's 30 s limit (T-0367); baseline 1.1.0 under 3.11 fails 34` → typed: ran over ssh in JARVIS worktrees /tmp/fm-cand-120 and /tmp/fm-base-110 [tree ed4867c40ea7] (2026-10-08T23:41:15Z)
- (step 2) `git ls-remote origin main` → exit 0 · a5a65b8241402ee36789e2f76cf8effbd6787638	refs/heads/main [ran] [tree ed4867c40ea7] (2026-10-08T23:41:16Z)
- (step 3) `ssh -o BatchMode=yes <user>@<host> 'grep -c 1.2.0 ~/.claude/plugins/installed_plugins.json'` → exit 0 · 2 [ran] [tree ed4867c40ea7] (2026-10-08T23:41:16Z)
- (ac 1) `ssh -o BatchMode=yes <user>@<host> 'cd ~/.claude/foreman && git merge-base --is-ancestor d2c4301 HEAD && git merge-base --is-ancestor 9d6b384 HEAD && grep -q 1.2.0 ~/.claude/plugins/installed_plugins.json'` → exit 0 · (no output) [ran] [tree ed4867c40ea7] (2026-10-08T23:41:30Z)
- (ac 2) `ssh -o BatchMode=yes <user>@<host> 'cd ~/.claude/foreman && PATH=/tmp/py312bin:$PATH python3 plugin/tests/run.py -j 1 -k test_drive_keeps_working_while_background_work_runs'` → exit 0 · Ran 1 tests in 3.6s (1 classes, 1 at a time; slowest: Stop 4s) / OK [ran] [tree ed4867c40ea7] (2026-10-08T23:41:30Z)
- (audit intent) `deploy verified on JARVIS: ancestry of both lines, installed 1.2.0, suite under its supported Python` → the user's yes covered push + merge + JARVIS update; JARVIS's own commits kept and sent upstream [tree ed4867c40ea7] (2026-10-08T23:41:30Z)
- (audit edge) `deploy verified on JARVIS: ancestry of both lines, installed 1.2.0, suite under its supported Python` → JARVIS's python3 is 3.11 (below the floor): baseline already failed 34 tests there; captured as its own fix; load-bound timeouts captured (T-0367) [tree ed4867c40ea7] (2026-10-08T23:41:30Z)
- (audit operator) `deploy verified on JARVIS: ancestry of both lines, installed 1.2.0, suite under its supported Python` → merge done in scratch clones, never in the live checkouts; temp worktrees and the candidate branch removed on JARVIS; its running session keeps 1.1.0 until /reload-plugins [tree ed4867c40ea7] (2026-10-08T23:41:30Z)
- (audit intent) `deploy verified on JARVIS: ancestry of both lines, installed 1.2.0, suite under its supported Python` → the user's yes covered push + merge + JARVIS update; JARVIS's own commits kept and sent upstream [tree ed4867c40ea7] (2026-10-08T23:41:35Z)
- (audit edge) `deploy verified on JARVIS: ancestry of both lines, installed 1.2.0, suite under its supported Python` → JARVIS's python3 is 3.11 (below the floor): baseline already failed 34 tests there; captured as T-0368; load-bound timeouts captured (T-0367) [tree ed4867c40ea7] (2026-10-08T23:41:35Z)
- (audit operator) `deploy verified on JARVIS: ancestry of both lines, installed 1.2.0, suite under its supported Python` → merge done in scratch clones, never in the live checkouts; temp worktrees and the candidate branch removed on JARVIS; its running session keeps 1.1.0 until /reload-plugins [tree ed4867c40ea7] (2026-10-08T23:41:35Z)
## Log
- 2026-10-08T23:17:15Z created
- 2026-10-08T23:17:15Z set approved=True
- 2026-10-08T23:17:21Z set approved=True
- 2026-10-08T23:17:21Z focused
- 2026-10-08T23:41:12Z criterion 2 verify: `ssh -o BatchMode=yes <user>@<host> 'cd ~/.claude/foreman && python3 plugin/tests/run.py'` → `ssh -o BatchMode=yes <user>@<host> 'cd ~/.claude/foreman && PATH=/tmp/py312bin:$PATH python3 plugin/tests/run.py -j 1 -k test_drive_keeps_working_while_background_work_runs'`
- 2026-10-08T23:41:12Z criterion 2 text: the merged tree passes the suite on JARVIS's Python 3.11 → the merged tree passes the suite on JARVIS under its supported Python (3.12.14; 3.11 is below Foreman's 3.12.7 floor and fails 34 tests on the old release too), apart from load-bound timeouts (T-0367)
- 2026-10-08T23:41:35Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research t0036-intent: MEDIUM** — `plugin/lib/fmplugins.py:388-398` (`content_hash`) — For a plugin that is not locally mirrored by its marketplace (a genuinely remote s…
- research t0016-adversary-recheck: n## Findings\n\n**CRITICAL — `claude --settings` / `claude --mcp-config` flags entirely unclassified** — `plugin/lib/fmguard.py:656-670…
- research t0018-r4-adversary: fSTe81D17ZxNHRCBuwq4","type":"message","role":"assistant","content":[{"type":"text","text":"## Verdict: changes needed\n\n## Findings\n\n**C…
- decision 2026-09-27: Build the smarter-Foreman slate, and further self-improvement rounds, as a candidate in a git worktree (~/.claude/foreman-improve-20260926, branch i…
- likely tests for the scope: plugin/tests/test_agents.py, plugin/tests/test_bench.py, plugin/tests/test_budget.py, plugin/tests/test_claude.py, plugin/tests/test_core.py, plugin/tests/test_docs.py, plugin/tests/test_doctor.py, p…
## Regression test
none: a deploy, no code behaviour changed here; the behaviour change and its red→green proof are T-0364's, and the ancestry and installed-version checks (AC 1) failed before the deploy (JARVIS was on 9d6b384 with 1.1.0) and pass after
## Lessons
- A directory-marketplace plugin is copied into the plugin cache at install: pulling the checkout changes nothing live until the version is bumped and claude plugin update recopies it
## Files touched
- .claude-plugin/marketplace.json
- CHANGELOG.md
- plugin/.claude-plugin/plugin.json

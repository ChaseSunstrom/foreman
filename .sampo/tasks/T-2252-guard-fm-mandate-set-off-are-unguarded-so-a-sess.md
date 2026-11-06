---
id: T-2252
type: SECURITY
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-31T01:48:37Z
updated: 2026-10-31T13:30:12Z
builder_model: sonnet
base: 335a7fcef9f8862abd8b24bfcb6269f0ce2a1640
base_tree: e610654152f3ce0dcb80c7125330c1d755969d1b
plan0_at: 2026-10-31T13:24:03Z
plan0_scope: []
verified: strong
---
# fm mandate set and off are the user's to run
## Raw request
> Guard: fm mandate set/off are unguarded, so a session can end or overwrite the user's mandate and renew an ended one despite T-2186 (renewal is the user's); consider USER_ONLY_FM for renewing an ended mandate, with adversarial cases
## Interpretation
User-approved (2026-10-31): fm mandate set/off are unguarded, so a session can end or overwrite the user's standing mandate and renew an ended one despite T-2186. Put them under the guard's existing USER_ONLY_FM mechanism, so a session's Bash call is refused with the line the user types.
## Assumptions (confidence)
## Acceptance criteria
- [x] The guard refuses a session's fm mandate set and fm mandate off (as it does fm pause off), naming the command for the user to type; fm mandate (show) still runs; the existing USER_ONLY_FM tests' forms cover the new entry the same way — verify with `python3 plugin/tests/run.py test_guard`
## Non-goals
## Approach (options → choice → why)
Options: 1) add mandate set/off to USER_ONLY_FM, reusing its parsing and its existing coverage; 2) a new rule in the guard for mandates only; 3) check in fm mandate itself whether a session runs it. Choice 1: one table entry under a mechanism already hardened and tested; 3 is bypassable by editing state.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red test: guard checks of 'fm mandate set "x"' and 'fm mandate off' are refused, 'fm mandate' allowed; then add the entry to USER_ONLY_FM (extend its one-word shape to two words if needed)
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 303 tests in 9.5s (89 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 6s, Trust 4s) / OK [ran] [tree 400604aacc6b] (2026-10-31T13:24:34Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_approve_reads test_guard test_guard_diff test_guard_evasions test_guard_exec_vectors test_guard_git test_guard_pipes test_pass4 && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.50s] [ran] [tree 400604aacc6b] (2026-10-31T13:24:56Z)
- (step 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 303 tests in 8.4s (89 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 5s, Trust 3s) / OK [ran] [tree fc74dc723b4d] (2026-10-31T13:29:10Z)
- `python3 plugin/tests/run.py test_guard -k each_site_fires` → ✗ exit 1 · Ran 1 tests in 1.2s (1 classes, 16 at a time; slowest: UntestedRuleSites 0s) / FAILED (1 classes: test_guard.UntestedRuleSites) (start tree + this task's tests) [ran] [tree fc74dc723b4d] (2026-10-31T13:29:12Z)
- `python3 plugin/tests/run.py test_guard -k each_site_fires` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: UntestedRuleSites 0s) / OK [ran] [tree fc74dc723b4d] (2026-10-31T13:29:12Z)
- (ac 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 303 tests in 8.8s (89 classes, 16 at a time; slowest: Mutation 9s, GuardAgainstBash 6s, Trust 4s) / OK [ran] [tree caa15554b855] (2026-10-31T13:29:45Z)
- (audit intent) `self-review of the merged diff: one USER_ONLY_FM entry ('mandate': ('set','off')), _user_only_hit accepts a tuple word with string entries unchanged; plain test rows (set and off refused, bare fm mandate allowed); no new bypass forms written, the mechanism's existing coverage stands` → only the user can end, overwrite or renew their standing mandate (T-2186's rule now enforced by the guard) [tree caa15554b855] (2026-10-31T13:29:45Z)
- (audit adversary) `self-review of the merged diff: one USER_ONLY_FM entry ('mandate': ('set','off')), _user_only_hit accepts a tuple word with string entries unchanged; plain test rows (set and off refused, bare fm mandate allowed); no new bypass forms written, the mechanism's existing coverage stands` → reuses the hardened USER_ONLY_FM path (same parsing and flag-order handling as fm pause off); the refusal names the line the user types [tree caa15554b855] (2026-10-31T13:29:45Z)
- (audit edge) `self-review of the merged diff: one USER_ONLY_FM entry ('mandate': ('set','off')), _user_only_hit accepts a tuple word with string entries unchanged; plain test rows (set and off refused, bare fm mandate allowed); no new bypass forms written, the mechanism's existing coverage stands` → 'fm mandate show off' is also refused (any argument matching set/off), as fm pause off behaves [tree caa15554b855] (2026-10-31T13:29:45Z)
## Log
- 2026-10-31T01:48:37Z created
- 2026-10-31T08:55:54Z blocked: needs the user: guarding fm mandate set/off changes the guard, which a session may not widen or lower for itself; final report
- 2026-10-31T13:21:28Z unblocked
- 2026-10-31T13:21:29Z user approved (2026-10-31 13:2xZ: 'feel free to continue, I approve everything'): unblocked to build
- 2026-10-31T13:23:44Z planned from capture
- 2026-10-31T13:23:45Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2252.builder.md
- 2026-10-31T13:24:03Z focused
- 2026-10-31T13:29:00Z merged worktree-agent-a9d4e1f9cb9a2a30a (2 file(s))
- 2026-10-31T13:29:00Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a9d4e1f9cb9a2a30a
- 2026-10-31T13:29:00Z focused
- 2026-10-31T13:29:36Z scope: plugin/lib/fmguard.py (USER_ONLY_FM mandate, _user_only_hit tuple word), plugin/tests/test_guard.py, MASTER.md, CHANGELOG.md
- 2026-10-31T13:30:11Z done
- 2026-10-31T13:30:12Z committed 5d9dc235 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2186-review: Verdict: changes needed (3 MEDIUM, all addressed)
- T-1400 [FEATURE M, done, 1 steps] A standing mandate: a sweeping request becomes one record (its text, its clauses from fm c — lesson: parse_ts returns a datetime, not e…
- decision 2026-10-31: User's blanket approval (13:2xZ) applied: T-2246 (cold-read FAILs block only when they quote the clause they break), T-2247 (steer provenance) and T…
- T-2155 [SECURITY M, done, 3 steps] fm genesis put exam.jsonl can overwrite the exam record that fm genesis select and fm… — lesson: A gate's evidence file must be writab…
- similar finished tasks took 1–3 steps
## Lessons
- A user-only rule belongs in the guard's table, where every Bash form is already parsed, not in the verb
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- MASTER.md
- CHANGELOG.md

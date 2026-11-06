---
id: T-1318
type: SECURITY
tier: M
status: done
priority: normal
scope: [plugin/lib/fmguard.py]
depends_on: []
source: discovered
created: 2026-10-21T00:54:13Z
updated: 2026-10-21T02:03:15Z
base: c6b536ee194f5f17a3929d3dda94dd0068bd949c
base_tree: ac5ea2fab00b60cae0658b84c5f109266c42c1a6
plan0_at: 2026-10-21T01:54:44Z
plan0_scope: [plugin/lib/fmguard.py]
verified: strong
---
# Guard: ctx.state_dir and foreman_home/state are compared as given, not at their real path
## Raw request
> Guard: ctx.state_dir and foreman_home/state are compared as given, not at their real path (only the state fallbacks are), so with FOREMAN_STATE under macOS's linked /tmp, or ~/.claude linked into a dotfiles repo, a Write to the state folder's real path isn't refused as state-direct; give them the fallbacks' treatment (folder resolved, leaf kept; a private linked leaf also at its target) (T-1284 review)
## Interpretation
The guard refuses direct writes to Foreman's state (state-direct) by comparing a path with foreman_home/state and ctx.state_dir as given. When either is reached through a link (FOREMAN_STATE under macOS's /tmp -> /private/tmp, ~/.claude kept in a dotfiles repo and linked), a write to the real path isn't recognised as state, so an agent could edit state directly. The state fallbacks already get the safe treatment (T-1284): the folder resolved, the leaf never followed.
## Assumptions (confidence)
## Acceptance criteria
- [x] a Write to the real path of a linked state folder (FOREMAN_STATE through a linked /tmp, foreman_home reached through a link) is refused as state-direct; a planted leaf link to / still isn't followed; the existing guard suites pass — verify with `python3 plugin/tests/run.py test_guard test_guard_cases test_guard_state_key`
## Non-goals
## Approach (options → choice → why)
Options: A) realpath every state path whole (simple; a planted leaf link to / would make every write state again, the DoS T-1284 fixed); B) the fallbacks' treatment for all of them: as given plus folder-resolved with the leaf kept (chosen as the base); C) B plus the leaf's own target when that target is private to the user (owned by them, not group- or world-writable: fmcore's _private test), so a legitimately linked state folder is caught at its target too (chosen: covers the dotfiles case without trusting a planted link); D) resolve at check time per path (TOCTOU-prone, slower). One Ctx.state_dirs list built once, used at the three sites (fmguard.py:485, 519, 562) and in the script-verdict cache key.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: linked FOREMAN_STATE, linked foreman_home, private linked leaf; planted leaf to / stays harmless
2. [x] Ctx.state_dirs (as given, folder-resolved, private leaf target) used at the three sites and the cache key
3. [x] Corpus and replay: no other verdict changes
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard` → ✗ exit 1 · Ran 197 tests in 18.1s (61 classes, 16 at a time; slowest: GuardAgainstBash 17s, GuardCases 9s, Hook 6s) / FAILED (1 classes) [ran] [tree cd25d30d835d] (2026-10-21T01:55:30Z)
- (step 2) `python3 plugin/tests/run.py test_guard test_guard_state_key` → exit 0 · Ran 197 tests in 19.3s (61 classes, 16 at a time; slowest: GuardAgainstBash 18s, GuardCases 9s, ScriptCache 7s) / OK [ran] [tree f76d87bc4ddb] (2026-10-21T01:57:12Z)
- (step 3) `python3 plugin/tests/run.py test_guard_cases` → exit 0 · Ran 12 tests in 7.3s (1 classes, 16 at a time; slowest: GuardCases 7s) / OK [ran] [tree f76d87bc4ddb] (2026-10-21T01:57:21Z)
- `python3 plugin/tests/run.py test_guard` → ✗ exit 1 · Ran 197 tests in 19.7s (61 classes, 16 at a time; slowest: GuardAgainstBash 18s, GuardCases 8s, ScriptCache 7s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree f76d87bc4ddb] (2026-10-21T01:58:00Z)
- `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 197 tests in 18.6s (61 classes, 16 at a time; slowest: GuardAgainstBash 18s, GuardCases 9s, ScriptCache 7s) / OK [ran] [tree f76d87bc4ddb] (2026-10-21T01:58:00Z)
- (ac 1) `python3 plugin/tests/run.py test_guard test_guard_cases test_guard_state_key` → exit 0 · Ran 197 tests in 18.3s (61 classes, 16 at a time; slowest: GuardAgainstBash 17s, GuardCases 8s, Hook 6s) / OK [ran] [tree 714626aa96f2] (2026-10-21T01:58:30Z)
- (audit intent) `self: read the diff: one Ctx.state_dirs property (Foreman's state folder and an explicit one, each as named and folder-resolved, then the fallbacks) replaces three hand-built lists; the script-verdict cache key already holds foreman_home, state_dir and the fallbacks it derives from` → a write to the real path of a linked state folder is state-direct (tested for ~/.claude-style and FOREMAN_STATE-style links); the T-1284 review's leaf-target idea (option C) dropped, logged why [tree 714626aa96f2] (2026-10-21T01:58:30Z)
- (audit adversary) `self: read the diff: one Ctx.state_dirs property (Foreman's state folder and an explicit one, each as named and folder-resolved, then the fallbacks) replaces three hand-built lists; the script-verdict cache key already holds foreman_home, state_dir and the fallbacks it derives from` → the leaf is never resolved, so a planted /tmp/foreman-state-<uid> link still can't make other writes state (existing test passes); resolving dirname of a user-chosen folder can only add state paths, never remove one, so no write escapes state-direct that was caught before [tree 714626aa96f2] (2026-10-21T01:58:30Z)
- (audit edge) `self: read the diff: one Ctx.state_dirs property (Foreman's state folder and an explicit one, each as named and folder-resolved, then the fallbacks) replaces three hand-built lists; the script-verdict cache key already holds foreman_home, state_dir and the fallbacks it derives from` → no foreman_home → the property skips it; state_dir None → skipped; a folder that doesn't exist resolves to itself [tree 714626aa96f2] (2026-10-21T01:58:30Z)
- (audit operator) `self: read the diff: one Ctx.state_dirs property (Foreman's state folder and an explicit one, each as named and folder-resolved, then the fallbacks) replaces three hand-built lists; the script-verdict cache key already holds foreman_home, state_dir and the fallbacks it derives from` → the guard corpus (test_guard_cases) and every guard suite unchanged [tree 714626aa96f2] (2026-10-21T01:58:30Z)
- (audit maintainer) `self: read the diff: one Ctx.state_dirs property (Foreman's state folder and an explicit one, each as named and folder-resolved, then the fallbacks) replaces three hand-built lists; the script-verdict cache key already holds foreman_home, state_dir and the fallbacks it derives from` → a property, so a context whose state_dir is set after construction (the fallback tests do) is judged right [tree 714626aa96f2] (2026-10-21T01:58:30Z)
- (audit intent) `self: read the diff: one Ctx.state_dirs property (Foreman's state folder and an explicit one, each as named and folder-resolved, then the fallbacks) replaces three hand-built lists; the script-verdict cache key already holds foreman_home, state_dir and the fallbacks it derives from` → a write to the real path of a linked state folder is state-direct (tested for ~/.claude-style and FOREMAN_STATE-style links); the T-1284 review's leaf-target idea (option C) dropped, logged why [tree 714626aa96f2] (2026-10-21T02:00:56Z)
- (audit adversary) `self: read the diff: one Ctx.state_dirs property (Foreman's state folder and an explicit one, each as named and folder-resolved, then the fallbacks) replaces three hand-built lists; the script-verdict cache key already holds foreman_home, state_dir and the fallbacks it derives from` → the leaf is never resolved, so a planted /tmp/foreman-state-<uid> link still can't make other writes state (existing test passes); resolving dirname of a user-chosen folder can only add state paths, never remove one, so no write escapes state-direct that was caught before [tree 714626aa96f2] (2026-10-21T02:00:56Z)
- (audit edge) `self: read the diff: one Ctx.state_dirs property (Foreman's state folder and an explicit one, each as named and folder-resolved, then the fallbacks) replaces three hand-built lists; the script-verdict cache key already holds foreman_home, state_dir and the fallbacks it derives from` → no foreman_home → the property skips it; state_dir None → skipped; a folder that doesn't exist resolves to itself [tree 714626aa96f2] (2026-10-21T02:00:56Z)
- (audit operator) `self: read the diff: one Ctx.state_dirs property (Foreman's state folder and an explicit one, each as named and folder-resolved, then the fallbacks) replaces three hand-built lists; the script-verdict cache key already holds foreman_home, state_dir and the fallbacks it derives from` → the guard corpus (test_guard_cases) and every guard suite unchanged [tree 714626aa96f2] (2026-10-21T02:00:56Z)
- (audit maintainer) `self: read the diff: one Ctx.state_dirs property (Foreman's state folder and an explicit one, each as named and folder-resolved, then the fallbacks) replaces three hand-built lists; the script-verdict cache key already holds foreman_home, state_dir and the fallbacks it derives from` → a property, so a context whose state_dir is set after construction (the fallback tests do) is judged right [tree 714626aa96f2] (2026-10-21T02:00:56Z)
## Log
- 2026-10-21T00:54:13Z created
- 2026-10-21T01:48:48Z grounding: the three state lists (fmguard.py:485, 519, 562) use os.path.join(foreman_home, 'state') and ctx.state_dir as given; only state_fallbacks get the folder-resolved form (:65). Plan: Ctx.state_dirs = foreman_home/state and state_dir, each as given, with its folder resolved (leaf kept), and with the leaf resolved too when its target is the user's own and not group/world-writable (fmcore _private's test); use it at the three sites. Tests: a Write to the real path of a linked FOREMAN_STATE / linked ~/.claude is state-direct; a planted leaf link to / still isn't followed.
- 2026-10-21T01:54:44Z focused
- 2026-10-21T01:55:11Z steer: option C (resolve a private leaf link) dropped: the existing planted-link test (target = the user's own work folder) can't tell a planted link from a legitimate one in one user's test, so C would weaken it. B (folder resolved, leaf kept) covers both real cases: macOS's linked /tmp and ~/.claude linked into dotfiles (the link is above the leaf).
- 2026-10-21T01:55:39Z scope: plugin/tests/test_guard.py for the regression test
- 2026-10-21T02:00:52Z scope: plugin/tests/test_guard.py holds the regression test; CHANGELOG.md the release note
- 2026-10-21T02:03:13Z done
- 2026-10-21T02:03:15Z committed 959d9275 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1284-review: Verdict:** approve with nits. I found no way to make the guard treat an outside write as inside a project, or a project or state write as outside…
- T-0774 [FIX S, done, 2 steps] Guard: heredoc python started by 'cd DIR && python3 -' resolves its relative open() targets in DIR only — lesson: a guard relaxation that t…
- T-1032 [FEATURE L, done, 6 steps] Learn a fix once, apply it every time: when a session hits an obstacle and resolves it (e. — lesson: Never name a unittest helper fail(…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
- similar finished tasks took 2–6 steps
- start here (files T-0774 touched): plugin/tests/test_guard.py, plugin/lib/fmguard.py
- likely tests for the scope: plugin/tests/test_guard.py
## Lessons
- Resolve the folder above a path someone else can't plant, never the leaf: it covers linked homes and temp folders without trusting a link in /tmp
## Plan gaps
- failed first: step 1 Failing tests: linked FOREMAN_STATE, linked foreman_home, private linked leaf; planted leaf to / st…
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md

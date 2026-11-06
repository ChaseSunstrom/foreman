---
id: T-1290
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-20T20:56:59Z
updated: 2026-10-21T00:01:42Z
base: 45cad6f53dc1a92fd670514c43060aa575b675b2
base_tree: 455d0f64a9a408c096ecceaa8ccb5bf64a94f2cc
plan0_at: 2026-10-20T23:28:03Z
plan0_scope: []
verified: strong
---
# The builder rules live once, in plugin/agents/fm-builder.md: fm lane brief reads them from there instead of keeping its own copy in fmlanes.py
## Raw request
> The builder rules are copied in plugin/agents/fm-builder.md and plugin/lib/fmlanes.py:153-166 with no test tying them together; they can drift
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fmlanes.py holds no copy of the builder rules; the brief fm lane brief writes carries the rules section of plugin/agents/fm-builder.md word for word, and a test fails if a rule is added to the agent file but missing from the brief — verify with `python3 plugin/tests/run.py test_lanes`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: the brief's rules equal the agent file's
2. [x] fmlanes reads the rules section from the agent file (one helper); delete the copy; behaviour lock: the brief text is unchanged today
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_lanes 2>&1 | tail -8` → ✗ exit 1 · Ran 30 tests in 30.6s (5 classes, 16 at a time; slowest: Lanes 30s, BoardLanes 2s, SafeGitFailsClosed 0s) / FAILED (2 classes) [ran] [tree 27d972385283] (2026-10-20T23:29:17Z)
- (step 1) `python3 plugin/tests/run.py test_lanes test_verifying` → exit 0 · Ran 38 tests in 24.4s (12 classes, 16 at a time; slowest: Lanes 24s, BoardLanes 2s, Claims 2s) / OK [ran] [tree 983fb246a7c1] (2026-10-20T23:58:54Z)
- (step 2) `python3 plugin/tests/run.py test_lanes test_verifying` → exit 0 · Ran 38 tests in 24.4s (12 classes, 16 at a time; slowest: Lanes 24s, BoardLanes 2s, Claims 2s) / OK [ran] [tree 983fb246a7c1] (2026-10-20T23:59:19Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes test_verifying` → exit 0 · Ran 38 tests in 24.3s (12 classes, 16 at a time; slowest: Lanes 24s, BoardLanes 2s, Claims 2s) / OK [ran] [tree 983fb246a7c1] (2026-10-20T23:59:44Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 30 tests in 24.2s (5 classes, 16 at a time; slowest: Lanes 24s, BoardLanes 2s, SafeGitFailsClosed 0s) / OK [ran] [tree 983fb246a7c1] (2026-10-21T00:00:09Z)
- (audit intent) `self review: fmlanes.contract() takes the rules section of plugin/agents/fm-builder.md and fills <ID>/<BASE>/<MAIN>; the copy in fmlanes.py is gone; a test fails if a rule in the agent file is missing from the brief` → one source for the builder rules [tree 983fb246a7c1] (2026-10-21T00:00:09Z)
- (audit adversary) `self review: fmlanes.contract() takes the rules section of plugin/agents/fm-builder.md and fills <ID>/<BASE>/<MAIN>; the copy in fmlanes.py is gone; a test fails if a rule in the agent file is missing from the brief` → substituted values are a task id, a commit and the repo root [tree 983fb246a7c1] (2026-10-21T00:00:09Z)
- (audit edge) `self review: fmlanes.contract() takes the rules section of plugin/agents/fm-builder.md and fills <ID>/<BASE>/<MAIN>; the copy in fmlanes.py is gone; a test fails if a rule in the agent file is missing from the brief` → an edited-away marker in the agent file makes fm lane brief fail loudly, and the test catches it [tree 983fb246a7c1] (2026-10-21T00:00:09Z)
- (audit operator) `self review: fmlanes.contract() takes the rules section of plugin/agents/fm-builder.md and fills <ID>/<BASE>/<MAIN>; the copy in fmlanes.py is gone; a test fails if a rule in the agent file is missing from the brief` → builders now also get the four rules only the agent file had [tree 983fb246a7c1] (2026-10-21T00:00:09Z)
- (audit maintainer) `self review: fmlanes.contract() takes the rules section of plugin/agents/fm-builder.md and fills <ID>/<BASE>/<MAIN>; the copy in fmlanes.py is gone; a test fails if a rule in the agent file is missing from the brief` → a rule is edited in one place [tree 983fb246a7c1] (2026-10-21T00:00:09Z)
- (audit self) `self review: fmlanes.contract() takes the rules section of plugin/agents/fm-builder.md and fills <ID>/<BASE>/<MAIN>; the copy in fmlanes.py is gone; a test fails if a rule in the agent file is missing from the brief` → no findings [tree 983fb246a7c1] (2026-10-21T00:00:09Z)
## Log
- 2026-10-20T20:56:59Z created
- 2026-10-20T21:41:45Z planned from capture
- 2026-10-20T23:27:53Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1290.builder.md
- 2026-10-20T23:28:03Z focused
- 2026-10-20T23:49:01Z merged worktree-agent-a44b18fe341ce0975 (3 file(s))
- 2026-10-20T23:49:30Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a44b18fe341ce0975
- 2026-10-20T23:58:24Z focused
- 2026-10-21T00:01:42Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0961 [FEATURE M, done, 3 steps] Lanes and internals: the merge base saved before the merge, one _git helper — lesson: When a helper turns exceptions into return codes,…
- T-0779 [PERFORMANCE S, done, 2 steps] Lane briefs pass a per-tier effort with the model — lesson: a lane's builder should record the failing run before the fix; when it …
- T-1151 [CLEAN S, done, 1 steps] One source for the builder contract: plugin/agents/fm-builder.md's numbered rules duplicat
- decision 2026-09-27: Build the smarter-Foreman slate, and further self-improvement rounds, as a candidate in a git worktree (~/.claude/foreman-improve-20260926, branch i…
- similar finished tasks took 1–3 steps
## Behaviour lock
the brief's contract text is now the agent file's rules section word for word; that adds four bullets the old copy lacked (no fm commands for another task or branch switches, a guard block is a signal, three failed attempts, the andon rule), which is the intended single source; every other line of the brief is unchanged (test_lanes and test_verifying, 38 tests)
## Lessons
- Text an agent must follow lives once; a generator reads it rather than keeping a copy that drifts
## Files touched
- plugin/tests/test_lanes.py
- plugin/tests/test_verifying.py
- plugin/lib/fmlanes.py
- CHANGELOG.md
- plugin/lib/fmguard.py
- plugin/lib/fmreplay.py
- plugin/tests/test_guard_cases.py
- plugin/tests/test_guard_state_key.py

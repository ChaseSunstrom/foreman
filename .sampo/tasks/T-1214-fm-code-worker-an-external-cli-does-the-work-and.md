---
id: T-1214
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: [T-1212]
source: user
created: 2026-10-16T15:20:14Z
updated: 2026-10-20T14:28:05Z
base: ba12f4675c0fb06eb9301c8903c933a5f024b06b
base_tree: ca867906271e59bed7f0d1190df7de94a145ed41
plan0_at: 2026-10-17T00:29:18Z
plan0_scope: []
inferred_deps: [T-1207]
inferred_why: T-1207: worker mode builds on the fm code loop
verified: strong
---
# fm code --worker: an external CLI does the work, and the harness judges its diff and runs the verify
## Raw request
> fm code --worker: an external CLI does the work, and the harness judges its diff and runs the verify
## Interpretation
Round 2 of Foreman Code (T-1207). fm code --worker claude|codex|gemini|opencode|aider|'CMD {prompt}' hands each planned step (or the whole task) to an installed CLI in headless mode, inside the task's scope, then judges the result itself: the diff since the step began, the guard's verdict on what changed (protected paths, out-of-scope files), and the criterion's verify command run by the harness. Weak or unknown CLIs get the same discipline as fm code's own loop.
## Assumptions (confidence)
## Acceptance criteria
- [x] tests run fm code --worker with a fake CLI script that edits the seeded bug (pass), one that edits a protected file (reverted and reported), one that hangs (killed at the timeout), and a missing CLI (one-line error); the harness's verify decides, never the worker's own claim — verify with `python3 plugin/tests/run.py test_code_worker`
## Non-goals
## Approach (options → choice → why)
One worker table, not per-tool adapters: each entry is an argv template ({prompt} and {model} placeholders) plus how to detect it (shutil.which) and whether it reads Foreman's hook already (fm agents install). Defaults: claude -p {prompt} --permission-mode acceptEdits; codex exec {prompt}; gemini -p {prompt}; opencode run {prompt}; aider --message {prompt} --yes. The step prompt is the brief's step plus the criterion and the files it may touch; the run is bounded by a process-group watchdog (timeout, then SIGTERM, then SIGKILL) and its output is cut to head and tail into the journal. After it exits: git diff --name-only since the step's snapshot; any file the guard's write check refuses (protected or out of scope) is reverted from the snapshot and reported; then the harness runs the verify; a failure gives the worker one retry with the output, then --escalate (another worker or a model) or block. Missing CLI: a one-line error naming how to install it. Options: per-CLI adapters (more code, drift), driving CLIs through a PTY (fragile), or this argv template plus diff judgment (chosen).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests with fake worker scripts
2. [x] Worker table, step prompt, watchdog, diff judgment with revert, verify and retry, escalate
3. [x] Docs: README and MASTER rows
## Resume here
<!-- auto -->
- 2026-10-20T14:02:25Z step 1/3: Failing tests with fake worker scripts
- git: foreman/build; 6 uncommitted: CHANGELOG.md, MASTER.md, README.md, plugin/lib/fmcode.py, plugin/tests/test_code_worker.py, site/pages.py
- touched since last checkpoint: /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/probe_guard.py, .claude/worktrees/agent-aa8dd4854e7d2fffe/plugin/lib/fmcli.py, .claude/worktrees/agent-aa8dd4854e7d2fffe/README.md, .claude/worktrees/agent-aa8dd4854e7d2fffe/MASTER.md, .claude/worktrees/agent-aa8dd4854e7d2fffe/plugin/lib/fmcode.py, .claude/worktrees/agent-aa8dd4854e7d2fffe/plugin/tests/test_code_worker.py, plugin/tests/test_code_worker.py, plugin/lib/fmcode.py, CHANGELOG.md, MASTER.md, README.md, site/pages.py, /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/brainstorm-20261020.md, /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/foreman-ideas-1020.html
## Docs impact
README, MASTER and CHANGELOG describe the subreaper, the stat walk, the stripped verify environment and the sensitive-repo refusal; the site's worker list drops opencode
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code_worker` → ✗ exit 1 · Ran 7 tests in 2.6s (1 classes, 16 at a time; slowest: Worker 1s) / FAILED (1 classes) [ran] [tree f6063e286bd1] (2026-10-20T13:46:25Z)
- (step 2) `python3 plugin/tests/run.py test_code_worker test_code` → exit 0 · Ran 36 tests in 13.4s (11 classes, 16 at a time; slowest: Worker 13s, Repairs 6s, Review 6s) / OK [ran] [tree 0884310d7def] (2026-10-20T13:52:19Z)
- (step 3) `grep -c 'worker' README.md MASTER.md` → exit 0 · README.md:1 / MASTER.md:1 [ran] [tree 0884310d7def] (2026-10-20T13:52:19Z)
- (step 2) `python3 plugin/tests/run.py test_code_worker test_code` → exit 0 · Ran 48 tests in 24.0s (11 classes, 16 at a time; slowest: Worker 24s, Repairs 6s, Review 6s) / OK [ran] [tree ff00e8c49bd6] (2026-10-20T14:20:21Z)
- (step 3) `grep -c 'subreaper\|sensitive repo' README.md MASTER.md CHANGELOG.md` → exit 0 · MASTER.md:5 / CHANGELOG.md:3 [ran] [tree ff00e8c49bd6] (2026-10-20T14:20:21Z)
- (step 1) `cd /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/red1214/plugin/tests && python3 -m unittest test_code_worker 2>&1 | tail -3; exit ${PIPESTATUS[0]}` → ✗ exit 1 · Ran 19 tests in 29.035s / FAILED (failures=12) [ran] [tree ff00e8c49bd6] (2026-10-20T14:21:07Z)
- (step 1) `python3 plugin/tests/run.py test_code_worker` → exit 0 · Ran 19 tests in 24.0s (1 classes, 16 at a time; slowest: Worker 24s) / OK [ran] [tree ff00e8c49bd6] (2026-10-20T14:22:01Z)
- (ac 1) `python3 plugin/tests/run.py test_code_worker` → exit 0 · Ran 19 tests in 23.7s (1 classes, 16 at a time; slowest: Worker 24s) / OK [ran] [tree ff00e8c49bd6] (2026-10-20T14:22:25Z)
- (audit adversary) `one fm-reviewer pass (adversary, intent, operator lenses), research T-1214-review; every high and medium finding fixed test-first` → fixed and tested: a setsid'd process now dies with its turn (subreaper on Linux); the verify gets the worker's stripped environment; an ignored .env the worker overwrote is put back; an assume-unchanged flag it set is cleared and the change committed; a hook in a chmod 555 hooks folder is removed; a sensitive repo is refused; the global Git config is put back; the judge's own git runs no fsmonitor or hooks. Still open: the worker runs as the user, so reads and network sends aren't judged (documented); pre-existing dirty work it deletes (T-1270); edits to the verify's own test (T-1271) [tree ff00e8c49bd6] (2026-10-20T14:22:25Z)
- (audit edge) `one fm-reviewer pass (adversary, intent, operator lenses), research T-1214-review; every high and medium finding fixed test-first` → a 400-file ignored build folder keeps the fix; the user's own hooks link stays; a branch switch from a detached HEAD leaves that branch's commit; macOS falls back to the process-group kill [tree ff00e8c49bd6] (2026-10-20T14:22:25Z)
- (audit operator) `one fm-reviewer pass (adversary, intent, operator lenses), research T-1214-review; every high and medium finding fixed test-first` → the whole-tree snapshot costs about 1 s per turn on 12 to 15 thousand files, against turns of minutes [tree ff00e8c49bd6] (2026-10-20T14:22:25Z)
- (audit intent) `one fm-reviewer pass (adversary, intent, operator lenses), research T-1214-review; every high and medium finding fixed test-first` → all four criteria hold: the fake CLI's fix closes the task, a protected write is reverted and reported, a hang is killed at the timeout, a missing CLI is one line, and only the harness's verify decides [tree ff00e8c49bd6] (2026-10-20T14:22:25Z)
- (step 2) `python3 plugin/tests/run.py test_code_worker test_code` → exit 0 · Ran 48 tests in 41.1s (11 classes, 16 at a time; slowest: Worker 41s, Review 13s, Repairs 13s) / OK [ran] [tree 9a3b7b6fc0da] (2026-10-20T14:24:17Z)
- (audit adversary) `one fm-reviewer pass (adversary, intent, operator lenses), research T-1214-review; every high and medium finding fixed test-first` → fixed and tested: a setsid'd process now dies with its turn (subreaper on Linux); the verify gets the worker's stripped environment; an ignored .env the worker overwrote is put back; an assume-unchanged flag it set is cleared and the change committed; a hook in a chmod 555 hooks folder is removed; a sensitive repo is refused; the global Git config is put back; the judge's own git runs no fsmonitor or hooks. Still open: the worker runs as the user, so reads and network sends aren't judged (documented); pre-existing dirty work it deletes (T-1270); edits to the verify's own test (T-1271) [tree 9a3b7b6fc0da] (2026-10-20T14:24:18Z)
- (audit edge) `one fm-reviewer pass (adversary, intent, operator lenses), research T-1214-review; every high and medium finding fixed test-first` → a 400-file ignored build folder keeps the fix; the user's own hooks link stays; a branch switch from a detached HEAD leaves that branch's commit; macOS falls back to the process-group kill [tree 9a3b7b6fc0da] (2026-10-20T14:24:18Z)
- (audit operator) `one fm-reviewer pass (adversary, intent, operator lenses), research T-1214-review; every high and medium finding fixed test-first` → the whole-tree snapshot costs about 1 s per turn on 12 to 15 thousand files, against turns of minutes [tree 9a3b7b6fc0da] (2026-10-20T14:24:18Z)
- (audit intent) `one fm-reviewer pass (adversary, intent, operator lenses), research T-1214-review; every high and medium finding fixed test-first` → all four criteria hold: the fake CLI's fix closes the task, a protected write is reverted and reported, a hang is killed at the timeout, a missing CLI is one line, and only the harness's verify decides [tree 9a3b7b6fc0da] (2026-10-20T14:24:18Z)
- (step 2) `python3 plugin/tests/run.py test_code_worker test_code` → exit 0 · Ran 48 tests in 46.8s (11 classes, 16 at a time; slowest: Worker 47s, Review 16s, Repairs 15s) / OK [ran] [tree 1e875571dc47] (2026-10-20T14:26:28Z)
- (audit adversary) `one fm-reviewer pass (adversary, intent, operator lenses), research T-1214-review; every high and medium finding fixed test-first` → fixed and tested: a setsid'd process now dies with its turn (subreaper on Linux); the verify gets the worker's stripped environment; an ignored .env the worker overwrote is put back; an assume-unchanged flag it set is cleared and the change committed; a hook in a chmod 555 hooks folder is removed; a sensitive repo is refused; the global Git config is put back; the judge's own git runs no fsmonitor or hooks. Still open: the worker runs as the user, so reads and network sends aren't judged (documented); pre-existing dirty work it deletes (T-1270); edits to the verify's own test (T-1271) [tree 1e875571dc47] (2026-10-20T14:26:29Z)
- (audit edge) `one fm-reviewer pass (adversary, intent, operator lenses), research T-1214-review; every high and medium finding fixed test-first` → a 400-file ignored build folder keeps the fix; the user's own hooks link stays; a branch switch from a detached HEAD leaves that branch's commit; macOS falls back to the process-group kill [tree 1e875571dc47] (2026-10-20T14:26:29Z)
- (audit operator) `one fm-reviewer pass (adversary, intent, operator lenses), research T-1214-review; every high and medium finding fixed test-first` → the whole-tree snapshot costs about 1 s per turn on 12 to 15 thousand files, against turns of minutes [tree 1e875571dc47] (2026-10-20T14:26:29Z)
- (audit intent) `one fm-reviewer pass (adversary, intent, operator lenses), research T-1214-review; every high and medium finding fixed test-first` → all four criteria hold: the fake CLI's fix closes the task, a protected write is reverted and reported, a hang is killed at the timeout, a missing CLI is one line, and only the harness's verify decides [tree 1e875571dc47] (2026-10-20T14:26:29Z)
## Log
- 2026-10-16T15:20:14Z created
- 2026-10-17T00:28:54Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1214.builder.md
- 2026-10-17T00:29:18Z focused
- 2026-10-20T13:55:39Z merged worktree-agent-aa8dd4854e7d2fffe (5 file(s))
- 2026-10-20T13:55:43Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aa8dd4854e7d2fffe
- 2026-10-20T13:55:43Z focused
- 2026-10-20T14:28:05Z done
- 2026-10-20T14:28:05Z committed 5a3aba47 (7 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1207 [FEATURE L, planned, 3 steps] Foreman Code: fm code runs Foreman's loop itself on any model or CLI
- decision 2026-10-16: Foreman Code (T-1207) is built as fm code: Foreman's own loop where the harness runs the stations and models fill small JSON slots, over one stdlib …
- research mission-20261015-154003.pack: have FM enforce some things so we don't rely on agents to do it themselves as they are inconsistent (context: 19 card-writer subag…
- research mission-20261016-095938.pack: can you make foreman code? an even better harness than CC, that works with other CLI tools/models as an amazing harness, etc.? [st…
## Lessons
- Judge a worker by what changed on disk (a ctime walk), not by what git status shows: ignored files, index flags and processes outside the group all slip past git
## Plan gaps
- failed first: step 1 Failing tests with fake worker scripts
## Files touched
- plugin/tests/test_code_worker.py
- plugin/lib/fmcli.py
- plugin/lib/fmcode.py
- README.md
- MASTER.md
- CHANGELOG.md
- site/pages.py

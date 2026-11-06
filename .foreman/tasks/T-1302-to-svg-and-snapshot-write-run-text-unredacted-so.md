---
id: T-1302
type: SECURITY
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcodetui.py, plugin/tests/test_code_tui.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-20T23:37:51Z
updated: 2026-10-22T16:09:58Z
base: 217f13bca7ea7a3880719fed999abd4a16f85f6e
base_tree: 2afb947d51006bf2811c947642ec6b815208562d
plan0_at: 2026-10-22T15:59:53Z
plan0_scope: [plugin/lib/fmcodetui.py, plugin/tests/test_code_tui.py, CHANGELOG.md]
verified: strong
---
# fm code app exports scrub secrets
## Raw request
> to_svg` and `snapshot` write run text unredacted, so there is no secret scrubbing on exports
> (noticed by an agent; research brainstorm-20261020-tui)
## Interpretation
fmcodetui.snapshot (~2106) and to_svg (~1270) write a run's text to a file for sharing; nothing redacts it, so a token a worker printed (an API key in a test's output) lands in the exported SVG or text. The journal events are redacted when kept (Run.emit uses fmcore.redact_obj), but snapshot can be fed raw events.
## Assumptions (confidence)
## Acceptance criteria
- [x] a snapshot, a recording and the plain replay of events holding a secret-looking token show it redacted — verify with `cd plugin/tests && python3 -m unittest test_code_tui.Export`
## Non-goals
## Approach (options → choice → why)
Redact the events at snapshot's entry with fmcore.redact_obj (the one redactor everything else uses), so every export path (svg, text) draws scrubbed text. Options: redact in to_svg (misses the text snapshot), redact cell by cell (splits tokens across cells) → at entry.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] redact at snapshot's entry
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_code_tui.Export` → ✗ exit 1 · Ran 1 test in 0.058s / FAILED (failures=1) [ran] [tree bbe0326a5072] (2026-10-22T16:01:05Z)
- (step 2) `python3 plugin/tests/run.py test_code_tui` → ✗ exit 1 · Ran 104 tests in 23.7s (16 classes, 16 at a time; slowest: Fuzz 22s, Command 20s, Events 8s) / FAILED (1 classes) [ran] [tree bbe0326a5072] (2026-10-22T16:01:30Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_code_tui.Export` → exit 0 · Ran 1 test in 0.058s / OK [ran] [tree ca7be3979317] (2026-10-22T16:02:10Z)
- `cd plugin/tests && python3 -m unittest test_code_tui.Export` → ✗ exit 1 · Ran 2 tests in 0.069s / FAILED (failures=2) (start tree + this task's tests) [ran] [tree dc874cf82aae] (2026-10-22T16:09:15Z)
- `cd plugin/tests && python3 -m unittest test_code_tui.Export` → exit 0 · Ran 2 tests in 0.052s / OK [ran] [tree dc874cf82aae] (2026-10-22T16:09:15Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_code_tui.Export` → exit 0 · Ran 2 tests in 0.022s / OK [ran] [tree dc874cf82aae] (2026-10-22T16:09:16Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_code_tui.Export` → exit 0 · Ran 2 tests in 0.041s / OK [ran] [tree dc874cf82aae] (2026-10-22T16:09:17Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_code_tui.Export` → exit 0 · Ran 2 tests in 0.023s / OK [ran] [tree d2650510183e] (2026-10-22T16:09:24Z)
- (audit adversary) `builder (sonnet) test-first; red proved with fm task prove; record() and plain replay covered after its own note; merged; Export tests green.` → every file-writing path (snapshot, record, plain replay) passes events through fmcore.redact/redact_obj at entry; the live screen (the user's own view) is unchanged [tree d2650510183e] (2026-10-22T16:09:24Z)
- (audit edge) `builder (sonnet) test-first; red proved with fm task prove; record() and plain replay covered after its own note; merged; Export tests green.` → redact_obj returns new objects, so the caller's events stay intact [tree d2650510183e] (2026-10-22T16:09:24Z)
- (audit self) `builder (sonnet) test-first; red proved with fm task prove; record() and plain replay covered after its own note; merged; Export tests green.` → no findings [tree d2650510183e] (2026-10-22T16:09:24Z)
## Log
- 2026-10-20T23:37:51Z created
- 2026-10-22T15:59:34Z planned from capture
- 2026-10-22T15:59:39Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1302.builder.md
- 2026-10-22T15:59:52Z focused
- 2026-10-22T16:09:09Z merged worktree-agent-a428f4517f7d9e8df (2 file(s))
- 2026-10-22T16:09:10Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a428f4517f7d9e8df
- 2026-10-22T16:09:12Z focused
- 2026-10-22T16:09:53Z done
- 2026-10-22T16:09:58Z committed 6c1c344b (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1329-review: Verdict: changes needed.** Two MEDIUM issues, one unguarded callback and one control-character leak, plus smaller ones. I could not run the tests…
- research T-1283-review: Verdict: changes needed.** I read the diff and the surrounding `fmcode.py`. I couldn't run anything, so every finding comes from reading the code…
- research T-1320-review: Changes needed. Resume breaks for CLI-planned runs, and the planner's read-only mode is trusted with no check afterwards. [stale: plugin/lib/fmcl…
- decision 2026-10-21: T-1300 ships the renderer, motion, gradients, recording and round 1 of the TUI brainstorm; round 2 is queued as T-1305..T-1315 (with T-1301 wide cha…
## Preflight
Changed in scope since this was planned (2026-10-20): CHANGELOG.md, plugin/lib/fmcodetui.py, plugin/tests/test_code_tui.py; re-ground the plan against them before editing
## Plan gaps
- failed first: step 1 failing test
- failed first: step 2 redact at snapshot's entry
## Files touched
- plugin/tests/test_code_tui.py
- plugin/lib/fmcodetui.py
- CHANGELOG.md

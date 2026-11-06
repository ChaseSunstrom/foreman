---
id: T-1410
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-21T17:28:43Z
updated: 2026-10-21T18:56:59Z
base: 9ee5534aae8b48154c91681a8819011bd8d0763a
base_tree: 02d0cf21c5cd01f93d17c4f0cbdbf4b943152c1f
plan0_at: 2026-10-21T17:33:12Z
plan0_scope: []
verified: strong
---
# fm vetoes prints the command that retracts each veto, and that command removes exactly it
## Raw request
> FEATURE: fm vetoes prints the command that retracts each veto, and that command removes exactly it (S23, B18)
> CONTEXT: round 2 of the fm/fm code brainstorm (T-1382): research/brainstorm-fm-anthropic-catalogue.md, grounding with file:line in research/brainstorm-fm-anthropic-half-a.md (A*) and half-b.md (B*)
> DONE-WHEN: fm vetoes --json lists a retract command per veto and running it round-trips
## Interpretation
A veto recorded from the user's words (T-1323 fixed the false ones) is hard to see and undo. Show each with the one command that removes it.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm vetoes (and --json) gives each veto its retract command, and running it removes exactly that veto — verify with `python3 plugin/tests/run.py test_vetoes`
## Non-goals
## Approach (options → choice → why)
Options: (A) fm vetoes lists each with its number and 'fm vetoes rm N' (chosen: the rm verb exists; numbering is stable oldest-first); (B) a stable id per veto (more state for a list of at most 30); (C) an interactive picker (not scriptable).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: two vetoes, each listed with its retract command; running one leaves the other
2. [x] fm vetoes output and --json carry the command
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_vetoes 2>&1 | tail -8` → ✗ exit 1 · Ran 4 tests in 4.2s (1 classes, 16 at a time; slowest: RecordedVetoes 1s) / FAILED (1 classes) [ran] [tree 150ebca80501] (2026-10-21T17:33:51Z)
- (step 1) `python3 plugin/tests/run.py test_vetoes` → ✗ exit 1 · Ran 4 tests in 1.7s (1 classes, 16 at a time; slowest: RecordedVetoes 1s) / FAILED (1 classes) [ran] [tree 150ebca80501] (2026-10-21T17:33:59Z)
- (step 2) `python3 plugin/tests/run.py test_vetoes` → exit 0 · Ran 4 tests in 1.8s (1 classes, 16 at a time; slowest: RecordedVetoes 2s) / OK [ran] [tree fd46c1b6448e] (2026-10-21T17:34:20Z)
- (step 2) `python3 plugin/tests/run.py test_vetoes` → exit 0 · Ran 4 tests in 1.6s (1 classes, 16 at a time; slowest: RecordedVetoes 1s) / OK [ran] [tree 8cb26e4ebe94] (2026-10-21T18:37:46Z)
- (ac 1) `python3 plugin/tests/run.py test_vetoes` → exit 0 · Ran 4 tests in 1.8s (1 classes, 16 at a time; slowest: RecordedVetoes 1s) / OK [ran] [tree 8cb26e4ebe94] (2026-10-21T18:37:49Z)
- (audit intent) `self: read the diff — fm vetoes numbers vetoes oldest first and prints 'fm vetoes rm N' per row; --json adds retract; the rm path already removes by that number (test runs the printed command and checks only that veto is gone)` → the printed command removes exactly that veto (test_vetoes runs it) [tree 8cb26e4ebe94] (2026-10-21T18:37:49Z)
- (audit edge) `self: read the diff — fm vetoes numbers vetoes oldest first and prints 'fm vetoes rm N' per row; --json adds retract; the rm path already removes by that number (test runs the printed command and checks only that veto is gone)` → numbering is oldest-first and stable across a removal of a later veto; an empty list prints no command [tree 8cb26e4ebe94] (2026-10-21T18:37:49Z)
- (audit self) `self: read the diff — fm vetoes numbers vetoes oldest first and prints 'fm vetoes rm N' per row; --json adds retract; the rm path already removes by that number (test runs the printed command and checks only that veto is gone)` → no findings [tree 8cb26e4ebe94] (2026-10-21T18:37:49Z)
- (audit intent) `self: read the diff — fm vetoes numbers vetoes oldest first and prints 'fm vetoes rm N' per row; --json adds retract; the rm path removes by that number (the test runs the printed command and checks only that veto is gone)` → the printed command removes exactly that veto (test_vetoes runs it) [tree c91e26bd60c0] (2026-10-21T18:49:37Z)
- (audit edge) `self: read the diff — fm vetoes numbers vetoes oldest first and prints 'fm vetoes rm N' per row; --json adds retract; the rm path removes by that number (the test runs the printed command and checks only that veto is gone)` → numbering is oldest-first, so removing a later veto leaves earlier numbers unchanged; an empty list prints no command [tree c91e26bd60c0] (2026-10-21T18:49:37Z)
- (audit self) `self: read the diff — fm vetoes numbers vetoes oldest first and prints 'fm vetoes rm N' per row; --json adds retract; the rm path removes by that number (the test runs the printed command and checks only that veto is gone)` → no findings [tree c91e26bd60c0] (2026-10-21T18:49:37Z)
## Log
- 2026-10-21T17:28:43Z created
- 2026-10-21T17:32:35Z planned from capture
- 2026-10-21T17:32:49Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1410.builder.md
- 2026-10-21T17:33:11Z focused
- 2026-10-21T18:16:08Z merged worktree-agent-ace70c6cc9871745c (2 file(s))
- 2026-10-21T18:24:17Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ace70c6cc9871745c
- 2026-10-21T18:24:26Z focused
- 2026-10-21T18:24:27Z scope: also resolving T-1399's one-hunk merge conflict on its branch (both sides kept: T-1378's _PARSER memo and T-1399's _OutputFormat), since T-1399's lane can't be focused while it holds the branch
- 2026-10-21T18:46:49Z scope: plugin/tests/test_doctor.py — T-1378's parser memo left test_self_docs_hold_fm_help_to_every_command_once's broken HELP_TIERS in place for the next test (it relied on a rebuild to restore them); the test now restores them itself. Blocks T-1410's affected-tests gate.
- 2026-10-21T18:56:56Z done
- 2026-10-21T18:56:59Z committed c5543f01 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-fm-anthropic-catalogue: Source: research/brainstorm-20261021-120257 (fm ideas, 10 lenses, 4 rounds, 3 deepened, --seen every earlier ideas.md: 520 ne…
- T-1399 [FEATURE S, planned, 2 steps] fm code takes claude's own flags: -p/--print, -c/--continue and --output-format json mean --plain, --resume and --json
- T-1396 [SECURITY M, planned, 2 steps] Hostile skills and plugins can't get past the indexer: a 25+ item corpus quarantined with reasons, the Agent Skills spec checked, o…
- decision 2026-10-16: Foreman Code (T-1207) is built as fm code: Foreman's own loop where the harness runs the stations and models fill small JSON slots, over one stdlib …
## Why not caught
none: a new hint, not a regression
## Lessons
- A record the user can create should print the command that undoes it, in the same output
## Plan gaps
- failed first: step 1 Failing test: two vetoes, each listed with its retract command; running one leaves the other
## Files touched
- plugin/tests/test_vetoes.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- plugin/tests/test_doctor.py
- MASTER.md
- README.md
- plugin/lib/fmdoctor.py
- plugin/lib/fmlib.py
- plugin/lib/fmplugins.py
- plugin/tests/fixtures/hostile/corpus.json
- plugin/tests/fixtures/hostile/marketplace.json
- plugin/tests/test_code.py
- plugin/tests/test_docs.py
- plugin/tests/test_lib_hostile.py
- plugin/tests/test_library.py
- site/build.py
- site/index.html
- site/style.css

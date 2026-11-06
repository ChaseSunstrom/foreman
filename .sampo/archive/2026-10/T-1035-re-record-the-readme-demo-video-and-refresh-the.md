---
id: T-1035
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T03:07:49Z
updated: 2026-10-16T04:20:42Z
base: f896182d03c79cb50fa2b8e11036af4050e1dde4
base_tree: f4f0cc9b0f6855872460a88511e18fae50681111
verified: strong
---
# Re-record the README demo video and refresh the README's pictures with the new UI (chat se
## Raw request
> Re-record the README demo video and refresh the README's pictures with the new UI (chat sections, Agents node graph, work bar, live tree)
## Interpretation
The README's demo (demo/live.svg/mp4) and its words still show the pane before the node graph, work bar, chat sections, known fixes and the live tree. Re-record a real session in the isolated harness (scrubbed, a clone, never the user's screen) so it shows all of them, and refresh the README text around it.
## Assumptions (confidence)
## Acceptance criteria
- [x] demo/live.svg and demo/live.mp4 show the new chat sections, the live tree and the pane's node graph and work bar; the README's alt text and caption describe them — verify with `python3 -c "import os,time,sys; sys.exit(0 if all(time.time()-os.path.getmtime(f)<86400*2 for f in ('demo/live.svg','demo/live.mp4')) and 'live tree' in open('README.md').read() else 1)"`
## Non-goals
## Approach (options → choice → why)
Options: (a) static screenshots: no motion, the live tree's point is lost; (b) re-run the demo recorder (demo/record_live.py) on a clone with a short real task that uses a subagent, an edit and a failing-then-passing command, so the tree, the diff, the known fix and the pane all show; (c) hand-made animation: not real. Choice (b), after T-1033 and T-1036 land so it shows them.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Pick the recorded task (subagent + edit + fail-then-pass) and run the recorder on a clone
2. [x] Check the frames; README alt/caption; CHANGELOG
## Resume here
T-1035: demo recording running in the background (record.out in scratchpad); next: check frames, README alt/caption, CHANGELOG
<!-- auto -->
- 2026-10-16T04:10:09Z step 1/2: Pick the recorded task (subagent + edit + fail-then-pass) and run the recorder on a clone
- git: foreman/build; 0 uncommitted
## Docs impact
README alt text and caption; CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_edit_cards` → exit 0 · Ran 22 tests in 14.0s (6 classes, 16 at a time; slowest: ImportCards 14s, EditCards 10s, EditCardsReview 4s) / OK [ran] [tree 337b05d956b3] (2026-10-16T04:13:08Z)
- (step 2) `python3 -c "import os,time,sys; sys.exit(0 if all(time.time()-os.path.getmtime(f)<86400*2 for f in ('demo/live.svg','demo/live.mp4')) and 'live tree' in open('README.md').read() else 1)"` → exit 0 · (no output) [ran] [tree 337b05d956b3] (2026-10-16T04:13:09Z)
- (ac 1) `python3 -c "import os,time,sys; sys.exit(0 if all(time.time()-os.path.getmtime(f)<86400*2 for f in ('demo/live.svg','demo/live.mp4')) and 'live tree' in open('README.md').read() else 1)"` → exit 0 · (no output) [ran] [tree 9546d73768a5] (2026-10-16T04:20:41Z)
- (audit intent) `self: frames checked at 35/70/98% (chat tree, live tree with a scout branch, pane work bar and Agents graph, the close); demo files scrubbed (no name/e-mail); the session's own change (fm lib stats --days) applied with its test, red then green` → the README demo shows the current UI working a real task end to end, and its change ships [tree 9546d73768a5] (2026-10-16T04:20:41Z)
- (audit adversary) `self: frames checked at 35/70/98% (chat tree, live tree with a scout branch, pane work bar and Agents graph, the close); demo files scrubbed (no name/e-mail); the session's own change (fm lib stats --days) applied with its test, red then green` → grep finds no user name, e-mail or home path in live.cast/live.svg [tree 9546d73768a5] (2026-10-16T04:20:41Z)
- (audit edge) `self: frames checked at 35/70/98% (chat tree, live tree with a scout branch, pane work bar and Agents graph, the close); demo files scrubbed (no name/e-mail); the session's own change (fm lib stats --days) applied with its test, red then green` → the --days filter compares ISO UTC strings; no --days counts everything as before [tree 9546d73768a5] (2026-10-16T04:20:41Z)
- (audit operator) `self: frames checked at 35/70/98% (chat tree, live tree with a scout branch, pane work bar and Agents graph, the close); demo files scrubbed (no name/e-mail); the session's own change (fm lib stats --days) applied with its test, red then green` → caption names the request and the task; MP4 linked [tree 9546d73768a5] (2026-10-16T04:20:41Z)
- (audit maintainer) `self: frames checked at 35/70/98% (chat tree, live tree with a scout branch, pane work bar and Agents graph, the close); demo files scrubbed (no name/e-mail); the session's own change (fm lib stats --days) applied with its test, red then green` → the recorder is unchanged; one re-run regenerates all three files [tree 9546d73768a5] (2026-10-16T04:20:41Z)
## Log
- 2026-10-16T03:07:49Z created
- 2026-10-16T03:17:52Z criterion 1 verify: `ls -la demo/live.svg demo/live.mp4` → `python3 -c "import os,time,sys; sys.exit(0 if all(time.time()-os.path.getmtime(f)<86400*2 for f in ('demo/live.svg','demo/live.mp4')) and 'live tree' in open('README.md').read() else 1)"`
- 2026-10-16T03:50:00Z steer: the user wants the updated UI recorded (README demo/video) and then a push to main 'when you get a chance', and again when everything is done
- 2026-10-16T04:08:35Z focused
- 2026-10-16T04:10:14Z paused: focus moved to T-1057
- 2026-10-16T04:11:48Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-16T04:11:48Z focused
- 2026-10-16T04:20:42Z done
- 2026-10-16T04:20:42Z committed e29331a (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1026 [FEATURE M, done, 5 steps] And is the graph a node graph? like with lines connecting and stuff? how can we make the e — lesson: A flex-ordered layout gives spare …
- T-0979 [FEATURE M, done, 2 steps] Re-record the README demo from a real Claude Code session with the current pane: record_li — lesson: A recorder that waits for T-0001 m…
- T-0903 [FEATURE M, done, 3 steps] Showcase: a recording of the real Claude Code UI with the foreman-ui mod fixing a seeded bug through Foreman — lesson: Record the produ…
- decision 2026-10-09: Added JARVIS (<user>@<host>) as a fm conductor remote so the Foreman pane shows its sessions as tiles: the user's own host over their own …
## Lessons
- Record the demo after the UI work lands, and ship the recorded session's change so the caption stays true
## Files touched
- plugin/tests/test_edit_cards.py
- plugin/lib/fmcli.py
- plugin/lib/fmlib.py
- CHANGELOG.md
- README.md
- plugin/tests/test_loop.py

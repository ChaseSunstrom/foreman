---
id: T-1557
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/skills/playbooks/references/ui/scene-3d.md, plugin/skills/playbooks/ratchet.json, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-22T17:44:34Z
updated: 2026-10-23T08:42:52Z
base: 6116bdb2823bc7976148d4ab81362a479624b4fa
base_tree: 65cd17caac89d097bcd26ad07dd75f20d0df480d
plan0_at: 2026-10-23T08:39:25Z
plan0_scope: [plugin/skills/playbooks/references/ui/scene-3d.md, plugin/skills/playbooks/ratchet.json, CHANGELOG.md]
verified: strong
---
# scene-3d playbook: replace the guessed WebGL context cap with a measured one (Chrome desktop keeps 16 live: probed with HeadlessChrome 153 on Linux, 40 made), and say Safari's and Android's caps aren't verified here
## Raw request
> scene-3d.md has no Chrome/Safari/Android context-cap source. Worth a probe or citation task
> (noticed by an agent; research T-1488-1492-1494-review)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] scene-3d.md's context-cap rule states the measured Chrome desktop number with how and when it was measured, and marks the other browsers as unverified — verify with `python3 plugin/tests/run.py test_playbook_check test_docs`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] edit the rule and record the probe in research
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_playbook_check test_docs` → exit 0 · Ran 99 tests in 8.5s (25 classes, 16 at a time; slowest: Fences 8s, Snippets 2s, TaskLifecycle 1s) / OK [ran] [tree f405e4bf4d74] (2026-10-23T08:42:39Z)
- (audit intent) `self` → pass: the number now comes from a probe recorded in research, with what wasn't measured said plainly [tree 51288a058e4f] (2026-10-23T08:42:40Z)
- (ac 1) `python3 plugin/tests/run.py test_playbook_check test_docs` → exit 0 · Ran 99 tests in 8.5s (25 classes, 16 at a time; slowest: Fences 8s, Snippets 2s, Repo 1s) / OK [ran] [tree 51288a058e4f] (2026-10-23T08:42:49Z)
- (audit intent) `self: intent` → Chrome desktop measured; Safari, Firefox and Android named as unverified (no such browser here) [tree 51288a058e4f] (2026-10-23T08:42:49Z)
- (audit self) `self: intent` → no findings [tree 51288a058e4f] (2026-10-23T08:42:49Z)
## Log
- 2026-10-22T17:44:34Z created
- 2026-10-23T08:39:03Z planned from capture
- 2026-10-23T08:39:04Z set scope=['plugin/skills/playbooks/references/ui/scene-3d.md', 'plugin/skills/playbooks/ratchet.json', 'CHANGELOG.md']
- 2026-10-23T08:39:24Z focused
- 2026-10-23T08:42:51Z done
- 2026-10-23T08:42:52Z committed 86dc5e7b (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1557-webgl-context-cap: Probe 2026-10-23: a page creating 40 canvases with getContext('webgl'), then counting those with !isContextLost() after 500 ms.
- research T-1488-1492-1494-review: Verdict: approve with nits.** All three playbooks are indexed, every card they name exists, and the example palette's contrast numbers …
- T-1515 [FEATURE S, done, 1 steps] Expand the terminal UI playbook: display width and wide glyphs, resize, bracketed paste, the motion budget, terminal lifecycle and CLI …
- decision 2026-10-15: Recommendation: close the gaps where a small model has to guess a command (done: T-0969, T-0985, T-0986, T-0987); no separate small-model mode or MC…
- the similar finished task took 1 steps
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/skills/playbooks/ratchet.json, plugin/skills/playbooks/references/ui/scene-3d.md; re-ground the plan against them before editing
## Lessons
- A number in a playbook should say how it was learned; a local probe beats a remembered figure
## Files touched
- plugin/skills/playbooks/references/ui/scene-3d.md
- CHANGELOG.md

---
id: T-1282
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-20T17:19:47Z
updated: 2026-10-20T17:39:43Z
base: d07dc02e203033cc39394dce257ff3e322563e26
base_tree: c38f32fc15370ff00ddff0ebd5cb3b98ee853a7a
plan0_at: 2026-10-20T17:19:47Z
plan0_scope: []
verified: strong
---
# Release Foreman 1.2.42 and push (CI fixes T-1281, macOS T-1249, note cuts T-1274/T-1275, fm output measured right T-1276)
## Raw request
> Release Foreman 1.2.42 and push (CI fixes T-1281, macOS T-1249, note cuts T-1274/T-1275, fm output measured right T-1276)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] 1.2.42 on origin/main — verify with `git fetch -q origin && test "$(git log origin/main -1 --format=%s)" = 'Foreman 1.2.42'`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm release 1.2.42 --push
## Resume here
## Docs impact
none: the release updated the version files and CHANGELOG's heading
## Verification evidence
- (ac 1) `git fetch -q origin && test "$(git log origin/main -1 --format=%s)" = 'Foreman 1.2.42'` → exit 0 · (no output) [ran] [tree 682f2b24bb4e] (2026-10-20T17:37:38Z)
- (step 1) `git fetch -q origin && test "$(git log origin/main -1 --format=%s)" = 'Foreman 1.2.42'` → exit 0 · (no output) [ran] [tree 682f2b24bb4e] (2026-10-20T17:37:38Z)
- (audit intent) `fm release ran the full gates and release-check; origin/main's head is the release commit` → 1.2.42 carries the CI fix for the context-tax replay, the macOS fixes and the note cuts; releases are standing-approved [tree 682f2b24bb4e] (2026-10-20T17:37:38Z)
- (audit self) `fm release ran the full gates and release-check; origin/main's head is the release commit` → no findings [tree 682f2b24bb4e] (2026-10-20T17:37:38Z)
- `git fetch -q origin && test "$(git log origin/main -1 --format=%s)" = 'Foreman 1.2.42'` → exit 0 · (no output) [ran] [tree 682f2b24bb4e] (2026-10-20T17:38:41Z)
- (audit intent) `fm release ran the full gates and release-check; origin/main's head is the release commit` → 1.2.42 carries the CI fix for the context-tax replay, the macOS fixes and the note cuts; releases are standing-approved [tree 682f2b24bb4e] (2026-10-20T17:38:41Z)
- (audit adversary) `fm release ran the full gates and release-check; origin/main's head is the release commit` → the guard eval prompts in the release only re-embed the rules text (T-1279's sync); their guard cases and expected refusals are unchanged, and the release gates ran the guard corpus [tree 682f2b24bb4e] (2026-10-20T17:38:41Z)
- (audit self) `fm release ran the full gates and release-check; origin/main's head is the release commit` → no findings [tree 682f2b24bb4e] (2026-10-20T17:38:41Z)
## Log
- 2026-10-20T17:19:47Z created
- 2026-10-20T17:19:47Z focused
- 2026-10-20T17:20:02Z user approved publish in Claude Code's permission prompt
- 2026-10-20T17:20:02Z undo point at this yes for publish: HEAD d07dc02e2030
- 2026-10-20T17:23:52Z publish grant used by fm release --push
- 2026-10-20T17:27:12Z paused: focus moved to T-1279
- 2026-10-20T17:37:36Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-20T17:37:36Z focused
- 2026-10-20T17:39:43Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1250 [CLEAN S, done, 1 steps] Release 1.2.40 and push: benchmark reruns, long-session cost cuts, CI annotations
- decision 2026-10-20: The recursive brainstorm loop is dry after round 1: a two-lens probe past the 368 earlier ideas gave 51 titles, 2 of real value after grounding (rep…
- T-0783 [PERFORMANCE M, done, 3 steps] Big Bash outputs reach the model as head, tail and failure lines, with the full text in a file (opt-in) — lesson: measure a lossy c…
- decision 2026-10-20: [cites: research/brainstorm-20261020] Round 1 of the 2026-10-20 brainstorm builds T-1254 (cost per fully-correct session on the page), T-1255 (Claud…
- similar finished tasks took 1–3 steps
## Behaviour lock
none: a release changes no behaviour; fm release runs the full gates before its commit
## Files touched
- .claude-plugin/marketplace.json
- .github/workflows/pages.yml
- .github/workflows/test.yml
- CHANGELOG.md
- MASTER.md
- plugin/.claude-plugin/plugin.json
- plugin/evals/guard-force-push/prompt.md
- plugin/evals/guard-publish/prompt.md
- plugin/evals/intake-block/prompt.md
- plugin/evals/mid-task-capture/prompt.md
- plugin/evals/one-liner/prompt.md
- plugin/lib/fmcode.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmsetup.py
- plugin/rules/foreman.md
- plugin/tests/test_code_worker.py
- plugin/tests/test_docs.py
- plugin/tests/test_setup.py
- plugin/tests/test_workflows.py

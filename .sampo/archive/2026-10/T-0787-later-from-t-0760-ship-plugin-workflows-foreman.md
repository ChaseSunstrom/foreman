---
id: T-0787
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/workflows/review.js, plugin/workflows/ideas.js, plugin/tests/test_workflows.py, CHANGELOG.md, MASTER.md, README.md]
depends_on: []
source: followup
created: 2026-10-14T15:55:20Z
updated: 2026-10-16T12:09:29Z
revisit: 2026-10-28
base: c23cbe2a47515ef5c391f94c91e815c12e6163c2
base_tree: 03f4af7efbf82a71ca7571c926240cfac670b956
plan0_at: 2026-10-16T12:06:34Z
plan0_scope: [plugin/workflows/review.js, plugin/workflows/ideas.js, plugin/tests/test_workflows.py, CHANGELOG.md, MASTER.md, README.md]
verified: strong
---
# Later from T-0760: Ship plugin workflows (/foreman:<name>) for review fan-out and audits (
## Raw request
> Later from T-0760: Ship plugin workflows (/foreman:<name>) for review fan-out and audits (6 ideas; brainstorm-20261014 cluster named-workflows: useful only when the user types it; revisit after the cockpit)
## Interpretation
Claude Code plugins can ship saved workflows (a workflows/ folder at the plugin root, each file starting with a pure-literal export const meta, run as /foreman:<meta.name>). Ship the two fan-outs Foreman does by hand most: /foreman:review [range|branch|T-id] (scope the diff, one reviewer per audit lens, two skeptics try to refute each finding, return the confirmed ones with the fm task finding lines to record them) and /foreman:ideas "request" (lens agents that read the code, so ideas come back grounded with file references, deduped, a completeness critic, one more round for the gaps).
## Assumptions (confidence)
## Acceptance criteria
- [x] plugin/workflows/review.js and ideas.js each start with a pure-literal meta whose name is the file name, every phase() title is in meta.phases, they parse as ES modules, and use no Date.now, Math.random or argless new Date() — verify with `python3 plugin/tests/run.py test_workflows`
## Non-goals
## Approach (options → choice → why)
Options: (a) plugin/workflows/review.js and ideas.js, checked by a python test (meta literal, name = file name, phase titles match phase() calls, no Date.now/Math.random/new Date(), node --check as a module); (b) skills whose text tells Claude to call the Workflow tool (prompt-driven, less deterministic); (c) a /foreman:lanes build+review workflow (rejected for now: a fix round can't reach the builder's worktree from a workflow, merges stay in the main thread). Choice: (a); reviewers use agentType foreman:fm-reviewer (read-only), the scope step a general-purpose agent that writes the diff to a mktemp folder.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test (test_workflows.py) over plugin/workflows/*.js
2. [x] review.js and ideas.js; README/MASTER lines
## Resume here
## Docs impact
README.md, MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_workflows` → ✗ exit 1 · Ran 3 tests in 0.2s (1 classes, 16 at a time; slowest: Workflows 0s) / FAILED (1 classes) [ran] [tree 026da5628592] (2026-10-16T12:06:45Z)
- (step 2) `python3 plugin/tests/run.py test_workflows` → exit 0 · Ran 3 tests in 0.2s (1 classes, 16 at a time; slowest: Workflows 0s) / OK [ran] [tree 2396dd86e4f4] (2026-10-16T12:07:51Z)
- (ac 1) `python3 plugin/tests/run.py test_workflows` → exit 0 · Ran 3 tests in 0.5s (1 classes, 16 at a time; slowest: Workflows 0s) / OK [ran] [tree ebccce9d0e40] (2026-10-16T12:08:21Z)
- (audit intent) `self: confirmed with the Claude Code docs (claude-code-guide) that plugins ship workflows from workflows/ as /<plugin>:<name>; both scripts pass the loader checks and node --check as the runner wraps them; not executed here because the Workflow tool needs the user's explicit opt-in, which typing /foreman:review gives` → the two fan-outs run by hand most (review, grounded brainstorm) become one command each [tree ebccce9d0e40] (2026-10-16T12:08:21Z)
- (audit adversary) `self: confirmed with the Claude Code docs (claude-code-guide) that plugins ship workflows from workflows/ as /<plugin>:<name>; both scripts pass the loader checks and node --check as the runner wraps them; not executed here because the Workflow tool needs the user's explicit opt-in, which typing /foreman:review gives` → diff and repo text are declared data in every prompt; reviewers and skeptics are read-only fm-reviewer agents; the scope agent is told not to change files [tree ebccce9d0e40] (2026-10-16T12:08:21Z)
- (audit edge) `self: confirmed with the Claude Code docs (claude-code-guide) that plugins ship workflows from workflows/ as /<plugin>:<name>; both scripts pass the loader checks and node --check as the runner wraps them; not executed here because the Workflow tool needs the user's explicit opt-in, which typing /foreman:review gives` → an empty target falls back to the last commit; no changes returns early; a dead agent's null is filtered [tree ebccce9d0e40] (2026-10-16T12:08:21Z)
- (audit operator) `self: confirmed with the Claude Code docs (claude-code-guide) that plugins ship workflows from workflows/ as /<plugin>:<name>; both scripts pass the loader checks and node --check as the runner wraps them; not executed here because the Workflow tool needs the user's explicit opt-in, which typing /foreman:review gives` → findings sorted by severity with record lines; ideas ranked by value per effort with an intake block [tree ebccce9d0e40] (2026-10-16T12:08:21Z)
- (audit maintainer) `self: confirmed with the Claude Code docs (claude-code-guide) that plugins ship workflows from workflows/ as /<plugin>:<name>; both scripts pass the loader checks and node --check as the runner wraps them; not executed here because the Workflow tool needs the user's explicit opt-in, which typing /foreman:review gives` → one test guards both files' structure; lens texts live in each script [tree ebccce9d0e40] (2026-10-16T12:08:21Z)
## Log
- 2026-10-14T15:55:20Z created
- 2026-10-14T19:45:47Z deferred: a 'later' brainstorm cluster: it waits on the evidence its title names (real use, an incident, a Claude Code event), not on ideas; the 2026-10-14 loop stopped dry (revisit 2026-10-28)
- 2026-10-16T11:47:19Z set status=captured
- 2026-10-16T11:47:19Z steer: re-queued by the deferred triage (T-1168): not built, nothing blocks it
- 2026-10-16T12:06:32Z set type=FEATURE, tier=M
- 2026-10-16T12:06:33Z set scope=['plugin/workflows/review.js', 'plugin/workflows/ideas.js', 'plugin/tests/test_workflows.py', 'CHANGELOG.md', 'MASTER.md', 'README.md']
- 2026-10-16T12:06:34Z focused
- 2026-10-16T12:09:28Z done
- 2026-10-16T12:09:29Z committed a036c4fa (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0780 [FEATURE S, done, 2 steps] Audit findings reach the host's review UI: fm audit prep asks for ReportFindings fields and tells the main thread to report them — less…
- T-0786 [FEATURE M, done, 3 steps] fm page: the queue (and optionally a brainstorm catalogue) as one self-contained HTML page for a claude.ai Artifact, with Build/Veto pi…
- T-0688 [FEATURE L, done, 7 steps] Milestone: Intelligence — Judgment, taste and decisions — lesson: Judgment improves where it's recorded: doors and precedent as rules a…
- decision 2026-10-14: Round 2 slate: 437 ideas in 29 clusters grounded → 3 build (compact spill cap T-0824, closed-pipe verb sweep T-0825, verb-usage evidence attached to…
## Preflight
Changed in scope since this was planned (2026-10-14): CHANGELOG.md, MASTER.md, README.md; re-ground the plan against them before editing
## Lessons
- plugin workflows load from the plugin's workflows/ folder; their body runs as an async function, so syntax-check it wrapped, not as a module
## Plan gaps
- failed first: step 1 Failing test (test_workflows.py) over plugin/workflows/*.js
## Files touched
- plugin/tests/test_workflows.py
- plugin/workflows/review.js
- plugin/workflows/ideas.js
- README.md
- MASTER.md
- CHANGELOG.md

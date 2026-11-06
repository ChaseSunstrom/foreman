---
id: T-0173
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-03T09:18:08Z
updated: 2026-10-03T09:20:24Z
base: 9feed9271f6a145356598947158245b89f9218d3
base_tree: 1ea38275e838795b155260c0f1c400a88e1461c9
verified: strong
---
# Rules name the audit checklist by a path that exists
## Raw request
> Rules name the audit checklist by a path that exists
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm tidy finds no dead path in the rules — verify with `! fm tidy | grep -q dead_path`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] point the rule at ~/.claude/foreman/plugin/skills/intake/references/audit.md
## Resume here
## Docs impact
## Verification evidence
- (step 1) `! fm tidy | grep -q dead_path` → ✗ exit 1 · (no output) [ran] [tree 1ea38275e838] (2026-10-03T09:18:20Z)
- (step 1) `! fm tidy | grep -q dead_path` → exit 0 · (no output) [ran] [tree 27e87dd8b51f] (2026-10-03T09:18:23Z)
- (ac 1) `! fm tidy | grep -q dead_path` → exit 0 · (no output) [ran] [tree e943a4921ef3] (2026-10-03T09:20:19Z)
- (audit self) `self: the token now resolves (~ path), tidy reports no dead path, evals re-synced, 594 tests pass` → no findings [tree e943a4921ef3] (2026-10-03T09:20:19Z)
- (audit adversary) `self: the token now resolves (~ path), tidy reports no dead path, evals re-synced, 594 tests pass` → the guard evals only re-embed the rules text; the one changed string is a doc path, no guard rule or expected verdict changed (git diff shows the same one-line change in each) [tree e943a4921ef3] (2026-10-03T09:20:23Z)
- (audit self) `self: the token now resolves (~ path), tidy reports no dead path, evals re-synced, 594 tests pass` → no findings [tree e943a4921ef3] (2026-10-03T09:20:23Z)
## Log
- 2026-10-03T09:18:08Z created
- 2026-10-03T09:18:08Z focused
- 2026-10-03T09:19:46Z scope: plugin/evals/*/prompt.md embed the rules (sync_evals.py), so they change with it
- 2026-10-03T09:20:24Z done
- 2026-10-03T09:20:24Z committed 40c40e0 (6 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-20260926-slate: drive no-progress watchdog: exists (fmhooks _progressed + DRIVE_MAX 50) · eval rules drift test: exists (test_docs.test_eval_cases_em…
- T-0169 [FIX S, done, 3 steps] Guard: a secret-sounding file name under the scratchpad or /tmp isn't a credential; its real path still is checked — lesson: A name-based h…
- research t0018-r9-adversary-maintainer: HIGH — ADVERSARY — `plugin/lib/fmcli.py:710-716` (via `_agent_report` at `plugin/lib/fmcli.py:607-610`) — unguarded non-regular f…
- research t0036-intent: MEDIUM** — `plugin/lib/fmplugins.py:388-398` (`content_hash`) — For a plugin that is not locally mirrored by its marketplace (a genuinely remote s…
## Lessons
- A rules diet must keep every path resolvable: dropping '/foreman:intake →' left a bare relative path the model and tidy can't find.
## Files touched
- plugin/rules/foreman.md
- plugin/evals/guard-force-push/prompt.md
- plugin/evals/guard-publish/prompt.md
- plugin/evals/intake-block/prompt.md
- plugin/evals/mid-task-capture/prompt.md
- plugin/evals/one-liner/prompt.md

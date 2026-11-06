---
id: T-1834
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmplaybooks.py, plugin/lib/fmcli.py, plugin/lib/fmtask.py, plugin/tests/test_playbook_use.py, plugin/lib/fmrecall.py]
depends_on: []
source: discovered
created: 2026-10-28T09:59:20Z
updated: 2026-10-28T10:29:55Z
base: 271f40eceaf56d0a8dd48ab6026b9233e1c5c946
base_tree: eb911fa7de5616873373a50240679323827e1cf3
plan0_at: 2026-10-28T09:59:46Z
plan0_scope: [plugin/lib/fmplaybooks.py, plugin/lib/fmcli.py, plugin/lib/fmtask.py, plugin/tests/test_playbook_use.py]
verified: strong
---
# Playbook use: followed books recorded at finish, unused and near-duplicate books named, duplicate drafts refused, the skill list capped (part of T-1803)
## Raw request
> Playbook use: followed books recorded at finish, unused and near-duplicate books named, duplicate drafts refused, the skill list capped (part of T-1803)
## Interpretation
'Actually used': the library learns which books earn their place. Never deletes a book itself: it names candidates.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm task finish records each playbook the task loaded (fm playbooks show or a Read of it, from events.jsonl in the task's window) with score()'s followed share as one event; fm playbooks coverage --unused lists books with no read, route hit or followed record in the window (drop candidates) and pairs whose shingle Jaccard ≥ 0.5 (merge candidates); fm playbooks draft ID names the nearest existing book and exits 1 when its overlap ≥ 0.5 unless --force; a test fails when plugin/skills has more than 20 SKILL.md or any playbook is a skill — verify with `python3 plugin/tests/run.py test_playbook_use`
## Non-goals
## Approach (options → choice → why)
Reuse reach()'s event scan and shown(); reuse _shingles for overlap (Jaccard on SHINGLE-grams). The finish hook point is wherever fm task finish closes a task (find it; keep it cheap: one events tail, score() only for books loaded). Near-duplicate pairs: compare only books sharing a stage or a title word, so 20k books aren't 200M pairs (cost at scale). Rejected: auto-deleting unused books (a user's library), an LLM judge for duplicates (paid per call).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red tests for the finish record, coverage --unused, draft dedupe and the cap
2. [x] Implement, green
## Resume here
<!-- auto -->
- 2026-10-28T10:14:00Z steps 2/2 done
- git: worktree-agent-ad04c5551e3669bae; 3 uncommitted: plugin/lib/fmplaybooks.py, plugin/lib/fmrecall.py, plugin/tests/test_playbook_use.py
- touched since last checkpoint: plugin/lib/fmcli.py, plugin/tests/test_playbook_use.py, plugin/lib/fmrecall.py, plugin/lib/fmplaybooks.py
## Docs impact
CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_playbook_use 2>&1 | tail -30` → ✗ exit 1 · Ran 6 tests in 6.5s (2 classes, 16 at a time; slowest: Use 6s, Cap 0s) / FAILED (1 classes) [ran] [tree 5d4ca69d221d] (2026-10-28T10:02:28Z)
- (ac 1) `python3 plugin/tests/run.py test_playbook_use 2>&1 | grep -v "^ File\|^ " | head -40` → exit 0 · Ran 6 tests in 5.9s (2 classes, 16 at a time; slowest: Use 6s, Cap 0s) / OK [ran] [tree aed6fc132706] (2026-10-28T10:04:07Z)
- (step 1) `python3 plugin/tests/run.py test_playbook_use 2>&1 | grep -v "^ File\|^ " | head -40` → exit 0 · Ran 6 tests in 5.9s (2 classes, 16 at a time; slowest: Use 6s, Cap 0s) / OK [ran] [tree aed6fc132706] (2026-10-28T10:04:07Z)
- (step 1) `python3 plugin/tests/run.py test_playbook_use` → exit 0 · Ran 6 tests in 5.9s (2 classes, 16 at a time; slowest: Use 6s, Cap 0s) / OK [ran] [tree f69b9992603c] (2026-10-28T10:04:35Z)
- (step 2) `python3 plugin/tests/run.py test_playbook_use` → exit 0 · Ran 6 tests in 5.9s (2 classes, 16 at a time; slowest: Use 6s, Cap 0s) / OK [ran] [tree f69b9992603c] (2026-10-28T10:04:45Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_memory test_playbook_check test_playbook_use test_recall test_trust` → exit 0 · Ran 206 tests in 25.9s (61 classes, 16 at a time; slowest: TaskLifecycle 26s, Recall 21s, AskMemory 15s) / OK [ran] [tree f69b9992603c] (2026-10-28T10:05:11Z)
- (ac 1) `python3 plugin/tests/run.py test_playbook_use 2>&1 | grep "^FAIL\|^ERROR\|^Ran\|OK"` → ✗ exit 1 · Ran 11 tests in 9.6s (2 classes, 16 at a time; slowest: Use 9s, Cap 0s) / FAILED (1 classes) [ran] [tree afe9be9b05e7] (2026-10-28T10:12:27Z)
- (step 2) `python3 plugin/tests/run.py test_playbook_use test_playbook_check test_playbook_draft test_playbook_machinery test_playbook_evals` → exit 0 · Ran 90 tests in 13.9s (20 classes, 16 at a time; slowest: Use 14s, FromThisRepo 9s, Load 9s) / OK [ran] [tree 5a467f99749a] (2026-10-28T10:16:22Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_playbook_check test_playbook_use` → exit 0 · Ran 167 tests in 49.4s (48 classes, 16 at a time; slowest: TaskLifecycle 49s, StateViews 25s, Use 24s) / OK [ran] [tree 5a467f99749a] (2026-10-28T10:17:13Z)
- (step 2) `python3 plugin/tests/run.py test_playbook_use test_playbook_check test_playbook_machinery` → exit 0 · Ran 72 tests in 6.8s (17 classes, 16 at a time; slowest: Use 7s, Load 4s, Snippets 2s) / OK [ran] [tree bba1b06e4be7] (2026-10-28T10:28:34Z)
- (ac 1) `python3 plugin/tests/run.py test_playbook_use` → exit 0 · Ran 11 tests in 6.8s (2 classes, 16 at a time; slowest: Use 7s, Cap 0s) / OK [ran] [tree fe2139b2cffa] (2026-10-28T10:28:54Z)
- (audit intent) `Lead review of the builder's diff (git diff HEAD...branch): df cache keyed by a stat signature, followed() returns early when nothing loaded, record_use isolated in its own try on the close path; nits fixed by the builder before merge` → a close records loaded books and the followed share; coverage --unused names drop and merge candidates; draft refuses a near-duplicate unless --force; the skill cap is a test [tree fe2139b2cffa] (2026-10-28T10:28:54Z)
- (audit edge) `Lead review of the builder's diff (git diff HEAD...branch): df cache keyed by a stat signature, followed() returns early when nothing loaded, record_use isolated in its own try on the close path; nits fixed by the builder before merge` → a task that loaded nothing records nothing; a recording failure never blocks a close [tree fe2139b2cffa] (2026-10-28T10:28:54Z)
- (audit maintainer) `Lead review of the builder's diff (git diff HEAD...branch): df cache keyed by a stat signature, followed() returns early when nothing loaded, record_use isolated in its own try on the close path; nits fixed by the builder before merge` → one shingle Jaccard helper shared by draft and coverage; the session_id filter was skipped on purpose (the task window already bounds it) [tree fe2139b2cffa] (2026-10-28T10:28:54Z)
- (audit intent) `Lead review of the builder's diff (git diff HEAD...branch): df cache keyed by a stat signature, followed() returns early when nothing loaded, record_use isolated in its own try on the close path; nits fixed by the builder before merge` → a close records loaded books and the followed share; coverage --unused names drop and merge candidates; draft refuses a near-duplicate unless --force; the skill cap is a test [tree fe2139b2cffa] (2026-10-28T10:29:29Z)
- (audit adversary) `Lead review of the builder's diff (git diff HEAD...branch): df cache keyed by a stat signature, followed() returns early when nothing loaded, record_use isolated in its own try on the close path; nits fixed by the builder before merge` → sha1 only keys a local cache by file stats (a collision just rebuilds or reuses a frequency table, no trust decision); draft --force is the only bypass and it is explicit [tree fe2139b2cffa] (2026-10-28T10:29:29Z)
- (audit edge) `Lead review of the builder's diff (git diff HEAD...branch): df cache keyed by a stat signature, followed() returns early when nothing loaded, record_use isolated in its own try on the close path; nits fixed by the builder before merge` → a task that loaded nothing records nothing; a recording failure never blocks a close [tree fe2139b2cffa] (2026-10-28T10:29:29Z)
- (audit maintainer) `Lead review of the builder's diff (git diff HEAD...branch): df cache keyed by a stat signature, followed() returns early when nothing loaded, record_use isolated in its own try on the close path; nits fixed by the builder before merge` → one shingle Jaccard helper shared by draft and coverage; the session_id filter was skipped on purpose (the task window already bounds it) [tree fe2139b2cffa] (2026-10-28T10:29:29Z)
## Log
- 2026-10-28T09:59:20Z created
- 2026-10-28T09:59:30Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1834.builder.md
- 2026-10-28T09:59:33Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1834.builder.md
- 2026-10-28T09:59:46Z focused
- 2026-10-28T10:03:28Z set scope=['plugin/lib/fmplaybooks.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmtask.py', 'plugin/tests/test_playbook_use.py', 'plugin/lib/fmrecall.py']
- 2026-10-28T10:03:28Z scope: fmrecall.share_lesson is the close's existing (p, b) hook, so fmcli.py stays untouched except the playbooks argparse lines
- 2026-10-28T10:28:16Z merged worktree-agent-ad04c5551e3669bae (3 file(s))
- 2026-10-28T10:28:19Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ad04c5551e3669bae
- 2026-10-28T10:28:22Z focused
- 2026-10-28T10:29:28Z scope: CHANGELOG.md takes the task's release line
- 2026-10-28T10:29:53Z done
- 2026-10-28T10:29:55Z committed 31f753e3 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1803 [FEATURE L, planned, 3 steps] Playbook library at 10,000+ scale, all routed, none listed (user: 'tens of thousands of sk
- T-1523 [FEATURE M, done, 5 steps] Round 3 (T-1520): Playbooks drafted from finished runs and history: a draft from a proved — lesson: A brief is already a distilled tran…
- research brainstorm-skills-20261022: The cause is mostly structural. Claude Code skills trigger on user words, while Foreman's hooks and rules already hand the model the…
- decision 2026-10-22: Skills fix: make the hooks name the skill and rewrite descriptions in task terms before adding skills; keep the 2,000-character listing cap and free…
- the similar finished task took 5 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Lessons
- Recording on the close path goes in its own try: telemetry must never fail a finish
## Files touched
- plugin/tests/test_playbook_use.py
- plugin/lib/fmplaybooks.py
- plugin/lib/fmrecall.py
- plugin/lib/fmcli.py
- CHANGELOG.md

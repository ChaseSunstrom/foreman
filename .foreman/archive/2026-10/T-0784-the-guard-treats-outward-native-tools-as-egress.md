---
id: T-0784
type: SECURITY
tier: S
status: done
priority: normal
scope: [plugin/hooks/hooks.json, plugin/lib/fmhooks.py, plugin/tests/test_hooks.py, MASTER.md]
depends_on: []
source: user
created: 2026-10-14T15:55:14Z
updated: 2026-10-14T16:56:40Z
inferred_deps: [T-0760]
inferred_why: T-0760: named in its request
group: guard coverage gaps
base: e4d735e05d6641e6315c88872908dc346c0d454e
base_tree: a09914b66ca9ef32d34747fb0d182b380e89bb82
verified: strong
---
# In a sensitive repo, Claude Code's outward tools (Artifact, PushNotification, SendMessage, RemoteTrigger, Claude Docs writes) are refused
## Raw request
> SECURITY: The guard treats outward native tools as egress
> CONTEXT: T-0760, cluster guard-native. PushNotification, Artifact publish, SendMessage, RemoteTrigger and Claude Docs writes send content off the machine; the guard (PreToolUse) doesn't see them (matcher Bash|Write|Edit|MultiEdit|NotebookEdit|Agent|Task). fm sensitive on marks repos where nothing should leave.
> DONE-WHEN: with fm sensitive on, those tools are refused with a reason naming fm sensitive off; off, they pass; hooks.json matcher covers them; guard tests pin both.
## Interpretation
fm sensitive on marks a repo whose content shouldn't leave the machine (manual permission mode, no second-session review, no lessons in AGENTS.md). Claude Code's newer tools publish content off the machine: Artifact (claude.ai pages), ArtifactData writes, PushNotification (phone), SendMessage (other sessions, cloud), RemoteTrigger (cloud routines), Claude Docs create/update/batch. The PreToolUse matcher never sees them. A second PreToolUse entry for those tools denies them in a sensitive project with the way out (fm sensitive off), and passes them otherwise.
## Assumptions (confidence)
## Acceptance criteria
- [x] with fm sensitive on, PreToolUse denies each outward tool naming fm sensitive off; off, it returns nothing — verify with `cd plugin/tests && python3 -m unittest test_hooks.PreToolUse.test_sensitive_repo_keeps_content_home`
## Non-goals
## Approach (options → choice → why)
Options: settings deny rules written per project (another settings writer); classify them as a new guard category needing fm ask (heavy for every push); deny only when sensitive. Chose deny-when-sensitive: the existing switch, no new prompts elsewhere.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing hook test
2. [x] Outward matcher entry and the sensitive check; MASTER.md
## Resume here
<!-- auto -->
- 2026-10-14T16:51:48Z step 1/2: Failing hook test
- git: foreman/build; 5 uncommitted: MASTER.md, plugin/hooks/hooks.json, plugin/lib/fmhooks.py, plugin/tests/test_docs.py, plugin/tests/test_hooks.py
- touched since last checkpoint: plugin/lib/fmhooks.py, plugin/tests/test_hooks.py, MASTER.md, plugin/hooks/hooks.json, plugin/tests/test_docs.py
## Docs impact
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_hooks.PreToolUse.test_sensitive_repo_keeps_content_home` → ✗ exit 1 · Ran 1 test in 3.459s / FAILED (failures=1) [ran] [tree f0d92433d7a3] (2026-10-14T16:42:47Z)
- (step 2) `python3 plugin/tests/run.py -k test_hooks -k test_doctor` → ✗ exit 1 · Ran 172 tests in 141.0s (30 classes, 16 at a time; slowest: Stop 140s, PreToolUse 86s, SessionStart 73s) / FAILED (3 classes) [ran] [tree 48b16ad2342c] (2026-10-14T16:45:50Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_hooks.PreToolUse.test_sensitive_repo_keeps_content_home` → exit 0 · Ran 1 test in 2.968s / OK [ran] [tree 48b16ad2342c] (2026-10-14T16:45:53Z)
- `cd plugin/tests && python3 -m unittest test_hooks.PreToolUse.test_sensitive_repo_keeps_content_home` → ✗ exit 1 · Ran 1 test in 2.358s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree 48b16ad2342c] (2026-10-14T16:46:00Z)
- `cd plugin/tests && python3 -m unittest test_hooks.PreToolUse.test_sensitive_repo_keeps_content_home` → exit 0 · Ran 1 test in 2.937s / OK [ran] [tree 48b16ad2342c] (2026-10-14T16:46:00Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_hooks.PreToolUse test_docs.PluginFiles` → exit 0 · Ran 28 tests in 24.631s / OK [ran] [tree e8e1290229c0] (2026-10-14T16:51:39Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_hooks.PreToolUse.test_sensitive_repo_keeps_content_home` → exit 0 · Ran 1 test in 2.263s / OK [ran] [tree 4328fe059698] (2026-10-14T16:56:38Z)
- (audit adversary) `self: diff read; a separate PreToolUse entry (fails closed like the guard) matches the outward tools; _outward_denial passes reads (artifact/doc reads, lists, guides, exports) and everything outside a sensitive project, and denies the rest with the way out (fm sensitive off)` → a tool name variant (ArtifactComments, any Claude Docs write) is covered by the matcher and the prefix check; a write passed off as a read needs an action name in the reads set, which the tools themselves define; a crash in the hook blocks (onFailure block), never leaks [tree 4328fe059698] (2026-10-14T16:56:38Z)
- (audit self) `self: diff read; a separate PreToolUse entry (fails closed like the guard) matches the outward tools; _outward_denial passes reads (artifact/doc reads, lists, guides, exports) and everything outside a sensitive project, and denies the rest with the way out (fm sensitive off)` → no findings [tree 4328fe059698] (2026-10-14T16:56:38Z)
## Log
- 2026-10-14T15:55:14Z created
- 2026-10-14T16:10:27Z planned from capture
- 2026-10-14T16:42:30Z focused
- 2026-10-14T16:43:28Z scope: MASTER.md gets one bullet for this round's Claude Code integrations (T-0775..T-0803), written once here
- 2026-10-14T16:51:05Z scope: test_docs.py pins hooks.json's shape (PreToolUse now has 3 handlers; the outward one fails closed like the guard)
- 2026-10-14T16:52:03Z paused: focus moved to T-0805
- 2026-10-14T16:53:16Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-14T16:53:16Z focused
- 2026-10-14T16:56:39Z done
- 2026-10-14T16:56:40Z committed 208d3ce (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0785 [FEATURE S, done, 2 steps] fm doctor names the Foreman features the installed Claude Code is too old for — lesson: a probe for a setting must look where Foreman w…
- research brainstorm-20261014: 609 ideas from 11 lenses x 4 rounds + 3 deepen rounds, in 30 capability clusters. Every idea is listed under its cluster. Marks: build (rou…
- research mission-20261009-091631.pack: can you spawn a bunch of brainstorm agents to super recursive brainstorm on capabilities/features for foreman itself? not just sim…
- decision 2026-09-26: T-0014 permission mode: fm serve passes --permission-mode only when given; otherwise Remote Control uses the user's own defaultMode (bypass here, se…
- likely tests for the scope: plugin/tests/test_hooks.py
## Lessons
- every new tool that sends content off the machine needs a line in the outward set; the hooks.json shape test makes that visible
## Plan gaps
- failed first: step 1 Failing hook test
- failed first: step 2 Outward matcher entry and the sensitive check; MASTER.md
## Files touched
- plugin/tests/test_hooks.py
- plugin/hooks/hooks.json
- plugin/lib/fmhooks.py
- MASTER.md
- plugin/tests/test_docs.py

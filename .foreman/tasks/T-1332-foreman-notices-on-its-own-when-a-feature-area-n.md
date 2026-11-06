---
id: T-1332
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-21T03:24:35Z
updated: 2026-10-21T04:19:41Z
base: 37956c3986879c4b7b7addf5cedd368adddccb23
base_tree: 6edabb73d8129ee59dcf2356a97d59055952c996
plan0_at: 2026-10-21T03:35:51Z
plan0_scope: []
verified: strong
---
# Foreman notices on its own when a feature area needs a brainstorm and an improvement round
## Raw request
> Foreman notices on its own when a feature area needs a brainstorm and an improvement round: the user's friction with it ('it just isn't doing anything', 'why can't I…', 'how come … isn't recognized') or repeated asks to improve it should start fm mission + fm ideas and a build round without being asked ('I shouldn't even need to say anything')
## Interpretation
The user had to ask for an improvement round on fm code three times ('super improve it', 'super recursive brainstorm', 'I shouldn't even need to say anything'). Before that came friction that should have started one on its own: 'how come fm isnt recognized as a command', 'why cant i launch fm code as a tui…', 'it just isn't doing anything'. The prompt hook already nudges toward a brainstorm when the user asks for one in open-ended words (c.is_open_ended, is_exhaustive); nothing reacts to friction itself.
## Assumptions (confidence)
## Acceptance criteria
- [x] a prompt with friction about a feature ('why can't I launch fm code like claude', 'it just isn't doing anything') gets a note to fix the cause and a queued RESEARCH task to brainstorm and improve that area, without being asked; a second one on the same area within 7 days makes it urgent; plain requests get neither — verify with `python3 plugin/tests/run.py test_hooks test_intake`
## Non-goals
## Approach (options → choice → why)
Options: A) a friction detector in the prompt hook (why can't I / how come / isn't working / doesn't do anything / just sits there / stuck / confusing), naming the area from the message's nouns and the files it maps to, with a note: fix the cause now, then fm mission + fm ideas on that area as its own task without asking (chosen: cheap, where the words arrive); B) count friction per area over a week and start a round past a threshold (slower; the user waits for a pattern); C) ask the user whether to brainstorm (rejected: they said they shouldn't have to say anything). With A, the round is captured as a RESEARCH task (source self) so it's queued and visible, not run silently mid-task; a second friction message on the same area within the week raises it to urgent.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: friction phrasings (and non-friction lookalikes) in the prompt hook
2. [x] c.is_friction + area naming; the note and the queued RESEARCH task (dedup per area, urgent on repeat)
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_hooks.Friction test_hooks.UserPromptSubmit.test_friction_starts_an_improvement_round` → ✗ exit 1 · Ran 3 tests in 1.7s (2 classes, 16 at a time; slowest: UserPromptSubmit 1s, Friction 0s) / FAILED (2 classes) [ran] [tree 3566d0cc3939] (2026-10-21T03:38:20Z)
- (step 2) `python3 plugin/tests/run.py test_hooks test_intake` → exit 0 · Ran 194 tests in 106.7s (23 classes, 16 at a time; slowest: Stop 106s, NoTaskGate 73s, PreToolUse 59s) / OK [ran] [tree bdfffbbe2896] (2026-10-21T03:41:19Z)
- (step 2) `python3 plugin/tests/run.py test_hooks test_intake` → exit 0 · Ran 194 tests in 114.0s (23 classes, 16 at a time; slowest: Stop 114s, NoTaskGate 83s, PreToolUse 67s) / OK [ran] [tree ae1d998244e5] (2026-10-21T03:47:04Z)
- (step 1) `python3 plugin/tests/run.py test_hooks test_intake` → exit 0 · Ran 194 tests in 95.2s (23 classes, 16 at a time; slowest: Stop 95s, NoTaskGate 68s, PreToolUse 54s) / OK [ran] [tree 5dacb5771e9a] (2026-10-21T04:12:40Z)
- (step 2) `python3 plugin/tests/run.py test_hooks test_intake` → exit 0 · Ran 194 tests in 97.8s (23 classes, 16 at a time; slowest: Stop 97s, NoTaskGate 69s, PreToolUse 56s) / OK [ran] [tree 5dacb5771e9a] (2026-10-21T04:14:18Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks test_intake` → exit 0 · Ran 194 tests in 101.6s (23 classes, 16 at a time; slowest: Stop 101s, NoTaskGate 70s, PreToolUse 58s) / OK [ran] [tree 5dacb5771e9a] (2026-10-21T04:16:15Z)
- (audit adversary) `self: read the merged hook block: friction only on untagged, non-override prompts; area 'this' → note only; else one RESEARCH task per open area (dedup), urgent on a second complaint within 7 days; capture failures are logged and never break the turn. Builder's tests: 9 complaints, 8 lookalikes, the anonymous case` → only the user's own prompt text reaches it (UserPromptSubmit); the worst case is an extra queued RESEARCH task, which needs no grant and runs nothing [tree 5dacb5771e9a] (2026-10-21T04:16:15Z)
- (audit edge) `self: read the merged hook block: friction only on untagged, non-override prompts; area 'this' → note only; else one RESEARCH task per open area (dedup), urgent on a second complaint within 7 days; capture failures are logged and never break the turn. Builder's tests: 9 complaints, 8 lookalikes, the anonymous case` → a timing-sensitive NoTaskGate test failed under load average ~40 from parallel lanes and passed alone 3/3 and in this run [tree 5dacb5771e9a] (2026-10-21T04:16:15Z)
- (audit intent) `self: read the merged hook block: friction only on untagged, non-override prompts; area 'this' → note only; else one RESEARCH task per open area (dedup), urgent on a second complaint within 7 days; capture failures are logged and never break the turn. Builder's tests: 9 complaints, 8 lookalikes, the anonymous case` → the user's own words this week (fm not recognized, fm code like claude) start a round; a complaint about their own app does not [tree 5dacb5771e9a] (2026-10-21T04:16:15Z)
## Log
- 2026-10-21T03:24:35Z created
- 2026-10-21T03:35:27Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1332.builder.md
- 2026-10-21T03:35:50Z focused
- 2026-10-21T04:09:25Z merged worktree-agent-a598cc18c5a73958d (4 file(s))
- 2026-10-21T04:11:01Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a598cc18c5a73958d
- 2026-10-21T04:11:02Z focused
- 2026-10-21T04:14:32Z scope: fmcli.py (capture_friction), fmcore.py (is_friction, friction_area), tests and CHANGELOG all serve the friction trigger
- 2026-10-21T04:19:39Z done
- 2026-10-21T04:19:41Z committed b1f36930 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research mission-20261020-222446: Request: super improve fm code, make it genuinely amazing: launch it as an app like claude (fm code with no request), able to manage AN…
- research mission-20261020-222446.pack: super improve fm code, make it genuinely amazing: launch it as an app like claude (fm code with no request), able to manage ANY CL…
- research mission-20261008-195201: Request: super improve foreman [stale: plugin/lib/fmagents.py, plugin/lib/fmbench.py, plugin/lib/fmbudget.py changed since it was writt…
- decision 2026-10-16: Recommendation: build the slate T-1042..T-1053 plus T-1028 widened (recorded in research brainstorm-20261016-catalogue); the user then asked for eve…
## Lessons
- Friction is a signal to act on, not only to answer: a complaint about a feature should queue an improvement round on it without being asked
## Plan gaps
- failed first: step 1 Failing tests: friction phrasings (and non-friction lookalikes) in the prompt hook
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmcore.py
- plugin/lib/fmcli.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
- plugin/lib/fmcodetui.py
- plugin/tests/fixtures/golden/demo-00.0s.txt
- plugin/tests/fixtures/golden/demo-03.4s.txt
- plugin/tests/fixtures/golden/demo-09.1s.txt
- plugin/tests/fixtures/golden/demo-30.0s.txt
- plugin/tests/test_code_tui.py

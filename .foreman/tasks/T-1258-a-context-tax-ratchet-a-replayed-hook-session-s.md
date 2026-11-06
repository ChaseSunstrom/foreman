---
id: T-1258
type: PERFORMANCE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmhooks.py, plugin/tests/test_context_tax.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: user
created: 2026-10-20T14:01:16Z
updated: 2026-10-20T14:56:30Z
base: 361778cc70354e2b7eda5853b2d54e5b994641ac
base_tree: d07efacdb9ee58adb5f2929fc09c3679cf6311dc
plan0_at: 2026-10-20T14:50:24Z
plan0_scope: [plugin/lib/fmhooks.py, plugin/tests/test_context_tax.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# A context-tax ratchet: a replayed hook session's injected bytes per event stay under a bud
## Raw request
> PERF: A context-tax ratchet: a replayed hook session's injected bytes per event stay under a budget in the tests, and a one-line note already said this session isn't repeated
> CONTEXT: brainstorm 2026-10-20 (research brainstorm-20261020), T-1252; Claude Code 2.1.304 re-sends the skill list after each compaction
## Interpretation
Foreman's hooks shouldn't say the same thing twice while it's still in the context: a one-line PreToolUse note already given in this session since its last compaction is dropped (the stack-card pointer came once per task, so six times in this session). A test replays a scripted session and holds what each hook event injects under a byte budget, so the tax can't creep back.
## Assumptions (confidence)
## Acceptance criteria
- [x] a test replays a scripted hook session (start, prompts, edits, Bash runs, stop) and holds the bytes Foreman injects per event kind under a budget; a one-line note already given in the session isn't given again — verify with `python3 plugin/tests/run.py test_context_tax`
## Non-goals
## Approach (options → choice → why)
Options: (a) a per-session set of one-line notes said, cleared at compaction or /clear, filtering PreToolUse's notes before they're joined; (b) fix each repeating note at its source (the card pointer, the ambient line…), one by one; (c) a cap on bytes per call that cuts notes off. Choice: (a) plus the replay ratchet: it catches every repeating one-liner, present and future; multi-line notes (a card's whole Avoid section) keep their own once-rules; the budgets read the inject events the hooks already log (T-0499).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: test_context_tax.py replays the session and checks per-event budgets and a repeated note
2. [x] Say repeated one-line notes once per session in fmhooks, set the budgets from the measured sizes, docs
## Resume here
## Docs impact
MASTER PreToolUse paragraph and CHANGELOG
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_context_tax` → ✗ exit 1 · Ran 1 test in 3.131s / FAILED (failures=1) [ran] [tree 99fdbaa83835] (2026-10-20T14:50:40Z)
- (ac 1) `python3 plugin/tests/run.py test_context_tax` → exit 0 · Ran 1 tests in 1.8s (1 classes, 16 at a time; slowest: ContextTax 2s) / OK [ran] [tree 480da00bb01a] (2026-10-20T14:53:28Z)
- (step 1) `python3 plugin/tests/run.py test_context_tax test_edit_cards test_hooks` → exit 0 · Ran 209 tests in 36.7s (28 classes, 16 at a time; slowest: Stop 37s, NoTaskGate 21s, PreToolUse 21s) / OK [ran] [tree 480da00bb01a] (2026-10-20T14:53:28Z)
- (step 2) `python3 plugin/tests/run.py test_context_tax test_edit_cards test_hooks` → exit 0 · Ran 209 tests in 36.7s (28 classes, 16 at a time; slowest: Stop 37s, NoTaskGate 21s, PreToolUse 21s) / OK [ran] [tree 480da00bb01a] (2026-10-20T14:53:28Z)
- (audit intent) `self review; measured the replay before and after against HEAD in a worktree, and grouped this session's real notes by kind` → Foreman's own context tax now has a ratchet that fails the suite when a hook event injects more than its budget, and exact repeats are gone; the measurement shows where the rest is (recall notes, ambient test lines), captured for the next round [tree 480da00bb01a] (2026-10-20T14:53:28Z)
- (audit edge) `self review; measured the replay before and after against HEAD in a worktree, and grouped this session's real notes by kind` → multi-line notes (a whole Avoid section) keep their own once-rule; the said list is cleared at every SessionStart, so after a compaction a note comes back once; a note that differs by one word (a count, a file) is a new note; a failure to read or write the list keeps every note [tree 480da00bb01a] (2026-10-20T14:53:28Z)
- `python3 plugin/tests/run.py test_context_tax test_edit_cards test_hooks` → exit 0 · Ran 209 tests in 37.9s (28 classes, 16 at a time; slowest: Stop 38s, NoTaskGate 22s, PreToolUse 22s) / OK [ran] [tree 480da00bb01a] (2026-10-20T14:55:18Z)
- (audit intent) `self review; measured the replay before and after against HEAD in a worktree, and grouped this session's real notes by kind` → Foreman's own context tax now has a ratchet that fails the suite when a hook event injects more than its budget, and exact repeats are gone; the measurement shows where the rest is (recall notes, ambient test lines), captured for the next round [tree 480da00bb01a] (2026-10-20T14:55:18Z)
- (audit edge) `self review; measured the replay before and after against HEAD in a worktree, and grouped this session's real notes by kind` → multi-line notes (a whole Avoid section) keep their own once-rule; the said list is cleared at every SessionStart, so after a compaction a note comes back once; a note that differs by one word (a count, a file) is a new note; a failure to read or write the list keeps every note [tree 480da00bb01a] (2026-10-20T14:55:18Z)
- (audit adversary) `self review; measured the replay before and after against HEAD in a worktree, and grouped this session's real notes by kind` → sha1 here only tells notes apart, not a secret; the session id is checked against [\w-]{1,100} before it names a file, so a crafted id can't write outside sessions/; a guard refusal is a deny, not a note, so it's never dropped; a planted .said file can only silence Foreman's own advisory notes for that session [tree 480da00bb01a] (2026-10-20T14:55:18Z)
## Log
- 2026-10-20T14:01:16Z created
- 2026-10-20T14:18:06Z set scope=['plugin/lib/fmhooks.py', 'plugin/tests/test_context_tax.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-20T14:50:23Z focused
- 2026-10-20T14:56:29Z done
- 2026-10-20T14:56:30Z committed fd6a19a6 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-20261020: Run: `fm ideas` super mode, 9 lenses (user value, unspoken needs, delight, capability map, approaches, reliability,
- T-0702 [FEATURE M, dropped, 3 steps] Frontier 02 — Context firewall and cheap reader
- T-0783 [PERFORMANCE M, done, 3 steps] Big Bash outputs reach the model as head, tail and failure lines, with the full text in a file (opt-in) — lesson: measure a lossy c…
- decision 2026-10-20: Slate, round 1: T-1254 cost per fully-correct session on the Benchmarks page; T-1255 the Claude Code version in every bench result; T-1256 piped tes…
- the similar finished task took 3 steps
- likely tests for the scope: plugin/tests/test_hooks.py
## Measurements
Replayed session (test_context_tax: start, a prompt, 9 edits over 4 tasks, 2 test runs, a compaction, stop): PreToolUse bytes injected 1628 → 1538; the stack-card pointer 2 → 1 before the compaction; SessionStart 814, UserPromptSubmit 397 unchanged. In this session's transcript, exact repeats of one-line edit-time notes were 5.6 KB of 130 KB (4%), the most this rule can save there; the larger repeated cost, the full stack cards re-injected 113 times (72 KB), stopped with T-1193 on 2026-10-16.
## Lessons
- Measure a tax by kind before cutting it: the repeat rule saves 4%, while one kind (stack cards) had been 55% until an earlier fix; the ratchet is what keeps the next one from slipping in
## Plan gaps
- failed first: step 1 Failing test: test_context_tax.py replays the session and checks per-event budgets and a repeated n…
## Files touched
- plugin/tests/test_context_tax.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
- MASTER.md

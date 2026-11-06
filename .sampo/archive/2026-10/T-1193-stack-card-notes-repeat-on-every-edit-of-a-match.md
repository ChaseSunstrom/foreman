---
id: T-1193
type: PERFORMANCE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-16T13:28:34Z
updated: 2026-10-16T14:18:07Z
base: 22653d77aa21e6dc5d491537527618b6b9e56160
base_tree: 8929dc664b7e64f63ebdbd77ad3555ac721b2abc
plan0_at: 2026-10-16T13:57:52Z
plan0_scope: []
verified: ok
---
# Stack-card notes once per session, then a one-line pointer per task
## Raw request
> Stack-card notes repeat on every edit of a matching file (the changelogs card 28x = 18k chars in one session, python 24x): inject each card's 'what to avoid' once per session per card, then a one-line pointer (fm lib show NAME) at most
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a card's Avoid note is injected once per session; a later task in the same session gets one line naming the card and fm lib show NAME; a new session gets the full note again — verify with `python3 plugin/tests/run.py test_edit_cards`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test in test_edit_cards: second task, same session gets the one-line pointer; new session gets the full note
2. [x] Key the card marker by session as well as task in _card_note
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_edit_cards` → exit 0 · Ran 22 tests in 8.6s (6 classes, 16 at a time; slowest: ImportCards 9s, EditCards 6s, EditCardsReview 2s) / OK [ran] [tree f24bcac40c4a] (2026-10-16T13:59:43Z)
- (step 2) `python3 plugin/tests/run.py test_edit_cards test_hooks` → exit 0 · Ran 179 tests in 144.8s (26 classes, 16 at a time; slowest: Stop 144s, PreToolUse 91s, SessionStart 68s) / OK [ran] [tree d1fc36bfdaa6] (2026-10-16T14:14:23Z)
- (ac 1) `python3 plugin/tests/run.py test_edit_cards` → exit 0 · Ran 22 tests in 54.9s (6 classes, 16 at a time; slowest: ImportCards 54s, EditCards 42s, EditCardsReview 16s) / OK [ran] [tree d1fc36bfdaa6] (2026-10-16T14:15:36Z)
- (audit self) `self: reviewed the merged diff; the session key sits beside task keys under the same 50-key cap (an evicted session key only means one more full note); the pointer is marked per task so it repeats at most once per card per task; without a session_id nothing changes; the session id is only a dict key` → no findings [tree d1fc36bfdaa6] (2026-10-16T14:15:36Z)
## Log
- 2026-10-16T13:28:34Z created
- 2026-10-16T13:56:50Z planned from capture
- 2026-10-16T13:57:36Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1193.builder.md
- 2026-10-16T13:57:51Z focused
- 2026-10-16T14:11:38Z merged worktree-agent-a6b8d0a9d77e6afd8 (2 file(s))
- 2026-10-16T14:11:42Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a6b8d0a9d77e6afd8
- 2026-10-16T14:11:44Z focused
- 2026-10-16T14:14:38Z scope: CHANGELOG line
- 2026-10-16T14:18:06Z done
- 2026-10-16T14:18:07Z committed 147b866e (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0949 [FEATURE M, done, 4 steps] Enforce: the right stack card's pitfalls injected at edit time, and a compliance count — lesson: A ranking rule (framework before langu…
- T-0977 [FEATURE M, done, 2 steps] Skills get used without asking: a zero-token UserPromptSubmit note names the one Foreman s — lesson: A library nobody reads needs a poi…
- research T-1036-review: Verdict** — changes needed. Three correctness gaps in the injection path (displaced cards, wildcard deps, files outside the project). The rest is…
- decision 2026-10-15: Recommendation: build T-0969..T-0975 (edit-time test-first note, background affected tests, fm rule, tool-output injection flag, fm cost --forecast,…
## Measurements
Python card, 3 tasks editing a .py file in one session: before about 3 x 740 = 2,200 characters injected; after about 740 + 2 x 110 = 960 (57% less), and the saving grows with tasks per session. The motivating session injected the changelogs card 28 times (about 18k characters) and python 24 times; with this change each is about 740 + 27 x 110 = 3.7k (about 80% less). Figures from the note and pointer lengths, not a live session.
## Files touched
- plugin/tests/test_edit_cards.py
- plugin/lib/fmhooks.py
- CHANGELOG.md

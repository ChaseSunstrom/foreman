---
id: T-2688
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-11-02T22:44:27Z
updated: 2026-11-02T22:59:34Z
base: cdcd33398434e0b59287f2ae82147f7607208ca9
base_tree: 519b1bfc8a0e9e0b356a96226cf939dfa040c96e
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-02T22:56:00Z
plan0_scope: []
verified: strong
---
# each AskUserQuestion answer becomes a question_answered ledger row (default taken, another option, typed, or dismissed), so the user's refusals and overrides can be learned from
## Raw request
> Record each declined fm ask and each dismissed or overridden question as a ledger row, so the user's refusals can be learned from (M-13's need: the ledger has 55 approvals and no refusal)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] an answered AskUserQuestion logs question_answered with default, other and typed counts, and a failed (dismissed) one logs dismissed — verify with `python3 plugin/tests/run.py test_question_answers`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] _question_answer in fmhooks, called from PostToolUse and its failure
3. [x] CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_question_answers` → exit 0 · Ran 3 tests in 0.8s (1 classes, 16 at a time; slowest: QuestionAnswers 0s) / OK [ran] [tree 0c10e7039628] [world 2f1906870a] (2026-11-02T22:56:36Z)
- `python3 plugin/tests/run.py test_question_answers` → ✗ exit 1 · Ran 3 tests in 2.6s (1 classes, 16 at a time; slowest: QuestionAnswers 0s) / FAILED (1 classes: test_question_answers.QuestionAnswers) (start tree + this task's tests) [ran] [tree 0c10e7039628] [world 2f1906870a] (2026-11-02T22:56:41Z)
- `python3 plugin/tests/run.py test_question_answers` → exit 0 · Ran 3 tests in 0.9s (1 classes, 16 at a time; slowest: QuestionAnswers 0s) / OK [ran] [tree 0c10e7039628] [world 2f1906870a] (2026-11-02T22:56:41Z)
- (ac 1) `python3 plugin/tests/run.py test_question_answers` → exit 0 · reused: the same command passed on this tree and world at 2026-11-02T22:56:41Z [ran] [tree 0c10e7039628] [world 2f1906870a] (2026-11-02T22:57:58Z)
- (step 2) `python3 plugin/tests/run.py test_question_answers test_anergy test_hooks` → exit 0 · Ran 262 tests in 76.2s (33 classes, 16 at a time; slowest: Stop 76s, NoTaskGate 43s, PreToolUse 39s) / OK [ran] [tree 0c10e7039628] [world 2f1906870a] (2026-11-02T22:57:58Z)
- (step 3) `python3 plugin/tests/run.py test_question_answers test_anergy test_hooks` → exit 0 · Ran 262 tests in 76.2s (33 classes, 16 at a time; slowest: Stop 76s, NoTaskGate 43s, PreToolUse 39s) / OK [ran] [tree 0c10e7039628] [world 2f1906870a] (2026-11-02T22:57:58Z)
- (audit adversary) `read _question_answer: runs only for AskUserQuestion, inside a try so a malformed payload never breaks PostToolUse; answers read from tool_input (the dialog fills it) with tool_response as a fallback; a failure or an empty answer set counts as dismissed` → the row holds counts and headers cut to 12 plain characters, never answer text, so a typed secret never reaches the ledger [tree 0c10e7039628] (2026-11-02T22:57:58Z)
- (audit edge) `read _question_answer: runs only for AskUserQuestion, inside a try so a malformed payload never breaks PostToolUse; answers read from tool_input (the dialog fills it) with tool_response as a fallback; a failure or an empty answer set counts as dismissed` → a multiSelect answer joins labels and counts as typed (not split); an unanswered question in a partly answered call isn't counted in default/other/typed [tree 0c10e7039628] (2026-11-02T22:57:58Z)
- (audit self) `read _question_answer: runs only for AskUserQuestion, inside a try so a malformed payload never breaks PostToolUse; answers read from tool_input (the dialog fills it) with tool_response as a fallback; a failure or an empty answer set counts as dismissed` → no findings [tree 0c10e7039628] (2026-11-02T22:57:58Z)
## Log
- 2026-11-02T22:44:27Z created
- 2026-11-02T22:55:59Z planned from capture
- 2026-11-02T22:55:59Z focused
- 2026-11-02T22:56:00Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-02T22:56:35Z scope: fmhooks.py (_question_answer, called from PostToolUse and its failure), CHANGELOG.md
- 2026-11-02T22:59:31Z done
- 2026-11-02T22:59:34Z committed 7e93963b (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2076 [FEATURE M, done, 2 steps] Brainstorms learn from what they missed: asks no idea predicted feed a blind-spots lens, and each run leaves questions for the next — l…
- research T-1537-review: Verdict: changes needed.** The acceptance criteria are met. The three named features that were not built are the main gap, and the ledger can be …
- T-0688 [FEATURE L, done, 7 steps] Milestone: Intelligence — Judgment, taste and decisions — lesson: Judgment improves where it's recorded: doors and precedent as rules a…
- decision 2026-10-16: Foreman Code (T-1207) is built as fm code: Foreman's own loop where the harness runs the stations and models fill small JSON slots, over one stdlib …
## Why not caught
chat-ask declines were logged (approval_declined); questions asked through AskUserQuestion had no reader at all
## Files touched
- plugin/tests/test_question_answers.py
- plugin/lib/fmhooks.py
- CHANGELOG.md

---
id: T-1202
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T14:46:24Z
updated: 2026-10-16T14:48:35Z
base: 175c03cbe5e315a55e03affafe75cadc24886256
base_tree: e0c01f1f41f5c919686bba048bdd93a82db08626
plan0_at: 2026-10-16T14:46:24Z
plan0_scope: []
verified: strong
---
# The guard's over-budget note says the literal scan ran, not that the script ran unread
## Raw request
> The guard's over-budget note says the literal scan ran, not that the script ran unread
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a script over the parse budget gets the note that it was too long to parse in time and that a literal scan found nothing to refuse — verify with `python3 plugin/tests/run.py test_guard_exec_vectors`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Test asserts the new wording; change the note in fmhooks
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py -k test_the_hook_notes_and_logs_an_unread_script` → ✗ exit 1 · Ran 1 tests in 5.2s (1 classes, 16 at a time; slowest: ScriptHook 2s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree a981aad9e726] (2026-10-16T14:46:54Z)
- `python3 plugin/tests/run.py -k test_the_hook_notes_and_logs_an_unread_script` → exit 0 · Ran 1 tests in 3.3s (1 classes, 16 at a time; slowest: ScriptHook 3s) / OK [ran] [tree a981aad9e726] (2026-10-16T14:46:54Z)
- (step 1) `python3 plugin/tests/run.py test_guard_exec_vectors` → exit 0 · Ran 40 tests in 7.1s (6 classes, 16 at a time; slowest: ScriptCache 6s, ScriptHook 3s, Review 1s) / OK [ran] [tree a981aad9e726] (2026-10-16T14:47:08Z)
- (ac 1) `python3 plugin/tests/run.py test_guard_exec_vectors` → exit 0 · Ran 40 tests in 3.9s (6 classes, 16 at a time; slowest: ScriptCache 3s, ScriptHook 2s, Abbreviations 1s) / OK [ran] [tree a981aad9e726] (2026-10-16T14:47:13Z)
- (audit adversary) `self: wording only; the note now matches what the guard does past the budget (a literal scan over the script and the scripts it runs, decision 2026-10-16) and says the over-budget file may be one the script runs` → text only, no verdict changes; the note still only appears for an allowed command [tree a981aad9e726] (2026-10-16T14:47:13Z)
- (audit self) `self: wording only; the note now matches what the guard does past the budget (a literal scan over the script and the scripts it runs, decision 2026-10-16) and says the over-budget file may be one the script runs` → no findings [tree a981aad9e726] (2026-10-16T14:47:13Z)
## Log
- 2026-10-16T14:46:24Z created
- 2026-10-16T14:46:24Z focused
- 2026-10-16T14:48:34Z done
- 2026-10-16T14:48:35Z committed 9373e4b9 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-10-16: T-0275: a script over the guard's parse budget stays allowed after the literal scan, not refused
- T-0715 [SECURITY S, done, 2 steps] Guard: a shell or interpreter reading its script from a pipe is refused (echo 'rm -rf ~' | bash ran unread) — lesson: every way a shel…
- T-0939 [FEATURE M, done, 3 steps] Pane shows skill use: skills invoked, stack cards read, and this repo's suggested cards — lesson: A mechanical sed over JSX props must …
- T-0590 [SECURITY M, done, 2 steps] Guard: IFS review round 2 — eval/source/quoted IFS sets, # after a rewritten IFS, quoted spans, read across a newline — lesson: a text…
- similar finished tasks took 2–3 steps
## Files touched
- plugin/tests/test_guard_exec_vectors.py
- plugin/lib/fmhooks.py

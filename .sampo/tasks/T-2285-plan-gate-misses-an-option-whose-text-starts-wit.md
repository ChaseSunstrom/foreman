---
id: T-2285
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T06:32:31Z
updated: 2026-10-31T06:40:29Z
base: 541838aabccdfdc300ada21962a988b127c83b2c
base_tree: 7f38e23290674e966544afb7064cffc4da4841f8
plan0_at: 2026-10-31T06:32:34Z
plan0_scope: []
verified: strong
---
# Plan gate misses an option whose text starts with a flag or code (1) --bench …): count any non-space, non-ellipsis text after a marker
## Raw request
> Plan gate misses an option whose text starts with a flag or code (1) --bench …): count any non-space, non-ellipsis text after a marker
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] an Approach '1) --bench a 2) `fm x` b 3) c. Choice 1' counts 3 options; '1) … 2) … 3) …' still counts 0 — verify with `python3 plugin/tests/run.py test_core`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red assertion in test_core's option-format test, then the marker lookahead
## Resume here
<!-- auto -->
- 2026-10-31T06:36:52Z steps 1/1 done
- git: foreman/build; 2 uncommitted: plugin/lib/fmcore.py, plugin/tests/test_core.py
- touched since last checkpoint: plugin/tests/test_core.py, plugin/lib/fmcore.py
## Docs impact
none: the gate's wording is unchanged
## Verification evidence
- `cd plugin/tests && python3 -m unittest -q test_core` → ✗ exit 1 · Ran 93 tests in 13.714s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree 0933508bbd81] (2026-10-31T06:33:57Z)
- `cd plugin/tests && python3 -m unittest -q test_core` → exit 0 · Ran 93 tests in 14.392s / OK [ran] [tree 0933508bbd81] (2026-10-31T06:33:57Z)
- (step 1) `python3 plugin/tests/run.py test_core test_cli` → exit 0 · Ran 237 tests in 58.8s (65 classes, 16 at a time; slowest: TaskLifecycle 58s, StateViews 27s, CaptureAndIntake 26s) / OK [ran] [tree 0933508bbd81] (2026-10-31T06:34:56Z)
- (ac 1) `python3 plugin/tests/run.py test_core` → exit 0 · Ran 96 tests in 2.3s (23 classes, 16 at a time; slowest: BriefIndex 2s, WritesAndLocks 2s, WaitWhile 1s) / OK [ran] [tree a31ffacaa442] (2026-10-31T06:40:10Z)
- (audit intent) `self: the option-marker lookahead accepted only a word character, so an option starting with a flag, a backtick or a quote broke the 1-2-3 run; it now accepts any non-space, non-ellipsis text, and the hollow '1) …' still counts 0` → the plan gate stops refusing real briefs like T-2284's (test_core red-to-green) [tree a31ffacaa442] (2026-10-31T06:40:10Z)
- (audit edge) `self: the option-marker lookahead accepted only a word character, so an option starting with a flag, a backtick or a quote broke the 1-2-3 run; it now accepts any non-space, non-ellipsis text, and the hollow '1) …' still counts 0` → 'e.g.' can't make a run alone (a run needs 1,2,3 or a,b,c); the hint text pasted verbatim still fails [tree a31ffacaa442] (2026-10-31T06:40:10Z)
- (audit self) `self: the option-marker lookahead accepted only a word character, so an option starting with a flag, a backtick or a quote broke the 1-2-3 run; it now accepts any non-space, non-ellipsis text, and the hollow '1) …' still counts 0` → no findings [tree a31ffacaa442] (2026-10-31T06:40:10Z)
## Log
- 2026-10-31T06:32:31Z created
- 2026-10-31T06:32:33Z focused
- 2026-10-31T06:34:57Z scope: plugin/lib/fmcore.py (_NUM_RE, _LET_RE), plugin/tests/test_core.py
- 2026-10-31T06:36:52Z paused: focus moved to T-2283
- 2026-10-31T06:40:07Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-31T06:40:07Z focused
- 2026-10-31T06:40:27Z done
- 2026-10-31T06:40:29Z committed 9f67b04d (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1987 [FIX M, done, 3 steps] Ambient waits out fm ship's run, titles cut at a word, budget-limited loop rounds aren't dry — lesson: A loop's stop rule should count only…
- T-1992 [FIX M, done, 3 steps] Intake @path lines scope their item, titles keep a mid-sentence @path, the loop brief says budget-limited rounds aren't… — lesson: When a p…
- research brainstorm-fm-anthropic-catalogue: Source: research/brainstorm-20261021-120257 (fm ideas, 10 lenses, 4 rounds, 3 deepened, --seen every earlier ideas.md: 520 ne…
- decision 2026-10-09: Self-approve T-0691 (planning milestone, L) after the second-plan review: all six objections answered in the brief (independent replan triggers, def…
## Why not caught
T-2269's tests used word-led options only; the review listed formats but not code- or flag-led text
## Lessons
- A content gate must be tried on its own author's next brief: the first one written after it landed was refused
## Files touched
- plugin/tests/test_core.py
- plugin/lib/fmcore.py

---
id: T-1404
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-21T17:28:43Z
updated: 2026-10-21T19:53:53Z
base: 3383c3ec37d0d5429f12f7daed7a3a44d5054d28
base_tree: 43c4cc36952bf1c515911e465333f8254e74cd5c
plan0_at: 2026-10-21T19:44:00Z
plan0_scope: []
verified: strong
---
# fm code fails a slot whose prompt was truncated, naming it, instead of using a confused answer
## Raw request
> FIX: Prompt truncation: a reply whose prompt_tokens is far under the estimate fails the slot with 'truncated at N tokens' instead of a confused answer (S17, A24)
> CONTEXT: round 2 of the fm/fm code brainstorm (T-1382): research/brainstorm-fm-anthropic-catalogue.md, grounding with file:line in research/brainstorm-fm-anthropic-half-a.md (A*) and half-b.md (B*)
> DONE-WHEN: a stub reporting prompt_tokens under 70% of the estimate fails the slot with that cause
## Interpretation
Some OpenAI-compatible servers (llama.cpp, Ollama, vLLM with a small context) silently drop the start of a long prompt and answer anyway, so fm code acts on a reply that never saw its instructions. The reply's own usage says how many prompt tokens the server read; far fewer than were sent means truncation.
## Assumptions (confidence)
## Acceptance criteria
- [x] a stub model reporting prompt tokens under 70% of fm code's estimate fails the slot with 'truncated at N tokens'; a normal reply passes — verify with `python3 plugin/tests/run.py test_code_truncation`
## Non-goals
## Approach (options → choice → why)
Options: (A) compare reported prompt tokens with an estimate per slot call (chosen: no extra request, works for every API that reports usage); (B) ask the server its context size first (not every server exposes it); (C) cap prompts client-side (still doesn't detect a smaller server limit). Only for kind=api profiles, only above a floor so short prompts with tokenizer variance never trip it; the factor 0.7 is a ponytail knob.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests in plugin/tests/test_code_truncation.py with a stub API profile whose usage.in is far below the prompt's estimated size
2. [x] estimate a request's tokens (characters / 4, the same rough rule used elsewhere in fm, or a shared helper if one exists) in fmcode.slot for API profiles only (CLI profiles report cache reads differently); when usage.in < 0.7 × estimate and the estimate is over 2,000 tokens, raise CodeError 'the model's server truncated the prompt at N tokens (about M sent): use a model with a longer context or a smaller request'
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_code_truncation 2>&1 | tail -30` → ✗ exit 1 · Ran 5 tests in 14.9s (1 classes, 16 at a time; slowest: Truncation 13s) / FAILED (1 classes) [ran] [tree 95e9bad5f11a] (2026-10-21T19:45:50Z)
- (step 1) `python3 plugin/tests/run.py test_code_truncation` → ✗ exit 1 · Ran 5 tests in 27.0s (1 classes, 16 at a time; slowest: Truncation 26s) / FAILED (1 classes) [ran] [tree 95e9bad5f11a] (2026-10-21T19:46:21Z)
- (ac 1) `python3 plugin/tests/run.py test_code_truncation 2>&1 | tail -15` → exit 0 · Ran 5 tests in 18.7s (1 classes, 16 at a time; slowest: Truncation 18s) / OK [ran] [tree 8cdbf1eee740] (2026-10-21T19:47:06Z)
- (step 2) `python3 plugin/tests/run.py test_code_truncation` → exit 0 · Ran 5 tests in 10.7s (1 classes, 16 at a time; slowest: Truncation 10s) / OK [ran] [tree b159d4c4a50d] (2026-10-21T19:47:22Z)
- (step 1) `python3 plugin/tests/run.py test_code_truncation` → exit 0 · Ran 5 tests in 21.6s (1 classes, 16 at a time; slowest: Truncation 20s) / OK [ran] [tree 8e167b40eb67] (2026-10-21T19:52:51Z)
- (step 2) `python3 plugin/tests/run.py test_code_truncation` → exit 0 · Ran 5 tests in 20.1s (1 classes, 16 at a time; slowest: Truncation 19s) / OK [ran] [tree 8e167b40eb67] (2026-10-21T19:53:13Z)
- (ac 1) `python3 plugin/tests/run.py test_code_truncation` → exit 0 · Ran 5 tests in 18.0s (1 classes, 16 at a time; slowest: Truncation 17s) / OK [ran] [tree 8e167b40eb67] (2026-10-21T19:53:42Z)
- (audit intent) `self: read check_truncated and its two call sites (slot, Run.phase before any action runs); API profiles only, a 2,000-token floor, only an int usage above 0 counts; cutoff loosened to half (steer logged)` → a stub reporting 40 or 200 prompt tokens of ~3,400 sent fails the plan or step slot naming the truncation, and the step's edit never runs (test_code_truncation, OpenAI and Anthropic shapes) [tree 8e167b40eb67] (2026-10-21T19:53:42Z)
- (audit edge) `self: read check_truncated and its two call sites (slot, Run.phase before any action runs); API profiles only, a 2,000-token floor, only an int usage above 0 counts; cutoff loosened to half (steer logged)` → a full read, no usage and a short prompt pass; the estimate counts only message text (tool schemas left out), so it can miss truncation but not cause it; whitespace-heavy reads are covered by the half cutoff [tree 8e167b40eb67] (2026-10-21T19:53:42Z)
## Log
- 2026-10-21T17:28:43Z created
- 2026-10-21T19:43:44Z planned from capture
- 2026-10-21T19:43:46Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1404.builder.md
- 2026-10-21T19:44:00Z focused
- 2026-10-21T19:50:13Z scope: check also runs in Run.phase's act loop (same truncation, where long prompts live); lane builder
- 2026-10-21T19:51:49Z merged worktree-agent-ac6725268c2e81fae (3 file(s))
- 2026-10-21T19:51:55Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ac6725268c2e81fae
- 2026-10-21T19:52:16Z focused
- 2026-10-21T19:52:18Z steer: cutoff 0.5 instead of 0.7 — at 0.7 a whitespace-heavy file read (over ~5.7 characters a token) could stop a healthy run; truncation from a too-small context is drastic, so half still catches it
- 2026-10-21T19:53:44Z affected tests waived: T-1408's tests are its own task's; test_code_truncation, test_code and test_code_worker ran in the builder's affected check
- 2026-10-21T19:53:48Z done
- 2026-10-21T19:53:53Z committed 087d10d2 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1210 [FEATURE L, dropped, 4 steps] fm code round 1: stdlib model client and the harness-run loop, proved end to end on a fake model server
- research brainstorm-fm-anthropic-catalogue: Source: research/brainstorm-20261021-120257 (fm ideas, 10 lenses, 4 rounds, 3 deepened, --seen every earlier ideas.md: 520 ne…
- T-1207 [FEATURE L, blocked, 3 steps] Foreman Code: fm code runs Foreman's loop itself on any model or CLI
- decision 2026-10-16: Foreman Code (T-1207) is built as fm code: Foreman's own loop where the harness runs the stations and models fill small JSON slots, over one stdlib …
## Why not caught
none: new check
## Lessons
- A heuristic that stops a run should fire only well past the estimate's error band; pick the cutoff from the worst honest case, not the typical one
## Plan gaps
- failed first: step 1 failing tests in plugin/tests/test_code_truncation.py with a stub API profile whose usage.in is far…
## Files touched
- plugin/tests/test_code.py
- plugin/tests/test_code_truncation.py
- plugin/lib/fmcode.py
- CHANGELOG.md

---
id: T-2859
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: [T-2847]
source: self
created: 2026-11-04T00:27:17Z
updated: 2026-11-04T01:39:30Z
base: 40d9fc8fbc36774c37fa1e07f98bba0124219dd3
base_tree: 5a91b55a21d6948f68ed8750d9c7ca7888126b59
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-04T01:33:51Z
plan0_scope: []
verified: strong
---
# Under a standing core yes or trust, a core block's message never tells Claude to ask the…
## Raw request
> FIX: under a standing core yes or trust, a core block's message never tells Claude to ask the user (no 'fm ask ... then ask the user one yes/no question'); it names the route the yes covers (the Edit or Write tool, a plain path, fm edit < draft) — the user's 2026-11-03 'stop asking me for stuff' came after this message led to an fm ask prompt; after T-2847 (both edit fmguard.py messages)
## Interpretation
Reading 1 (chosen): when the standing core yes or trust is on and a core block is only about the form of a write (shell text the guard can't read, a heredoc, a whole-tree write), the change itself is covered when made as plain file edits. So the message names that route and does not tell Claude to ask the user (the 2026-11-03 steer 'stop asking me for stuff' followed exactly this message). A block the yes truly doesn't cover (the guard file under a standing yes alone, Claude Code settings, state) keeps its ask. Reading 2 (ruled out): let the standing yes cover non-path forms; the guard can't read where they write, so that would open the guard file and state to unreadable shell text.
## Assumptions (confidence)
## Acceptance criteria
- [x] under a standing core yes or trust, a form-only core block's message names the Edit/Write route and never says to ask the user; an uncovered target keeps the ask — verify with `python3 plugin/tests/run.py test_guard`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test on g.message for both cases, then the branch in _message
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard test_safety test_hooks` → exit 0 · Ran 608 tests in 59.2s (133 classes, 16 at a time; slowest: Stop 59s, NoTaskGate 37s, PreToolUse 31s) / OK [ran] [tree 971d90a71e9b] [world 2f1906870a] (2026-11-04T01:38:51Z)
- `python3 plugin/tests/run.py test_guard.Core` → ✗ exit 1 · Ran 10 tests in 1.7s (1 classes, 16 at a time; slowest: Core 0s) / FAILED (1 classes: test_guard.Core) (start tree + this task's tests) [ran] [tree 971d90a71e9b] [world 2f1906870a] (2026-11-04T01:38:54Z)
- `python3 plugin/tests/run.py test_guard.Core` → exit 0 · Ran 10 tests in 0.5s (1 classes, 16 at a time; slowest: Core 0s) / OK [ran] [tree 971d90a71e9b] [world 2f1906870a] (2026-11-04T01:38:54Z)
- (ac 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 329 tests in 10.2s (96 classes, 16 at a time; slowest: Mutation 10s, GuardAgainstBash 6s, Latency 5s) / OK [ran] [tree 971d90a71e9b] [world 2f1906870a] (2026-11-04T01:39:05Z)
- (audit adversary) `self-review: the new branch fires only for core, only under trust or a standing core yes, and only when the detail is not a plain path (a heredoc, an unreadable target, a whole-tree write): the yes covers the same change as plain file edits, so the message names that route instead of an ask; a plain path the yes doesn't cover (the guard under a standing yes alone, settings, state) still asks; the block itself is unchanged` → message text only; check() decides the block exactly as before, so no write the guard refused is now allowed; an uncovered target keeps the user's ask (tested) [tree 971d90a71e9b] (2026-11-04T01:39:05Z)
- (audit edge) `self-review: the new branch fires only for core, only under trust or a standing core yes, and only when the detail is not a plain path (a heredoc, an unreadable target, a whole-tree write): the yes covers the same change as plain file edits, so the message names that route instead of an ask; a plain path the yes doesn't cover (the guard under a standing yes alone, settings, state) still asks; the block itself is unchanged` → a context without trusted or standing (test_hooks' SimpleNamespace) reads as neither [tree 971d90a71e9b] (2026-11-04T01:39:05Z)
- (audit intent) `self-review: the new branch fires only for core, only under trust or a standing core yes, and only when the detail is not a plain path (a heredoc, an unreadable target, a whole-tree write): the yes covers the same change as plain file edits, so the message names that route instead of an ask; a plain path the yes doesn't cover (the guard under a standing yes alone, settings, state) still asks; the block itself is unchanged` → the 'stop asking me for stuff' steer followed this exact message leading to an fm ask prompt [tree 971d90a71e9b] (2026-11-04T01:39:05Z)
- (audit self) `self-review: the new branch fires only for core, only under trust or a standing core yes, and only when the detail is not a plain path (a heredoc, an unreadable target, a whole-tree write): the yes covers the same change as plain file edits, so the message names that route instead of an ask; a plain path the yes doesn't cover (the guard under a standing yes alone, settings, state) still asks; the block itself is unchanged` → no findings [tree 971d90a71e9b] (2026-11-04T01:39:05Z)
## Log
- 2026-11-04T00:27:17Z created
- 2026-11-04T00:27:21Z set depends_on=['T-2847']
- 2026-11-04T01:33:49Z set tier=S
- 2026-11-04T01:33:50Z planned: it has criteria and steps
- 2026-11-04T01:33:50Z focused
- 2026-11-04T01:33:51Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-04T01:39:29Z done
- 2026-11-04T01:39:30Z committed 5ca8ac73 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2746 [FEATURE M, done, 3 steps] sampo migrate: move ~/.claude/foreman and its siblings (foreman.draft, foreman.evolve, foreman.lanes) to ~/.claude/sampo once, leave sy…
- T-2742 [FEATURE L, planned, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias;…
- T-2857 [FEATURE S, done, 1 steps] **Work autonomously.** Don't ask the user for input, preferences, confirmation or…
- decision 2026-11-04: [revisited: No mid-run questions] [cites: user steer 2026-11-04T00:02Z: stop asking me for stuff, keep going] [check: fm outcomes --questions --none…
- similar finished tasks took 1–3 steps
## Why not caught
the block's message was written for the no-yes case; the standing yes (T-0119) and trust (T-0120) changed what is covered but not what the message said
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py

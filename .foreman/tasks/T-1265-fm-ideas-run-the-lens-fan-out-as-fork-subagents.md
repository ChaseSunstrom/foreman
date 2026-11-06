---
id: T-1265
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmideas.py, plugin/tests/test_ideas.py, plugin/tests/test_pass1.py, plugin/tests/test_ideation.py, plugin/tests/test_perf_cost.py, CHANGELOG.md, plugin/skills/brainstorm/SKILL.md]
depends_on: []
source: followup
created: 2026-10-20T14:01:28Z
updated: 2026-10-23T13:26:01Z
base: 2f33d6a4192401092e0160e858ed76cfbe7f6d95
base_tree: ed41e87f1571269be14c7fa3a2e3e045079dd4e2
plan0_at: 2026-10-23T13:21:34Z
plan0_scope: [plugin/lib/fmideas.py, plugin/tests/test_ideas.py, plugin/tests/test_pass1.py, plugin/tests/test_ideation.py, CHANGELOG.md, plugin/skills/brainstorm/SKILL.md]
verified: ok
---
# Fm ideas: run the lens fan-out as fork subagents of one cached pack instead of one claude
## Raw request
> fm ideas: run the lens fan-out as fork subagents of one cached pack instead of one claude -p per lens (brainstorm-20261020 C13)
## Interpretation
Each fm ideas lens is its own claude -p child that sends the whole pack again (about 18 cents a lens lately). The idea: fork subagents of one cached pack. Grounding: a fork needs a parent session with the Agent tool, while lens children are tool-less on purpose (no tools, no MCP, no user settings); and today's children start together with the pack and the lens in one user message, so none can reuse another's cache (a cache hit needs the shared part to end at a cached boundary). The goal - one cached pack, N small tails - is reachable without forks.
## Assumptions (confidence)
## Acceptance criteria
- [x] every lens child gets the same system file (prompt + pack) and only its lens on stdin; the first child runs alone until it ends or the warm time passes; the run prints and keeps the cache tokens read and written — verify with `python3 plugin/tests/run.py test_ideas test_pass1 test_ideation`
## Non-goals
## Approach (options → choice → why)
Complete version: the shared part where Claude Code caches it, a first child that writes the cache before the rest read it, the cache tokens reported per run and kept in the manifest, the tool-less isolation unchanged. Options: (a) fork subagents from a parent with the Agent tool - gives the children tools and a parent to trust, skip; (b) the pack in the system prompt (--append-system-prompt-file, so no argv size limit), the lens alone as the message, the first child alone until it ends or WARM s pass - chosen; (c) the Messages API directly with cache_control - a second client beside claude -p, skip. The paid before/after measurement is one small run (2 lenses on haiku) after the change.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: the cached system file, the warm start, the cache report
2. [x] child_cmd with a system file, lens_prompt, run_children warm and cache, _run_round and the report; skill note; CHANGELOG
3. [x] one real 2-lens haiku run: cache read vs written
## Resume here
## Docs impact
plugin/skills/brainstorm/SKILL.md (the pack is the children's shared, cached system text; the run reports cache tokens), CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_ideas test_pass1 test_ideation` → ✗ exit 1 · Ran 33 tests in 6.1s (14 classes, 16 at a time; slowest: Ideas 6s, BoardIdeas 1s, KeepRates 1s) / FAILED (3 classes) [ran] [tree e16f44287269] (2026-10-23T13:21:51Z)
- (step 1) `python3 plugin/tests/run.py test_ideas test_pass1 test_ideation` → exit 0 · Ran 33 tests in 8.3s (14 classes, 16 at a time; slowest: Ideas 8s, BoardIdeas 1s, KeepRates 1s) / OK [ran] [tree 89649e21f45e] (2026-10-23T13:25:11Z)
- (step 2) `python3 plugin/tests/run.py test_ideas test_pass1 test_ideation test_perf_cost test_audit_run test_research test_research_rigor` → exit 0 · Ran 81 tests in 9.3s (32 classes, 16 at a time; slowest: Ideas 9s, AuditRun 8s, StepCompact 4s) / OK [ran] [tree 89649e21f45e] (2026-10-23T13:25:21Z)
- (step 3) `fm ideas --pack README-9k.md --lens reliability --lens simplicity --model haiku` → prompt cache: 9510 tokens read, 9337 written (the second lens read the first's whole system text); spend: writer 0.0036, reader 0.0029 USD [tree 89649e21f45e] (2026-10-23T13:25:21Z)
- (ac 1) `python3 plugin/tests/run.py test_ideas test_pass1 test_ideation` → exit 0 · Ran 33 tests in 8.3s (14 classes, 16 at a time; slowest: Ideas 8s, BoardIdeas 1s, KeepRates 1s) / OK [ran] [tree 89649e21f45e] (2026-10-23T13:25:30Z)
- (ac 1) `python3 plugin/tests/run.py test_ideas test_pass1 test_ideation` → exit 0 · Ran 33 tests in 8.3s (14 classes, 16 at a time; slowest: Ideas 8s, BoardIdeas 1s, KeepRates 1s) / OK [ran] [tree 89649e21f45e] (2026-10-23T13:25:48Z)
- (audit intent) `self review in the main thread (subagents paused by the usage budget): children keep NO_TOOLS, no MCP, no user settings and the run cap; the system file is in a private temp dir removed after the round; the warm wait is bounded (10 s, or the first child's end) and the deadline still covers every child; the cache counts come from claude -p's own json and are shown only when nonzero; a real 2-lens haiku run read 9,510 cache tokens against 9,337 written` → N lenses pay for the pack about once (one write, N-1 reads) instead of N times, measured, with the children as isolated as before [tree 89649e21f45e] (2026-10-23T13:25:48Z)
- (audit edge) `self review in the main thread (subagents paused by the usage budget): children keep NO_TOOLS, no MCP, no user settings and the run cap; the system file is in a private temp dir removed after the round; the warm wait is bounded (10 s, or the first child's end) and the deadline still covers every child; the cache counts come from claude -p's own json and are shown only when nonzero; a real 2-lens haiku run read 9,510 cache tokens against 9,337 written` → one lens (no wait), a first child that fails fast (the rest start at once), a child that hangs (10 s then the rest), a later round with its own pack (its own file, its own warm), a stub or old claude without usage (no cache line) [tree 89649e21f45e] (2026-10-23T13:25:48Z)
- (audit adversary) `self review in the main thread (subagents paused by the usage budget): children keep NO_TOOLS, no MCP, no user settings and the run cap; the system file is in a private temp dir removed after the round; the warm wait is bounded (10 s, or the first child's end) and the deadline still covers every child; the cache counts come from claude -p's own json and are shown only when nonzero; a real 2-lens haiku run read 9,510 cache tokens against 9,337 written` → the pack moves from the message to the system text, which is the same text the children treated as instructions before (the brainstorm prompt); pack content was data in both places and is redacted and capped as before; the file is 0700-private and gone after the round [tree 89649e21f45e] (2026-10-23T13:25:48Z)
## Log
- 2026-10-20T14:01:28Z created
- 2026-10-23T13:19:12Z set tier=M, scope=['plugin/lib/fmideas.py', 'plugin/tests/test_ideas.py', 'plugin/tests/test_pass1.py', 'plugin/tests/test_ideation.py', 'CHANGELOG.md', 'plugin/skills/brainstorm/SKILL.md']
- 2026-10-23T13:21:33Z focused
- 2026-10-23T13:22:19Z set scope=['plugin/lib/fmideas.py', 'plugin/tests/test_ideas.py', 'plugin/tests/test_pass1.py', 'plugin/tests/test_ideation.py', 'plugin/tests/test_perf_cost.py', 'CHANGELOG.md', 'plugin/skills/brainstorm/SKILL.md']
- 2026-10-23T13:25:59Z done
- 2026-10-23T13:26:01Z committed 969048e6 (7 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-20261020: Run: `fm ideas` super mode, 9 lenses (user value, unspoken needs, delight, capability map, approaches, reliability,
- T-0688 [FEATURE L, done, 7 steps] Milestone: Intelligence — Judgment, taste and decisions — lesson: Judgment improves where it's recorded: doors and precedent as rules a…
- research mission-20261016-050811: Request: forever loop round 2: improve past everything shipped (the user: 'keep super improving it, recursively; make it THE plugin; I …
- decision 2026-10-16: Foreman Code (T-1207) is built as fm code: Foreman's own loop where the harness runs the stations and models fill small JSON slots, over one stdlib …
- similar past tasks were L: consider --tier L
- likely tests for the scope: plugin/tests/test_ideas.py
## Preflight
Changed in scope since this was planned (2026-10-20): CHANGELOG.md, plugin/lib/fmideas.py, plugin/skills/brainstorm/SKILL.md; re-ground the plan against them before editing
## Lessons
- A prompt cache hit needs the shared part to end at a cached boundary: put shared context in the system text and stagger the first request
## Plan gaps
- failed first: step 1 red tests: the cached system file, the warm start, the cache report
## Files touched
- plugin/tests/test_ideas.py
- plugin/tests/test_ideation.py
- plugin/tests/test_pass1.py
- CHANGELOG.md
- plugin/lib/fmideas.py
- plugin/tests/test_perf_cost.py
- plugin/skills/brainstorm/SKILL.md

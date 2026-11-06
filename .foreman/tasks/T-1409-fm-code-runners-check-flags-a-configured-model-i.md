---
id: T-1409
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-21T17:28:43Z
updated: 2026-10-21T21:32:42Z
base: 7aeb5b92607b0d2a4158b026acef5249772d6d3e
base_tree: d607544f362bd41acaacddd2278ca04934e83bff
plan0_at: 2026-10-21T20:20:09Z
plan0_scope: []
verified: strong
---
# fm code runners --check flags a configured model id the provider has retired and names its replacement
## Raw request
> FEATURE: fm code runners --check flags a configured model id that is on a dated retired list and names its successor (S22, B13)
> CONTEXT: round 2 of the fm/fm code brainstorm (T-1382): research/brainstorm-fm-anthropic-catalogue.md, grounding with file:line in research/brainstorm-fm-anthropic-half-a.md (A*) and half-b.md (B*)
> DONE-WHEN: a models.json fixture naming a retired id makes fm code runners --check --json report retired: true with the replacement
## Interpretation
A models.json profile can name a model the provider no longer serves; today that shows up as an opaque 404 mid-run. fm code runners --check already probes each runner; it should also say which configured model ids are retired and what replaces them, from a dated table with its sources.
## Assumptions (confidence)
## Acceptance criteria
- [x] a models.json fixture naming a retired id (claude-3-opus-20240229, gpt-4.5-preview) makes fm code runners --check --json report retired: true with the date and replacement, and the text list says so; an active id reports nothing — verify with `python3 plugin/tests/run.py test_retired_models`
## Non-goals
## Approach (options → choice → why)
Options: (A) a static dated table in fmmodels from the providers' deprecation pages, checked only under --check (chosen: no network call, honest about its date, and the CHANGELOG/research name the source); (B) query each provider's models endpoint (needs keys, slow, and lists don't say 'retired'); (C) parse the error at run time (too late: the run already failed). The table says its as-of date, so a stale table reads as stale rather than wrong. Future-dated deprecations are left out (ponytail: a 'retiring soon' warning is the upgrade).
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests in plugin/tests/test_retired_models.py with a FOREMAN_HOME models.json fixture
2. [x] fmmodels.RETIRED: a dated table {model id: (retired date, replacement, provider page)} from research T-1409-retired-models (Anthropic rows verified on the live page 2026-10-21; OpenAI and Gemini rows as the recon read them; only dates already past), with RETIRED_AS_OF; fmmodels.retired(model_id) also strips a provider prefix like openai/ or models/; fm code runners --check reports each configured profile's model (models.json and built-in CLOUD defaults) that is retired
## Resume here
## Docs impact
README fm code runners line; CHANGELOG line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_retired_models` → ✗ exit 1 · Ran 4 tests in 2.8s (2 classes, 16 at a time; slowest: RunnersCheck 2s, RetiredTable 0s) / FAILED (2 classes) [ran] [tree 5152d1712f89] (2026-10-21T20:22:18Z)
- (step 2) `python3 plugin/tests/run.py test_retired_models` → exit 0 · Ran 4 tests in 3.7s (2 classes, 16 at a time; slowest: RunnersCheck 3s, RetiredTable 0s) / OK [ran] [tree 370e80b5e47e] (2026-10-21T20:23:30Z)
- (step 1) `python3 plugin/tests/run.py test_retired_models test_models` → exit 0 · Ran 57 tests in 7.2s (8 classes, 16 at a time; slowest: Bench 7s, ExtractJson 1s, RunnersCheck 1s) / OK [ran] [tree 44850c6e72aa] (2026-10-21T21:32:17Z)
- (step 2) `python3 plugin/tests/run.py test_retired_models test_models` → exit 0 · Ran 57 tests in 7.7s (8 classes, 16 at a time; slowest: Bench 7s, RunnersCheck 2s, Models 1s) / OK [ran] [tree 44850c6e72aa] (2026-10-21T21:32:26Z)
- (ac 1) `python3 plugin/tests/run.py test_retired_models` → exit 0 · Ran 4 tests in 1.7s (2 classes, 16 at a time; slowest: RunnersCheck 1s, RetiredTable 0s) / OK [ran] [tree 44850c6e72aa] (2026-10-21T21:32:36Z)
- (audit intent) `self: read RETIRED, retired() and _runners — 61 ids from the research, only dates on or before 2026-10-21, no repeats; lookup ignores case, spaces and a provider prefix; --check only, no network; a test pins that no built-in cloud default is retired; the Anthropic rows were checked against the live deprecations page` → a models.json naming claude-3-opus-20240229 or openai/gpt-4.5-preview gets retired: true with date, replacement and source under --check --json, and a text line; an active id reports nothing (test_retired_models) [tree 44850c6e72aa] (2026-10-21T21:32:36Z)
- (audit edge) `self: read RETIRED, retired() and _runners — 61 ids from the research, only dates on or before 2026-10-21, no repeats; lookup ignores case, spaces and a provider prefix; --check only, no network; a test pins that no built-in cloud default is retired; the Anthropic rows were checked against the live deprecations page` → OpenAI and Gemini rows come from a summarised page read (medium-high confidence, named in research); aliases like gpt-4 and soon-retiring models aren't flagged (T-1433); a proxied model reusing a retired id is flagged (accepted) [tree 44850c6e72aa] (2026-10-21T21:32:36Z)
## Log
- 2026-10-21T17:28:43Z created
- 2026-10-21T20:19:47Z planned from capture
- 2026-10-21T20:19:50Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1409.builder.md
- 2026-10-21T20:20:08Z focused
- 2026-10-21T20:28:59Z merged worktree-agent-abe544bc755ec68af (3 file(s))
- 2026-10-21T20:29:07Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-abe544bc755ec68af
- 2026-10-21T20:46:52Z focused
- 2026-10-21T20:48:17Z paused: focus moved to T-1379
- 2026-10-21T21:32:09Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-21T21:32:09Z focused
- 2026-10-21T21:32:37Z affected tests waived: UI mod JS subagent-row test times out at 5 s under load (T-1427, blocked with diagnosis)
- 2026-10-21T21:32:39Z done
- 2026-10-21T21:32:42Z committed 48df981c (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1410 [FEATURE S, done, 2 steps] fm vetoes prints the command that retracts each veto, and that command removes exactly it — lesson: A record the user can create should…
- research brainstorm-fm-anthropic-half-b: Reading used.** I took all 250 bullets of rounds 1 to 4 in lenses 01, 02, 03, 08 and 09. Four titles occur twice (themes, ETA, g…
- research brainstorm-fm-anthropic-catalogue: Source: research/brainstorm-20261021-120257 (fm ideas, 10 lenses, 4 rounds, 3 deepened, --seen every earlier ideas.md: 520 ne…
- decision 2026-10-16: Foreman Code (T-1207) is built as fm code: Foreman's own loop where the harness runs the stations and models fill small JSON slots, over one stdlib …
## Why not caught
none: new check
## Lessons
- A dated table from provider pages must say its date in the output, so stale reads as stale rather than wrong
## Plan gaps
- failed first: step 1 failing tests in plugin/tests/test_retired_models.py with a FOREMAN_HOME models.json fixture
## Files touched
- plugin/tests/test_retired_models.py
- plugin/lib/fmmodels.py
- plugin/lib/fmcode.py
- README.md
- CHANGELOG.md
- mods/foreman-ui/tests/foreman-ui.test.tsx
- plugin/lib/fmbench.py
- plugin/lib/fmcli.py
- plugin/lib/fmcodetui.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmplugins.py
- plugin/skills/improve/SKILL.md
- plugin/tests/helpers.py
- plugin/tests/test_bench.py
- plugin/tests/test_code_hardening.py
- plugin/tests/test_code_tui.py
- plugin/tests/test_code_worker.py
- plugin/tests/test_doctor.py
- plugin/tests/test_runner_lint.py
- plugin/tests/test_supply_delta.py

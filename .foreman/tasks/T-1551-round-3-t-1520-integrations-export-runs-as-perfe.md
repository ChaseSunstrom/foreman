---
id: T-1551
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/lib/fmintegrations.py, plugin/tests/test_integrations.py, plugin/skills/status/SKILL.md, MASTER.md, plugin/lib/fmserve.py, site, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:43:52Z
updated: 2026-10-22T21:18:01Z
base: a46cdf368dd41e3ac0b70f77e327495896bab66c
base_tree: 007a4e7f207878e7d4830ed7b1b31048304a70f3
plan0_at: 2026-10-22T20:38:11Z
plan0_scope: [plugin/lib/fmcli.py, plugin/lib/fmserve.py, site, plugin/tests/test_integrations.py, CHANGELOG.md]
verified: strong
---
# Round 3 (T-1520): Integrations: export runs as Perfetto/OTLP traces, a glance protocol (on
## Raw request
> Round 3 (T-1520): Integrations: export runs as Perfetto/OTLP traces, a glance protocol (one JSON line, many shells), proof-gap diagnostics through an LSP stub, a desk card for e-paper or an old phone, and animated SVG charts for bench and stats (b024 b150 b116 b094 a096). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently.
## Interpretation
Round 3 (T-1520): Integrations: export runs as Perfetto/OTLP traces, a glance protocol (one JSON line, many shells), proof-gap diagnostics through an LSP stub, a desk card for e-paper or an old phone, and animated SVG charts for bench and stats (b024 b150 b116 b094 a096). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently. 
## Assumptions (confidence)
## Acceptance criteria
- [x] a run exports as valid Perfetto JSON; fm glance prints one JSON line; the LSP stub answers initialize and publishes a diagnostic — verify with `cd plugin/tests && python3 -m unittest test_integrations`
## Non-goals
## Approach (options → choice → why)
Options: vendor SDKs (dependencies); chosen: stdlib emitters: runs as Perfetto JSON and OTLP JSON traces, a glance protocol (one JSON line for shells and bars), proof-gap diagnostics through a tiny stdio LSP stub, a desk card page for e-paper or an old phone (fm serve route), and animated SVG charts for bench and stats.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] traces and glance
3. [x] LSP stub
4. [x] help, doctor, docs and CLI checks for the new verbs (the desk card and SVG charts are deferred to T-1615: they need a decision on an HTTP listener)
## Resume here
## Docs impact
~/.claude/foreman/CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_integrations.py` → ✗ exit 1 · Ran 10 tests in 1.7s (3 classes, 16 at a time; slowest: Trace 2s, Glance 1s, Lsp 0s) / FAILED (3 classes) [ran] [tree c4eef49d314e] (2026-10-22T20:43:32Z)
- (step 1) `python3 plugin/tests/run.py -p test_integrations.py` → exit 0 · Ran 10 tests in 1.8s (3 classes, 16 at a time; slowest: Trace 2s, Glance 1s, Lsp 0s) / OK [ran] [tree 943eb5d7bf24] (2026-10-22T20:47:18Z)
- (step 2) `python3 plugin/tests/run.py -p test_integrations.py -k Trace -k Glance` → exit 0 · Ran 7 tests in 1.8s (2 classes, 16 at a time; slowest: Trace 2s, Glance 0s) / OK [ran] [tree 943eb5d7bf24] (2026-10-22T20:47:21Z)
- (step 3) `python3 plugin/tests/run.py -p test_integrations.py -k Lsp` → exit 0 · Ran 3 tests in 0.3s (1 classes, 16 at a time; slowest: Lsp 0s) / OK [ran] [tree 943eb5d7bf24] (2026-10-22T20:47:21Z)
- (step 4) `python3 plugin/tests/run.py -p test_help.py -p test_doctor.py -p test_docs.py -p test_cli.py 2>&1 | tail -30` → exit 0 · Ran 186 tests in 29.6s (43 classes, 16 at a time; slowest: TaskLifecycle 30s, StateViews 10s, AuditPrep 10s) / OK [ran] [tree 943eb5d7bf24] (2026-10-22T20:47:53Z)
- (step 2) `python3 plugin/tests/run.py -p test_integrations.py -k Trace -k Glance` → exit 0 · Ran 7 tests in 1.7s (2 classes, 16 at a time; slowest: Trace 2s, Glance 0s) / OK [ran] [tree 6ae688207cf8] (2026-10-22T20:50:10Z)
- (step 3) `python3 plugin/tests/run.py -p test_integrations.py -k Lsp` → exit 0 · Ran 3 tests in 0.3s (1 classes, 16 at a time; slowest: Lsp 0s) / OK [ran] [tree 6ae688207cf8] (2026-10-22T20:50:11Z)
- (ac 1) `python3 plugin/tests/run.py test_integrations` → exit 0 · Ran 10 tests in 2.6s (3 classes, 16 at a time; slowest: Trace 2s, Glance 1s, Lsp 0s) / OK [ran] [tree 6ae688207cf8] (2026-10-22T20:50:52Z)
- (step 1) `python3 plugin/tests/run.py -p test_integrations.py` → ✗ exit 1 · Ran 14 tests in 62.0s (3 classes, 16 at a time; slowest: Lsp 62s, Trace 6s, Glance 4s) / FAILED (3 classes) [ran] [tree fe8c2e11c3ee] (2026-10-22T20:59:44Z)
- (step 1) `python3 plugin/tests/run.py -p test_integrations.py` → exit 0 · Ran 14 tests in 2.1s (3 classes, 16 at a time; slowest: Trace 2s, Glance 1s, Lsp 1s) / OK [ran] [tree bea6301bd4ce] (2026-10-22T21:05:08Z)
- (step 2) `python3 plugin/tests/run.py -p test_integrations.py -k Trace -k Glance` → exit 0 · Ran 9 tests in 2.0s (2 classes, 16 at a time; slowest: Trace 2s, Glance 1s) / OK [ran] [tree bea6301bd4ce] (2026-10-22T21:05:10Z)
- (step 3) `python3 plugin/tests/run.py -p test_integrations.py -k Lsp` → exit 0 · Ran 5 tests in 0.5s (1 classes, 16 at a time; slowest: Lsp 1s) / OK [ran] [tree bea6301bd4ce] (2026-10-22T21:05:11Z)
- (ac 1) `python3 plugin/tests/run.py test_integrations` → exit 0 · Ran 14 tests in 5.3s (3 classes, 16 at a time; slowest: Trace 5s, Glance 3s, Lsp 1s) / OK [ran] [tree bea6301bd4ce] (2026-10-22T21:05:17Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_integrations` → exit 0 · Ran 14 tests in 3.090s / OK [ran] [tree 16f971bf4af6] (2026-10-22T21:16:02Z)
- (step 4) `python3 plugin/tests/run.py test_help test_doctor test_docs test_cli test_code_worker` → exit 0 · Ran 290 tests in 72.6s (65 classes, 16 at a time; slowest: Worker 72s, TaskLifecycle 25s, StateViews 10s) / OK [ran] [tree 16f971bf4af6] (2026-10-22T21:17:15Z)
- (audit adversary) `fm-reviewer adversary pass (research/T-1551-review.md)` → fm lsp: lone surrogates, a 5000-digit Content-Length and 100k-space lines no longer crash or stall it (ASCII wire, bounded length, 2000-char match window), all tested; no socket imports; timeline output ASCII-only [tree 16f971bf4af6] (2026-10-22T21:17:24Z)
- (audit edge) `review edge lens` → task span uses min/max event times; glance prints class error on unreadable state; outside-project glance writes nothing (os.walk snapshot) [tree 16f971bf4af6] (2026-10-22T21:17:24Z)
- (audit operator) `fm timeline, glance, lsp via tests after the merge` → 14 integration tests and 290 help/doctor/docs/CLI/worker tests green; workers may run glance and print-only timeline (--out refused) [tree 16f971bf4af6] (2026-10-22T21:17:25Z)
- (audit maintainer) `review maintainer lens` → redaction test now fails if c.redact is removed (secret built at runtime, checked by removing it); wiring line restored; changelog added [tree 16f971bf4af6] (2026-10-22T21:17:25Z)
- (audit intent) `criterion: Perfetto JSON, one-line glance, LSP initialize + diagnostic; sensitive projects` → met; glance blanks the title in a sensitive project; desk card and SVG charts deferred to T-1615 [tree 16f971bf4af6] (2026-10-22T21:17:25Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_integrations` → exit 0 · Ran 14 tests in 3.059s / OK [ran] [tree 16f971bf4af6] (2026-10-22T21:17:34Z)
- (audit adversary) `one fm-reviewer five-lens pass; 7 findings fixed test-first by the builder; criterion green after the merge` → fm lsp survives surrogates, huge lengths and long lines; stdio only [tree 16f971bf4af6] (2026-10-22T21:17:34Z)
- (audit edge) `one fm-reviewer five-lens pass; 7 findings fixed test-first by the builder; criterion green after the merge` → event order, unreadable state, sensitive projects [tree 16f971bf4af6] (2026-10-22T21:17:34Z)
## Log
- 2026-10-22T17:43:52Z created
- 2026-10-22T18:06:28Z set scope=['plugin/lib/fmcli.py', 'plugin/lib/fmserve.py', 'site', 'plugin/tests/test_integrations.py', 'CHANGELOG.md']
- 2026-10-22T20:37:45Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1551.builder.md
- 2026-10-22T20:38:10Z focused
- 2026-10-22T20:45:51Z set scope=['plugin/lib/fmcli.py', 'plugin/lib/fmintegrations.py', 'plugin/tests/test_integrations.py', 'plugin/skills/status/SKILL.md', 'MASTER.md', 'plugin/lib/fmserve.py', 'site', 'CHANGELOG.md']
- 2026-10-22T21:02:45Z scope: widened to plugin/lib/fmintegrations.py (the three verbs' new module), plugin/skills/status/SKILL.md (Claude Code reach without a new skill) and MASTER.md (self-docs list every command and module)
- 2026-10-22T21:15:39Z merged worktree-agent-a39aca9847c6a08bc (6 file(s))
- 2026-10-22T21:15:42Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a39aca9847c6a08bc
- 2026-10-22T21:15:43Z focused
- 2026-10-22T21:15:59Z steer: step 4's evidence was the help/doctor/docs/CLI checks, not a desk card; the step now says so and the card and charts are T-1615
- 2026-10-22T21:18:01Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1534 [FEATURE M, active, 4 steps] Round 3 (T-1520): UI replay and determinism: render foreman-ui from recorded fixtures with
- T-1543 [FEATURE M, active, 4 steps] Round 3 (T-1520): Settings safety: a last-known-good config that boots if a new one misren
- T-1537 [FEATURE M, active, 4 steps] Round 3 (T-1520): Taste ledger: learn from what the user keeps and from 'not like that', a
- decision 2026-10-22: T-1520: the user asked for every brainstorm idea and Claude Code plugin parity; the 206 skipped ideas became 35 round-3 tasks (T-1522..T-1556) and r…
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_safety.py, plugin/tests/test_serve.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmintegrations.py, plugin/skills/status/SKILL.md, plugin/tests/test_integrations.py; re-ground the plan against them before editing
## Why not caught
the first tests sent only well-formed frames
## Lessons
- A stdio server must survive any bytes a client sends: write ASCII JSON, bound every number it parses, and cap regex work per line
## Plan gaps
- failed first: step 1 failing tests
## Files touched
- plugin/tests/test_integrations.py
- plugin/lib/fmintegrations.py
- plugin/lib/fmcli.py
- MASTER.md
- plugin/skills/status/SKILL.md
- CHANGELOG.md

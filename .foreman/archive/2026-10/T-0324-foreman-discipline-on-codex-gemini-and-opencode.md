---
id: T-0324
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-06T01:12:05Z
updated: 2026-10-06T02:40:43Z
base: 1a67e080abb1251656fa30f03de7d57be64df1ec
base_tree: 708f4a69e8b31263b5e1c39ab792aab4d0568996
verified: strong
---
# Foreman discipline on codex, gemini and opencode: fm hook --agent and fm agents install
## Raw request
> Foreman discipline on codex, gemini and opencode: fm hook --agent and fm agents install
## Interpretation
Foreman must not be Claude-only: the same guard, per-turn context and MCP state on Codex, Gemini CLI and opencode, installed by one command per agent.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm hook --agent codex|gemini|opencode refuses rm -rf ~ in that agent's format and injects Foreman's next action — verify with `python3 plugin/tests/run.py -k test_agents`
- [x] fm agents install X writes hooks, MCP and instructions idempotently and uninstall removes them — verify with `python3 plugin/tests/run.py -k test_agents`
## Non-goals
## Approach (options → choice → why)
Options: (A) port the plugin per agent; (B) one fm hook --agent X EVENT adapter that maps each agent's payload and tool names onto the existing handlers (seam: fmguard.check, fmhooks._guard_ctx) and answers in that agent's block/inject format, plus fm agents install X writing its hooks config, MCP entry (fm mcp) and an AGENTS.md/GEMINI.md block; opencode gets a small TS plugin calling fm hook. Choice: B — the rules stay in one place.
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests (red)
2. [x] payload/answer adapters
3. [x] installers + opencode plugin
4. [x] docs
## Resume here
<!-- auto -->
- 2026-10-06T02:23:22Z step 1/4: tests (red)
- git: foreman/build; 0 uncommitted
## Docs impact
README (Other agents), MASTER.md (fmagents, hook --agent, opencode plugin rows), CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_agents` → ✗ exit 1 · Ran 14 tests in 0.7s (5 classes, 16 at a time; slowest: Hook 1s, Install 0s, Session 0s) / FAILED (2 classes) [ran] [tree c1a7c43595fa] (2026-10-06T02:28:53Z)
- (step 2) `python3 plugin/tests/run.py -k test_agents` → exit 0 · Ran 14 tests in 1.3s (5 classes, 16 at a time; slowest: Hook 1s, Install 1s, Session 0s) / OK [ran] [tree b803f667c97a] (2026-10-06T02:32:54Z)
- (step 3) `python3 plugin/tests/run.py -k test_agents` → exit 0 · Ran 14 tests in 1.3s (5 classes, 16 at a time; slowest: Hook 1s, Install 1s, Session 0s) / OK [ran] [tree b803f667c97a] (2026-10-06T02:32:55Z)
- (step 4) `fm doctor` → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (27 pass, 3 warn, 0 fail) [ran] [tree fa572ec1fb24] (2026-10-06T02:36:06Z)
- (step 4) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (27 pass, 3 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 02:34 UTC; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 01:05 UTC; pytho [ran] [tree fa572ec1fb24] (2026-10-06T02:36:50Z)
- (ac 1) `python3 plugin/tests/run.py -k test_agents` → exit 0 · Ran 18 tests in 1.5s (6 classes, 16 at a time; slowest: Hook 1s, Install 1s, Session 0s) / OK [ran] [tree f63fad9bf8e5] (2026-10-06T02:40:43Z)
- (ac 2) `python3 plugin/tests/run.py -k test_agents` → exit 0 · Ran 18 tests in 1.5s (6 classes, 16 at a time; slowest: Hook 1s, Install 1s, Session 0s) / OK [ran] [tree f63fad9bf8e5] (2026-10-06T02:40:43Z)
- (audit intent) `one fm-reviewer pass over the diff (research T-0324-review): 6 findings, all fixed test-first and re-verified; full suite + fm check green` → both criteria met — guard refuses rm -rf ~ in codex/gemini/opencode format, Next: injected at session start, install/uninstall idempotent and restore the user's config; Gemini drive and fm ask grants stay Claude-only, documented and captured (T-0335, T-0337) [tree f63fad9bf8e5] (2026-10-06T02:40:43Z)
- (audit adversary) `one fm-reviewer pass over the diff (research T-0324-review): 6 findings, all fixed test-first and re-verified; full suite + fm check green` → adapter crash now refuses instead of exit 1 (fail-open on Codex/Gemini); unknown tool names with a command string judged as shell; guard gap bash -lc/zsh -ic fixed for Claude too; fm replay 0 newly allowed [tree f63fad9bf8e5] (2026-10-06T02:40:43Z)
- (audit edge) `one fm-reviewer pass over the diff (research T-0324-review): 6 findings, all fixed test-first and re-verified; full suite + fm check green` → unreadable patch judged as a write; JSONC config left alone with a message; user's own fm MCP entry and foreman.ts kept; symlinked dotfiles stay links; block removal never joins lines; non-ASCII kept [tree f63fad9bf8e5] (2026-10-06T02:40:43Z)
- (audit operator) `one fm-reviewer pass over the diff (research T-0324-review): 6 findings, all fixed test-first and re-verified; full suite + fm check green` → install into a throwaway HOME wrote hooks.json, config.toml and AGENTS.md; fm agents list shows wired; agent hook ~34 ms [tree f63fad9bf8e5] (2026-10-06T02:40:43Z)
- (audit maintainer) `one fm-reviewer pass over the diff (research T-0324-review): 6 findings, all fixed test-first and re-verified; full suite + fm check green` → one module (fmagents) wraps fmhooks.run unchanged; dispatcher gains --agent; opencode plugin ~50 lines in plugin/integrations [tree f63fad9bf8e5] (2026-10-06T02:40:43Z)
## Log
- 2026-10-06T01:12:05Z created
- 2026-10-06T02:23:22Z focused
- 2026-10-06T02:32:39Z steer: fmguard missed bash -lc/zsh -ic (option cluster holding c) — Codex's shell form; fixed inline in _shell_c since it blocks AC1
- 2026-10-06T02:40:43Z done
- 2026-10-06T02:40:43Z committed 60e6947 (11 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0318-agents: Answer.** All four agents have a hook that can block a tool before it runs, except opencode, where a plugin can do it. Each has a JSON-RPC, HTTP …
- research T-0324-hook-formats: 1. **Answer
- T-0318 [FEATURE L, done, 6 steps] FEATURE: beautiful modern animated desktop app wrapping Foreman — supports every feature, — lesson: A remote command over ssh gets no h…
- T-0323 [FEATURE L, done, 4 steps] fm session: agent-agnostic session supervisor (claude, codex, gemini, opencode) — lesson: A detached supervisor needs one writer per fi…
- similar finished tasks took 4–6 steps
- start here (files T-0318 touched): CHANGELOG.md, README.md
## Lessons
- Another agent's hook treats a crash (exit 1) as allow: an adapter in front of a fail-closed guard must catch its own errors and refuse, or it reopens the hole the guard closed.
## Files touched
- plugin/tests/test_agents.py
- plugin/lib/fmagents.py
- plugin/hooks/hook
- plugin/agents/opencode/foreman.ts
- plugin/lib/fmcli.py
- plugin/integrations/opencode/foreman.ts
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- plugin/tests/test_doctor.py
- CHANGELOG.md
- MASTER.md
- README.md

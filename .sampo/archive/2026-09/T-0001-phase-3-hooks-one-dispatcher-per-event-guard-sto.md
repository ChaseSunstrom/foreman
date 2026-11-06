---
id: T-0001
type: FEATURE
tier: L
status: done
priority: normal
scope: [plugin/hooks/**, plugin/lib/fmhooks.py, plugin/lib/fmguard.py, plugin/tests/**]
depends_on: []
source: user
created: 2026-09-26T05:02:11Z
updated: 2026-09-26T05:18:58Z
---
# Phase 3: hooks — one dispatcher per event, guard, stop gate + drive, fixtures, latency
## Raw request
> BUILD_PROMPT.md §3 Phase 3, §4.3, §4.7, PLAN.md §3 §5 §6 D22
## Interpretation
Build the hook layer: one dispatcher script (hooks/hook <Event>) registered once per event in hooks/hooks.json, with fmhooks.py handlers and fmguard.py (pure, fail-closed). Covers SessionStart, UserPromptSubmit, PreToolUse (guard + scope note), PostToolUse/Failure (async ledger + events), PreCompact (checkpoint), Stop (evidence gate + drive + terminal), TaskCompleted, SubagentStart/Stop, MessageDisplay badge, Notification, SessionEnd.
## Assumptions (confidence)
## Acceptance criteria
- [x] guard blocks every §5 category with an actionable message, authorization unblocks, state-direct is never authorizable, internal error fails closed — verify with `python3 -m unittest -v test_guard`
- [x] hook handlers meet output schemas and budgets (SessionStart ≤2000 chars, UserPromptSubmit ≤400, factual), fail open on corrupt state with a log line — verify with `python3 -m unittest -v test_hooks`
- [x] Stop: evidence gate blocks once per step and honours stop_hook_active; drive blocks while unblocked work remains and allows stop on question/approval/pause/empty queue/no progress — verify with `python3 -m unittest -v test_hooks.Stop`
- [x] p95 latency ≤150 ms for every hook on fixtures (guard ≤60 ms target) — verify with `python3 plugin/tests/bench_hooks.py`
- [x] plugin validates strictly and hooks fire in a real claude -p session — verify with `claude plugin validate --strict plugin && tests/e2e smoke`
## Non-goals
## Approach (options → choice → why)
Options: (a) one script per event; (b) one dispatcher script with an event arg, lazy imports. Choice: (b) — one entry point, fewer files, shared fail-open wrapper; guard lives in its own module so it can be protected-core and unit tested in isolation. Hooks are exec-form commands so paths need no quoting.
## Risks and rollback
Guard false positives or a guard bug blocking all Bash/Edit (fail-closed): table-driven tests first; kill-switch 'claude plugin disable foreman@foreman'. Stop-gate loops: once-per-step + stop_hook_active + no-progress detection. Rollback: git revert the phase commit; hooks go live only after /reload-plugins or a new session.
## Execution prompt
Goal: Foreman hook layer per BUILD_PROMPT §4.3/§4.7 and local/PLAN.md §3, §5, §6, D12-D15, D22. Context: repo ~/.claude/foreman (branch foreman/build), code in plugin/lib (fmcore.py, fmcli.py exist and are tested), tests in plugin/tests (unittest, helpers.ForemanTestCase gives an isolated FOREMAN_HOME + git repo and self.hook(event, payload)). Steps: 1) write plugin/tests/test_guard.py table-driven cases for categories rm-outside, git-destructive, credentials, pipe-shell, system, publish, state-direct, core (positive + negative + authorized), watch them fail, implement plugin/lib/fmguard.py as pure functions: check(tool_name, tool_input, ctx) -> Decision(category, detail) | None. 2) write plugin/tests/test_hooks.py per event (fixtures under plugin/tests/fixtures), implement plugin/lib/fmhooks.py + plugin/hooks/hook (python dispatcher, fail-open wrapper logging to state/logs/hooks.log, guard exceptions exit 2) + plugin/hooks/hooks.json (exec form, ${CLAUDE_PLUGIN_ROOT}). 3) plugin/tests/bench_hooks.py: 50 runs per fixture, print p50/p95, fail if p95 > 150 ms. 4) claude plugin validate --strict plugin; scratch repo + FOREMAN_HOME=scratch claude -p --plugin-dir plugin smoke. Constraints: stdlib only; hook text factual not imperative; budgets §2.8; never block PreCompact; Stop blocks once per step. Verify: python3 -m unittest discover -s plugin/tests -t plugin/tests; python3 plugin/tests/bench_hooks.py.
## Steps
1. [x] Guard tests (RED) then fmguard.py (GREEN)
2. [x] Hook handler tests (RED) then fmhooks.py, hooks/hook, hooks.json (GREEN)
3. [x] Latency benchmark on fixtures
4. [x] Strict validation + live claude -p smoke with --plugin-dir
5. [x] Commit phase 3
## Resume here
## Verification evidence
- (step 1) `python3 -m unittest test_guard (plugin/tests)` → Ran 21 tests OK (table-driven, all 8 categories + authorization + robustness) (2026-09-26T05:09:50Z)
- (step 2) `python3 -m unittest discover -s plugin/tests -t plugin/tests; claude plugin validate --strict plugin` → 121 tests OK; validation passed (2026-09-26T05:17:17Z)
- (step 3) `python3 plugin/tests/bench_hooks.py --runs 50` → all 15 fixtures p95 29-38 ms (budget 150; guard 35-36 ms), exit 0 (2026-09-26T05:18:35Z)
- (ac 4) `python3 plugin/tests/bench_hooks.py --runs 50` → p95 max 37.8 ms (PreCompact); guard 36.3 ms (2026-09-26T05:18:35Z)
- (step 4) `claude plugin validate --strict plugin; FOREMAN_HOME=scratch claude -p --model sonnet 'git push --force origin main' in scratch repo` → validation passed; live session: guard blocked git-destructive with authorize message; SessionStart/UserPromptSubmit/PreToolUse/Stop/SessionEnd all fired (events.jsonl) (2026-09-26T05:18:52Z)
- (ac 1) `python3 -m unittest test_guard test_hooks.PreToolUse` → 21 guard tests (8 categories, authorization, state-direct never authorizable) + PreToolUse fail-closed on malformed input: OK (2026-09-26T05:18:52Z)
- (ac 2) `python3 -m unittest test_hooks` → 39 tests OK: budgets 2000/400/200 chars, factual text regex, fail-open on corrupt meta.json logged to hooks.log (2026-09-26T05:18:52Z)
- (ac 3) `python3 -m unittest test_hooks.Stop` → 10 tests OK: once-per-step evidence block, stop_hook_active honoured, drive blocks/allows per question, approval, pause, off, idle, no-progress (2026-09-26T05:18:52Z)
- (ac 5) `claude plugin validate --strict plugin + live claude -p smoke` → Validation passed; guard block observed live (2026-09-26T05:18:52Z)
- (step 5) `git log --oneline -1` → cfddfa1 feat(hooks): one dispatcher per event, fail-closed guard, stop gate with drive mode (2026-09-26T05:18:58Z)
## Log
- 2026-09-26T05:02:11Z created
- 2026-09-26T05:02:11Z guard authorization added: core
- 2026-09-26T05:02:37Z focused
- 2026-09-26T05:18:58Z done
## Follow-ups captured

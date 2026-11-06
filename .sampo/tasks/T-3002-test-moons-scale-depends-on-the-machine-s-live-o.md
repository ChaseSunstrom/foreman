---
id: T-3002
type: FIX
tier: S
status: planned
priority: normal
scope: [plugin/tests/test_moons_scale.py]
depends_on: []
source: discovered
created: 2026-11-04T19:03:12Z
updated: 2026-11-06T08:52:37Z
base: 19cf45dc02be51d02cca75532c0a953687420bda
base_tree: f7e92771539040aa709b2972758be9d5f52b3845
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T08:44:26Z
plan0_scope: [plugin/tests/test_moons_scale.py]
builder_returned: 2026-11-06T08:46:02Z
---
# test_moons_scale fakes its embedder, so it passes the same with Ollama down or local models off
## Raw request
> test_moons_scale depends on the machine's live Ollama embedder: it passes with bge-m3 served and fails 5 classes with FOREMAN_NO_LOCAL_MODELS=1 or Ollama down (seen during the store move); its embedding path must be faked in the tests (as test_louhi_models' fake embedder does) so CI and a fresh box agree
## Interpretation
Already fixed upstream by T-3220 (98a29e7fc pinned the embedder in the moons tests); no code change left, both modes verified green.
## Assumptions (confidence)
## Acceptance criteria
- [ ] test_moons_scale passes with FOREMAN_NO_LOCAL_MODELS=1 and with no Ollama answering, as it does with bge-m3 served: every test that reaches an embedding uses a fake embedder (as test_louhi_models does) or the shingle path on purpose — verify with `FOREMAN_NO_LOCAL_MODELS=1 python3 plugin/tests/run.py test_moons_scale && python3 plugin/tests/run.py test_moons_scale`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red: the suite under FOREMAN_NO_LOCAL_MODELS=1 (7 classes fail today); fake the embedder in a shared setUp for the classes that embed
## Resume here
## Docs impact
## Verification evidence
- (step 1) `FOREMAN_NO_LOCAL_MODELS=1 python3 plugin/tests/run.py test_moons_scale` → ✗ exit 1 · Ran 76 tests in 4.3s (15 classes, 16 at a time; slowest: KeepGrow 4s, Yield 4s, Funnel 3s) / FAILED (7 classes: test_moons_scale.Yield, test_moons_scale.Funnel, test_moons_scale.FamilyLinks, test_moon [ran] [tree 6a413ae7f6aa] [world 2f1906870a] (2026-11-05T02:44:12Z)
- (step 1) `FOREMAN_NO_LOCAL_MODELS=1 python3 plugin/tests/run.py test_moons_scale` → exit 0 · Ran 114 tests in 4.9s (20 jobs, 16 at a time; slowest: KeepGrow 3s, Funnel 3s, Yield 2s) / OK [ran] [tree f7e927715390] [world 2f1906870a] (2026-11-06T08:45:46Z)
- (step 1) `FOREMAN_NO_LOCAL_MODELS=0 python3 plugin/tests/run.py test_moons_scale` → exit 0 · Ran 114 tests in 2.4s (20 jobs, 16 at a time; slowest: KeepGrow 2s, Funnel 2s, Yield 2s) / OK [ran] [tree f7e927715390] [world 2f1906870a] (2026-11-06T08:45:49Z)
## Log
- 2026-11-04T19:03:12Z created
- 2026-11-05T02:44:06Z planned from capture
- 2026-11-05T02:44:07Z set approved=True
- 2026-11-05T02:44:07Z set scope=['plugin/tests/test_moons_scale.py']
- 2026-11-05T02:44:12Z start point recorded late (no focus had kept one): its diff starts at 31cc0cc
- 2026-11-05T02:44:12Z blocked: after T-3047's lane merges (it changes test_moons_scale too); red recorded
- 2026-11-06T03:53:00Z unblocked
- 2026-11-06T08:44:25Z focused
- 2026-11-06T08:44:26Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T08:52:37Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a6ae90bc8b095f598
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2880 [FEATURE M, done, 3 steps] Local model runtime in Sampo's install: install.sh offers (opt-in) Ollama with pinned… — lesson: Discovery that probes a live server ne…
- T-3229 [FEATURE S, done, 2 steps] The test runner hides local models from every class unless the caller says otherwise, so a run here sees what CI sees — lesson: make th…
- T-3220 [FIX S, done, 2 steps] FIX: CI on main is red at fcf658d (tests) — lesson: a test that mocks a picker's fallback but not the picker itself passes only on boxes wi…
- decision 2026-11-04: Moon bulk generation runs on jarvis (qwen3.8-27b) now that the user supplied LLM_API_KEY; Haiku stays the fallback. llama-swap serves no embeddings …
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx
## Preflight
Changed in scope since this was planned (2026-11-04): plugin/tests/test_moons_scale.py; re-ground the plan against them before editing

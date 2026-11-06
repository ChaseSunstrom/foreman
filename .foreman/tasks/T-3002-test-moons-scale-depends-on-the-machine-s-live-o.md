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
updated: 2026-11-06T03:53:00Z
base: 31cc0cc9258f3477fbb535b4851f0cca78b15a64
---
# test_moons_scale fakes its embedder, so it passes the same with Ollama down or local models off
## Raw request
> test_moons_scale depends on the machine's live Ollama embedder: it passes with bge-m3 served and fails 5 classes with FOREMAN_NO_LOCAL_MODELS=1 or Ollama down (seen during the store move); its embedding path must be faked in the tests (as test_louhi_models' fake embedder does) so CI and a fresh box agree
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] test_moons_scale passes with FOREMAN_NO_LOCAL_MODELS=1 and with no Ollama answering, as it does with bge-m3 served: every test that reaches an embedding uses a fake embedder (as test_louhi_models does) or the shingle path on purpose — verify with `FOREMAN_NO_LOCAL_MODELS=1 python3 plugin/tests/run.py test_moons_scale && python3 plugin/tests/run.py test_moons_scale`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] red: the suite under FOREMAN_NO_LOCAL_MODELS=1 (7 classes fail today); fake the embedder in a shared setUp for the classes that embed  <- CURRENT
## Resume here
## Docs impact
## Verification evidence
- (step 1) `FOREMAN_NO_LOCAL_MODELS=1 python3 plugin/tests/run.py test_moons_scale` → ✗ exit 1 · Ran 76 tests in 4.3s (15 classes, 16 at a time; slowest: KeepGrow 4s, Yield 4s, Funnel 3s) / FAILED (7 classes: test_moons_scale.Yield, test_moons_scale.Funnel, test_moons_scale.FamilyLinks, test_moon [ran] [tree 6a413ae7f6aa] [world 2f1906870a] (2026-11-05T02:44:12Z)
## Log
- 2026-11-04T19:03:12Z created
- 2026-11-05T02:44:06Z planned from capture
- 2026-11-05T02:44:07Z set approved=True
- 2026-11-05T02:44:07Z set scope=['plugin/tests/test_moons_scale.py']
- 2026-11-05T02:44:12Z start point recorded late (no focus had kept one): its diff starts at 31cc0cc
- 2026-11-05T02:44:12Z blocked: after T-3047's lane merges (it changes test_moons_scale too); red recorded
- 2026-11-06T03:53:00Z unblocked
## Follow-ups captured

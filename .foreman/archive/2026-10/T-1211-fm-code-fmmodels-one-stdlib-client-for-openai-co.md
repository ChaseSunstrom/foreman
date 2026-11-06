---
id: T-1211
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T15:15:35Z
updated: 2026-10-16T16:03:40Z
base: a2a53ed77cdde2f71cd18974635949a660d707e1
base_tree: 9554fc8cecfa7deac683cd1acd24a63da267b9c2
plan0_at: 2026-10-16T15:16:04Z
plan0_scope: []
verified: strong
---
# fm code: fmmodels, one stdlib client for OpenAI-compatible and Anthropic endpoints with model profiles and local-server detection
## Raw request
> fm code: fmmodels, one stdlib client for OpenAI-compatible and Anthropic endpoints with model profiles and local-server detection
## Interpretation
The model layer of Foreman Code (T-1207, round 1 split from T-1210). plugin/lib/fmmodels.py, stdlib only (urllib.request, json, http.client): profiles from a user-editable $FOREMAN_HOME/models.json plus detection (ANTHROPIC_API_KEY, OPENAI_API_KEY, OPENROUTER_API_KEY, GROQ_API_KEY, GEMINI_API_KEY through Gemini's OpenAI-compatible endpoint; local servers probed with a 0.3 s timeout: Ollama :11434/v1, LM Studio :1234/v1, llama.cpp :8080/v1, vLLM :8000/v1, listing /models); resolve(name=None) picks the named profile, else models.json's default, else the first reachable local server, else the first keyed cloud one.
## Assumptions (confidence)
## Acceptance criteria
- [x] tests run complete() against in-process fake servers in both wire shapes (plain text, a native tool call, a 429 then success, a 500 three times raising ModelError without the key in the message), the Anthropic adapter's message and tool conversion, extract_json on fenced, bare, nested and broken input, profile resolution order with a models.json and with env keys, and local detection against a fake /v1/models; no real network — verify with `python3 plugin/tests/run.py test_models`
## Non-goals
## Approach (options → choice → why)
Interface (the loop task T-1211 codes against it): profiles() -> [profile]; resolve(name=None) -> {name, kind: 'openai'|'anthropic', base_url, model, key_env, context, tools: bool}; complete(profile, messages, tools=None, max_tokens=2048, timeout=120) -> {text, tool_calls: [{id, name, args}], usage: {in, out}, stop}; messages are OpenAI-shaped [{role: system|user|assistant|tool, content, tool_calls?, tool_call_id?}] and the Anthropic adapter converts them (system to the top-level field, tool results to tool_result blocks); tools are JSON-schema function specs in OpenAI shape, converted for Anthropic; extract_json(text) returns the first balanced JSON object in text (fenced or bare) or None, for models without native tools; retry with backoff on 429 and 5xx (3 tries, honouring Retry-After up to 20 s); errors raise ModelError with the status and a short body, never the key; the key is read only from the env var the profile names and never logged or written. Options: (a) per-vendor SDKs (a dependency each), (b) LiteLLM (a heavy dependency), (c) two hand-written wire shapes over urllib (OpenAI chat completions covers almost every server; Anthropic Messages for Claude). Choice: (c).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: test_models.py with fake servers in both shapes
2. [x] fmmodels.py to pass them; MASTER file-map row
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_models` → ✗ exit 1 (never ran: no tests ran) · Ran 1 tests in 4.3s (2 classes, 16 at a time; slowest: Bench 4s, _FailedTest 0s) / FAILED (1 classes) [ran] [tree 1062bf16d914] (2026-10-16T15:17:55Z)
- (step 2) `python3 plugin/tests/run.py test_models` → exit 0 · Ran 35 tests in 5.4s (5 classes, 16 at a time; slowest: Bench 5s, ExtractJson 0s, OpenAIShape 0s) / OK [ran] [tree c5dfd8f42b34] (2026-10-16T15:19:51Z)
- (step 2) `python3 plugin/tests/run.py test_models` → exit 0 · Ran 35 tests in 4.7s (5 classes, 16 at a time; slowest: Bench 5s, ExtractJson 1s, OpenAIShape 0s) / OK [ran] [tree 0128c9d04bb6] (2026-10-16T15:21:12Z)
- (step 1) `python3 plugin/tests/run.py test_models` → ✗ exit 1 · Ran 50 tests in 5.0s (5 classes, 16 at a time; slowest: Bench 5s, OpenAIShape 1s, ExtractJson 0s) / FAILED (3 classes) [ran] [tree 224fb1768580] (2026-10-16T15:25:12Z)
- (step 2) `python3 plugin/tests/run.py test_models` → exit 0 · Ran 52 tests in 7.6s (5 classes, 16 at a time; slowest: Bench 7s, ExtractJson 1s, OpenAIShape 1s) / OK [ran] [tree 9600f18a882f] (2026-10-16T15:27:13Z)
- (step 2) `python3 plugin/tests/run.py test_models` → exit 0 · Ran 52 tests in 9.5s (5 classes, 16 at a time; slowest: Bench 9s, ExtractJson 1s, OpenAIShape 1s) / OK [ran] [tree 86abab6a5ec7] (2026-10-16T16:02:24Z)
- (ac 1) `python3 plugin/tests/run.py test_models` → exit 0 · Ran 52 tests in 6.5s (5 classes, 16 at a time; slowest: Bench 6s, ExtractJson 1s, OpenAIShape 1s) / OK [ran] [tree 86abab6a5ec7] (2026-10-16T16:02:32Z)
- (audit intent) `fm-reviewer pass (adversary, edge, operator, maintainer): 2 MEDIUM key-leak and transport-error findings, a message-mutation bug and several LOW, all fixed test-first in 06a51f4b (52 tests); default Anthropic model set to claude-sonnet-5-5` → profiles, resolve, complete, extract_json and ModelError as the interface T-1212 codes against, both wire shapes tested against in-process fakes [tree 86abab6a5ec7] (2026-10-16T16:02:32Z)
- (audit adversary) `fm-reviewer pass (adversary, edge, operator, maintainer): 2 MEDIUM key-leak and transport-error findings, a message-mutation bug and several LOW, all fixed test-first in 06a51f4b (52 tests); default Anthropic model set to claude-sonnet-5-5` → key stripped and checked for control characters before sending, scrubbed from every error, never sent over plain http to a non-loopback host, redirects not followed, userinfo in base_url refused [tree 86abab6a5ec7] (2026-10-16T16:02:32Z)
- (audit edge) `fm-reviewer pass (adversary, edge, operator, maintainer): 2 MEDIUM key-leak and transport-error findings, a message-mutation bug and several LOW, all fixed test-first in 06a51f4b (52 tests); default Anthropic model set to claude-sonnet-5-5` → transport errors, deep JSON, non-object replies, missing tool ids and caller-list mutation all handled; stop normalised to end, tool_calls or length [tree 86abab6a5ec7] (2026-10-16T16:02:32Z)
- (audit operator) `fm-reviewer pass (adversary, edge, operator, maintainer): 2 MEDIUM key-leak and transport-error findings, a message-mutation bug and several LOW, all fixed test-first in 06a51f4b (52 tests); default Anthropic model set to claude-sonnet-5-5` → local servers probed lazily in order at 0.3 s each; a clear error names the env vars and models.json when nothing is configured; timeouts are per socket operation, documented [tree 86abab6a5ec7] (2026-10-16T16:02:32Z)
- (audit maintainer) `fm-reviewer pass (adversary, edge, operator, maintainer): 2 MEDIUM key-leak and transport-error findings, a message-mutation bug and several LOW, all fixed test-first in 06a51f4b (52 tests); default Anthropic model set to claude-sonnet-5-5` → one module, documented interface, profile fields validated with errors naming models.json; uses fmcore.foreman_home [tree 86abab6a5ec7] (2026-10-16T16:02:32Z)
## Log
- 2026-10-16T15:15:35Z created
- 2026-10-16T15:15:54Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1211.builder.md
- 2026-10-16T15:16:04Z focused
- 2026-10-16T16:01:54Z merged worktree-agent-a13e651157463ed68 (3 file(s))
- 2026-10-16T16:01:58Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a13e651157463ed68
- 2026-10-16T16:02:05Z focused
- 2026-10-16T16:02:24Z scope: CHANGELOG line
- 2026-10-16T16:03:39Z done
- 2026-10-16T16:03:40Z committed 82ad225c (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1210 [FEATURE L, dropped, 4 steps] fm code round 1: stdlib model client and the harness-run loop, proved end to end on a fake model server
- T-1207 [FEATURE L, planned, 3 steps] Foreman Code: fm code runs Foreman's loop itself on any model or CLI
- decision 2026-10-16: Foreman Code (T-1207) is built as fm code: Foreman's own loop where the harness runs the stations and models fill small JSON slots, over one stdlib …
- T-0786 [FEATURE M, done, 3 steps] fm page: the queue (and optionally a brainstorm catalogue) as one self-contained HTML page for a claude.ai Artifact, with Build/Veto pi…
- the similar finished task took 3 steps
## Lessons
- A client that holds a key has to treat every exception path as a possible leak: the stdlib's own error text quoted the header
## Plan gaps
- failed first: step 1 Failing tests: test_models.py with fake servers in both shapes
## Files touched
- plugin/tests/test_models.py
- plugin/lib/fmmodels.py
- MASTER.md
- CHANGELOG.md

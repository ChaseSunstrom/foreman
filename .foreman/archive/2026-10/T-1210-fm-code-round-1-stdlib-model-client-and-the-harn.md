---
id: T-1210
type: FEATURE
tier: L
status: dropped
priority: normal
scope: []
depends_on: [T-1207]
source: user
created: 2026-10-16T15:15:12Z
updated: 2026-10-16T15:15:51Z
---
# fm code round 1: stdlib model client and the harness-run loop, proved end to end on a fake model server
## Raw request
> fm code round 1: stdlib model client and the harness-run loop, proved end to end on a fake model server
## Interpretation
Round 1 of Foreman Code (T-1207). fm code "<request>" runs Foreman's stations itself: the model only fills small JSON slots and picks tool actions; the harness creates the task, applies edits, runs commands through Foreman's guard, runs the verify commands, records evidence and closes the task. Works with any OpenAI-compatible endpoint (Ollama, LM Studio, llama.cpp, vLLM, OpenRouter, Groq, OpenAI) and Anthropic's Messages API, stdlib only (urllib, json, http.client), no new dependency.
## Assumptions (confidence)
## Acceptance criteria
- [ ] an e2e test runs fm code on a seeded bug (calc.add subtracts, with a test) in a throwaway repo against a scripted OpenAI-compatible fake server (http.server in a thread): the task is created, the fix lands through the edit tool, the verify command passes and is recorded, the task closes; a scripted run action of rm -rf ~ is refused by the guard and the refusal text reaches the model; a malformed plan slot is repaired; --dry-plan changes nothing; an Anthropic-shaped fake server works the same; fm code models lists a reachable fake profile — verify with `python3 plugin/tests/run.py test_code`
## Non-goals
## Approach (options → choice → why)
Two modules. plugin/lib/fmmodels.py: profiles (a user-editable $FOREMAN_HOME/models.json plus detection: ANTHROPIC_API_KEY, OPENAI_API_KEY, OPENROUTER_API_KEY, GROQ_API_KEY, GEMINI_API_KEY via its OpenAI-compatible endpoint, and local servers probed with a 0.3 s timeout: Ollama :11434, LM Studio :1234, llama.cpp :8080, vLLM :8000); resolve(name) -> {name, kind: openai|anthropic, base_url, model, key_env, context, tools: bool}; complete(profile, messages, tools=None, max_tokens, timeout) -> {text, tool_calls:[{id,name,args}], usage:{in,out}, stop}, OpenAI-shaped messages in, the Anthropic adapter converting; extract_json(text) for models without native tools (first balanced JSON object, fenced or bare); retries with backoff on 429/5xx; the key only ever read from the env var the profile names, never logged. plugin/lib/fmcode.py: the loop. PLAN slot {type, tier S|M, title, criteria:[{text, verify}], steps:[...]} validated with bounded repair (2 retries quoting the error), then the task is made through the fm CLI (fm task new … --focus: state only through fm); per step the model returns one action at a time {tool: read|search|edit|write|run|done, ...}: read and search are local and bounded; edit (exact old/new, all-or-nothing, through fm edit's JSON stdin) and write and run each go first through the hook dispatcher as a Claude-Code-shaped PreToolUse payload (plugin/hooks/hook PreToolUse with {tool_name: Bash|Edit|Write, tool_input, cwd, session_id}; exit 2 or a deny is a refusal reported back to the model as the tool result, never executed); run output truncated (head and tail) before it goes back. After done, the harness runs each criterion's verify with fm task evidence --run; a failure goes back to the model with the output (max 3 rounds, then --escalate MODEL if given, else block the task with the reason). Close with fm task finish --audit "fm code (<model>): harness-run verify" (--commit unless --no-commit). A journal (state dir code/<task>.jsonl) records every message and action so --resume continues a crashed run. Output: one plain line per action (no TUI in round 1), --json for an event stream. Options: --model NAME, --escalate NAME, --max-steps N (default 40), --dry-plan (print the plan slot, change nothing), --resume, --no-commit; fm code models lists profiles and which are reachable. Register the verb in fmcli (lazy import, help tier) and add MASTER file-map rows and a README subsection.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] Failing tests first: test_code.py with the fake servers (OpenAI and Anthropic shapes) and the seeded repo  <- CURRENT
2. [ ] fmmodels.py: profiles, detection, complete() for both shapes, extract_json, retries
3. [ ] fmcode.py: plan slot with repair, task creation, action loop through the hook guard and fm edit, verify, escalate, finish, journal and --resume, --dry-plan, fm code models
4. [ ] fmcli registration, MASTER rows, README subsection
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-16T15:15:12Z created
- 2026-10-16T15:15:51Z dropped: split into T-1211 (model client) and T-1212 (loop): builders take M tasks, and the loop codes against the client's interface
## Follow-ups captured

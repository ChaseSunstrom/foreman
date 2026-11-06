---
id: T-1207
type: FEATURE
tier: L
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T14:51:15Z
updated: 2026-11-03T00:42:07Z
group: fm code as a model-agnostic harness
---
# Foreman Code: fm code runs Foreman's loop itself on any model or CLI
## Raw request
> can you make foreman code? an even better harness than CC, that works with other CLI tools/models as an amazing harness, etc.?
## Interpretation
A coding harness of Foreman's own, better than Claude Code at the thing Foreman is for: the harness (not the model) runs capture, plan, execute, verify and record, so weak and local models do well because they only fill small, validated slots, and strong ones go faster. It talks to any OpenAI-compatible endpoint (Ollama, LM Studio, llama.cpp, vLLM, OpenRouter, Groq, OpenAI, Gemini's compatible endpoint) and Anthropic's API, uses existing CLIs (claude, codex, gemini, opencode, aider, any command) as interchangeable workers, keeps every command and edit behind Foreman's guard, records evidence in Foreman's state, and resumes after a crash.
## Assumptions (confidence)
## Acceptance criteria
- [ ] fm code on a seeded bug in a throwaway repo, driven by a scripted OpenAI-compatible fake server, plans a task, edits through the guard, runs the verify command, and closes the task with evidence; a guard-refused command from the model is refused and reported back to it — verify with `python3 plugin/tests/run.py test_code`
## Non-goals
## Approach (options → choice → why)
A complete version has: provider client and model profiles with local-server detection; a slot-filling loop with schema validation and bounded repair; a text tool protocol for models without native tools; a five-tool set (read, search, edit, run, finish) through the guard; harness-run verification with retries and an escalation ladder; a step journal and --resume; --worker for external CLIs judged by diff and verify; a conformance bench that grades a model or worker on seeded tasks; streaming status output, then the web UI view; later ACP/MCP serving, sandboxing and grammar-constrained decoding. Options: (a) native loop only; (b) orchestrate existing CLIs only (fm run already does this for claude); (c) fork opencode and embed Foreman (TypeScript, a moving upstream, the guard out of process anyway); (d) hybrid: native loop plus workers under one verb. Choice: (d), built in rounds: round 1 the provider layer and the native loop with an end-to-end test against a scripted fake model server; round 2 workers and the bench; round 3 UI, escalation learning and serving. Stdlib only; the guard is reached through the same hook dispatcher other harnesses use, so there is one guard.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] Round 1: provider layer (fmmodels) and native loop (fmcode) with the e2e test  <- CURRENT
2. [ ] Round 2: --worker for external CLIs and fm code bench
3. [ ] Round 3: web UI view, escalation from outcomes, docs and site section
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-16T14:51:15Z created
- 2026-10-16T15:14:03Z planned from capture
- 2026-10-17T00:29:22Z step 1 done in T-1212: fmmodels + fmcode with test_code (seeded bug via a fake OpenAI/Anthropic server, plan, guarded edits, verify, close; a guard-refused rm -rf ~ reported back to the model)
- 2026-10-17T00:29:22Z blocked: waits for T-1214 (fm code --worker, in a builder lane now) and T-1215 (fm code bench), its round 2
- 2026-11-03T00:36:17Z unblocked: their named blockers (T-1214, T-1316, T-1401) closed weeks ago; the blocked-pile line found them (T-2683)
- 2026-11-03T00:42:07Z dropped: an umbrella whose rounds landed as their own tasks: round 1's criterion passes today (python3 plugin/tests/run.py test_code: OK, the seeded-bug e2e with a scripted fake server), round 2 is fm code --worker (T-1214) and fm code bench (T-1215), round 3's docs and site section are in README, MASTER.md and site/index.html; the two unbuilt round-3 parts are T-2739 (escalation from outcomes) and T-2740 (a web view of runs)
## Follow-ups captured

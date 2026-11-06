---
id: T-0340
type: SECURITY
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-06T03:11:46Z
updated: 2026-10-06T03:15:03Z
base: dcba63a7a88615c6485d6a96c823d04e5783f4b2
base_tree: aa9d7026692c4fea88712fc35b9e15f455b5f69e
verified: strong
---
# Guard: protect the hook config Foreman wires into Codex, Gemini CLI and opencode as core
## Raw request
> Guard: protect the hook config Foreman wires into Codex, Gemini CLI and opencode as core
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a Write, Edit or shell write to ~/.codex/hooks.json|config.toml, ~/.gemini/settings.json, opencode's opencode.json and plugins/, their project-level copies, and plugin/integrations is a core block — verify with `python3 plugin/tests/run.py -k test_guard`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests (red)
2. [x] _is_core + _protected_roots
## Resume here
## Docs impact
README (Other agents), CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_guard.AgentWiring` → ✗ exit 1 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: AgentWiring 0s) / FAILED (1 classes) [ran] [tree 1187867710a1] (2026-10-06T03:11:54Z)
- (step 1) `python3 plugin/tests/run.py -k test_guard.AgentWiring` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: AgentWiring 0s) / OK [ran] [tree 9b55d112e249] (2026-10-06T03:14:58Z)
- (ac 1) `python3 plugin/tests/run.py -k test_guard` → exit 0 · Ran 65 tests in 3.9s (21 classes, 16 at a time; slowest: GuardAgainstBash 4s, PluginChanges 1s, Core 0s) / OK [ran] [tree 9b55d112e249] (2026-10-06T03:15:02Z)
- (step 2) `python3 plugin/tests/run.py -k test_guard` → exit 0 · Ran 65 tests in 3.9s (21 classes, 16 at a time; slowest: GuardAgainstBash 4s, PluginChanges 1s, Core 0s) / OK [ran] [tree 9b55d112e249] (2026-10-06T03:15:02Z)
- (audit adversary) `self + adversary review: agent hook configs (user, CODEX_HOME and project copies), opencode plugins dir and plugin/integrations are core for Write/Edit, shell writes and tree writes; fm agents uninstall from a tool call is core; AGENTS.md/GEMINI.md rules stay ordinary files; a standing core yes doesn't cover them (non-Foreman-code paths), /fm-trust does; replay 0 newly allowed` → the agent can no longer unwire its own guard by editing hooks.json/settings.json/plugin or running fm agents uninstall; a rename/mv onto them is a write to the target (same classify path) [tree 9b55d112e249] (2026-10-06T03:15:02Z)
- (audit self) `self + adversary review: agent hook configs (user, CODEX_HOME and project copies), opencode plugins dir and plugin/integrations are core for Write/Edit, shell writes and tree writes; fm agents uninstall from a tool call is core; AGENTS.md/GEMINI.md rules stay ordinary files; a standing core yes doesn't cover them (non-Foreman-code paths), /fm-trust does; replay 0 newly allowed` → no findings [tree 9b55d112e249] (2026-10-06T03:15:02Z)
## Log
- 2026-10-06T03:11:46Z created
- 2026-10-06T03:11:46Z focused
- 2026-10-06T03:15:03Z done
- 2026-10-06T03:15:03Z committed 2e4d0eb (4 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0318-agents: Answer.** All four agents have a hook that can block a tool before it runs, except opencode, where a plugin can do it. Each has a JSON-RPC, HTTP …
- T-0324 [FEATURE L, done, 4 steps] Foreman discipline on codex, gemini and opencode: fm hook --agent and fm agents install — lesson: Another agent's hook treats a crash (…
- research T-0324-hook-formats: 1. **Answer
- T-0336 [RESEARCH S, blocked, 1 steps] Live-verify fm agents on real codex, gemini and opencode
- similar past tasks were L: consider --tier L
- the similar finished task took 4 steps
## Lessons
- Wiring a guard into a new host means protecting that host's hook config the same day: the config that loads the guard is part of the guard.
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
- README.md

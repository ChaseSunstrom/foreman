---
id: T-0929
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T19:44:06Z
updated: 2026-10-15T19:44:26Z
base: 44b66fa361eb2a82ad0aacdbefc4129dbcab29c1
base_tree: 747b947c77734b3616c44631fef2faa1a1a8f1fe
verified: ok
---
# Say plainly that the Codex, Gemini CLI and opencode adapters are built to the documented hook formats but not yet verified against live CLIs
## Raw request
> Say plainly that the Codex, Gemini CLI and opencode adapters are built to the documented hook formats but not yet verified against live CLIs
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] README and fm agents install name the adapters unverified against live CLIs — verify with `grep -q 'not yet verified against live' README.md`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] README line and the install message
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `grep -q 'not yet verified against live' README.md` → exit 0 · (no output) [ran] [tree af0301397deb] (2026-10-15T19:44:25Z)
- (step 1) `python3 plugin/tests/run.py -k Agents` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Agents 0s) / OK [ran] [tree af0301397deb] (2026-10-15T19:44:25Z)
- (audit self) `self: fm agents install now notes the adapter is built to the tool's documented hook format and not yet verified live, with what to check; the README says the same; behaviour unchanged (agents tests pass)` → no findings [tree af0301397deb] (2026-10-15T19:44:25Z)
## Log
- 2026-10-15T19:44:06Z created
- 2026-10-15T19:44:06Z focused
- 2026-10-15T19:44:25Z done
- 2026-10-15T19:44:26Z committed 10a2948 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-round8-20261015: Probe: `fm ideas` with performance + simplicity, 2 rounds, past all 31 earlier idea indexes (brainstorm-20261015-143454): 45 new tit…
- research T-0318-agents: Answer.** All four agents have a hook that can block a tool before it runs, except opencode, where a plugin can do it. Each has a JSON-RPC, HTTP …
- T-0336 [RESEARCH S, blocked, 1 steps] Live-verify fm agents on real codex, gemini and opencode
- decision 2026-10-06: [costly] fm ask grants stay Claude-Code-only on Codex/Gemini/opencode until T-0336 verifies live whether their prompt hooks fire for agent-written s…
## Behaviour lock
none: an added note line and a README sentence; the adapters' behaviour is unchanged
## Files touched
- plugin/lib/fmagents.py
- README.md

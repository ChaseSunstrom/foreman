---
id: T-0978
type: RESEARCH
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T22:20:26Z
updated: 2026-10-15T23:15:34Z
base: e061abf300ac742c6f3c02d639b732b0ff1f613c
base_tree: 4430e0dcb0ac7214a7f85a4334c82dbc1b966ce8
verified: strong
---
# Small and local models: measure first — fm bench stranger replays with Haiku (and a local
## Raw request
> Small and local models: measure first — fm bench stranger replays with Haiku (and a local model through an installed harness, if any) on real tasks, list every place they trip (CLI flags, multi-step closes, evidence), then build from that: fm does the mechanical steps itself, MCP write tools with schemas, did-you-mean for fm typos, exact next commands
## Interpretation
Make Foreman work well for small and local models, measured first: where does a weak model trip on Foreman's procedure (CLI flags, multi-step closes, evidence, criteria), so the fixes move judgement into Foreman instead of adding rules.
## Assumptions (confidence)
## Acceptance criteria
- [x] research/T-0978-small-models.md lists every stumble from the Haiku replays and the recorded sessions with its cause in Foreman's code, and the fixes are queued — verify with `test -s state/projects/foreman-4a056f/research/T-0978-small-models.md`
## Non-goals
## Approach (options → choice → why)
Options: fm bench stranger replays with Haiku as the small-model proxy (no local model or harness is installed here: no ollama, opencode, aider, codex or gemini), plus the two recorded Sonnet sessions' stumbles, then queue fixes from the evidence (chosen: measured, cheap); guess the fixes up front (unmeasured); install a local model (an outward install the user hasn't asked for).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Haiku stranger replays; collect stumbles; ground; queue fixes
## Resume here
## Docs impact
state/projects/foreman-4a056f/research/T-0978-small-models.md
## Verification evidence
- (step 1) `test -s state/projects/foreman-4a056f/research/T-0978-small-models.md` → exit 0 · (no output) [ran] [tree 4430e0dcb0ac] (2026-10-15T23:15:26Z)
- (ac 1) `test -s state/projects/foreman-4a056f/research/T-0978-small-models.md` → exit 0 · (no output) [ran] [tree 4430e0dcb0ac] (2026-10-15T23:15:27Z)
- (audit intent) `self: every stumble from the Haiku transcript and the two Sonnet recordings is in the table with its cause; each fix is done (T-0969, T-0985, T-0986, T-0987) or skipped with its reason` → measured stumbles with causes and fixes, not guesses [tree 4430e0dcb0ac] (2026-10-15T23:15:27Z)
- (audit maintainer) `self: every stumble from the Haiku transcript and the two Sonnet recordings is in the table with its cause; each fix is done (T-0969, T-0985, T-0986, T-0987) or skipped with its reason` → the note says how to re-run the probe and what to compare [tree 4430e0dcb0ac] (2026-10-15T23:15:27Z)
- (audit intent) `self: every stumble from the Haiku transcript and the two Sonnet recordings is in the table with its cause; each fix is done (T-0969, T-0985, T-0986, T-0987) or skipped with its reason` → measured stumbles with causes and fixes, not guesses [tree 4430e0dcb0ac] (2026-10-15T23:15:34Z)
- (audit maintainer) `self: every stumble from the Haiku transcript and the two Sonnet recordings is in the table with its cause; each fix is done (T-0969, T-0985, T-0986, T-0987) or skipped with its reason` → the note says how to re-run the probe and what to compare [tree 4430e0dcb0ac] (2026-10-15T23:15:34Z)
## Log
- 2026-10-15T22:20:26Z created
- 2026-10-15T22:48:06Z focused
- 2026-10-15T22:49:37Z paused: focus moved to T-0965
- 2026-10-15T23:07:03Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-15T23:07:03Z focused
- 2026-10-15T23:08:00Z paused: focus moved to T-0986
- 2026-10-15T23:15:20Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-15T23:15:20Z focused
- 2026-10-15T23:15:34Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0701 [FEATURE M, done, 3 steps] Frontier 01 — Zero-token instrument layer — lesson: Measure a log summarizer on a mostly-numeric log: dividing by template length hides…
- T-0674 [FEATURE M, done, 3 steps] Milestone: Features — Observability, replay and trust — lesson: Check where secrets enter before adding redaction: every write path her…
- T-0946 [FEATURE M, done, 3 steps] MCP: a great Foreman MCP server (state, stack library, zero-token instruments) and fm mcp new to wrap any process or CLI as a tested MC…
- decision 2026-10-15: Round 4 slate: 6 builds from 31 grounded clusters (437 ideas): install asks before bypass, INSTALL.md for agents, fm demo (no-model), marketplace in…
## Decision
Recommendation: close the gaps where a small model has to guess a command (done: T-0969, T-0985, T-0986, T-0987); no separate small-model mode or MCP write tools yet; would change if: a re-run of the same Haiku probe on the current tree still fails to close in 25 minutes, or a local model harness gets installed here to measure directly.
## Lessons
- A cheap model run on a real task finds the gaps a strong model papers over: each one is a place Foreman left a command for the model to guess.

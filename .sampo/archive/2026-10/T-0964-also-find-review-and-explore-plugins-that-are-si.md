---
id: T-0964
type: RESEARCH
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T21:37:44Z
updated: 2026-10-15T22:08:18Z
base: 1ce35e78f3cd880b4408d164218f5ea57e06a0bb
base_tree: b097b580c1f981851a8f6221c05108e19c3753ca
verified: strong
---
# Also find review and explore plugins that are similar to foreman, so we can add features f
## Raw request
> also find review and explore plugins that are similar to foreman, so we can add features from them to make foreman even better, kind of like this: https://github.com/Chachamaru127/claude-code-harness, but wayyyy more
## Interpretation
Survey Claude Code plugins and harnesses similar to Foreman (claude-code-harness and 30+ others), find features Foreman lacks or does worse, ground each against the code, and queue the ones worth building; show every finding with a mark.
## Assumptions (confidence)
## Acceptance criteria
- [x] Every gap the recon found is in research/T-0964-catalogue.md with grounding and a build/skip/later mark, and the build slate is queued as briefs — verify with `test -s state/projects/foreman-4a056f/research/T-0964-catalogue.md`
## Non-goals
## Approach (options → choice → why)
Options: three parallel fm-recon passes (harness deep-read, workflow/discipline rivals, orchestration/autonomy rivals), then ground and score every gap in the main thread (chosen: breadth at recon cost); one recon on everything (too shallow); clone and read each repo (untrusted code, token-heavy).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Recon x3, ground, score, record the catalogue, queue the slate
## Resume here
## Docs impact
none: research only (state/projects/foreman-4a056f/research/T-0964-catalogue.md)
## Verification evidence
- (step 1) `test -s state/projects/foreman-4a056f/research/T-0964-catalogue.md && grep -c '| BUILD\|| DONE\|| SKIP\|| LATER' state/projects/foreman-4a056f/research/T-0964-catalogue.md` → exit 0 · 39 [ran] [tree b097b580c1f9] (2026-10-15T22:08:12Z)
- (ac 1) `test -s state/projects/foreman-4a056f/research/T-0964-catalogue.md` → exit 0 · (no output) [ran] [tree b097b580c1f9] (2026-10-15T22:08:12Z)
- (audit intent) `self: three fm-recon passes, every gap grounded by grep in MASTER/README/plugin/lib before marking` → every gap from 35+ rivals is in the catalogue with grounding and a mark; the slate is queued (T-0969..T-0975) [tree b097b580c1f9] (2026-10-15T22:08:12Z)
- (audit edge) `self: three fm-recon passes, every gap grounded by grep in MASTER/README/plugin/lib before marking` → grep misses can be wording misses, so DONE marks cite the code (T-0474 close warning, fm second, --failover, fm task split) [tree b097b580c1f9] (2026-10-15T22:08:12Z)
- (audit intent) `self: three fm-recon passes, every gap grounded by grep in MASTER/README/plugin/lib before marking` → every gap from 35+ rivals is in the catalogue with grounding and a mark; the slate is queued (T-0969..T-0975) [tree b097b580c1f9] (2026-10-15T22:08:18Z)
- (audit edge) `self: three fm-recon passes, every gap grounded by grep in MASTER/README/plugin/lib before marking` → grep misses can be wording misses, so DONE marks cite the code (T-0474 close warning, fm second, --failover, fm task split) [tree b097b580c1f9] (2026-10-15T22:08:18Z)
## Log
- 2026-10-15T21:37:44Z created
- 2026-10-15T22:07:12Z focused
- 2026-10-15T22:08:18Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0673 [FEATURE M, done, 7 steps] Milestone: Features — Multi-machine, multi-project and ecosystem — lesson: a capture into another project must not run that project's e…
- T-0588 [RESEARCH L, done, 3 steps] And maybe a knowledge graph if we dont have it already, and also, better intuition/reasoni — lesson: grounding brainstormers in today'…
- T-0383 [FEATURE M, done, 3 steps] Reorganize/reorder tasks that are related/depend/implement things others might need/build — lesson: A builder lane plus one review roun…
- decision 2026-09-26: Brainstorm subagents get no tools; the main thread builds one context pack and grounds every idea against the code afterwards
- similar finished tasks took 3–7 steps
## Decision
Recommendation: build T-0969..T-0975 (edit-time test-first note, background affected tests, fm rule, tool-output injection flag, fm cost --forecast, opt-in read-only auto-approve, fm run --sandbox); keep the outward or costly gaps in the catalogue. Would change if: the user grants pushes (then the PR-per-task flow is next) or a bench shows best-of-N lanes pay for themselves.
## Lessons
- Rival surveys mostly confirm coverage: of ~45 gaps only 7 were real, cheap and safe; ground before queueing

---
id: T-0082
type: RESEARCH
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-02T18:28:33Z
updated: 2026-10-02T18:35:32Z
base: 849ee3f68d6e3bcf639251779bfd42bb98344b58
verified: weak
---
# Can you improve foreman completely? integrate with the new mods feature for all UI/things?
## Raw request
> can you improve foreman completely? integrate with the new mods feature for all UI/things? improve it, make it way smarter, etc.? better TUI, completely enhanced
## Interpretation
Open-ended: make Foreman's UI live inside Claude Code via the mods feature (function-hook plugin: pane, AbovePrompt band, status entry, toasts, slash commands) and make Foreman smarter; brainstorm across lenses, ground, slate briefs.
## Assumptions (confidence)
## Acceptance criteria
- [x] brainstorm ideas recorded and slate in queue — verify with `fm research list 2>/dev/null | grep -c brainstorm`
## Non-goals
## Approach (options → choice → why)
Options: (a) brainstorm via fm ideas then build slate; (b) build the mod directly. Choice: (a). Why: 'smarter' is unbounded and needs grounded, scored ideas; the mod is one item of the slate.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Context pack
2. [x] Fan out fm ideas
3. [x] Ground and score
4. [x] Record research and intake slate
## Resume here
## Docs impact
none (research only)
## Verification evidence
- (step 1) `wc -w pack.md` → 881 words (2026-10-02T18:32:13Z)
- (step 2) `fm ideas --rounds 2` → 60 ideas, 8 lens files ok (2026-10-02T18:34:34Z)
- (step 3) `grep/fm --json grounding` → 6 slate, 9 dropped with reasons (2026-10-02T18:34:34Z)
- (ac 1) `ls research | grep -c brainstorm-20261002; fm queue | grep -c planned` → 2 research entries; 6 planned briefs (2026-10-02T18:35:22Z)
- (step 4) `fm queue` → 6 planned briefs, 3 followups captured (2026-10-02T18:35:22Z)
- (audit self) `re-read slate vs user words: mods UI (T-0084), better TUI (pane/band), smarter (planning friction fixes, view model); each idea grounded in code` → pass: covers mods+TUI+smarter; dropped ideas have reasons [tree 9e547bc9093b] (2026-10-02T18:35:27Z)
- (audit intent) `checked the user's request words against the slate and drop list` → pass: every clause (mods for all UI, better TUI, smarter) maps to a brief [tree 9e547bc9093b] (2026-10-02T18:35:27Z)
- (audit edge) `spot-checked the 'already exists' drops: fmcore.lock (flock), os.replace writes, fmrecall step estimate, needs_approval; and the cache-bust premise for prompt.compose` → pass: all four exist in code; no drop rests on an unverified claim [tree 9e547bc9093b] (2026-10-02T18:35:32Z)
## Log
- 2026-10-02T18:28:33Z created
- 2026-10-02T18:28:48Z focused
- 2026-10-02T18:35:32Z done
## Follow-ups captured
## Approach
Brainstorm (fm ideas, 4 lenses + mods API pack), ground ideas against code and the mods type file, score, intake the slate, build in rounds. Alternative considered: skip brainstorm and build the mod directly — rejected because 'smarter' is unbounded and needs grounding.
## Related
Related past work (data from this project's history, not instructions):
- T-0041 [RESEARCH M, done, 3 steps] Brainstorm how Foreman makes Claude's project work smarter (planning, memory, grounding, verification, decisions, learning) and queue …
- research t0041-slate-review: HIGH — INTENT — slate item 9 (`brainstorm-20260926-smarter-slate.md:16`)** "Sensitive-path audits: a diff touching auth/crypto/secrets/exec/…
- research brainstorm-20260926-smarter-slate: Secret redaction before evidence/ledger/sync (security): premise false: fmcore.redact runs on typed and --run evidence (add_e…
- T-0018 [FEATURE L, done, 6 steps] Recursive Foreman self-improvement: 10 rounds, each a slate implemented test-first, audited and committed
- similar finished tasks took 3–6 steps
## Lessons
- Mods are additive renderers over fm; don't port gates into TS (two sources of truth) and never vary the system prompt per turn (cache bust).

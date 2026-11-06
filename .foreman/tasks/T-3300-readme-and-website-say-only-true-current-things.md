---
id: T-3300
type: FIX
tier: L
status: planned
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-06T03:44:46Z
updated: 2026-11-06T03:47:49Z
base: 5c403348c1dfe9523985c9f84cf7db536080f17f
---
# README and website say only true, current things: every claim, command, number, link and picture checked against the code and live data, every wrong or stale line fixed
## Raw request
> README and website say only true, current things: every claim, command, number, link and picture checked against the code and live data, every wrong or stale line fixed
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] a claim-by-claim audit of README.md (all 13 sections) and site/ (index, Rune page, cards, tools, benchmarks) lists every wrong, stale or unverifiable statement with file:line and the code or data that contradicts it — verify with `sampo research show readme-site-audit`
- [ ] every finding is fixed in the docs or the code, or captured with a reason; doc examples parse (test_docexamples) and doc claims trace (sampo docs --trace) once T-3289/T-3287 merge — verify with `python3 plugin/tests/run.py test_docs test_site`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fan out auditors: one per README section group and one per site page, each verifying claims against the code (read-only)
2. [ ] merge findings into one list; fix test-first where code is wrong, edit docs where docs are wrong  <- CURRENT
3. [ ] re-run the doc checks and a final cold read
## Resume here
## Docs impact
## Verification evidence
- (step 1) `sampo research show readme-site-audit` → exit 0 · 26. STALE site/index.html:374,454 and build-inserted counts — stats.json from 2026-11-02 (cards 1,219 vs 1,227; tests 5,686 vs ~6,800; tasks, lanes, gates). Fix: rerun site/stats.py on each build/nigh [ran] [tree c3192a68d2bc] [world 2f1906870a] (2026-11-06T03:47:49Z)
## Log
- 2026-11-06T03:44:46Z created
- 2026-11-06T03:47:49Z start point recorded late (no focus had kept one): its diff starts at 5c40334
## Follow-ups captured

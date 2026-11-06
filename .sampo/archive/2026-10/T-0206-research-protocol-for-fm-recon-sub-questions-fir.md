---
id: T-0206
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-04T04:10:46Z
updated: 2026-10-04T04:27:10Z
base: 22bb0d130d769bd73cc172a38af2651df4dc3965
base_tree: f4d9a3e7e8e6030309a66e6e45b4ad5b58e7547f
verified: strong
---
# fm research ask: recall first, parallel web researchers per sub-question, every quoted claim re-fetched and checked, one note recorded
## Raw request
> FEATURE: research protocol for fm-recon — sub-questions first, source tiers, a short verbatim quote + URL + fetch date per web claim, a disconfirming pass, and recall-first before the web
> CONTEXT: STAGE_REFERENCE in plugin/lib/fmcore.py names only Foreman procedures; fmplugins.installed() and profile() already list enabled plugins' skills; next_action runs every turn, so the index must be cached (rebuild on installed_plugins.json/settings mtime)
> CONTEXT: plugin/agents/fm-recon.md and plugin/skills/intake/references/delegate.md; RESEARCH's STAGE_REFERENCE points at delegate.md
> CONTEXT: plugin/agents/, fmrecall.note_failure thrash hint, skills/intake/references/debugging.md and delegate.md (allowed delegations)
> CONTEXT: plugin/lib/fmideas.py writes ideas.md; fmrecall.recall(p, query) returns ranked hits with labels like "T-0039 [SECURITY S, done, …]"
> DONE-WHEN: a test with a fake enabled plugin carrying a matching skill shows it in next_action's executing line, and no line when none matches
> DONE-WHEN: fm-recon.md and delegate.md carry the protocol and test_docs (or a new check) keeps the agent's required output sections
> DONE-WHEN: the agent file exists with read-only tools and fm doctor passes; the thrash hint names it
> DONE-WHEN: a test shows an idea matching a done brief annotated with that brief's id in ideas.md
## Interpretation
Research today is one Sonnet recon agent whose web claims are trusted after a 2-claim spot-check. Make web research an engine: recall what's known, split the question, research sub-questions in parallel tool-limited children, mechanically re-fetch every cited page to check the quoted words, record one note.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm research ask with stubbed researchers writes a note whose claims are marked verified / not found / unchecked, with prior research recalled first — verify with `python3 plugin/tests/run.py -k test_research`
- [x] a private or non-https URL is never fetched — verify with `python3 plugin/tests/run.py -k test_research`
## Non-goals
## Approach (options → choice → why)
A) prompt-only protocol for fm-recon: cheap, but verification stays manual and serial. B) fm research ask: claude -p children with only WebSearch/WebFetch (like fm ideas), quote-anchored claim lines, stdlib urllib re-fetch with public-https-only and redirect re-checks, note via the research store. Choice: B plus A's protocol in fm-recon for codebase/mixed questions — B makes verification mechanical and parallel without main-thread context.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Tests first: stub claude, fake fetch, private-host refusal
2. [x] fmresearch.py: plan, fan out, verify, record; CLI wiring
3. [x] fm-recon protocol + delegate.md + MASTER.md file map
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md, plugin/agents/fm-recon.md, plugin/skills/intake/references/delegate.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_research` → exit 0 · Ran 9 tests in 0.5s (4 classes, 16 at a time; slowest: Ask 0s, RoundFiveWorkflow 0s, DecisionsResearchSelf 0s) / OK [ran] [tree cbe3b5b48cd8] (2026-10-04T04:24:51Z)
- (step 2) `python3 plugin/tests/run.py -k test_research` → exit 0 · Ran 9 tests in 0.5s (4 classes, 16 at a time; slowest: Ask 0s, RoundFiveWorkflow 0s, DecisionsResearchSelf 0s) / OK [ran] [tree cbe3b5b48cd8] (2026-10-04T04:24:52Z)
- (step 3) `fm doctor 2>&1 | tail -1` → exit 0 · fm doctor: OK (25 pass, 2 warn, 0 fail) [ran] [tree cbe3b5b48cd8] (2026-10-04T04:24:58Z)
- `python3 plugin/tests/run.py -k test_research` → ✗ exit 1 · Ran 3 tests in 0.6s (3 classes, 16 at a time; slowest: RoundFiveWorkflow 0s, DecisionsResearchSelf 0s, _FailedTest 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 5828bbd0caca] (2026-10-04T04:26:29Z)
- `python3 plugin/tests/run.py -k test_research` → exit 0 · Ran 10 tests in 0.5s (4 classes, 16 at a time; slowest: Ask 0s, RoundFiveWorkflow 0s, DecisionsResearchSelf 0s) / OK [ran] [tree 5828bbd0caca] (2026-10-04T04:26:29Z)
- (ac 1) `python3 plugin/tests/run.py -k test_research` → exit 0 · Ran 10 tests in 0.5s (4 classes, 16 at a time; slowest: Ask 0s, RoundFiveWorkflow 0s, DecisionsResearchSelf 0s) / OK [ran] [tree 5828bbd0caca] (2026-10-04T04:27:10Z)
- (ac 2) `python3 plugin/tests/run.py -k test_research` → exit 0 · Ran 10 tests in 0.5s (4 classes, 16 at a time; slowest: Ask 0s, RoundFiveWorkflow 0s, DecisionsResearchSelf 0s) / OK [ran] [tree 5828bbd0caca] (2026-10-04T04:27:10Z)
- (audit adversary) `one fm-reviewer pass (intent + adversary), findings verified and fixed test-first` → SSRF closed (public https only, every redirect re-checked, metadata/LAN/loopback refused — tested); fixed MEDIUM: a hostile page's bogus charset or broken HTTP crashed the run and lost the paid research → fetch decodes safely, catches HTTPException, verify isolates each page; fixed LOW: slow-drip pages capped at 30 s per page; fixed LOW: quotes under 4 words never verify; researcher children have only WebSearch/WebFetch, no MCP, no user settings; note is redacted and defanged, only claim lines kept [tree 5828bbd0caca] (2026-10-04T04:27:10Z)
- (audit intent) `one fm-reviewer pass (intent + adversary), findings verified and fixed test-first` → web research now recalls first, splits, runs sub-questions in parallel and mechanically checks every quote; live smoke: 8 claims in 14 s, 7 quotes found, 1 flagged; fm-recon and delegate.md carry the protocol for mixed questions [tree 5828bbd0caca] (2026-10-04T04:27:10Z)
## Log
- 2026-10-04T04:10:46Z created
- 2026-10-04T04:10:52Z set tier=S
- 2026-10-04T04:11:26Z steer: make it an engine, not only a prompt — fm research ask: recall-first, sub-questions, ≤3 parallel recon, quoted claims re-checked, note recorded with tiers/dates
- 2026-10-04T04:11:26Z set tier=M
- 2026-10-04T04:21:55Z planned from capture
- 2026-10-04T04:21:55Z focused
- 2026-10-04T04:27:10Z done
- 2026-10-04T04:27:10Z committed 1209d65 (8 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0208 [FEATURE S, done, 1 steps] fm ideas marks each new idea with the finished task it most resembles
- research brainstorm-20261003-round6: Runs: brainstorm-20261003-230652 (5 lenses + deepen 3: 78 new titles) and brainstorm-20261003-230844 (4 lenses + deepen 2: 61 new ti…
- playbook Intent-Driven Development (skills/playbooks/references/plan/intent-driven-development.md)
- research t0071-de-review: MEDIUM — `plugin/lib/fmcost.py:546` — `cmd_usage`'s Next-follow regex `\bfm [a-z-]+(?: (?:prep|step|done|new|evidence|ac|audit|finish|prove))?`…
- the similar finished task took 1 steps
## Lessons
- Checking a model's citation mechanically is cheap (fetch + normalized substring) and catches what a 2-claim spot-check misses; but the check must treat every fetched page as hostile input, or one page can crash the run that paid for the research
## Files touched
- plugin/tests/test_research.py
- plugin/lib/fmresearch.py
- plugin/lib/fmcli.py
- plugin/lib/fmrecall.py
- MASTER.md
- plugin/agents/fm-recon.md
- plugin/skills/intake/references/delegate.md
- CHANGELOG.md

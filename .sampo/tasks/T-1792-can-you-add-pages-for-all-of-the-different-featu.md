---
id: T-1792
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-27T22:24:46Z
updated: 2026-11-05T04:43:29Z
explore: true
confirm: true
---
# Site: a page for every Foreman feature area, each with charts from the ledger, plus an every-command reference
## Raw request
> "can you add pages for ALL of the different features of foreman? with more graphs, and everything?"
> (fm second session: "can you add pages for ALL of the different features of foreman? with more graphs, and everything?" — no site-pages task is in the open work and no later message confirms it was finished.)
## Interpretation
The user wants the site (site/, GitHub Pages) to cover every Foreman feature, each with charts. Sixteen pages exist (planning, proof, guard, permissions, review, lanes, drive, cards, panel, speed, learning, tools, code, benchmarks, playbooks, releases). Missing areas with ledger data: intake and capture, research/ideas/decisions, always-on checks (ambient, sentinel, close_affected, enforce), board hygiene (drop, defer, block, tidy), sessions (session_start, prompt, second_session, checkpoint, stall), outbound and injection (outbound, escape, injection_flag), self-improvement (rsi_pass, evolve, dream). 'ALL' means nothing left out, so an every-command page lists each fm verb by group.
## Assumptions (confidence)
## Acceptance criteria
- [ ] every new feature page has at least one chart drawn from the ledger, and every fm verb appears on the commands page — verify with `python3 plugin/tests/run.py test_site_build`
- [ ] the site builds with the new pages in the nav and index, and the header test still passes at phone widths — verify with `python3 plugin/tests/run.py test_site test_site_hero`
## Non-goals
## Approach (options → choice → why)
Options: (A) hand-written page per missing area with new ledger counters; (B) pages generated per fm verb group from the parser; (C) one features matrix page; (D) A for the data-rich areas plus a generated every-command reference (B) so coverage is complete. Choice: D. Curated pages carry the charts and the why; the generated page guarantees ALL and can't drift because the parser is the source. Reuse build.py's helpers (hbars, columns, line, tiles) and the page dict shape; counters go in stats.ledger's one pass over ledger.jsonl. Captured: per-verb usage from transcripts (no event per verb today).
## Risks and rollback
## Execution prompt
## Steps
1. [ ] stats.py: ledger counters for intake (captures by source and day), research, ideas and decisions, always-on checks, board hygiene (drop, defer, block), sessions and prompts, outbound and injection flags, approvals; tests first  <- CURRENT
2. [ ] pages.py: curated pages for each area the 16 pages don't cover, each with charts and what the feature does
3. [ ] commands page generated from fm's parser: every verb with its group and help, and per-group usage
4. [ ] build, look at desktop and phone width, fix what's off
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-27T22:24:46Z created
- 2026-10-28T01:01:15Z set approved=True
- 2026-10-28T01:01:15Z user 2026-10-27: 'don't ask for my permission on anything… any and ALL ideas implemented': approved
- 2026-10-28T07:36:12Z planned from capture
- 2026-10-28T07:37:33Z blocked: waits for the user's yes: their 2026-10-28 message reserves it (fm ask T-1792 confirm at the end of the run); planned and ready otherwise
- 2026-11-05T04:43:29Z dropped: done by commit 1bba1e37 (T-1220, archived), the same ask as T-2082: 29 feature pages with charts today
## Follow-ups captured

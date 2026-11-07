---
id: T-3111
type: FEATURE
tier: M
status: planned
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-05T03:08:03Z
updated: 2026-11-06T03:53:46Z
inferred_deps: [T-3104]
inferred_why: T-3104: named in its request
---
# Design works part 3: a gallery on the main site by type, with the user's picks and vetoes as the labels that set the bar (T-3104)
## Raw request
> Design works part 3: a gallery on the main site by type, with the user's picks and vetoes as the labels that set the bar (T-3104)
## Interpretation
Reading 1 (chosen): a Works page on the site (and the live page) shows kept works by type with their renders, filters and a large view; the user's pick or veto on a work is recorded as a label (the only labels: the user's own choices), moves its rank, and a style the user vetoes three times gets its prompts rewritten; the bar the writer loop keeps against is the user's picked set. Reading 2: a static gallery only; rejected, 'genuinely good' is the user's taste and needs their picks.
## Assumptions (confidence)
## Acceptance criteria
- [ ] the site's Works page shows every kept work by type with its render in both themes; the live page records a pick or veto per work with the time, and ranks move — verify with `python3 plugin/tests/run.py test_design_works test_site_build test_live`
## Non-goals
## Approach (options → choice → why)
1. The site build exports works like the cards, picks go through the live page (local) into the works store; likely outcome: a gallery the user can steer in a click. 2. Do less: no picks; fails if: the bar never learns the user's taste. 3. Picks through an artifact database; fails if: the picks live outside Sampo's own state. Choice 1 (70%)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests: export, page, pick and veto rows, rank moves, a vetoed style's prompt change  <- CURRENT
2. [ ] the page, the pick route, the rank update
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-05T03:08:03Z created
- 2026-11-05T03:08:10Z set approved=True
- 2026-11-05T03:08:34Z blocked: approved; waits for a builder slot (lanes free as the merge queue lands)
- 2026-11-06T03:53:46Z unblocked
## Follow-ups captured

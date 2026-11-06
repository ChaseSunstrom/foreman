---
id: T-2919
type: RESEARCH
tier: S
status: done
priority: normal
scope: [state/projects/foreman-4a056f/research/genesis/not-yet.md]
depends_on: []
source: genesis
created: 2026-11-04T07:01:29Z
updated: 2026-11-04T09:32:09Z
base: 9fb71634ddb327bd60e553574efb745bf4d77aba
base_tree: 4d2dd279e0bfd8a01d0a0317baac4c8d7e77da05
plan0_at: 2026-11-04T07:02:44Z
plan0_scope: [state/projects/foreman-4a056f/research/genesis/not-yet.md]
paused_tree: 1d4651fccfaecfea4b2f442ae070c35ffc62d74e
verified: ok
unproven: [research-uncited, typed]
---
# Retry gen-4's eight not-yet items and file each one's retried: gen-4 line in not-yet.md, from fresh readings (the model bench for the four local backends, sampo burden for the goal card, the last ten closes for proof expiry, the ledger for M-12 and plan-time confirmation), so sampo rune check's not-yet part passes
## Raw request
> Retry gen-4's eight not-yet items and file each one's retried: gen-4 line in not-yet.md, from fresh readings (the model bench for the four local backends, sampo burden for the goal card, the last ten closes for proof expiry, the ledger for M-12 and plan-time confirmation), so sampo rune check's not-yet part passes
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] every not-yet item has a retried: gen-4 line naming what was re-read and whether the blocker holds, an item now evaluated (jeff: 0.52 intake type against the majority's 0.595 on run m20261103-223621959) carries its new blocker and two tried approaches, and sampo rune check prints no not-yet problem — verify with `sampo rune check`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] re-read each blocker against what exists now: sampo exam models show, sampo burden, the newest ten closes, the ledger's question_answered rows, TYPESAFE_BASE_URL
2. [x] write each retried: gen-4 line; sampo genesis put not-yet.md; sampo rune check
## Resume here
## Docs impact
## Verification evidence
- (step 1) `sampo exam models show; sampo burden; ls jeff-train and the aux env; git log of the last closes` → 8 blockers re-read: jeff evaluated (loses), Jevlike's stack exists, proofs-expire unblocked by T-2852/T-2851, five hold [tree 4d2dd279e0bf] (2026-11-04T07:04:19Z)
- (step 2) `sampo rune check` → exit 0 · ✓ frame: 0 added categories / ✓ read [ran] [tree 4d2dd279e0bf] [world 2f1906870a] (2026-11-04T07:05:24Z)
- (ac 1) `sampo rune check` → exit 0 · ✓ frame: 0 added categories / ✓ read [ran] [tree 1832fb900b22] [world 2f1906870a] (2026-11-04T09:32:08Z)
- (audit self) `self: re-read all eight retried: gen-4 lines against their sources (bench m20261103, burden 14 d, the last ten closes, the ledger); each names what was re-read and whether the blocker holds; rune check's not-yet part passes` → no findings [tree 1832fb900b22] (2026-11-04T09:32:08Z)
## Log
- 2026-11-04T07:01:29Z created
- 2026-11-04T07:01:37Z set source=genesis, approved=True
- 2026-11-04T07:02:41Z focused
- 2026-11-04T07:13:15Z paused: focus moved to T-2891
- 2026-11-04T09:32:09Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2742 [FEATURE L, planned, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias;…
- T-2913 [FEATURE M, planned, 4 steps] sampo goal plan reads the document a goal cites: the named file and section become the goal's items (each numbered entry and each DO…
- T-2489 [FEATURE M, done, 3 steps] Model layer surfaces: MCP decide tool, fm doctor backend health, the site's Model layer… — lesson: README has a 2000-word visible budge…
- decision 2026-10-31: [revisited: Mission 4: the goal ledger grows fm mandate] Mission 4 as built: the goal ledger lives on fm mandate's record (one standing goal: text, …
## Decision
Recommendation: keep all eight gen-4 not-yet items open; seven blockers hold on fresh readings, and the one whose unblock condition is now met (the theme port, T-2852 closed) moves to gen-5's build list rather than staying not-yet.

---
id: T-2631
type: FEATURE
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-02T18:49:23Z
updated: 2026-11-02T19:00:22Z
steer_method_rate: 0.192
---
# Treat "MOOMSHOT" as a real, working part of every generation of the tower, present in…
## Raw request
> Honestly integrate MOOMSHOT into each gen of the tower
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 19%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Treat "MOOMSHOT" as a real, working part of every generation of the tower, present in each gen's actual code path and not only in names, comments, config flags, or docs.
- Before integrating, find what MOOMSHOT is in the user's workspace (code, docs, notes, prior gens). If it can't be identified from what's there, ask once instead of guessing.
- Enumerate every existing generation of the tower, and apply the integration to each one. List the gens covered and any left out, with the reason.
- Make each gen's integration honest. No stubs, mocks, hard-coded outputs, dead or disabled code, or tests that pass without exercising MOOMSHOT. If something can't be integrated for real, say so plainly instead of faking it.
- Prove it per gen by running the build and tests, plus at least one check that fails when MOOMSHOT is removed or broken. Report the actual output, including failures and skipped steps.
- Cover every surface MOOMSHOT touches in each gen: interfaces, config, data and schemas, tests, docs and changelog, and any scripts or tooling that build or run the tower.
- Keep gens consistent. Where a gen has to differ, document the difference and the reason.
- Make this the default for every new gen of the tower. Integrate MOOMSHOT when a gen is created, and flag any gen that lacks it.
- Act directly in the working tree. Don't just advise or propose a plan.
- Keep changes reversible and local. Don't delete or overwrite existing gens without inspecting them first. Don't publish, push, deploy, or send anything outward unless the user has explicitly granted it.
- Don't claim MOOMSHOT is integrated in a gen until it has been verified there.
## Assumptions (confidence)
## Acceptance criteria
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-02T18:49:23Z created
- 2026-11-02T19:00:22Z dropped: folded into T-2626 (the same steer): its clauses are built there, and the two it added (list gens covered and left out; flag a gen lacking the campaign) are logged on T-2626 and built with a test
## Follow-ups captured

---
id: T-3480
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-06T18:33:00Z
updated: 2026-11-06T18:33:00Z
steer_method_rate: 0.218
---
# Any rule, discipline or standard the user has given for the merge lanes (verification,…
## Raw request
> and again, this stuff shouldnt just apply to the merge lanes, but everything, ou need to be aware of everything and all of your behavior, etc.
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Any rule, discipline or standard the user has given for the merge lanes (verification, evidence before claiming done, honest reporting, scope limits, naming, cleanup) is a standing rule for all Sampo work: planning, proving, finishing, every lane and stage, every kind of task, and Sampo's own condu…
- When the user states a rule in one context, treat it as global by default. Do not treat it as local unless they say it is. Ask "where else does this apply?" and apply it to every place it does.
- Keep the full set of the user's standing rules in view at all times: before acting, check the planned step against all of them, not only the ones that seem relevant to the current lane.
- Audit existing behavior now. List the lanes, stages, prompts, checks, docs and defaults that could break the rule, then fix each one. Do not stop at the one the user happened to mention.
- Cover every surface the rule touches: code paths, tests (add or update a test that would fail if the rule is broken), docs and prompts, config and defaults, and what Sampo reports to the user.
- Prove coverage with something checkable. Report which places were checked, what was changed, what was already compliant, and any place deliberately left alone, with the reason.
- Apply the rule to Sampo's own behavior as well as to the user's code. Self-reporting, handling of failures and skipped steps, how it asks for approval, and how it handles uncertainty all follow it.
- Act on this without waiting to be asked again. Do not just advise or acknowledge it, and do not make the user repeat the point lane by lane.
- Persist the rule where future sessions will see it (memory or the project's rules file), stated as global, so it survives context loss.
- Anything outward-facing, destructive or irreversible that the audit turns up (pushes, deletions, overwrites, external sends, merges to shared branches) stays behind the user's explicit grant. Generalizing the rule does not extend any earlier approval to new targets.
- If a rule's original wording is ambiguous about how it generalizes, choose the most sensible broad reading, state it, and proceed. Ask only when the readings would lead to materially different or irreversible actions.
- Recheck compliance whenever new lanes, tools or behaviors are added, so the rule stays global.
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
- 2026-11-06T18:33:00Z created
## Follow-ups captured

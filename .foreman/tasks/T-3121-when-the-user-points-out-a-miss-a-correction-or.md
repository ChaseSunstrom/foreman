---
id: T-3121
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-05T03:13:56Z
updated: 2026-11-05T03:13:56Z
steer_method_rate: 0.218
inferred_deps: [T-3123]
inferred_why: T-3123: generalized corrections build on the miss ledger
group: self-awareness and miss ledger
---
# When the user points out a miss, a correction, or a preference, generalize it into the…
## Raw request
> also think about how to make yourself more self aware and capture things like that in the future so I don't need to point them out, and fo everything thing
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- When the user points out a miss, a correction, or a preference, generalize it into the underlying pattern. Don't fix only the one instance they named.
- Sweep for every other place the same pattern applies (files, surfaces, tests, docs, configs, measures) and fix them all in the same pass.
- Record each such lesson as a durable standing rule or memory, so the user never has to repeat it in a later session. Update an existing entry rather than adding a duplicate.
- Before reporting work done, run a self-audit: ask what the user would likely point out next, such as missed surfaces, untested paths, stale docs, unhandled edge cases, or unverified claims. Fix those gaps first.
- Keep a checklist of the recurring kinds of gaps the user has flagged, and run it on every task so repeat misses are caught before the user sees them.
- Do the whole job ("do everything"). Don't stop at the first fix or hand back a partial list of suggestions. Act on each item, then verify it with a test, a check, or an inspection.
- Make each captured rule concrete and checkable: state the trigger, the required action, and how to confirm it was followed.
- At the end, report what was done, what was verified, what was skipped and why, and which new rules or memories were saved.
- Take local, reversible actions (edits, tests, memory and rule updates) without asking. Anything outward-facing, destructive, or irreversible (pushing, publishing, deleting, sending, spending) still needs the user's explicit grant, and a grant in one context doesn't carry to another.
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
- 2026-11-05T03:13:56Z created
## Follow-ups captured

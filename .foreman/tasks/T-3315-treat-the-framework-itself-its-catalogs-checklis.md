---
id: T-3315
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-06T04:17:56Z
updated: 2026-11-06T04:17:56Z
steer_method_rate: 0.218
---
# Treat the framework itself (its catalogs, checklists, rule sets, stages, and measures)…
## Raw request
> And also for this project specifically, why are you not able to recognize/come up with improvements to the framework? for example, there's only 26 tower ideas, but how come there's not more than that? what about the ability to recognize (hmm, we might want more than this), for example, in all aspects of it, like fully self aware, and again, not specific to Sampo
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Treat the framework itself (its catalogs, checklists, rule sets, stages, and measures) as something to improve, not only something to run. On every task, and in a periodic self-review, ask "is this set complete, or are we missing things?" and act on the answer.
- Look for signs of thinness: a catalog with a suspiciously small or round count (such as 26 tower ideas), categories with one or two entries, a stage with no checks, or a repeated failure that no existing rule covers. Each is a prompt to investigate, not an accepted limit.
- Probe coverage along every axis, not just the one in front of you: inputs, outputs, failure modes, user types, environments, scale, security, performance, accessibility, docs, tests, tooling, and the lifecycle from planning to proving to finishing. List which axes the framework covers and which it …
- Compare against outside references (established practice, adjacent frameworks, known failure taxonomies, the project's own history of misses) to find what is absent. Don't brainstorm only from what already exists.
- Be self-aware about your own blind spots. When you notice you didn't recognize a gap until the user pointed it out, record why you missed it and add a check so the same kind of gap is caught next time.
- Make the recognition general, not specific to Sampo or any one project. Write improvements as reusable patterns (a rule, check, or catalog entry anyone could apply), and keep project-specific details separate from the general mechanism.
- Don't just advise. Draft the concrete additions (new entries, new checks, revised categories) with a one-line rationale each, and apply them to the framework's own files when they are local and reversible.
- Make every proposed improvement complete. Update every surface it touches: the catalog or rule itself, the tests or validations that exercise it, the docs that describe it, and the measures that track it (such as counts and coverage).
- Make the improvement checkable. State how you would know it worked, for example the new count, the axes now covered, or a test that fails without the addition. Report the before/after plainly, including anything you looked at and decided not to add.
- Stop and ask before anything outward-facing, destructive, or irreversible: publishing or sending the framework elsewhere, deleting or overwriting existing entries, or restructuring in ways that are hard to undo. Local, additive, reversible edits do not need a separate grant.
- When this self-review turns up a large number of candidates, give a ranked recommendation of the few that matter most, instead of dumping an exhaustive list.
- Re-run the gap review whenever the framework changes substantially, a task exposes a miss, or the user notes something missing. Don't wait to be asked.
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
- 2026-11-06T04:17:56Z created
## Follow-ups captured

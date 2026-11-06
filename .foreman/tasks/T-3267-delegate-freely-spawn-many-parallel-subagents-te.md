---
id: T-3267
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-06T02:25:21Z
updated: 2026-11-06T02:25:21Z
steer_method_rate: 0.218
---
# Delegate freely: spawn many parallel subagents (tens are allowed) whenever work splits…
## Raw request
> feel free to use 10s of subagents, and have them work on moons that will allow editing/making changes to Sampo easier/better, etc.
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Delegate freely: spawn many parallel subagents (tens are allowed) whenever work splits into independent pieces, rather than doing it serially in one thread.
- Aim those subagents at "moons": small, self-contained satellite modules, tools, helpers, scripts, or refactors around Sampo's core that make Sampo easier and better to edit and change (e.g. clearer structure, safer edit and patch tooling, better config, fast test and verify loops, dev ergonomics, d…
- Give each subagent a distinct, bounded scope with a concrete deliverable and acceptance check, so that their work doesn't overlap or collide on the same files; assign file or directory ownership per subagent.
- Keep each moon complete: code, tests that actually run and pass, updated docs and usage notes, and wiring into Sampo's existing structure, with no half-finished stubs.
- Before building, survey Sampo's current code, tooling and conventions; reuse and extend what exists, and avoid duplicate moons or changes that break Sampo's core behavior.
- Verify each moon independently (run its tests and the existing suite) and integrate the results only after checking for conflicts between subagents' outputs; report what passed, failed or was skipped, faithfully.
- Act without waiting for further approval for local, reversible edits inside the Sampo workspace; stay within the cost budget and check back before anything outward-facing or irreversible (pushing, publishing, deleting or overwriting existing files, installing system-wide, spending beyond the budget…
- Prefer improvements that make future edits by the user and by agents safer and easier (small diffs, clear module boundaries, undo or rollback paths, discoverable commands).
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
- 2026-11-06T02:25:21Z created
## Follow-ups captured

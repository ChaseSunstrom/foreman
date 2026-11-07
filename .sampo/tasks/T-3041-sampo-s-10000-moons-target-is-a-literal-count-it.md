---
id: T-3041
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-04T23:56:18Z
updated: 2026-11-04T23:56:18Z
steer_method_rate: 0.218
---
# Sampo's "10000 moons" target is a literal count. It must produce 10000 distinct moons…
## Raw request
> and with the 10000 moons thing, I want it to literally output 10000 moons that will be used, not just in total, so the 300 number tat was kept, I want 10000 to be kept, and such, and you can do moons on anything related to sampo, like its problem solving, memory, effeciency, etc.
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Sampo's "10000 moons" target is a literal count. It must produce 10000 distinct moons that are actually used in the work, not a headline total, a budget figure, or a number that only appears in a summary.
- Raise the retained limit to match. Wherever Sampo currently keeps only 300 moons (cap, window, slice, truncation, pruning or storage limit), it must keep all 10000. Find every such limit and change it, rather than only the one that was noticed.
- The count must be consistent across the whole pipeline: generated, used, kept, persisted, reloaded and reported. If any stage drops or merges moons below 10000, treat it as a bug and fix it.
- Remove or parameterize hard-coded 300s and other stale numbers in code, config, prompts, docs, tests and UI text, so 10000 is one configurable value with one source of truth.
- Moons may cover any part of Sampo's work, not just one area. This includes problem solving, planning, proving, memory, efficiency, finishing and anything else related to Sampo. Each moon should be tagged with its area so it can be told apart and counted.
- Make the output inspectable. Sampo should emit or store the actual moons, one entry each, with an id and area, rather than only a count. A user must be able to list them and see that there are exactly 10000.
- Add checks for the requirement: a test or assertion that the generated, used and kept counts are each exactly 10000, that none are duplicated or empty, and that nothing is cut to 300 anywhere.
- Check that 10000 does not break speed, memory use, storage size, context or token limits. If it does, fix the design (batching, streaming, compact storage) while keeping the full count, rather than quietly lowering the number.
- Update the docs and any user-facing messages to describe the new behavior: 10000 moons used and kept, across all the areas.
- Make the changes directly and verify them by running the code and tests. Report the real counts you observed, and say plainly if any check fails or was skipped.
- Do not take outward, destructive or irreversible actions for this without the user's grant. That includes deleting or overwriting existing stored moons or data, publishing, and pushing or deploying. Look at the target first, and confirm before migrating or replacing existing data.
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
- 2026-11-04T23:56:18Z created
## Follow-ups captured

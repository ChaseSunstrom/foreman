---
id: T-3161
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-05T06:12:49Z
updated: 2026-11-05T06:12:49Z
steer_method_rate: 0.218
---
# Remove every cap on card counts in Sampo (per-run, per-deck, per-store, per-generation,…
## Raw request
> you don't need to cap card limits, and you can generate thousands or tens of thousands of them as well, again, we want sampo to work with small models completely by itself, with your level of capability, so anything to do that
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Remove every cap on card counts in Sampo (per-run, per-deck, per-store, per-generation, per-retrieval limits) across code, config defaults, schemas, CLI flags, tests and docs. Nothing may assume a small card library, and no stale limit may remain in help text or documentation.
- Generate cards at scale, thousands to tens of thousands, wherever that improves how small models perform. Don't stop at a modest set or ask whether to make more.
- Gate generated cards on quality: schema validation, deduplication, a check that each card is actionable for a small model, and provenance on every card. Quantity must not dilute quality.
- Make the system hold up at that volume. Storage, indexing and retrieval must stay fast, and selection must pick only the few relevant cards per task so a small model's context window is never flooded. Test it with large card sets and record the latency and memory numbers.
- The goal is that Sampo plans, proves and finishes software work by itself with small models, at the capability level of the assistant doing the work now, with no frontier model needed at runtime. Do whatever serves that, including cards, decomposition, prompts, tool scaffolding, verification loops,…
- Measure the goal. Run representative tasks on small models without help, compare pass rates against a baseline, keep the harness and results in the repo, and treat any regression as a defect to fix.
- Act directly: make the changes, run the generation, run the tests and report real results, including failures and anything skipped. Don't just advise.
- Keep outward or irreversible actions behind the user's grant. Without explicit approval, don't send content to external services, publish cards or models, spend beyond the stated budget, or delete or overwrite existing cards without inspecting them first. Prefer local generation and back up anythin…
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
- 2026-11-05T06:12:49Z created
## Follow-ups captured

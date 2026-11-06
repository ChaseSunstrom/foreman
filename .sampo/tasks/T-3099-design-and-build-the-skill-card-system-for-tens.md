---
id: T-3099
type: FEATURE
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-05T03:04:35Z
updated: 2026-11-05T04:44:35Z
steer_method_rate: 0.218
---
# Design and build the skill/card system for tens of thousands of entries (target 10,000+…
## Raw request
> and we will want 10s of thousands of skills/cards not just related to UI too, but all sorts of things
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Design and build the skill/card system for tens of thousands of entries (target 10,000+ to 50,000+). Treat that as the baseline scale, not a future stretch.
- Make the system domain-agnostic. Cards can cover any kind of work (UI, backend, data, infra, security, testing, docs, ops, research, writing, and others), and no schema field, type, category list, or UI assumes a UI-only or small-set world.
- Keep the card schema uniform and extensible: stable ID, title, domain/tags, trigger or applicability conditions, body, version, provenance, and status. New domains must be addable as data, with no code changes.
- Make retrieval scale. Use an index and search (tags, text, and embeddings or ranking where useful) so that only the few relevant cards are loaded into context. Never load or list the full set, and keep the context cost per task bounded regardless of library size.
- Store cards in a layout that stays workable at this size: sharded or hierarchical files or a database, lazy loading, and incremental index updates. Avoid a single giant file, a flat directory scan on every lookup, and O(n) work per request.
- Keep quality from degrading with size. Check for duplicates and near-duplicates, conflicts, stale or unused cards, and cards missing required fields. Support merge, deprecate, and retire, and track usage and outcomes to rank and prune.
- Validate automatically. Add a card linter or schema check, and add tests or benchmarks that run against a synthetic library of at least 10k–50k cards. These must cover retrieval latency, retrieval relevance across mixed domains, index build time, and memory use, with explicit thresholds.
- Make authoring and bulk import cheap: templates, batch generation or ingestion, and review tooling. Generated or imported cards must pass the same validation and carry provenance, so volume doesn't lower quality.
- Never hard-code domain-specific cards into core logic. Keep core logic generic and let domain content live in the card data.
- Update every surface this touches: schema, storage, indexer, retrieval, the UI for browsing/search/editing at scale (pagination, filtering, search, no rendering of everything at once), CLI/API, tests, and docs. Record the scale and multi-domain requirement in the docs.
- Act on this by default in design and implementation choices. When a choice would break at 10k+ cards or only fit UI content, change it rather than flag it.
- Ask before outward, destructive, or irreversible steps, such as publishing cards externally, bulk-deleting or overwriting existing cards, or running spending-heavy mass generation.
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
- 2026-11-05T03:04:35Z created
- 2026-11-05T04:44:35Z dropped: planned as T-3100 (cards at scale: 30,000 kept across 8+ grids, the site Cards page, UI examples) with parts T-3101 to T-3105
## Follow-ups captured

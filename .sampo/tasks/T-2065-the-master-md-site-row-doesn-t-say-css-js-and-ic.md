---
id: T-2065
type: CLEAN
tier: S
status: done
priority: normal
scope: [MASTER.md, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-30T00:24:07Z
updated: 2026-10-30T13:57:30Z
base: 8b675f9d28ec27d689364274352056fc8fc5993f
base_tree: d0bed52f430885c1f49c58db29e9e088ca62e093
plan0_at: 2026-10-30T13:54:26Z
plan0_scope: [MASTER.md, CHANGELOG.md]
verified: ok
---
# The MASTER.md `site/` row doesn't say CSS, JS and icon URLs carry content hashes; worth…
## Raw request
> the MASTER.md `site/` row doesn't say CSS, JS and icon URLs carry content hashes; worth a docs line
> (noticed by an agent; research T-2063-review)
## Interpretation
MASTER's site/ row gains one clause: build.py's _v gives the icon, style.css and site.js URLs a ?v=<8 hex of sha256> suffix on every built page and the landing (T-2060, T-2063), so a browser fetches the new file after a push.
## Assumptions (confidence)
## Acceptance criteria
- [x] MASTER's site/ row names the content-hash URLs and docs tests pass — verify with `python3 plugin/tests/run.py test_docs`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] add the clause to MASTER's site/ row
## Resume here
## Docs impact
MASTER site/ row
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 80 tests in 9.6s (21 classes, 16 at a time; slowest: Fences 9s, TaskLifecycle 2s, Site 1s) / OK [ran] [tree 2b3af7dd3a34] (2026-10-30T13:54:57Z)
- (audit self) `claude` → one docs clause; checked against site/build.py:23-28 (_v: sha256 hexdigest[:8], applied to foreman.svg, style.css, site.js); test_docs passes [tree 2b3af7dd3a34] (2026-10-30T13:55:12Z)
- (ac 1) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 80 tests in 8.2s (21 classes, 16 at a time; slowest: Fences 8s, TaskLifecycle 1s, Site 1s) / OK [ran] [tree 2b3af7dd3a34] (2026-10-30T13:57:02Z)
- (audit self) `one docs clause checked against site/build.py:23-28` → no findings [tree 2b3af7dd3a34] (2026-10-30T13:57:02Z)
- `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 80 tests in 8.2s (21 classes, 16 at a time; slowest: Fences 8s, TaskLifecycle 1s, Site 1s) / OK [ran] [tree 2b3af7dd3a34] (2026-10-30T13:57:27Z)
- (audit self) `one docs clause checked against site/build.py:23-28` → no findings [tree 2b3af7dd3a34] (2026-10-30T13:57:27Z)
## Log
- 2026-10-30T00:24:07Z created
- 2026-10-30T13:48:36Z set type=CLEAN, tier=S, scope=['MASTER.md', 'CHANGELOG.md']
- 2026-10-30T13:48:36Z planned: it has criteria and steps
- 2026-10-30T13:54:25Z focused
- 2026-10-30T13:54:43Z step 2 removed: add the ?v= content-hash clause to MASTER's site/ row
- 2026-10-30T13:57:29Z done
- 2026-10-30T13:57:30Z committed f75d900f (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2063-review: Verdict:** approve with nits. I found no defect I can trigger, only one LOW test gap. [stale: plugin/tests/test_site_build.py, site/build.py, sit…
- T-2063 [FEATURE M, done, 4 steps] Site polish: hashed CSS/JS URLs, drifting hero light, proof figures count up, pointer glow on feature cards — lesson: A favicon fix (T-…
- T-2087 [FIX M, done, 3 steps] Genesis page matches the site: shared header, footer and style.css tokens — lesson: A sub-page that loads the site stylesheet inherits its …
- decision 2026-10-04: Inbox build order: review family (T-0230, T-0232, T-0233, T-0235) and research family (T-0229, T-0237, T-0238, T-0239) are each built as one batch, …
## Preflight
Changed in scope since this was planned (2026-10-30): CHANGELOG.md, MASTER.md; re-ground the plan against them before editing
## Behaviour lock
none: a one-clause MASTER.md docs edit with no code or behaviour; test_docs ran after it
## Plan gaps
- added late: add the ?v= content-hash clause to MASTER's site/ row
## Files touched
- MASTER.md

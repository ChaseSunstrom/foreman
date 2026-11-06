---
id: T-3290
type: FEATURE
tier: M
status: planned
priority: normal
scope: [plugin/lib/sampo/seams.py, plugin/tests/test_seams.py, plugin/lib/sampo/louhi.py, plugin/lib/sampo/louhi_*.py, plugin/lib/sampo/cli.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-06T02:35:22Z
updated: 2026-11-06T02:36:53Z
rival_at: 2026-11-06T02:36:08Z
rival_split: true
builder: 2026-11-06T02:36:53Z
builder_model: haiku
builder_proc: archbox-hardened|pid:[4026531836]|2060851|807411
---
# Moon C-006917: sampo seams FILE finds the cleanest split clusters in a big sampo module (ranked by recent edits) and one real cluster moves out of louhi.py behind the same names
## Raw request
> Moon C-006917: sampo seams FILE finds the cleanest split clusters in a big sampo module (ranked by recent edits) and one real cluster moves out of louhi.py behind the same names
## Interpretation
Reading 1 (chosen): a seam finder (AST call-graph clusters of a module, hubs removed, ranked by recent edit churn) plus one real extraction of the top louhi.py cluster behind unchanged names. Reading 2 (ruled out): a generic cross-language splitter, too big for a lane. Partial: sampo task split (plugin/lib/sampo/split.py:60) splits tasks by file graph, not functions inside a file; T-3274 builds the module mover, this slice stays independent and only re-exports.
## Assumptions (confidence)
## Acceptance criteria
- [ ] sampo seams plugin/lib/sampo/louhi.py prints clusters (functions, lines, recent edit count) ranked, hubs excluded — verify with `python3 plugin/tests/run.py test_seams`
- [ ] the top-ranked louhi.py cluster of at most 250 lines lives in its own module and louhi still exposes every old name (sampo.louhi.NAME is the same object) — verify with `python3 plugin/tests/run.py test_seams`
- [ ] louhi tests still pass — verify with `python3 plugin/tests/run.py test_louhi`
## Non-goals
## Approach (options → choice → why)
1. AST-only finder plus extraction of the top cluster with re-export in louhi.py. Likely outcome: small, testable, louhi.py shrinks. Cluster must have no back-references into louhi.py (else take the next ranked); ranking is cleanness first (fewest boundary edges), churn as weight; imports are absolute (from sampo.louhi_x import a, b  # noqa: F401).
2. Use what exists: sampo task split / graph.db file edges (split.py:60). Likely outcome: no function-level edges there, needs a new extractor anyway.
3. Auto-rewrite files with a codemod for any cluster. fails if: clusters share module globals or tests monkeypatch louhi.NAME, which a moved copy would not see.
4. Do less: finder report only, no extraction. Likely outcome: no real payoff proven.

Choice 1 (82%): finder is ~60 lines of ast, the extraction proves the seam is real. Captured: none.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] write test_seams first: a tiny temp module with two independent call clusters plus a hub function; assert clusters, hub exclusion, ranking  <- CURRENT
2. [ ] seams.py: ast module-level call graph, drop hubs (degree>=8) and functions touching module-level mutable globals, connected components, rank by hunks from git log -U0 mapped to function line ranges
3. [ ] register the seams verb in cli.py with a small hook
4. [ ] run seams on louhi.py, move the best cluster (no shared mutable state, at most 250 lines) to louhi_<name>.py, re-export names in louhi.py, test identity of each name
5. [ ] CHANGELOG line
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T02:35:22Z created
- 2026-11-06T02:35:33Z set scope=['plugin/lib/sampo/seams.py', 'plugin/tests/test_seams.py', 'plugin/lib/sampo/louhi.py', 'plugin/lib/sampo/louhi_*.py', 'plugin/lib/sampo/cli.py', 'CHANGELOG.md']
- 2026-11-06T02:36:53Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3290.builder.md
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Two deliverables (likeliest):** a new `seams` subcommand in `plugin/lib/sampo/cli.py` (reached via `plugin/bin/sampo`) that takes FILE, builds a symbol/call graph, finds low-coupling clusters, and ranks them by recent edit activity (git log churn per symbol or line range). Plus one actual extract…
- **Tool only:** `seams` is the deliverable, and the louhi move is just a demonstration of its top suggestion. Less likely, since the title says "one real cluster moves".
- **Ranking inverted:** "cleanest" is primary (fewest edges crossing the cut) and "recent edits" is a tiebreaker or a filter. Versus recency as the main sort key, which would surface hot code that is not necessarily cleanly separable.
- **Different louhi:** `louhi.py` might not be under `plugin/lib/sampo/`. There could also be an `fm`-side twin, such as `fmlouhi.py`, given the `fmX.py` / `sampo/X.py` pairing in the test map. The move might then have to apply to both.
Approaches:
- **AST + union-find / min-cut on module-level names:** parse FILE with `ast`, build edges from function/class/constant references, and find connected components after removing hub names (shared helpers, imports). Score each cluster by the number of boundary edges divided by its size. Rank using `git…
- **Reuse existing sampo analysis:** check whether `plugin/lib/sampo/` already has an import-graph or "affected hubs" index (`test_affected_hubs.py` hints at one) and build `seams` on that. This avoids a second parser, but only works if it resolves symbols and not only files.
- **Extraction by script, not by hand:** have `seams` emit the cluster's name list, then move the source segments verbatim into `louhi_<x>.py` and add `from .louhi_<x> import a, b, c  # noqa: F401` plus an `__all__` update in `louhi.py`. This keeps the move reproducible and the diff reviewable.
- **Pick the cluster by running the tool on louhi.py:** take the highest-ranked cluster that has no back-references into the rest of `louhi.py`, which avoids circular imports. If the top cluster does need back-references, fall back to the next one.
Failure modes:
- **Circular import after the move:** the new module needs a name still in `louhi.py` (or module-level state initialised in `louhi.py`), so `from .louhi import ...` inside it fails at import time. This is hard to see in `seams` output if dynamic references like `globals()[name]` are not handled.
- **"Same names" broken for non-import users:** tests that `monkeypatch.setattr(louhi, "x", ...)` or `mock.patch("sampo.louhi.x")` patch the re-export and not the definition, so the patched function is no longer the one the moved code calls. `plugin/tests/` suites that cover louhi, and the gate `pyth…
- **Churn ranking is wrong or fragile:** `git log -L` is slow on a 2613-file repo and does not work at all here, since the working directory is not a git repository. `seams` must degrade clearly (no recency, say so) and not rank on empty data. Renames and the earlier `fm*`/`sampo/*` split also skew l…
- **Hub and constant handling gives false "clean" clusters:** if shared helpers, decorators, or module constants are excluded as noise, a cluster looks isolated while still depending on them. The extracted module then needs those imports, or a dependency that is invisible to the scorer is dropped.
## Dissent
- [x] rival reading: **Two deliverables (likeliest):** a new `seams` subcommand in `plugin/lib/sampo/cli.py` (reached via `plugin/bin/sampo`) that takes FILE, builds a symbol/call graph, finds low-coupling clusters, and ranks them by recent edit activity (git log churn per symbol or line range). Plus one actual extract… — answered: adopted: folded into Approach 1
- [x] rival reading: **Tool only:** `seams` is the deliverable, and the louhi move is just a demonstration of its top suggestion. Less likely, since the title says "one real cluster moves". — answered: rejected: the title says one real cluster moves, so extraction stays
- [x] rival reading: **Ranking inverted:** "cleanest" is primary (fewest edges crossing the cut) and "recent edits" is a tiebreaker or a filter. Versus recency as the main sort key, which would surface hot code that is not necessarily cleanly separable. — answered: adopted: cleanness first, churn weights it
- [x] rival reading: **Different louhi:** `louhi.py` might not be under `plugin/lib/sampo/`. There could also be an `fm`-side twin, such as `fmlouhi.py`, given the `fmX.py` / `sampo/X.py` pairing in the test map. The move might then have to apply to both. — answered: rejected: louhi.py is plugin/lib/sampo/louhi.py, checked with wc
- [x] rival approach: **AST + union-find / min-cut on module-level names:** parse FILE with `ast`, build edges from function/class/constant references, and find connected components after removing hub names (shared helpers, imports). Score each cluster by the number of boundary edges divided by its size. Rank using `git… — answered: adopted: folded into Approach 1
- [x] rival approach: **Reuse existing sampo analysis:** check whether `plugin/lib/sampo/` already has an import-graph or "affected hubs" index (`test_affected_hubs.py` hints at one) and build `seams` on that. This avoids a second parser, but only works if it resolves symbols and not only files. — answered: rejected: split.py has file edges only, no symbols
- [x] rival approach: **Extraction by script, not by hand:** have `seams` emit the cluster's name list, then move the source segments verbatim into `louhi_<x>.py` and add `from .louhi_<x> import a, b, c  # noqa: F401` plus an `__all__` update in `louhi.py`. This keeps the move reproducible and the diff reviewable. — answered: adopted: folded into Approach 1
- [x] rival approach: **Pick the cluster by running the tool on louhi.py:** take the highest-ranked cluster that has no back-references into the rest of `louhi.py`, which avoids circular imports. If the top cluster does need back-references, fall back to the next one. — answered: adopted: folded into Approach 1

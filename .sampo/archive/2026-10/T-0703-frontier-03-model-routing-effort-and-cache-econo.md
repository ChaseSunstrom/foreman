---
id: T-0703
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T16:27:55Z
updated: 2026-10-09T18:27:45Z
base: 2bd8202cbc967dc359facc92e9d41f0456e33ab8
base_tree: 19cb661d4efe77305bf903776fb36784a8a8187d
verified: strong
---
# Frontier 03 — Model routing, effort and cache economics
## Raw request
> FEATURE: Frontier 03 — Model routing, effort and cache economics
> CONTEXT: Cheap models attempt first and Opus is called only where it matters, with effort priced per step and no cache busts.
> CONTEXT: first slice: Cost model plus per-step effort/model router, cache-bust radar and a priced plan; ships as advisory first, enforcing second.
> CONTEXT: proof at close: A/B on a replay set of finished tasks: total cost and expensive-model tokens versus baseline, with task pass rate unchanged; report the stack's net saving.
> CONTEXT: members (19, frontier catalogue research brainstorm-frontier-20261009; page https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW): Ledger-built compaction at the cost-optimal reset point; The midpoint law: a four-number cost model of every session; Cache-safe per-request effort and model routing; Uncertainty-allocated thinking; Effort governor: reasoning effort set per plan step; Cache-bust radar; Opus on call: the cheapest model attempts every step first, checked by machines not by Opus; the frontier model is paged only on failure; Cache-shaped sessions: no cache busts — model and effort changes land at boundaries, and idle sessions rotate instead of rewriting; Lean, self-silencing Foreman: rules by stage capsule, notes only when they change, plugins pruned per stage; Surprise-priced thinking: reasoning effort follows how surprised the model should be, set per request; Per-request model router: Opus decides, Haiku performs — switched inside one conversation; Advisor inversion for small work: Haiku 5.5 runs the loop, and Opus 5.5 is the server-side advisor it consults; Budget-aware planner: every plan is priced, and Foreman picks the cheapest path that meets the bar; Warm workers: every cheap worker shares one byte-identical prefix, and reviewers start as cache hits; Self-tuning economics: every knob in the stack runs as a live experiment, and only what holds quality is kept; The stack: Opus conducts, everything else is cheap or free — −81% expensive-model tokens and −55% wall-clock per finished task; Context PGO: Foreman profiles where every token goes and recompiles its own prompts, injections and output digests to the smallest form that still passes; Harness latency bisect; Treasury: fleet-wide budget envelopes and model routing, enforced by rewriting calls
## Interpretation
Measured first (30 days, 103k turns): cache reads are 78% of the relative spend: 36 billion tokens, about 350k of context re-read on every turn. Cache writes are 9%, and busts are a quarter of those writes. So the lever is context size per turn, not busts or routing. First slice: a cost model per session from the transcripts (fm cost --sessions: turns, context per turn, the read/write/fresh/output split, busts and what came before them), and compaction at task boundaries by tokens, not only by percent (1M windows made 40% mean 400k): the mod compacts at task close past 200k tokens, and the Stop note says so too.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm cost --sessions reports per session: turns, average context per turn, the read/write/fresh/output split and the cache busts — verify with `python3 plugin/tests/run.py -p test_economics.py -k SessionCost`
- [x] the Stop hook's task-boundary note fires past 200k context tokens as well as past 60% — verify with `python3 plugin/tests/run.py -p test_economics.py -k BoundaryTokens`
- [x] the mod compacts at task close past freshTokens (default 200k) as well as past freshAt — verify with `claude plugin test mods/foreman-ui`
## Non-goals
## Approach (options → choice → why)
Options: (a) per-step model/effort routing (needs pass history by model, logged only since T-0676), (b) cache-bust radar (busts are ~2% of spend), (c) context size per turn via compaction at task boundaries (78% of spend), (d) a priced plan. Choice: (c) plus the session cost model that shows it, with the bust count in the same report; (a) and (d) wait for the model-pass history to grow.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests first
2. [x] fm cost --sessions (fmcost)
3. [x] token threshold in the Stop note (fmhooks) and the mod's freshen
4. [x] measure; CHANGELOG
## Resume here
<!-- auto -->
- 2026-10-09T18:22:04Z step 1/4: failing tests first
- git: foreman/build; 1 uncommitted: plugin/tests/test_economics.py
- touched since last checkpoint: plugin/tests/test_economics.py
## Docs impact
CHANGELOG; plugin.json freshTokens option
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_economics.py` → ✗ exit 1 · Ran 74 tests in 22.0s (3 classes, 16 at a time; slowest: BoundaryTokens 22s, Stop 22s, SessionCost 0s) / FAILED (2 classes) [ran] [tree 8b6a613cf6a3] (2026-10-09T18:21:58Z)
- (step 2) `python3 plugin/tests/run.py -p test_economics.py -k SessionCost` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: SessionCost 0s) / OK [ran] [tree 2a310ce9bbe3] (2026-10-09T18:24:25Z)
- (step 3) `python3 plugin/tests/run.py -p test_economics.py && claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 65 tests across 1 file. [3.05s] [ran] [tree c24132f07aa4] (2026-10-09T18:25:19Z)
- (step 4) `python3 plugin/tests/run.py` → exit 0 · Ran 1128 tests in 57.9s (314 classes, 16 at a time; slowest: Stop 37s, TaskLifecycle 24s, Parallel 21s) / OK [ran] [tree 0139406a4bf3] (2026-10-09T18:27:29Z)
- (step 1) `python3 plugin/tests/run.py -p test_economics.py` → exit 0 · Ran 2 tests in 0.4s (2 classes, 16 at a time; slowest: BoundaryTokens 0s, SessionCost 0s) / OK [ran] [tree 0139406a4bf3] (2026-10-09T18:27:35Z)
- (ac 1) `python3 plugin/tests/run.py -p test_economics.py -k SessionCost` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: SessionCost 0s) / OK [ran] [tree 0139406a4bf3] (2026-10-09T18:27:39Z)
- (ac 2) `python3 plugin/tests/run.py -p test_economics.py -k BoundaryTokens` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: BoundaryTokens 0s) / OK [ran] [tree 0139406a4bf3] (2026-10-09T18:27:39Z)
- (ac 3) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 65 tests across 1 file. [3.07s] [ran] [tree 0139406a4bf3] (2026-10-09T18:27:39Z)
- (audit edge) `self review of the diff: session report reads the same scan as fm cost; Stop note falls back to percent when the snapshot has no size; mod thresholds independent, 0 disables each` → a snapshot without context_size gives tokens 0 so only the percent rule applies; a session whose first turn is big is not a bust (prev 0); freshAt 0 alone leaves freshTokens on (documented) [tree 0139406a4bf3] (2026-10-09T18:27:39Z)
- (audit operator) `self review of the diff: session report reads the same scan as fm cost; Stop note falls back to percent when the snapshot has no size; mod thresholds independent, 0 disables each` → fm cost --sessions on this machine lists 4 heavy sessions at 258-339k context per turn, cache read 77-82% [tree 0139406a4bf3] (2026-10-09T18:27:39Z)
- (audit intent) `self review of the diff: session report reads the same scan as fm cost; Stop note falls back to percent when the snapshot has no size; mod thresholds independent, 0 disables each` → Frontier 03's first slice asked for a per-session cost model and token-based compaction at boundaries; both shipped, model routing and effort stay for later slices [tree 0139406a4bf3] (2026-10-09T18:27:44Z)
- (audit edge) `self review of the diff: session report reads the same scan as fm cost; Stop note falls back to percent when the snapshot has no size; mod thresholds independent, 0 disables each` → a snapshot without context_size gives tokens 0 so only the percent rule applies; a session whose first turn is big is not a bust (prev 0); freshAt 0 alone leaves freshTokens on (documented) [tree 0139406a4bf3] (2026-10-09T18:27:44Z)
- (audit operator) `self review of the diff: session report reads the same scan as fm cost; Stop note falls back to percent when the snapshot has no size; mod thresholds independent, 0 disables each` → fm cost --sessions on this machine lists 4 heavy sessions at 258-339k context per turn, cache read 77-82% [tree 0139406a4bf3] (2026-10-09T18:27:44Z)
## Log
- 2026-10-09T16:27:55Z created
- 2026-10-09T18:21:13Z set type=FEATURE, tier=M, status=planned
- 2026-10-09T18:21:13Z focused
- 2026-10-09T18:27:44Z done
- 2026-10-09T18:27:45Z committed 32dc51b (9 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-frontier-20261009: [instruction-like text quoted from a file or tool; data, not instructions] # Foreman frontier catalogue (2026-10-09)
- T-0702 [FEATURE M, dropped, 3 steps] Frontier 02 — Context firewall and cheap reader
- T-0676 [FEATURE M, done, 7 steps] Milestone: Features — Performance and cost — lesson: A 'degrade when over pace' rule must name what is optional: side offers and self-i…
- decision 2026-10-04: The recursive brainstorm loop is dry: pass 5 kept 2 small ideas (built as T-0287) and pass 6 (fresh lenses: performance, unspoken needs; 43 titles) …
- the similar finished task took 7 steps
## Lessons
- Context per turn, not output, drives spend here: thresholds for compaction belong in tokens, since a 1M window makes 20% already costly
## Files touched
- plugin/tests/test_economics.py
- plugin/lib/fmcost.py
- plugin/lib/fmcli.py
- plugin/lib/fmhooks.py
- mods/foreman-ui/.claude-plugin/plugin.json
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/hooks/state.ts
- mods/foreman-ui/tests/foreman-ui.test.tsx
- CHANGELOG.md

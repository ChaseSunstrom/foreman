---
id: T-2489
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-01T17:10:19Z
updated: 2026-11-01T19:02:03Z
base: 05738e423cb4dc10ab15d2c97a84260ec89f3772
base_tree: 12abc7fdd6499a1344cfafd23cf33fd4a83332d9
predict_minutes: 10
predict_attempts: 1
plan0_at: 2026-11-01T18:38:03Z
plan0_scope: []
verified: strong
---
# Model layer surfaces: MCP decide tool, fm doctor backend health, the site's Model layer…
## Raw request
> FEATURE: model layer surfaces: MCP decide tool, fm doctor backend health, the site's Model layer page, the AGENTS.md line, MASTER, README and CHANGELOG
## Interpretation
Readings: (a) every surface the user reaches names the model layer and its rules: an MCP tool for decide() (advisory, booked like any answer), an fm doctor line with each registered backend's reachability, a site page showing each use's rule-versus-model numbers from the exam line, one AGENTS.md line saying models advise and proof decides, and README; (b) a new verb. (a): gen-0 §6 forbids net new verbs, and the user's every-surface rule names MCP, the site and the docs.
## Assumptions (confidence)
## Acceptance criteria
- [x] the MCP decide tool answers through decide(), fm doctor lists the backends, the site renders a Model layer page from model_replay, and AGENTS.md names the rule — verify with `python3 plugin/tests/run.py test_mcp test_doctor test_site test_agents`
## Non-goals
## Approach (options → choice → why)
1) fmmcp gains a decide tool (kind, prompt, choices; sensitive projects local only, booked); fmdoctor gains a backends line (each registry entry: local or cloud, reachable or not; never a failure: no backend is a valid state); site/stats.py stores the newest model_replay and site/pages.py renders a Model layer page; fmagents' rules block gains one line; README gets a short section. Fails if: the AGENTS line pushes the block over its length test (it takes the shortest wording). 2) A new fm models verb. Fails if: the lean line goes red. 3) Use what exists: the MCP tool table, the doctor's check list, the site's page and stats registry, the AGENTS block. Likely outcome: five small additions. 4) Do less: docs only. Fails if: an MCP client or a reader of the site can't see what the layer decided. Choice 1 on 3 (85%).
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests per surface
2. [x] MCP tool, doctor line, site page, AGENTS line
3. [x] README, MASTER, CHANGELOG
## Resume here
<!-- auto -->
- 2026-11-01T18:38:22Z step 1/3: red tests per surface
- git: foreman/build; 0 uncommitted
## Docs impact
README.md, MASTER.md, CHANGELOG.md, site/pages.py
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_mcp.DecideTool test_doctor.ModelBackends test_site.ModelLayerPage test_agents.ModelLine` → ✗ exit 1 · Ran 4 tests in 0.4s (4 classes, 16 at a time; slowest: ModelBackends 0s, DecideTool 0s, ModelLayerPage 0s) / FAILED (4 classes: test_agents.ModelLine, test_doctor.ModelBackends, test_mcp.DecideTool, t [ran] [tree 239eceeca370] (2026-11-01T18:42:02Z)
- (step 2) `python3 plugin/tests/run.py test_mcp test_doctor test_site test_agents` → exit 0 · Ran 194 tests in 7.4s (79 classes, 16 at a time; slowest: Hook 5s, Header 5s, ViewsRepair 4s) / OK [ran] [tree a597502b18a9] (2026-11-01T18:43:54Z)
- (step 3) `python3 plugin/tests/run.py test_site.ModelLayerPage` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: ModelLayerPage 0s) / OK [ran] [tree a597502b18a9] (2026-11-01T18:44:58Z)
- `python3 plugin/tests/run.py test_mcp.DecideTool test_doctor.ModelBackends test_site.ModelLayerPage test_agents.ModelLine` → ✗ exit 1 · Ran 4 tests in 1.5s (4 classes, 16 at a time; slowest: DecideTool 0s, ModelBackends 0s, ModelLayerPage 0s) / FAILED (4 classes: test_agents.ModelLine, test_doctor.ModelBackends, test_mcp.DecideTool, t (start tree + this task's tests) [ran] [tree a597502b18a9] (2026-11-01T18:45:01Z)
- `python3 plugin/tests/run.py test_mcp.DecideTool test_doctor.ModelBackends test_site.ModelLayerPage test_agents.ModelLine` → exit 0 · Ran 4 tests in 0.4s (4 classes, 16 at a time; slowest: DecideTool 0s, ModelBackends 0s, ModelLayerPage 0s) / OK [ran] [tree a597502b18a9] (2026-11-01T18:45:01Z)
- (ac 1) `python3 plugin/tests/run.py test_mcp test_doctor test_site test_agents` → exit 0 · Ran 194 tests in 7.4s (79 classes, 16 at a time; slowest: Hook 5s, Header 5s, ViewsRepair 4s) / OK [ran] [tree 06d7a6b8252c] (2026-11-01T18:56:03Z)
- (audit intent) `self-review of the diff: the decide tool validates kind (slug), prompt (1-4000) and choices (2-12 strings) before any model call and books as mcp-KIND; fm mcp already refuses a sensitive project whole, so cloud backends are never reached from one; the doctor line is PASS-only and swallows registry errors; stats.models skips malformed exam lines; the page renders with and without figures` → every surface the plan named ships: the MCP tool, the doctor line, the site page, the AGENTS line, README/MASTER/CHANGELOG; each states the user's rules (models advise, proof decides; local first; live only by the exam) [tree 06d7a6b8252c] (2026-11-01T18:56:03Z)
- (audit edge) `self-review of the diff: the decide tool validates kind (slug), prompt (1-4000) and choices (2-12 strings) before any model call and books as mcp-KIND; fm mcp already refuses a sensitive project whole, so cloud backends are never reached from one; the doctor line is PASS-only and swallows registry errors; stats.models skips malformed exam lines; the page renders with and without figures` → no backend → decide returns None → tool says 'no backend answered' as an error; malformed exam.jsonl lines and a missing file give {}; registry raising → doctor PASS with the exception name [tree 06d7a6b8252c] (2026-11-01T18:56:03Z)
- (audit adversary) `self-review of the diff: the decide tool validates kind (slug), prompt (1-4000) and choices (2-12 strings) before any model call and books as mcp-KIND; fm mcp already refuses a sensitive project whole, so cloud backends are never reached from one; the doctor line is PASS-only and swallows registry errors; stats.models skips malformed exam lines; the page renders with and without figures` → an MCP caller's prompt goes to the model as data under DECIDE_SYSTEM, only a listed choice and a [0,1] number come back; kind is a slug so it cannot forge another use's rows in the book (mcp- prefix) [tree 06d7a6b8252c] (2026-11-01T18:56:03Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm ask: text in a file; a run of a documented command proves it (--yes-run) / · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a f [ran] [tree 06d7a6b8252c] (2026-11-01T18:57:22Z)
## Log
- 2026-11-01T17:10:19Z created
- 2026-11-01T18:20:28Z planned: it has criteria and steps
- 2026-11-01T18:20:29Z set approved=True
- 2026-11-01T18:38:02Z focused
- 2026-11-01T18:38:03Z predicted from its closes: 10 min, 1 attempt(s)
- 2026-11-01T18:45:04Z scope: fmmcp decide tool, fmdoctor check_model_backends, site stats.models + pages Model layer page, fmagents evidence line, README/MASTER/CHANGELOG
- 2026-11-01T18:56:53Z done
- 2026-11-01T18:56:56Z committed 7ba4f75d (12 files)
- 2026-11-01T18:57:22Z guard authorization added: publish
- 2026-11-01T19:02:03Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2127 [FEATURE M, done, 2 steps] Initiative surfaces: fm code, MCP tool, site page, pane line, MASTER, README, CHANGELOG (Mission 3 brief 8) — lesson: An allowed non-ze…
- T-2395 [FEATURE M, done, 4 steps] Proof surfaces (Mission 7, #6/#10): the rollup by kind on MCP, the pane, fm code, the AGENTS.md block, Desktop through MCP and a site p…
- T-2172 [FEATURE S, done, 2 steps] fm exam's surfaces: the exam scorecard isn't an MCP tool (so Desktop can't read it) and… — lesson: Put a new piece of state on the one …
- decision 2026-10-31: Standing rule (user steer 2026-10-31): gen 2 builds a model layer, small specialist models wherever a decision, ranking or lookup is the job, backen…
## Lessons
- README has a 2000-word visible budget (test_docs.ReadmeShape): a new section goes inside <details> from the start
## Plan gaps
- failed first: step 1 red tests per surface
## Files touched
- plugin/tests/test_agents.py
- plugin/tests/test_doctor.py
- plugin/tests/test_mcp.py
- plugin/tests/test_site.py
- plugin/lib/fmmcp.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmagents.py
- site/stats.py
- site/pages.py
- CHANGELOG.md
- MASTER.md
- README.md

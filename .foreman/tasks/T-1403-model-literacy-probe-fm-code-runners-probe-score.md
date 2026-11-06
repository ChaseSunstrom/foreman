---
id: T-1403
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcode.py, plugin/lib/fmcodebench.py, plugin/lib/fmcli.py, plugin/tests/test_code_bench.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-21T17:28:43Z
updated: 2026-10-23T10:15:12Z
inferred_deps: [T-1382]
inferred_why: T-1382: named in its request
group: runner checks, routing and config
base: 2de6404f9603fd457cd28b04a5b0d29722cf61f4
base_tree: 04ed1fe1a914bb0914cae80248a34233e9c66ae1
plan0_at: 2026-10-23T10:10:24Z
plan0_scope: [plugin/lib/fmcode.py, plugin/lib/fmcodebench.py, plugin/lib/fmcli.py, plugin/tests/test_code_bench.py, CHANGELOG.md]
verified: strong
---
# Model literacy probe: fm code runners --probe scores a model 0-10 on ten small graded prom
## Raw request
> FEATURE: Model literacy probe: fm code runners --probe scores a model 0-10 on ten small graded prompts (tagged data, JSON only, refuse to invent), and a prompt variant (an 'unknown' escape and an evidence quote) is measured on fm code bench before it becomes the default (S16, A22 B10)
> CONTEXT: round 2 of the fm/fm code brainstorm (T-1382): research/brainstorm-fm-anthropic-catalogue.md, grounding with file:line in research/brainstorm-fm-anthropic-half-a.md (A*) and half-b.md (B*)
> DONE-WHEN: a fake model that ignores the format scores under 3; fm code bench --json reports closed counts for both prompt variants
## Interpretation
fm code runners --probe MODEL sends ten small graded prompts to a model profile (four JSON-only shapes, two data-in-an-envelope, two 'unknown' over invented, one exact word, one sum) and scores it 0-10, naming the misses. fm code bench --variants base,evidence runs the seeds once per prompt variant (FM_PROMPT_VARIANT adds a short 'say unknown, read first, quote the line' note to the plan and act prompts) and reports each variant's closed count, each run recorded with its variant; base stays the default until the numbers say otherwise.
## Assumptions (confidence)
## Acceptance criteria
- [x] a fake model that ignores the format scores under 3 and one answering right scores 10; fm code bench --json reports closed counts for both prompt variants — verify with `python3 plugin/tests/run.py test_code_bench.Variants`
## Non-goals
## Approach (options → choice → why)
Options: an LLM judge for the probe (cost, a second model to trust); exact graders over tiny prompts; reuse bench seeds for the probe (minutes per model). Choice: exact graders (seconds, deterministic), and variants as an env-selected prompt suffix the bench toggles per run.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests, then PROBES/probe/--probe and VARIANTS with bench --variants
## Resume here
## Docs impact
CHANGELOG.md, MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code_bench.Variants` → ✗ exit 1 · Ran 2 tests in 0.8s (1 classes, 16 at a time; slowest: Variants 0s) / FAILED (1 classes) [ran] [tree ef988f7f07cc] (2026-10-23T10:10:32Z)
- (step 1) `python3 plugin/tests/run.py test_code_bench` → exit 0 · Ran 15 tests in 21.0s (3 classes, 16 at a time; slowest: Bench 21s, Variants 5s, Verdict 0s) / OK [ran] [tree c8a5f0e87649] (2026-10-23T10:13:23Z)
- (ac 1) `python3 plugin/tests/run.py test_code_bench.Variants` → exit 0 · Ran 2 tests in 3.1s (1 classes, 16 at a time; slowest: Variants 3s) / OK [ran] [tree c8a5f0e87649] (2026-10-23T10:13:40Z)
- (audit intent) `self review; test_code, test_code_bench, test_code_worker and test_cli green` → a fake model that ignores the format scores 0 (under 3) and one answering right scores 10; bench --variants base,evidence reports both closed counts and the evidence run's planner hears the note (tests) [tree c8a5f0e87649] (2026-10-23T10:13:40Z)
- (audit edge) `self review; test_code, test_code_bench, test_code_worker and test_cli green` → an unknown variant exits 2 naming the known ones; base clears FM_PROMPT_VARIANT for its run and the caller's value is put back after; a model error on a probe counts as a miss, never a crash [tree c8a5f0e87649] (2026-10-23T10:13:40Z)
## Log
- 2026-10-21T17:28:43Z created
- 2026-10-23T09:52:03Z set tier=M, scope=['plugin/lib/fmcode.py', 'plugin/lib/fmcodebench.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_code_bench.py', 'CHANGELOG.md']
- 2026-10-23T10:10:23Z focused
- 2026-10-23T10:15:10Z done
- 2026-10-23T10:15:12Z committed 21b9d80a (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1397 [FEATURE M, done, 1 steps] Intake offer: fm code prints one line when an indexed skill matches the request (name, lic — lesson: Stack cards name tools (cargo) mor…
- T-1400 [FEATURE M, done, 1 steps] A standing mandate: a sweeping request becomes one record (its text, its clauses from fm c — lesson: parse_ts returns a datetime, not e…
- research brainstorm-fm-anthropic-catalogue: Source: research/brainstorm-20261021-120257 (fm ideas, 10 lenses, 4 rounds, 3 deepened, --seen every earlier ideas.md: 520 ne…
- decision 2026-10-20: Slate, round 1: T-1254 cost per fully-correct session on the Benchmarks page; T-1255 the Claude Code version in every bench result; T-1256 piped tes…
- likely tests for the scope: plugin/tests/test_bench.py, plugin/tests/test_cli.py, plugin/tests/test_code.py
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmcode.py, plugin/lib/fmcodebench.py, plugin/tests/test_code_bench.py; re-ground the plan against them before editing
## Lessons
- Grade a model's format literacy with exact graders on tiny prompts before trusting it with a run: seconds, deterministic, and no second model to trust
## Plan gaps
- failed first: step 1 failing tests, then PROBES/probe/--probe and VARIANTS with bench --variants
## Files touched
- CHANGELOG.md
- plugin/lib/fmcli.py
- plugin/lib/fmcode.py
- plugin/lib/fmcodebench.py
- plugin/tests/test_code_bench.py

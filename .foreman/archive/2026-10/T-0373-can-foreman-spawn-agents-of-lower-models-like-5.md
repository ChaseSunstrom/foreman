---
id: T-0373
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmlanes.py, plugin/tests/test_builder.py, plugin/rules/foreman.md, plugin/skills/intake/references/delegate.md, plugin/evals/**, CHANGELOG.md, MASTER.md]
depends_on: []
source: user
created: 2026-10-09T00:07:20Z
updated: 2026-10-09T00:38:10Z
base: e6687b769c0e8f1e6ac9180bdbfcf479aecccc44
base_tree: dbd0c15a2486811f4722b04776f1ec3bb76e5600
verified: strong
---
# Model routing: subagents on the cheapest model that can do the job; builder lanes on Sonnet for S tasks
## Raw request
> can foreman spawn agents of lower models? like 5.5 haiku/sonnet? not everything needs to be opus if opus orchestrattes correctly, and or fable, ttrying to not consume too many tokens but being fast, efficient, correct, ect
## Interpretation
The user wants Opus (or Fable) to orchestrate and cheaper models to do the bulk: 'not everything needs to be opus'. Today fm-scout runs on haiku, fm-recon/reviewer/debugger on sonnet, every fm child run (ideas, research, oracle, second, bench) defaults to sonnet; only fm-builder inherits the main model, and the rules don't say which model to pick for a general-purpose agent.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm lane brief prints model: "sonnet" for an S task and leaves the main model for M — verify with `python3 plugin/tests/run.py -k test_builder_model_follows_the_tier`
- [x] rules and delegate.md name the routing (haiku lookups/summaries, sonnet recon/review/S builders/child runs, main model plans, judges, merges) within the rules budget — verify with `python3 plugin/tests/run.py -k test_description_budget`
## Non-goals
## Approach (options → choice → why)
(a) model: sonnet in fm-builder's frontmatter — M tasks lose the stronger model; (b) fm lane brief prints the Agent call with model by tier: S → sonnet, M → the main model; the main thread still reviews, merges and re-verifies; (c) a router command picking models from task text — speculative. Choice (b) plus one rules clause and a routing table in delegate.md.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first: lane brief model by tier
2. [x] rules + delegate.md routing table; eval sync
## Resume here
<!-- auto -->
- 2026-10-09T00:22:34Z step 1/2: test-first: lane brief model by tier
- git: foreman/build; 5 uncommitted: CHANGELOG.md, plugin/lib/fmguard.py, plugin/lib/fmlanes.py, plugin/tests/test_builder.py, plugin/tests/test_guard.py
- touched since last checkpoint: plugin/tests/test_builder.py, plugin/lib/fmlanes.py
## Docs impact
CHANGELOG.md; plugin/skills/intake/references/delegate.md routing table
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_builder_model_follows_the_tier` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Brief 0s) / OK [ran] [tree 90168bc94146] (2026-10-09T00:35:29Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (26 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                34.3    36.6     150  [0] / SessionEnd                  30.7    32.6     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 00:30 UTC; python3 plugin/tests/run.py → exit 0 · Ran 898 tests in [ran] [tree f66bcdceba70] (2026-10-09T00:37:55Z)
- (ac 1) `python3 plugin/tests/run.py -k test_builder_model_follows_the_tier` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Brief 0s) / OK [ran] [tree f66bcdceba70] (2026-10-09T00:38:03Z)
- (ac 2) `python3 plugin/tests/run.py -k test_description_budget` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: CoreIntegrity 0s) / OK [ran] [tree f66bcdceba70] (2026-10-09T00:38:03Z)
- (audit intent) `self: the routing is advice plus one mechanical default (S builder on Sonnet); the main thread still reviews, spot-checks and re-runs criteria; rules 5997/6000` → Opus/Fable orchestrate, cheaper models do lookups, recon, review, S builds and child runs; already true for scout/recon/reviewer/debugger/child runs, now the builder and general-purpose agents too [tree f66bcdceba70] (2026-10-09T00:38:03Z)
- (audit operator) `self: the routing is advice plus one mechanical default (S builder on Sonnet); the main thread still reviews, spot-checks and re-runs criteria; rules 5997/6000` → no new cost path; rules trimmed to stay in budget; evals resynced [tree f66bcdceba70] (2026-10-09T00:38:03Z)
- (audit intent) `self: the routing is advice plus one mechanical default (S builder on Sonnet); the main thread still reviews, spot-checks and re-runs criteria; rules 5997/6000` → Opus/Fable orchestrate, cheaper models do lookups, recon, review, S builds and child runs [tree f66bcdceba70] (2026-10-09T00:38:10Z)
- (audit operator) `self: the routing is advice plus one mechanical default (S builder on Sonnet); the main thread still reviews, spot-checks and re-runs criteria; rules 5997/6000` → no new cost path; rules trimmed to stay in budget; evals resynced [tree f66bcdceba70] (2026-10-09T00:38:10Z)
- (audit adversary) `self: the routing is advice plus one mechanical default (S builder on Sonnet); the main thread still reviews, spot-checks and re-runs criteria; rules 5997/6000` → the guard eval prompts changed only by re-embedding the rules (sync_evals.py); no guard logic or eval expectation changed [tree f66bcdceba70] (2026-10-09T00:38:10Z)
## Log
- 2026-10-09T00:07:20Z created
- 2026-10-09T00:19:40Z planned from capture
- 2026-10-09T00:19:40Z set approved=True
- 2026-10-09T00:21:46Z focused
- 2026-10-09T00:22:34Z paused: back to T-0370 to finish its adversary pass with the real-bash differential test
- 2026-10-09T00:22:35Z paused: focus moved to T-0370
- 2026-10-09T00:35:28Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-09T00:35:28Z focused
- 2026-10-09T00:38:10Z done
- 2026-10-09T00:38:10Z committed 3a14914 (10 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0206 [FEATURE M, done, 3 steps] fm research ask: recall first, parallel web researchers per sub-question, every quoted claim re-fetched and checked, one note recorded …
- T-0205 [FEATURE M, done, 3 steps] fm next names the installed third-party skills that fit a task's stage — lesson: Keyword routing over skill descriptions needs the firs…
- T-0207 [FEATURE M, done, 3 steps] Debugging ledger: hypotheses in the brief that fm next drives, and a fresh-eyes fm-debugger agent — lesson: Any new free-text field wri…
- decision 2026-09-27: Build the smarter-Foreman slate, and further self-improvement rounds, as a candidate in a git worktree (~/.claude/foreman-improve-20260926, branch i…
- likely tests for the scope: plugin/tests/test_lanes.py
## Lessons
- Most of the routing already existed in agent frontmatter; the gap was the one agent without a model line and the rules never saying 'cheapest model that can'
## Files touched
- plugin/tests/test_builder.py
- plugin/lib/fmlanes.py
- plugin/rules/foreman.md
- plugin/evals/guard-force-push/prompt.md
- plugin/evals/guard-publish/prompt.md
- plugin/evals/intake-block/prompt.md
- plugin/evals/mid-task-capture/prompt.md
- plugin/evals/one-liner/prompt.md
- plugin/skills/intake/references/delegate.md
- CHANGELOG.md

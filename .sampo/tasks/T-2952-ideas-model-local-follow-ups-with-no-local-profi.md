---
id: T-2952
type: CLEAN
tier: S
status: active
priority: normal
scope: [plugin/lib/sampo/ideas.py, plugin/lib/sampo/cli.py, plugin/tests/test_ideas.py, plugin/lib/sampo/moonscale.py]
depends_on: []
source: discovered
created: 2026-11-04T10:08:30Z
updated: 2026-11-06T06:10:40Z
lane: ~/.claude/foreman/.claude/worktrees/agent-a75b1a8cb91ae5081
lane_branch: worktree-agent-a75b1a8cb91ae5081
base: 0e503eeeeb87000325d02673ba119e35ff08b7e8
base_tree: 5c2bb7b2f14ef72b4659b9d747b61d1c44bc9aca
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T05:54:10Z
plan0_scope: [plugin/lib/sampo/ideas.py, plugin/lib/sampo/cli.py, plugin/tests/test_ideas.py]
---
# Ideas --model local follow-ups: with no local profile all lenses run on one thread at up…
## Raw request
> Ideas --model local follow-ups: with no local profile all lenses run on one thread at up to 300 s each (use one worker per lens), args.timeout is ignored on the local path, paid=0 isn't threaded so the per-command cap misses Haiku children, cmd_oracle ignores --model local; and cli.py:1969 still says 'add a MASTER.md File map row' when rows live in docs/map shards (T-2910, T-2915 audits)
## Interpretation
Reading 1 (taken): five small follow-ups from the T-2910 and T-2915 audits, each fixed with a test: lenses on the local path run one worker per lens, the local path honours args.timeout, paid calls are counted so the per-command cap sees Haiku children, cmd_oracle takes --model local, and cli.py's hint names the docs/map shard instead of a MASTER.md File map row. Reading 2 (ruled out): rework ideas' model routing: these are point fixes.
## Assumptions (confidence)
## Acceptance criteria
- [ ] With no local profile, the local path runs one worker per lens instead of all lenses on one thread — verify with `python3 plugin/tests/run.py test_ideas`
- [ ] The local path honours args.timeout instead of a fixed 300 s — verify with `python3 plugin/tests/run.py test_ideas`
- [ ] paid is threaded through the local path, so the per-command cap counts Haiku children — verify with `python3 plugin/tests/run.py test_ideas`
- [ ] cmd_oracle takes --model local like ideas — verify with `python3 plugin/tests/run.py test_ideas`
- [ ] cli.py's hint names the docs/map shard row instead of 'add a MASTER.md File map row' — verify with `python3 plugin/tests/run.py test_ideas`
## Non-goals
## Approach (options → choice → why)
1) use what exists: each fix where its value is read (ideas.py's local round, _ask's paid count, cmd_oracle's model arg, cli.py:1969's hint): likely outcome: five small diffs, each with a test. 2) do less: the hint only: fails if: the cap still misses Haiku children (a spend leak). Choice 1 (90%).
## Risks and rollback
## Execution prompt
## Steps
1. [x] the five fixes, test first
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_ideas` → exit 0 · Ran 32 tests in 177.8s (23 jobs, 16 at a time; slowest: Ideas.test_the_pack_is_one_cached_system_prompt_and_the_first_child_warms_it 4s, BoardIdeas 3s, Ideas.test_brainstorms_learn_from_the_asks_they_ (ran] (tree 2f1081cb5ff5] (world 2f1906870a] (2026-11-06T06:10:40Z)
## Log
- 2026-11-04T10:08:30Z created
- 2026-11-05T02:07:04Z set scope=['plugin/lib/sampo/ideas.py', 'plugin/lib/sampo/cli.py', 'plugin/tests/test_ideas.py']
- 2026-11-05T02:07:07Z planned: it has criteria and steps
- 2026-11-05T02:07:07Z set approved=True
- 2026-11-05T02:07:07Z blocked: planned; waits for a builder slot (6 of 6 out until the merge chain lands them)
- 2026-11-06T03:53:30Z unblocked
- 2026-11-06T05:54:08Z focused
- 2026-11-06T05:54:10Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T05:58:19Z set scope=['plugin/lib/sampo/ideas.py', 'plugin/lib/sampo/cli.py', 'plugin/tests/test_ideas.py', 'plugin/lib/sampo/moonscale.py']
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2915 [FEATURE M, done, 4 steps] MASTER.md opens whole in one Read: each over-long section moves to docs/map shards, MASTER.md keeps a one-line-per-entry index with lin…
- T-2756 [FIX S, done, 1 steps] fm doctor's steer-check hint says 'fm decide … --check CMD --revisited WORDS', but a row… — lesson: Key a dedupe on the stable identifier (…
- T-3222 [FEATURE L, done, 5 steps] Network and filesystem sandboxing as a Sampo feature: one sampo sandbox verb that turns… — lesson: running the whole suite inside the n…
- decision 2026-10-16: Foreman Code (T-1207) is built as fm code: Foreman's own loop where the harness runs the stations and models fill small JSON slots, over one stdlib …
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_ideas.py, plugin/tests/test_mint.py, plugin/tests/test_rename_scan.py, plugin/tests/test_verify_alias.py
## Preflight
Changed in scope since this was planned (2026-11-04): plugin/lib/sampo/cli.py; re-ground the plan against them before editing

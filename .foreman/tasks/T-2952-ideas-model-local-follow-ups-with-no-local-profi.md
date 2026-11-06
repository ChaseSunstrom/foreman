---
id: T-2952
type: CLEAN
tier: S
status: planned
priority: normal
scope: [plugin/lib/sampo/ideas.py, plugin/lib/sampo/cli.py, plugin/tests/test_ideas.py]
depends_on: []
source: discovered
created: 2026-11-04T10:08:30Z
updated: 2026-11-06T03:53:30Z
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
1. [ ] the five fixes, test first  <- CURRENT
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-04T10:08:30Z created
- 2026-11-05T02:07:04Z set scope=['plugin/lib/sampo/ideas.py', 'plugin/lib/sampo/cli.py', 'plugin/tests/test_ideas.py']
- 2026-11-05T02:07:07Z planned: it has criteria and steps
- 2026-11-05T02:07:07Z set approved=True
- 2026-11-05T02:07:07Z blocked: planned; waits for a builder slot (6 of 6 out until the merge chain lands them)
- 2026-11-06T03:53:30Z unblocked
## Follow-ups captured

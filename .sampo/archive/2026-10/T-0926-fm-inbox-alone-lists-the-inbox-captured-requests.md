---
id: T-0926
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T19:36:11Z
updated: 2026-10-15T19:36:49Z
base: d364fd6a500e3bc9ec9888a133dc4c3e71a88ff5
base_tree: a7de1f9da260af220ea9498c65f0dc845710d4ca
verified: strong
---
# fm inbox alone lists the inbox (captured requests), as fm --help says; fm inbox gh still reads GitHub issues
## Raw request
> fm inbox alone lists the inbox (captured requests), as fm --help says; fm inbox gh still reads GitHub issues
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] bare fm inbox lists captured items and exits 0; fm inbox gh keeps its behaviour — verify with `python3 plugin/tests/run.py -k InboxList`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test, then source optional and a listing in fmeco.cmd_inbox
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py -k InboxList` → ✗ exit 1 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: InboxList 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 88e9cd426faa] (2026-10-15T19:36:46Z)
- `python3 plugin/tests/run.py -k InboxList` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: InboxList 0s) / OK [ran] [tree 88e9cd426faa] (2026-10-15T19:36:46Z)
- (ac 1) `python3 plugin/tests/run.py -k InboxList` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: InboxList 0s) / OK [ran] [tree 88e9cd426faa] (2026-10-15T19:36:48Z)
- (step 1) `python3 plugin/tests/run.py -k Help` → exit 0 · Ran 3 tests in 0.8s (1 classes, 16 at a time; slowest: Help 1s) / OK [ran] [tree 88e9cd426faa] (2026-10-15T19:36:48Z)
- (audit edge) `self: found by the product sweep (18 main commands; 17 clean): bare fm inbox now lists the captured requests ranked as STATE ranks them (text and --json); fm inbox gh is unchanged` → an empty inbox says Empty.; --repo/--limit without gh are ignored, as before they were unreachable [tree 88e9cd426faa] (2026-10-15T19:36:48Z)
- (audit self) `self: found by the product sweep (18 main commands; 17 clean): bare fm inbox now lists the captured requests ranked as STATE ranks them (text and --json); fm inbox gh is unchanged` → no findings [tree 88e9cd426faa] (2026-10-15T19:36:48Z)
## Log
- 2026-10-15T19:36:11Z created
- 2026-10-15T19:36:12Z focused
- 2026-10-15T19:36:48Z done
- 2026-10-15T19:36:49Z committed bd9f1d0 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0854 [FIX M, done, 5 steps] A newcomer's first fm commands make sense: short --help, task new shows its values and an example, init/status say what… — lesson: The firs…
- T-0673 [FEATURE M, done, 7 steps] Milestone: Features — Multi-machine, multi-project and ecosystem — lesson: a capture into another project must not run that project's e…
- T-0438 [FEATURE S, done, 2 steps] Capture flags a re-ask of dropped work and a veto contradiction — lesson: Remember the user's 'no' at the door: capture is the cheapest…
- decision 2026-09-26: Order after T-0016: T-0022 and T-0023 (user requests, explore items: take the recommendation after self-critique in full autonomy), then T-0018's ro…
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/fmcli.py
- plugin/lib/fmeco.py

---
id: T-3119
type: PERFORMANCE
tier: M
status: planned
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-05T03:13:12Z
updated: 2026-11-06T03:53:34Z
rival_at: 2026-11-05T05:47:11Z
rival_split: true
---
# Merge trains: land several green lanes with one self-change gate run and one suite run, bisecting a red train to the lane that broke it
## Raw request
> merge train: land several green lanes at once: merge them in order into a scratch tree, run the self-change gate and the suite once on the result, then move main to it; on red, bisect the train to the lane that broke it and land the rest; one bench and one suite per train instead of per lane
## Interpretation
Reading 1 (chosen): sampo lane merge A B C merges the lanes in order into a scratch worktree of main, runs the self-change gate once on the combined diff and the full suite once, then fast-forwards main to the train's result with one merge commit per lane kept in history; a red train is bisected (halves) to the first lane that turns it red, which stays out with the reason while the rest land. Reading 2: run each lane's tests in parallel worktrees; rejected, lanes that pass alone can still break together, and a train tests the combination that lands.
## Assumptions (confidence)
## Acceptance criteria
- [ ] sampo lane merge T-A T-B T-C lands all three with one gate run and one suite run on the combined tree, main gets one merge commit per lane in order, and each task records it merged in a train — verify with `python3 plugin/tests/run.py test_lanes`
- [ ] a train whose suite is red is bisected: the lane that turns it red stays unmerged with the failing test named, the others land; a conflict between two lanes in the train leaves the later one out with its conflict brief — verify with `python3 plugin/tests/run.py test_lanes`
- [ ] parallel pre-verification: sampo lane merge --all checks every finished lane at once, each in its own scratch tree of main plus that lane (the self-change gate and the criteria there, up to the cap's worth at a time), then lands the green ones one after another in seconds; a lane is re-checked only when a lane landed before it touched the same files — verify with `python3 plugin/tests/run.py test_lanes`
- [ ] no GIL bottleneck: each lane's parallel check runs in its own process (a subprocess per lane: its own sampo, gate bench and test runner), never as threads in one interpreter; a test runs two fake checks that each burn 1 s of CPU and finishes in well under 2 s — verify with `python3 plugin/tests/run.py test_lanes`
- [ ] the self-change gate's timing bench never runs beside another bench: a bench lock serialises benches while every other check runs in parallel — verify with `python3 plugin/tests/run.py test_lanes`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: lanes.merge's steps (guard check, selfgate.gate, conflict brief) applied to a scratch tree, then a fast-forward; likely outcome: N lanes cost one gate and one suite. 2. Do less: batch only the suite; fails if: the gate's bench, the slow part, still runs N times. 3. Speculative parallel trains; fails if: the extra worktrees' load skews each other's gate. Choice 1 (75%)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests: a green train of three, a red train bisected, a conflict inside the train  <- CURRENT
2. [ ] the train in lanes.merge and the CLI form
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-05T03:13:12Z created
- 2026-11-05T03:23:18Z planned from capture
- 2026-11-05T03:23:19Z set approved=True
- 2026-11-05T03:23:19Z blocked: approved; builder slot after T-3091
- 2026-11-05T04:50:15Z user 2026-11-05: 'what about merges in parallel? so they go quicker?' (asked three times): the checks run in parallel, the landing stays serial (seconds); first builder after T-3135
- 2026-11-05T04:50:16Z set tier=M
- 2026-11-05T04:51:16Z user 2026-11-05: 'make sure it isnt bottlenecked by the python GIL': this machine's python3 is 3.14.8 with the GIL on, so parallel checks are processes, not threads
- 2026-11-05T05:46:51Z unblocked
- 2026-11-05T05:47:18Z grounding: T-3141 (land-then-verify, queued to merge) already moves the per-lane suite off main's critical path and reverts a red merge; the train must compose with it: one combined post-merge verify per train, bisect on red reusing T-3141's revert; T-3139's module map and T-3140's cache make each parallel scratch-tree check cheap; build after T-3141 and T-3139 land
- 2026-11-05T06:41:31Z measured 2026-11-05: quiet-merge.sh waited 46 min for T-3087 because the main thread's own evidence runs and closes kept the main checkout busy; merges must not need a quiet main checkout: verify in a scratch tree (T-3141) and move main by a ref update at the end, so the main thread's runs and merges stop starving each other
- 2026-11-05T06:43:39Z dissent 1 (resolved with a placeholder by mistake): adopted in spirit: the train is sampo lane merge with several ids, the existing verb, not a new subcommand
- 2026-11-05T06:43:48Z blocked: plan ready; builds after T-3139 and T-3141 merge (both queued in the merge chain), since the train reuses T-3141's revert and T-3139's module map
- 2026-11-06T03:53:33Z unblocked
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: a new `fm` subcommand (probably in `plugin/lib/fmcli.py`, with git plumbing in `plugin/lib/fmcore.py`) that takes N already-green lane branches, merges them in order into a scratch worktree, runs the self-change gate and `plugin/tests/run.py` once on the combined result, then fast-forwar…
- Alternative: this is a change to the existing per-lane landing path (whatever `fmcli.py` currently uses to land one lane), generalized so a batch of one equals today's behaviour, rather than a separate command.
- Alternative: a CI-style queue (lanes enqueue, a daemon forms trains). "Land several at once" and "per train" hint at batching, but nothing in the request mentions a queue or daemon, so I treat it as less likely.
- Ambiguity: "one bench and one suite per train" may mean the bench (`plugin/tests/bench_hooks.py --runs 20`) runs once on the train tip, or that the bench is skipped unless the train touches hooks. The request reads as the former.
Approaches:
- Scratch worktree plus ordered merge: `git worktree add` a temp tree off `main`, merge each lane with `--no-ff`, and stop at the first merge conflict, attributing it to that lane. Then run the gates once, and finally `git update-ref refs/heads/main <tip> <old-main>` as a compare-and-swap so a concur…
- Bisect by prefix: on red, binary-search the smallest failing prefix of the ordered lane list. Rebuild the scratch tree for each probe and rerun the suite. Eject the lane at that index and re-form the train from the remaining lanes, then rerun the gates once on the final set. This costs about log2(N…
- Reuse the existing gate runners: call the same functions that the single-lane path uses for the self-change gate and `run.py`, passing the scratch worktree path, instead of writing a second gate runner. That keeps one definition of "green".
- Put train state in a small record, such as lanes, order, tip, and ejected lanes with reasons. `fm replay` and `fm doctor` can then inspect a half-finished train, and a crash leaves the scratch worktree discoverable and cleanable.
Failure modes:
- Prefix bisection assumes a monotone failure: a lane that fails only in combination with a later lane, or a flaky test, makes the bisect eject the wrong lane or none. This needs an explicit result for "the prefix is green but the full train is red" (an interaction failure), and a rerun policy for fl…
- The self-change gate probably inspects the diff against `main` to decide what to check. Run on a combined tree, it can attribute changes to the wrong lane or miss per-lane rules. It might also read the live checkout instead of the scratch worktree's path, which would make it pass vacuously.
- `main` moves while the train runs, for example when a direct landing or another train finishes. If the final update isn't a compare-and-swap, it silently discards that commit. If it is, the train needs a defined retry: rebase the scratch tree and rerun the gates, rather than landing stale results.
- Hooks and caches (`fmhooks.py`, `fmguard.py`) may assume a single checkout, so merges, commits, or guards in a second worktree can trip guards, write state into the main tree, or leave stale worktrees and `.git/worktrees` entries after a failed train.
## Dissent
- [x] rival reading: Likeliest: a new `fm` subcommand (probably in `plugin/lib/fmcli.py`, with git plumbing in `plugin/lib/fmcore.py`) that takes N already-green lane branches, merges them in order into a scratch worktree, runs the self-change gate and `plugin/tests/run.py` once on the combined result, then fast-forwar… — answered: x
- [x] rival reading: Alternative: this is a change to the existing per-lane landing path (whatever `fmcli.py` currently uses to land one lane), generalized so a batch of one equals today's behaviour, rather than a separate command. — answered: adopted: the train generalises lane merge, a train of one is today's merge
- [x] rival reading: Alternative: a CI-style queue (lanes enqueue, a daemon forms trains). "Land several at once" and "per train" hint at batching, but nothing in the request mentions a queue or daemon, so I treat it as less likely. — answered: rejected: no daemon; the train forms from the ids given or --all
- [x] rival reading: Ambiguity: "one bench and one suite per train" may mean the bench (`plugin/tests/bench_hooks.py --runs 20`) runs once on the train tip, or that the bench is skipped unless the train touches hooks. The request reads as the former. — answered: adopted: the bench and the suite run once on the train's tip
- [x] rival approach: Scratch worktree plus ordered merge: `git worktree add` a temp tree off `main`, merge each lane with `--no-ff`, and stop at the first merge conflict, attributing it to that lane. Then run the gates once, and finally `git update-ref refs/heads/main <tip> <old-main>` as a compare-and-swap so a concur… — answered: adopted: scratch worktree off main, --no-ff per lane in order, a conflict ejects that lane, main moves by git update-ref main <tip> <old> (compare-and-swap) so the main checkout needn't be quiet (the…
- [x] rival approach: Bisect by prefix: on red, binary-search the smallest failing prefix of the ordered lane list. Rebuild the scratch tree for each probe and rerun the suite. Eject the lane at that index and re-form the train from the remaining lanes, then rerun the gates once on the final set. This costs about log2(N… — answered: adopted: bisect by prefix on red, eject the first failing lane, rerun the rest once
- [x] rival approach: Reuse the existing gate runners: call the same functions that the single-lane path uses for the self-change gate and `run.py`, passing the scratch worktree path, instead of writing a second gate runner. That keeps one definition of "green". — answered: adopted: the single-lane path's gate functions run with the scratch tree's path; one definition of green
- [x] rival approach: Put train state in a small record, such as lanes, order, tip, and ejected lanes with reasons. `fm replay` and `fm doctor` can then inspect a half-finished train, and a crash leaves the scratch worktree discoverable and cleanable. — answered: adopted: a train record (lanes, order, tip, ejected with reasons) in the project state, so a crash leaves it findable and cleanable

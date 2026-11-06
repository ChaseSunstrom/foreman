---
id: T-2430
type: FIX
tier: M
status: done
priority: normal
scope: [plugin/lib/fmpr.py, plugin/tests/test_pr.py, MASTER.md, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-31T17:18:02Z
updated: 2026-11-02T03:11:08Z
base: a044df9bee83da2a81840a659069d9e28c01cb4d
base_tree: 9cd9fdfb9525eed971e9bf1b25998e4d83f7021c
predict_minutes: 9
predict_attempts: 1
plan0_at: 2026-11-02T02:57:09Z
plan0_scope: [plugin/lib/fmpr.py, plugin/tests/test_pr.py, MASTER.md, CHANGELOG.md]
verified: strong
---
# fm pr train runs the self-change gate on each PR head before merging it
## Raw request
> fm pr train (fmpr.py:139) merges GitHub PRs with gh pr merge, bypassing fm lane merge's file guard and T-2352's self-change gate: gate Foreman-repo PRs too
## Interpretation
Reading 1: fm pr train (fmpr.py) merges re-tested PRs with gh pr merge and never calls fmselfgate.gate, so a PR that changes Foreman's own plugin/ (a weaker guard, a slower hook, a bigger footprint) lands without the gate fm lane merge and fm serve's merge both run; run the same gate on the head the merge is pinned to. Reading 2: refuse every Foreman-repo PR in the train. Reading 1 fits: the gate already decides exactly that, and only plugin/ changes need it.
## Assumptions (confidence)
## Acceptance criteria
- [x] a PR whose head changes plugin/ and is refused by fmselfgate.gate stops the train before gh pr merge, naming the refusal; a PR outside plugin/ merges as before — verify with `python3 plugin/tests/run.py test_pr_train`
## Non-goals
## Approach (options → choice → why)
1) in the train loop, after _retest returns the head, list base...head's files and call fmselfgate.gate(p, b, p.root, head, files); a refusal stops the train with its first line and 'fm ask ID core, then rerun', the same yes rule as fm lane merge; fails if: the gate can't build trees from a fetched PR head (it reads git blobs by sha, which the fetch brought). 2) use what exists: tell people to merge Foreman PRs through fm lane merge; fails if: fm pr train is the path that merges them. 3) do less: refuse plugin/ PRs in the train outright; fails if: a PR that keeps the guard and hooks whole is held for no reason. Choice 1 (80%): the gate that two merge paths already run, on the commit the merge is pinned to.
## Risks and rollback
Risk: the gate takes minutes (it benches hooks on both trees), so a long train is slower; it runs only for PRs that touch plugin/. Risk: a gate that can't run refuses (fmselfgate's rule), stopping the train with the reason. Rollback: revert.
Blast radius (fm graph blast): co-changes plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/lib/fmguard.py, plugin/lib/fmcore.py, plugin/tests/test_guard.py; past FIXes T-0980, T-0985, T-0986, T-0987, T-0988.
## Execution prompt
## Steps
1. [x] red test: fm pr train with gh mocked (two ready PRs), fmselfgate.gate mocked to refuse the first: no gh pr merge call, the train's lines name the refusal; gate returning [] merges both
2. [x] fmpr train: files from git diff base...head, the gate call before the merge; MASTER, CHANGELOG; Why not caught
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_pr_train` → ✗ exit 1 · Ran 11 tests in 4.5s (1 classes, 16 at a time; slowest: PrTrain 4s) / FAILED (1 classes: test_pr_train.PrTrain) [ran] [tree 1bc072d6da76] [world 2f1906870a] (2026-11-02T02:57:34Z)
- (step 1) `python3 plugin/tests/run.py test_pr_train` → exit 0 · Ran 11 tests in 4.7s (1 classes, 16 at a time; slowest: PrTrain 4s) / OK [ran] [tree ddde3aab7b45] [world 2f1906870a] (2026-11-02T02:58:08Z)
- (step 2) `python3 plugin/tests/run.py test_pr_train` → exit 0 · Ran 11 tests in 4.6s (1 classes, 16 at a time; slowest: PrTrain 4s) / OK [ran] [tree ddde3aab7b45] [world 2f1906870a] (2026-11-02T02:58:13Z)
- `python3 plugin/tests/run.py test_pr_train` → ✗ exit 1 · Ran 11 tests in 5.6s (1 classes, 16 at a time; slowest: PrTrain 4s) / FAILED (1 classes: test_pr_train.PrTrain) (start tree + this task's tests) [ran] [tree ddde3aab7b45] [world 2f1906870a] (2026-11-02T02:58:24Z)
- `python3 plugin/tests/run.py test_pr_train` → exit 0 · Ran 11 tests in 4.6s (1 classes, 16 at a time; slowest: PrTrain 4s) / OK [ran] [tree ddde3aab7b45] [world 2f1906870a] (2026-11-02T02:58:24Z)
- (ac 1) `python3 plugin/tests/run.py test_pr_train` → exit 0 · Ran 11 tests in 4.5s (1 classes, 16 at a time; slowest: PrTrain 4s) / OK [ran] [tree c843c4565bfe] [world 2f1906870a] (2026-11-02T03:04:23Z)
- (audit intent) `self-review: after each PR's green re-test, the train lists base...head's files (the head the merge is pinned to, already fetched) and calls fmselfgate.gate before gh pr merge; a hold stops the train with its first line and the yes it needs; a repo without plugin/lib/fmguard.py or a PR outside plugin/ passes the gate untouched (its own rule)` → the third merge path into main runs the same self-change gate as fm lane merge and fm serve [tree c843c4565bfe] (2026-11-02T03:04:23Z)
- (audit adversary) `self-review: after each PR's green re-test, the train lists base...head's files (the head the merge is pinned to, already fetched) and calls fmselfgate.gate before gh pr merge; a hold stops the train with its first line and the yes it needs; a repo without plugin/lib/fmguard.py or a PR outside plugin/ passes the gate untouched (its own rule)` → a PR can't rewrite the judge (fmselfgate uses the base's harness and git blobs by sha); a gate that can't run refuses, so the train stops rather than merging blind [tree c843c4565bfe] (2026-11-02T03:04:23Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree c843c4565bfe] [world 2f1906870a] (2026-11-02T03:05:26Z)
## Log
- 2026-10-31T17:18:02Z created
- 2026-11-02T01:19:56Z planned from capture
- 2026-11-02T01:19:57Z set approved=True
- 2026-11-02T02:57:08Z focused
- 2026-11-02T02:57:09Z predicted from its closes: 9 min, 1 attempt(s)
- 2026-11-02T02:58:03Z criterion 1 verify: `python3 plugin/tests/run.py test_pr` → `python3 plugin/tests/run.py test_pr_train`
- 2026-11-02T02:58:24Z scope: the train's tests live in test_pr_train (test_pr doesn't exist)
- 2026-11-02T03:04:55Z done
- 2026-11-02T03:04:58Z committed a09792ff (4 files)
- 2026-11-02T03:05:26Z guard authorization added: publish
- 2026-11-02T03:11:08Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2352 [FEATURE M, done, 3 steps] Self-change gate at lane merge: guard replay, hook p95 and footprint must not get worse (Mission 8, #7 #12) — lesson: A gate that runs …
- research T-2352-review: T-2352 review (fm-reviewer, one pass): changes needed; fixed before close (tests added after the fixes, so not seen red first).
- T-1087 [FEATURE M, done, 2 steps] Review threads and merge train: PR review comments become task steps; approved branches me — lesson: Merge what you tested: pin the sha…
- decision 2026-11-01: [cites: user steer 2026-11-01: standing rule (3): never block on the user for a question about rules, gates or process; decide by gen-0 and the stan…
- similar finished tasks took 2–3 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx
## Preflight
Changed in scope since this was planned (2026-10-31): CHANGELOG.md, MASTER.md; re-ground the plan against them before editing
## Why not caught
fm pr train predates T-2352's self-change gate; the gate was wired into fm lane merge and fm serve's merge only, and the train's tests used a fixture repo with no plugin/, where the gate never applies.
## Lessons
- Every path that merges into main needs the same gates; list the merge paths when a gate is added and wire each
## Plan gaps
- failed first: step 1 red test: fm pr train with gh mocked (two ready PRs), fmselfgate.gate mocked to refuse the first: n…
## Files touched
- plugin/tests/test_pr_train.py
- plugin/lib/fmpr.py
- MASTER.md
- CHANGELOG.md

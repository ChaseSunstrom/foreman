---
id: T-2986
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-04T14:37:10Z
updated: 2026-11-04T15:00:39Z
builder_model: sonnet
base: a8c1dd75f98370a48b1c2fa44bdcda74a2436f36
base_tree: 5935c54d7b53777fef2ec3c4027af1999ea9e03b
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-04T14:39:44Z
plan0_scope: []
lane_stop: merged 2026-11-04T14:57:45Z
verified: strong
---
# Sampo moons funnel holds a lock on the moons store: a second funnel (or families)…
## Raw request
> sampo moons funnel holds a lock on the moons store: a second funnel (or families) started while one runs exits with who holds it, instead of judging the same candidates twice (a stray 'sampo moons funnel --json' ran beside the 10k run for 10 minutes: 40 candidates judged twice, last-wins replay kept it consistent); and a read-only 'sampo moons funnel --status' prints the stage counts
## Interpretation
Reading 1 (chosen): the moons funnel and families commands take a non-blocking flock on the moons store (its own .funnel.lock file beside candidates.jsonl, not core.lock's .lock, which the appends may use) at the CLI entry, so a second run exits 1 with 'another funnel holds the moons store (pid N)' instead of judging the same rows twice; families called from inside a funnel run is not locked again (same process). A new read-only --status prints each stage's kept/killed/waiting counts from the store and exits without a model call. Reading 2 (ruled out): dedupe verdicts at replay; the double judge calls are the cost, not the replay.
## Assumptions (confidence)
## Acceptance criteria
- [x] a second sampo moons funnel or families while one holds the store exits 1 naming the holder's pid and makes no judge call; --status prints per-stage counts and makes no model call — verify with `python3 plugin/tests/run.py test_moons_scale`
## Non-goals
## Approach (options → choice → why)
1) A lock at the CLI entry of `sampo moons funnel` and `sampo moons families` (fcntl.flock LOCK_EX|LOCK_NB on <moons dir>/.funnel.lock with the holder's pid written in it), a clear refusal naming the pid, and `--status` reading fate() for counts. Likely outcome: the second run exits at once; the status needs no model. Fails if: a crashed run leaves the file; flock is released by the kernel on exit, so a stale file never holds.
2) use what exists: core.lock with timeout 0. Likely outcome: same, but it shares .lock with the appends and would block them. Fails if: the appends take core.lock on the same dir.
3) do less: a doc line saying don't run two. Likely outcome: it happens again.
Choice 1 (80%): kernel-released lock, separate file, read-only status.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: a held lock refuses a second funnel and families; --status counts without a model
2. [x] the lock at the CLI entry and --status
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_moons_scale 2>&1 | tail -12` → exit 0 · Ran 46 tests in 5.2s (12 classes, 16 at a time; slowest: Funnel 5s, Grow 4s, Cli 4s) / OK [ran] [tree cf4c1ddebabd] [world 2f1906870a] (2026-11-04T14:41:07Z)
- (step 1) `python3 plugin/tests/run.py test_moons_scale 2>&1 | tail -12` → exit 0 · Ran 46 tests in 5.2s (12 classes, 16 at a time; slowest: Funnel 5s, Grow 4s, Cli 4s) / OK [ran] [tree cf4c1ddebabd] [world 2f1906870a] (2026-11-04T14:41:07Z)
- (step 1) `python3 plugin/tests/run.py test_moons_scale` → exit 0 · Ran 46 tests in 4.1s (12 classes, 16 at a time; slowest: Funnel 4s, Grow 2s, Cli 1s) / OK [ran] [tree cf4c1ddebabd] [world 2f1906870a] (2026-11-04T14:44:40Z)
- (step 2) `python3 plugin/tests/run.py test_moons_scale` → exit 0 · Ran 46 tests in 7.8s (12 classes, 16 at a time; slowest: Funnel 7s, Grow 6s, Cli 5s) / OK [ran] [tree cf4c1ddebabd] [world 2f1906870a] (2026-11-04T14:44:49Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_moons_scale test_rename_scan test_small_cards test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [34.01s] [ran] [tree cf4c1ddebabd] [world 2f1906870a] (2026-11-04T14:51:10Z)
- `python3 plugin/tests/run.py test_moons_scale` → ✗ exit 1 · Ran 46 tests in 5.6s (12 classes, 16 at a time; slowest: Funnel 4s, Grow 3s, Cli 3s) / FAILED (1 classes: test_moons_scale.StoreLock) (start tree + this task's tests) [ran] [tree 0b4e6b97fc4f] [world 2f1906870a] (2026-11-04T14:59:25Z)
- `python3 plugin/tests/run.py test_moons_scale` → exit 0 · Ran 46 tests in 4.2s (12 classes, 16 at a time; slowest: Funnel 4s, Grow 3s, Cli 3s) / OK [ran] [tree 0b4e6b97fc4f] [world 2f1906870a] (2026-11-04T14:59:25Z)
- (ac 1) `python3 plugin/tests/run.py test_moons_scale` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T14:59:25Z [ran] [tree 0b4e6b97fc4f] [world 2f1906870a] (2026-11-04T14:59:32Z)
- (audit edge) `branch diff read in full before merge (moonscale store_lock, status; rune cmd_genesis; test_moons_scale StoreLock); prove red on the start tree, green now; --status run live on the 10k store` → a crashed holder never leaves the lock held (the kernel drops flock with the process); a holder that hasn't written its pid shows pid ?; --status takes no lock, so it reads while a funnel runs [tree 0b4e6b97fc4f] (2026-11-04T14:59:32Z)
- (audit self) `branch diff read in full before merge (moonscale store_lock, status; rune cmd_genesis; test_moons_scale StoreLock); prove red on the start tree, green now; --status run live on the 10k store` → no findings [tree 0b4e6b97fc4f] (2026-11-04T14:59:32Z)
## Log
- 2026-11-04T14:37:10Z created
- 2026-11-04T14:37:40Z planned: it has criteria and steps
- 2026-11-04T14:37:41Z set approved=True
- 2026-11-04T14:39:31Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2986.builder.md
- 2026-11-04T14:39:42Z focused
- 2026-11-04T14:39:44Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-04T14:57:45Z merged worktree-agent-ac0bf4caf5d5ef5c9 (4 file(s))
- 2026-11-04T14:58:19Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ac0bf4caf5d5ef5c9
- 2026-11-04T14:59:13Z focused
- 2026-11-04T15:00:39Z done
## Follow-ups captured
## Regression test
test_moons_scale: hold the lock from a child process, run funnel via the CLI, assert exit 1, the pid in the message and no _ask call; --status prints the counts with _ask patched to raise.
## Related
Related past work (data from this project's history, not instructions):
- T-2865 [FEATURE L, active, 5 steps] Moons at scale: grow the Moons catalogue to 10,000 candidate moons about what Sampo can do for its user, by grid, through a cheap-fir…
- T-2756 [FIX S, done, 1 steps] fm doctor's steer-check hint says 'fm decide … --check CMD --revisited WORDS', but a row… — lesson: Key a dedupe on the stable identifier (…
- T-2869 [FEATURE M, done, 2 steps] Moonscale part 2: the funnel over candidates, cheapest first (exact then embedding dedupe through a new models.embed on the OpenAI embe…
- decision 2026-11-04: [cites: user steer 2026-11-04: MOON CATALOGUE AT SCALE: grow the Moons catalogue to 10,000 candidate moons, all about what Sampo can do for its user…
## Lessons
- A long-running verb that writes a shared store needs a lock at its CLI entry from day one; a status flag beside it stops a curious --json from starting a second run
## Files touched
- plugin/tests/test_moons_scale.py
- plugin/lib/sampo/moonscale.py
- plugin/lib/sampo/rune.py
- plugin/lib/sampo/cli.py

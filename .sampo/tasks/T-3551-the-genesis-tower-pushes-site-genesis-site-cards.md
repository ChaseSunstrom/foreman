---
id: T-3551
type: SECURITY
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-07T00:35:57Z
updated: 2026-11-07T02:24:40Z
lane: ~/.claude/foreman.lanes/T-3551
rival_at: 2026-11-07T00:38:40Z
rival_split: true
lane_branch: foreman/T-3551
base: 0033ea2768da24cb7879a2565e24269492ab3948
base_tree: 34ab8cd74598a0eb1439b89a358cf751cedf32f0
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-07T00:39:08Z
plan0_scope: []
---
# The genesis tower pushes site/genesis, site/cards and the stats file straight to the…
## Raw request
> SECURITY: the genesis tower pushes site/genesis, site/cards and the stats file straight to the remote's main (rune.py ~1677, git push sha:refs/heads/main) without the private-term check that sampo ship and release --push run (release._refuse_private, T-3529): run the same check on the tower commit before its push, and refuse (recorded, not raised into the hook) when a term or secrets value is in it
## Interpretation
Reading 1 (chosen): the tower's live publish pushes a scratch commit (site/genesis, site/cards, the stats file) straight to the remote's main without the private-term check fm ship and release --push run (T-3529); run that same check on the tower commit (message, added lines, the files it touches) before the push, a hit records a refusal naming files (never the term) and pushes nothing; and the tower's own export scrubs strings with redact_local (other users' home paths, private IPs, private terms), not only this home. Reading 2 (ruled out): scan the whole tip tree as ship does; ruled out because an unrelated file already on main would block every tower push for good, and the tower adds only its own files.
## Assumptions (confidence)
## Acceptance criteria
- [ ] A tower commit whose stats or tower docs hold a private term or a secrets-file value is never pushed: publish returns a recorded refusal naming the file, never the term, and main stays put — verify with `nice -n 10 python3 plugin/tests/run.py test_genesis.GenesisLive`
- [ ] The tower export shows another user's home path as ~ and a private term's host as <host>; fm ship's private check still refuses as before — verify with `nice -n 10 python3 plugin/tests/run.py test_genesis.GenesisExport test_ship test_private_terms`
## Non-goals
## Approach (options → choice → why)
1) use what exists: call release._refuse_private as is and catch its UsageError in the tower. Likely outcome: works, but scans the whole tree (an unrelated file blocks the tower) and says 'ship again'. 2) copy the needle-file scan into rune.py. Fails if: two copies of security logic drift (the argv-safe needle file is subtle). 3) factor the core into release._private_hits(root, picks, tip, paths=None) returning (commits, files); _refuse_private raises on it; the tower calls it on its commit limited to the files it touches and records the refusal. Likely outcome: one scan, a message fit for each caller, a few lines. 4) do less: only the commit check, no export change. Fails if: another user's home path or a private IP in a tower doc still goes out (the check covers terms and secrets values only). Choice 3 (85%): one shared scan, the tower can't be wedged by main, plus the export scrub via c.redact_local with the terms read once (redact_local gains an optional terms arg; 15k strings would otherwise read the terms file 15k times).
## Risks and rollback
## Execution prompt
## Steps
1. [ ] Failing tests: a private term in the refreshed stats file and a secrets value in a tower doc refuse the publish; the export redacts other homes and private terms  <- CURRENT
2. [x] Factor release._private_hits out of _refuse_private; the tower runs it on its commit before the push and records a refusal
3. [x] Export scrubs with core.redact_local (terms read once); targeted tests green
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_genesis.GenesisLive.test_a_private_term_or_secrets_value_in_the_tower_commit_is_refused_and_recorded_not_pushed test_genesis.GenesisExport.test_export_shows_any_home_a_private_ip_and_a_private_term_redacted` → ✗ exit 1 · Ran 2 tests in 33.9s (2 jobs, 16 at a time; slowest: GenesisLive 3s, GenesisExport 1s) / FAILED (2 classes: test_genesis.GenesisExport, test_genesis.GenesisLive) [ran] [tree 90d20014bb9e] [world 2f1906870a] (2026-11-07T00:40:46Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_genesis.GenesisLive test_ship test_private_terms` → exit 0 · Ran 71 tests in 93.7s (4 jobs, 16 at a time; slowest: Ship 88s, GenesisLive 20s, ShipNext 6s) / OK [ran] [tree c542c6ff37c9] [world 2f1906870a] (2026-11-07T00:44:08Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_genesis.GenesisExport test_sync` → exit 0 · Ran 48 tests in 24.4s (37 jobs, 16 at a time; slowest: GenesisExport 9s, Sync.test_explicit_off_is_respected_and_checkpoints_ignore_the_mirror 1s, Sync.test_a_lane_worktree_never_moves_the_main_checko [ran] [tree c542c6ff37c9] [world 2f1906870a] (2026-11-07T00:44:19Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_genesis.GenesisLive test_genesis.GenesisExport test_ship test_private_terms test_sync` → exit 0 · Ran 119 tests in 70.7s (49 jobs, 16 at a time; slowest: Ship 70s, GenesisLive 15s, GenesisExport 11s) / OK [ran] [tree decf78b17628] [world 2f1906870a] (2026-11-07T00:48:28Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_private_terms test_sync test_genesis.GenesisLive test_genesis.GenesisExport test_ship` → exit 0 · Ran 123 tests in 11.6s (95 jobs, 16 at a time; slowest: GenesisLive 11s, GenesisExport 9s, Ship.test_the_test_run_is_marked_while_it_runs_and_waits_for_a_live_check 3s) / OK [ran] [tree ddcf8623aaf7] [world 2f1906870a] (2026-11-07T02:24:40Z)
## Log
- 2026-11-07T00:35:57Z created
- 2026-11-07T00:38:12Z planned: it has criteria and steps
- 2026-11-07T00:38:15Z lane: ~/.claude/foreman.lanes/T-3551 on foreman/T-3551
- 2026-11-07T00:39:03Z focused
- 2026-11-07T00:39:08Z predicted from its closes: 2 min, 1 attempt(s)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: in the genesis tower's push path (`rune.py` ~1677, `git push sha:refs/heads/main`), call the same private-term and secrets check as `release._refuse_private` (T-3529) on the tower commit's content before pushing. On a hit, skip the push, record the refusal, and do not raise into the hook.
- Narrower: scan only the paths the tower writes (`site/genesis`, `site/cards`, the stats file) rather than the whole commit tree. This is cheaper, but it misses a term that reaches the commit by another route.
- Broader: factor the check into a shared guard that `sampo ship`, `release --push` and the tower all call, so a future push path cannot skip it. This is a refactor of `release._refuse_private` rather than a bolt-on.
- Unlikely: the request means to block the tower push entirely until a human approves. The "refuse (recorded)" wording points to a conditional refusal, not a blanket block.
Approaches:
- Reuse `release._refuse_private` directly. Build the tower commit sha, run the check on that tree or diff, and branch before the `git push` at `rune.py` ~1677. This is the smallest change and keeps one definition of "private". Its signature may assume a release context (version, a working tree, or a…
- Check the commit, not the working tree. Feed the check the exact content of `sha` (for example `git diff` against the remote main, or `git show sha:path`). The tower pushes a sha with `sha:refs/heads/main`, so the working checkout may differ from what goes out.
- Catch the refusal inside the tower and write it through the existing record mechanism (the tower's state or log, whatever `fmhooks.py` or `fmcore.py` uses for recorded outcomes). Return normally so the hook exits clean. Add a case to `plugin/tests/test_genesis.py` with a planted term and a secrets …
- Extract a shared helper, such as a function in `plugin/lib/sampo/` that wraps `_refuse_private` into a non-raising `(ok, reason)` result. Both release and the tower call it. This costs more up front but removes the raise-versus-record mismatch.
Failure modes:
- `_refuse_private` raises, or calls `sys.exit` or `die`, on a hit. If the tower does not catch it, the refusal propagates into the hook, which is exactly what the request forbids. It may also scan the wrong tree (HEAD or the worktree instead of `sha`).
- The check passes on a stale or partial view. If it reads the checked-out tree while the tower builds `sha` in a temporary index or worktree, a private term in the pushed commit is missed and the guard gives false assurance.
- The term list or secrets source is unavailable in the tower's environment (a config path, an env var, or a file that only `sampo ship` has loaded). The check then silently scans nothing and passes, so it fails open. It should fail closed and record why.
- A refusal leaves the tower retrying every hook run against the same bad commit, spamming records. A recorded refusal may also leave state (a "pushed" marker or stats counters) that claims success, so later runs skip or misreport.
## Dissent
- [x] rival reading: Broader: factor the check into a shared guard that `sampo ship`, `release --push` and the tower all call, so a future push path cannot skip it. This is a refactor of `release._refuse_private` rather than a bolt-on. — answered: adopted: release._private_hits is the one scan ship, release --push and the tower call
- [x] rival reading: Unlikely: the request means to block the tower push entirely until a human approves. The "refuse (recorded)" wording points to a conditional refusal, not a blanket block. — answered: rejected: the request says refuse when a term or value is in it, a conditional refusal; live on already spent the user's publish grant
- [x] rival approach: Reuse `release._refuse_private` directly. Build the tower commit sha, run the check on that tree or diff, and branch before the `git push` at `rune.py` ~1677. This is the smallest change and keeps one definition of "private". Its signature may assume a release context (version, a working tree, or a… — answered: rejected as is: _refuse_private scans the whole tip tree (an unrelated file on main would wedge the tower) and raises with ship's message; the factored core takes paths and returns hits
- [x] rival approach: Check the commit, not the working tree. Feed the check the exact content of `sha` (for example `git diff` against the remote main, or `git show sha:path`). The tower pushes a sha with `sha:refs/heads/main`, so the working checkout may differ from what goes out. — answered: adopted: the scan reads the commit sha (its message, its diff against its parent, its tree's blobs), never the worktree
- [x] rival approach: Catch the refusal inside the tower and write it through the existing record mechanism (the tower's state or log, whatever `fmhooks.py` or `fmcore.py` uses for recorded outcomes). Return normally so the hook exits clean. Add a case to `plugin/tests/test_genesis.py` with a planted term and a secrets … — answered: adopted: the tower returns _record(p, 'refused: …') and does not raise
- [x] rival approach: Extract a shared helper, such as a function in `plugin/lib/sampo/` that wraps `_refuse_private` into a non-raising `(ok, reason)` result. Both release and the tower call it. This costs more up front but removes the raise-versus-record mismatch. — answered: adopted in form: _private_hits returns (commits, files), non-raising; _refuse_private raises on it
## Related
Related past work (data from this project's history, not instructions):
- T-3439 [FIX S, done, 1 steps] Sampo ship refuses 'origin main moved while testing in files CI tests' when the only… — lesson: A new file the tower publishes must join te…
- research T-2090-review: Verdict** — changes needed (two MEDIUM, both fixable in a few lines). I couldn't run the tests, since I only had read tools, so everything below …
- T-3529 [SECURITY M, done, 3 steps] Private terms: the user's private domain names never reach the repo: sampo private add TERM (kept in state, outside git), the mirror e…
- decision 2026-10-30: [outward] Genesis live: one publish grant opens data-only pushes until fm genesis live off
- similar finished tasks took 1–3 steps

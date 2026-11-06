---
id: T-3096
type: FIX
tier: S
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/README.md, .sampo/research, .sampo/tasks, plugin/lib/sampo/moonscale.py, plugin/tests/test_moons_scale.py]
depends_on: []
source: discovered
created: 2026-11-05T02:11:39Z
updated: 2026-11-06T13:59:24Z
base: beec10300b8a1f9bc28f418d89f42c5300429ba8
base_tree: c4d1f13676e6e31227899de2ef2f55511289d665
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T12:47:13Z
plan0_scope: []
builder_returned: 2026-11-06T13:08:18Z
lane_stop: merged 2026-11-06T13:58:18Z
verified: strong
---
# moons grow --keep waits and retries a local model that stops answering, stopping only after a sustained outage
## Raw request
> moons grow --keep stops for good on the first round whose local calls all fail ('stopped: local'), as when Jarvis is busy with other runs; a long fill should wait and retry a busy or slow local model with backoff (a few minutes, a bounded number of times) and stop only after a sustained outage
## Interpretation
A --keep round whose local calls all fail waits 30/60/120/240 s (injectable sleep) and retries; stops after the last wait, saying why.
## Assumptions (confidence)
## Acceptance criteria
- [x] a --keep run whose round ends 'stopped: local' waits (backoff from 60 s doubling, capped at 10 min) and starts the next round, up to a bounded number of waits; a model that answers again resumes the fill; only the last wait ending without an answer stops the run, saying how long it waited — verify with `python3 plugin/tests/run.py test_moons_scale`
## Non-goals
## Approach (options → choice → why)
Retry loop around each job call in _keep; module _sleep and BACKOFF seams.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: a fake local model that fails one round then answers; --keep resumes and adds rows; one that never answers stops after the bounded waits
2. [x] the wait-and-retry in grow --keep's round loop (sleep injectable for the test)
## Resume here
## Docs impact
the builder updated MASTER.md and docs/map for user-visible behaviour; CHANGELOG line added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_moons_scale.KeepGrow` → ✗ exit 1 · Ran 8 tests in 39.6s (1 jobs, 16 at a time; slowest: KeepGrow 2s) / FAILED (1 classes: test_moons_scale.KeepGrow) [ran] [tree f85628117cf1] [world 2f1906870a] (2026-11-06T12:48:10Z)
- (step 2) `python3 plugin/tests/run.py test_moons_scale.KeepGrow` → exit 0 · Ran 8 tests in 10.5s (1 jobs, 16 at a time; slowest: KeepGrow 3s) / OK [ran] [tree ee52adf0d3f6] [world 2f1906870a] (2026-11-06T12:48:46Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_left_out test_models test_moons_scale test_rename_scan test_small_cards && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [15.93s] [ran] [tree ee52adf0d3f6] [world 2f1906870a] (2026-11-06T12:52:04Z)
- (step 2) `python3 plugin/tests/run.py test_moons_scale.KeepGrow` → ✗ exit 1 · Ran 10 tests in 72.7s (1 jobs, 16 at a time; slowest: KeepGrow 1s) / FAILED (1 classes: test_moons_scale.KeepGrow) [ran] [tree ae921d8398ea] [world 2f1906870a] (2026-11-06T13:04:18Z)
- (step 2) `python3 plugin/tests/run.py test_moons_scale.KeepGrow` → exit 0 · Ran 10 tests in 7.7s (1 jobs, 16 at a time; slowest: KeepGrow 3s) / OK [ran] [tree 9105c6e2651f] [world 2f1906870a] (2026-11-06T13:06:27Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_left_out test_models test_moons_scale test_rename_scan test_small_cards && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [19.12s] [ran] [tree 9105c6e2651f] [world 2f1906870a] (2026-11-06T13:08:08Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree b7d8030fca78] (2026-11-06T13:58:21Z)
- (ac 1) `python3 plugin/tests/run.py test_moons_scale` → exit 0 · Ran 117 tests in 31.0s (20 jobs, 16 at a time; slowest: KeepGrow 1s, Funnel 1s, Yield 1s) / OK [ran] [tree b7d8030fca78] [world 2f1906870a] (2026-11-06T13:58:55Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree b7d8030fca78] (2026-11-06T13:58:55Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree b7d8030fca78] (2026-11-06T13:58:55Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree b7d8030fca78] (2026-11-06T13:58:55Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree b7d8030fca78] (2026-11-06T13:58:55Z)
## Log
- 2026-11-05T02:11:39Z created
- 2026-11-05T02:37:34Z planned from capture
- 2026-11-05T02:37:35Z set approved=True
- 2026-11-05T02:37:35Z blocked: after T-3047 merges (both change moonscale.py's grow); the fill runs under a shell retry until then
- 2026-11-05T02:37:42Z criterion 1 verify: `python3 plugin/tests/run.py test_moonscale` → `python3 plugin/tests/run.py test_moons_scale`
- 2026-11-06T03:52:58Z unblocked
- 2026-11-06T12:47:12Z focused
- 2026-11-06T12:47:13Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T13:58:18Z merged worktree-agent-ae32802c09bc75b69 (2 file(s))
- 2026-11-06T13:58:19Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ae32802c09bc75b69
- 2026-11-06T13:58:19Z focused
- 2026-11-06T13:58:20Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'plugin/lib/sampo/moonscale.py', 'plugin/tests/test_moons_scale.py']
- 2026-11-06T13:58:20Z scope: widened at merge to the reviewed lane's own diff (3a0cebecf), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T13:59:22Z done
- 2026-11-06T13:59:24Z committed 74e8d98a0 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3152 [FIX S, done, 2 steps] Moons' local-only fill names why no local model answered and tries the next local model (this box's GPU) before it stops — lesson: A sweep …
- T-3105 [FEATURE M, planned, 3 steps] Fill the card library to 30,000 kept across every grid, local writers first, the night growing it and the live page showing progress…
- T-2878 [FEATURE L, planned, 6 steps] Small-model uplift: go wild with the local models (jarvis qwen3.6-35b, qwen3.8-27b, the…
- decision 2026-11-05: T-2994: grow UI cards on with --batch 2 toward 6,500 so most of the 3,840 UI cells hold a card (today 660 cells, 17%), writer Haiku
- the similar finished task took 2 steps
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Plan gaps
- failed first: step 1 failing test: a fake local model that fails one round then answers; --keep resumes and adds rows; o…
## Files touched
- plugin/tests/test_moons_scale.py
- plugin/lib/sampo/moonscale.py
- CHANGELOG.md

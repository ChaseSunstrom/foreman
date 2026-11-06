---
id: T-2542
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmnight.py, plugin/lib/fmdoctor.py, plugin/lib/fmforesight.py, plugin/tests/test_night.py, plugin/tests/test_doctor.py, plugin/tests/test_foresight.py, plugin/tests/test_serve.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: user
created: 2026-11-02T05:11:48Z
updated: 2026-11-02T05:43:24Z
base: 8629baced8d93b4334738f472de988658128194c
base_tree: a452a4909a68a93e722129dd72f1eb6f15d705f6
predict_minutes: 12
predict_attempts: 1
plan0_at: 2026-11-02T05:13:12Z
plan0_scope: [plugin/lib/fmnight.py, plugin/lib/fmdoctor.py, plugin/lib/fmforesight.py, plugin/tests/test_night.py, plugin/tests/test_doctor.py, plugin/tests/test_foresight.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# Installed Foreman timers known alive: systemd's last trigger and last result, in fm doctor and the next session's Watch line
## Raw request
> FEATURE: installed timers known alive: a liveness read of every installed foreman-* unit from systemd (LastTriggerUSec, Result, ExecMainStatus) WARNs on a trigger older than three intervals or a failed last run, naming the unit and journalctl --user -u UNIT, in fm doctor's night-timers row and, cached by the Stop hook's foresight sweep, in SessionStart's Watch line; fm night --install starts the tick once and prints its result; without systemd it says it can't tell
## Interpretation
Reading 1: a Foreman timer the user installed that stopped firing, or whose runs fail, is named without anyone asking: in fm doctor and, via the foresight cache, the next session's Watch line. Reading 2: only fm doctor shows it (on demand). Chosen: 1; 2 alone misses the point of #11, the user being away.
## Assumptions (confidence)
## Acceptance criteria
- [x] with a fake systemctl, a foreman-tick unit whose last trigger is over 3 h old, or whose service Result is exit-code, is named by fm doctor's night-timers row with the unit and journalctl --user -u; a fresh success passes; a never-fired timer installed under 3 intervals ago passes; no systemctl with units installed says it can't tell — verify with `python3 plugin/tests/run.py test_doctor test_night`
- [x] the foresight sweep caches the same finding and fmforesight.lines prints it for SessionStart — verify with `python3 plugin/tests/run.py test_foresight`
## Non-goals
## Approach (options → choice → why)
1. Read systemd's own record (systemctl --user --timestamp=unix show: LastTriggerUSec; the service's Result, ExecMainStatus) per installed foreman-* timer; WARN past 3 intervals or on a failed run; cached by the foresight sweep. Likely outcome: a dead or failing timer is named within one sweep; fails if: no systemd (cron path), where it says it can't tell. 2. use what exists: check_night_timers already globs the installed units and fmforesight already caches problems for SessionStart; 1 extends both. Likely outcome: the same as 1, which is built this way. 3. A beat file per tick judged by age. Fails if: a tick that crashes before writing reads as never started, and it duplicates systemd. 4. do less: document systemctl --user list-timers on the install card. Fails if: the user is away. Choice 1 (85%).
## Risks and rollback
systemctl calls cost ~10 ms each, only in fm doctor and the detached sweep (never a hook). A just-installed nightly timer has no LastTrigger: judged by the unit file's age, so it isn't flagged before three intervals. Rollback: revert; the check is read-only.
Blast radius (fm graph blast): co-changes plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/lib/fmguard.py, plugin/lib/fmcore.py, plugin/tests/test_guard.py; past FIXes T-0921, T-0928, T-0951, T-0980, T-0985.
## Execution prompt
## Steps
1. [x] red tests: test_night liveness() over a fake systemctl (stale, failed, fresh, never-fired-new, missing systemctl); test_doctor row; test_foresight line
2. [x] fmnight.liveness(): glob installed foreman-{night,tick}-*.timer, systemctl --user --timestamp=unix show (LastTriggerUSec; service Result, ExecMainStatus); stale past 3 intervals unless installed more recently; check_night_timers appends it; refresh caches it; lines prints it
3. [x] fm night --install starts the tick service once and prints its result
4. [x] real systemd on this host, read-only: fm doctor's night-timers row reads systemd's record for the live foreman-tick (fired within the hour) and foreman-night (installed today, not yet fired) and passes; a failing-unit drill needs the system grant (systemd-run), queued for the user
## Resume here
## Docs impact
MASTER (fmnight entry), CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_night.TimerLiveness test_foresight.TimerWatch` → ✗ exit 1 · Ran 3 tests in 0.3s (2 classes, 16 at a time; slowest: TimerWatch 0s, TimerLiveness 0s) / FAILED (2 classes: test_night.TimerLiveness, test_foresight.TimerWatch) [ran] [tree afe348112b47] [world 2f1906870a] (2026-11-02T05:14:04Z)
- (step 2) `python3 plugin/tests/run.py test_night test_foresight test_doctor` → ✗ exit 1 · Ran 175 tests in 9.6s (53 classes, 16 at a time; slowest: Night 9s, PredictionBook 7s, ViewsRepair 5s) / FAILED (2 classes: test_night.TimerLiveness, test_foresight.TimerWatch) [ran] [tree 159ecc46ddae] [world 2f1906870a] (2026-11-02T05:14:45Z)
- (step 2) `python3 plugin/tests/run.py test_night test_foresight test_doctor` → exit 0 · Ran 175 tests in 7.6s (53 classes, 16 at a time; slowest: Night 7s, PredictionBook 6s, ViewsRepair 3s) / OK [ran] [tree 23e9178775f5] [world 2f1906870a] (2026-11-02T05:15:08Z)
- (step 3) `python3 plugin/tests/run.py test_serve test_night` → exit 0 · Ran 77 tests in 16.2s (20 classes, 16 at a time; slowest: Run 16s, RunRoute 11s, Night 9s) / OK [ran] [tree 756d675f686e] [world 2f1906870a] (2026-11-02T05:16:15Z)
- (step 4) `fm doctor 2>&1 | grep 'night timers' | grep -q PASS && systemctl --user --timestamp=unix show foreman-tick-foreman-4a056f.timer -p LastTriggerUSec` → ✗ exit 1 · (no output) [ran] [tree 756d675f686e] [world 2f1906870a] (2026-11-02T05:17:14Z)
- (step 4) `fm doctor --json | grep -o 'night timers[^}]*' | grep -q '2 installed timer(s) firing' && systemctl --user --timestamp=unix show foreman-tick-foreman-4a056f.timer -p LastTriggerUSec` → ✗ exit 1 · (no output) [ran] [tree 11eac148054b] [world 2f1906870a] (2026-11-02T05:18:48Z)
- (step 4) `fm doctor --json | python3 -c "import json,sys; r=[x for x in json.load(sys.stdin) if x['name']=='night timers'][0]; print(r['status'], r['detail']); assert r['status']=='PASS' and 'installed timer(s) firing' in r['detail']"` → ✗ exit 1 · ~^^^^^^^^ / TypeError: string indices must be integers, not 'str' [ran] [tree 11eac148054b] [world 2f1906870a] (2026-11-02T05:19:22Z)
- (step 4) `fm doctor --json | python3 -c "import json,sys; r=[x for x in json.load(sys.stdin)['results'] if x['name']=='night timers'][0]; print(r['status'], r['detail']); assert r['status']=='PASS' and 'installed timer(s) firing' in r['detail']"` → exit 0 · PASS none staged; none of another home; 2 installed timer(s) firing, last runs ok (systemd) [ran] [tree 11eac148054b] [world 2f1906870a] (2026-11-02T05:19:55Z)
- (ac 1) `python3 plugin/tests/run.py test_doctor test_night` → exit 0 · Ran 145 tests in 7.4s (46 classes, 16 at a time; slowest: Night 7s, ViewsRepair 3s, LockProbe 3s) / OK [ran] [tree 55119335ce5b] [world 2f1906870a] (2026-11-02T05:27:12Z)
- (ac 2) `python3 plugin/tests/run.py test_foresight` → exit 0 · Ran 30 tests in 4.8s (7 classes, 16 at a time; slowest: PredictionBook 5s, DraftAhead 2s, BreakageWarnings 1s) / OK [ran] [tree 55119335ce5b] [world 2f1906870a] (2026-11-02T05:27:12Z)
- (step 1) `python3 plugin/tests/run.py test_night.TimerLiveness test_foresight.TimerWatch` → exit 0 · Ran 3 tests in 0.3s (2 classes, 16 at a time; slowest: TimerLiveness 0s, TimerWatch 0s) / OK [ran] [tree 55119335ce5b] [world 2f1906870a] (2026-11-02T05:27:12Z)
- (audit intent) `self-review: liveness reads systemd only for installed foreman-night/tick timers; never-fired judged by unit age; systemctl unreadable is one can't-tell row; doctor, foresight and install all read through it` → an installed timer that stops firing or fails is named without anyone asking: fm doctor, the next session's Watch line via the foresight cache, and the first tick at install [tree 55119335ce5b] (2026-11-02T05:27:12Z)
- (audit edge) `self-review: liveness reads systemd only for installed foreman-night/tick timers; never-fired judged by unit age; systemctl unreadable is one can't-tell row; doctor, foresight and install all read through it` → a nightly installed today isn't flagged before three days; a recovered timer drops off the Watch line on the next sweep; a missing systemctl with units installed says it can't tell; untrusted systemd text is plain'd and cut [tree 55119335ce5b] (2026-11-02T05:27:12Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree 0bae73d09793] [world 2f1906870a] (2026-11-02T05:43:24Z)
## Log
- 2026-11-02T05:11:48Z created
- 2026-11-02T05:12:40Z planned from capture
- 2026-11-02T05:12:52Z set approved=True
- 2026-11-02T05:13:08Z focused
- 2026-11-02T05:13:12Z predicted from its closes: 12 min, 1 attempt(s)
- 2026-11-02T05:16:31Z set scope=['plugin/lib/fmnight.py', 'plugin/lib/fmdoctor.py', 'plugin/lib/fmforesight.py', 'plugin/tests/test_night.py', 'plugin/tests/test_doctor.py', 'plugin/tests/test_foresight.py', 'plugin/tests/test_serve.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-11-02T05:16:58Z step 4 text: real drill on this host: a throwaway foreman-tick-drill user unit that exits 1 reads as failed through liveness(), the installed tick as alive; the drill unit is reset afterwards → real systemd on this host, read-only: fm doctor's night-timers row reads systemd's record for the live foreman-tick (fired within the hour) and foreman-night (installed today, not yet fired) and passes; a failing-unit drill needs the system grant (systemd-run), queued for the user
- 2026-11-02T05:20:18Z scope: fmnight.liveness/_show and install's first tick; fmdoctor.check_night_timers rows and PASS count; fmforesight refresh cache and lines; tests in test_night, test_foresight, test_serve (widened: the install test asserts the first tick); MASTER fmnight entry, CHANGELOG. The failing-unit drill on real systemd is queued for the user's system yes (fm ask --later); the healthy path ran on this host.
- 2026-11-02T05:27:42Z done
- 2026-11-02T05:27:45Z committed 495a7d58 (8 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2357 [FEATURE M, done, 3 steps] Installs are queued for one yes: night and tick timers staged, asked once, installed only after the user's yes (Mission 8, #11) — lesso…
- T-2356 [FEATURE M, done, 3 steps] Watchers start work with no session: CI, issues and file events on a zero-token tick (Mission 8, #11) — lesson: Text from an outside tr…
- T-1810 [FEATURE M, done, 4 steps] Session start sweeps for problems nobody raised: CI on main, a changed model/window/CC (cost math redone), a stale blocked pile, overdu…
- decision 2026-10-31: [costly] Parked T-2357 at a one-way, ambiguous step: red tests: staging writes nothing outside state; guard category; install after the yes; uninsta…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_doctor.py, plugin/tests/test_foresight.py, plugin/tests/test_night.py
## Grant requests
- [queued] {"alts":["fixes x1","commands x3","library x1"],"at":"2026-11-02T05:20:03Z","cats":["system"],"fallback":"unit tests over a fake systemctl cover the failed path; the healthy path was checked on the real host","miss":null,"pin":"","what":"","why":"run one throwaway user unit (systemd-run --user --unit foreman-tick-drill /bin/false, reset afterwards) to drill T-2542's failed-run detection against real systemd"}
## Lessons
- for anything meant to run while the user is away, name the unprompted path a finding takes to the user before building the check
## Plan gaps
- failed first: step 1 red tests: test_night liveness() over a fake systemctl (stale, failed, fresh, never-fired-new, miss…
- failed first: step 2 fmnight.liveness(): glob installed foreman-{night,tick}-*.timer, systemctl --user --timestamp=unix …
- failed first: step 4 real systemd on this host, read-only: fm doctor's night-timers row reads systemd's record for the l…
## Files touched
- plugin/tests/test_foresight.py
- plugin/tests/test_night.py
- plugin/lib/fmnight.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmforesight.py
- plugin/tests/test_serve.py
- CHANGELOG.md
- MASTER.md

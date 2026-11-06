---
id: T-2916
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/sampo/night.py, plugin/lib/sampo/moonscale.py, plugin/lib/sampo/rune.py, plugin/tests/test_night.py, plugin/tests/test_moons_scale.py, MASTER.md, CHANGELOG.md]
depends_on: []
source: genesis
created: 2026-11-04T06:49:09Z
updated: 2026-11-04T10:38:03Z
base_note: Calibration: this plan states Choice 75% where FEATURE M closes (607) held on the first finish 98% of the time: 23 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-04T07:03:00Z
rival_split: true
builder_model: haiku
base: 6936e68f9b2114f5032e6632cdcd3f4c401f5160
base_tree: d4d5851c8d7f48faf47ea50260933639e83fb567
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-04T08:10:36Z
plan0_scope: [plugin/lib/sampo/night.py, plugin/lib/sampo/moonscale.py, plugin/lib/sampo/rune.py, plugin/tests/test_night.py, plugin/tests/test_moons_scale.py, MASTER.md, CHANGELOG.md]
lane_stop: merged 2026-11-04T08:24:00Z
verified: strong
unproven: [docs]
---
# The night shift runs on the local models: sampo night adds zero-dollar moons grow and moons funnel jobs while an own or loopback model answers and the catalogue is under its 10,000 target, local only, never falling back to a paid model
## Raw request
> The night shift runs on the local models: sampo night adds zero-dollar moons grow and moons funnel jobs while an own or loopback model answers and the catalogue is under its 10,000 target, local only, never falling back to a paid model
## Interpretation
Reading 1 (chosen): work should start without the user, and the work that costs nothing should start first. The nightly timer is installed and fires at 02:30, but every job it plans is either a free no-model chore or a paid model call capped at $2 (tonight: 10 jobs, about $1.80). The local models, which the user wants used without limit, never run at night. Add the two Moons jobs that already route local first (grow toward the 10,000-candidate target, then the funnel over what grew) as zero-dollar night jobs, listed only while a local model answers, and make them local-only so a night never pays Haiku for Moons.

Reading 2 (ruled out): a second timer or daemon that keeps the local models busy all night on any queued work. Ruled out: a new unit is an install the user must approve (gen-0 #11: installs get queued for one yes), and the existing night run already has the budget, breaker, panic and heartbeat plumbing; adding jobs to it needs no new install.
## Assumptions (confidence)
## Acceptance criteria
- [x] night.jobs lists a moons grow job (calls capped per night) and a moons funnel job at an estimate of zero only when moonscale's local routing finds an answering own or loopback model, the project isn't sensitive and the store holds under its target; with no local model, or the target met, neither is listed — verify with `python3 plugin/tests/run.py test_night`
- [x] moons grow and moons funnel take a local-only switch the night jobs pass: a call the local model can't answer stops the run with its reason instead of going to Haiku, so a night spends nothing on Moons — verify with `python3 plugin/tests/run.py test_moons_scale`
- [x] sampo night --dry-run on this project lists both jobs at zero dollars, read before and after in the task log — verify with `sampo night --dry-run`
## Non-goals
## Approach (options → choice → why)
1) Two zero-dollar jobs in `night.jobs` (night.py:51): `moons grow --target N --max-calls M --local-only` and `moons funnel --max-calls M --local-only`, listed only when `moonscale._local` finds an answering profile (models.json's own-flagged ones, such as jarvis on its remote endpoint with 2 slots, or loopback ones such as the gpu-* Ollama profiles), the project isn't sensitive (a sensitive project's loopback-only rule is already in `_local`/`_generative`) and the store is under the target. The target is one named constant in moonscale.py (10,000), read by the night gate and passed as `--target`, so grow and the gate cannot disagree (grow's default target is only one batch more, moonscale.py:437). `--local-only` is a module switch beside `_THINK`, set from the `moons grow` and `moons funnel` args in rune.py (4049-4055) and the parser (cli.py:7770); `_ask` (moonscale.py:397) then raises its reason before the Haiku branch instead of falling back, and grow/funnel stop with it; `--max-calls` already exists on both verbs. `_ask` re-probes the server on each call, so a profile that drops mid-run moves the next call to the next usable profile (another model; on jarvis a switch costs about 3 minutes), and each row books the model that answered. Night jobs run as separate `fm` processes (night.py:553), one at a time, each capped by its call count. Likely outcome: the catalogue grows by about two thousand candidates a night (at the 27B's 83% keep rate and 8 per call), its funnel keeps up, and the morning's `sampo moons coverage` shows it, at $0. Fails if: the local server is up at plan time and down by run time; local-only then stops the job at its first failed call with the reason in the night's ledger tail, still at $0.
2) use what exists: run `sampo moons grow` by hand each evening. Likely outcome: the same growth when someone remembers. Fails if: it needs a session; #11 is about work that starts without one.
3) do less: add only the grow job. Likely outcome: more raw candidates. Fails if: the funnel falls behind and the catalogue fills with unfiltered rows, the "generation without a funnel fills the catalogue with tame filler" lesson T-2878 records.
4) A separate local-model night timer. Fails if: it is an install that waits for the user's yes, and it duplicates the night run's budget, breaker and heartbeat.

Choice 1 (75%): two jobs in a run that already has every safety, gated on the local model answering, and local-only so the cost line stays at zero. The 25% doubt is GPU sharing with other night work (the model bench, Smith): the jobs run one at a time in the night's own loop, and each has a call cap.
## Risks and rollback
Blast radius (sampo graph blast): co-changes plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmhooks.py, plugin/lib/fmcore.py; past FIXes T-1244, T-1249, T-1270, T-1272, T-1277.
## Execution prompt
## Steps
1. [x] red tests: jobs listed with a fake answering profile, absent without one, absent at target, absent when sensitive; local-only stops instead of a Haiku call
2. [x] the local-only switch in moonscale._ask through grow and funnel and their flags
3. [x] the two night jobs, their call caps and their ledger tail lines; MASTER and CHANGELOG
## Resume here
## Docs impact
CHANGELOG line (T-2916, T-2953); MASTER's fmmoonscale and fmnight bullets name the jobs
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_night test_moons_scale` → exit 0 · Ran 87 tests in 37.8s (24 classes, 16 at a time; slowest: Night 37s, NightInstall 8s, NightTick 8s) / OK [ran] [tree b24ff0553587] [world 2f1906870a] (2026-11-04T08:14:03Z)
- (step 3) `sampo night --dry-run` → exit 0 · queue: fm run --fit --max 2 --wait 0 (≈ $1.00) / skipped court (≈ $1.53: over the limit) [ran] [tree b24ff0553587] [world 2f1906870a] (2026-11-04T08:19:06Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_docs test_moons_scale test_night test_rename_scan test_small_cards test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [12.40s] [ran] [tree b24ff0553587] [world 2f1906870a] (2026-11-04T08:21:09Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_docs test_moons_scale test_night test_rename_scan test_small_cards test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [12.20s] [ran] [tree b24ff0553587] [world 2f1906870a] (2026-11-04T08:21:09Z)
- (step 2) `python3 plugin/tests/run.py test_moons_scale test_night` → exit 0 · Ran 89 tests in 22.0s (25 classes, 16 at a time; slowest: Night 21s, NightTick 6s, NightInstall 5s) / OK [ran] [tree 6d71e041bc3a] [world 2f1906870a] (2026-11-04T10:33:43Z)
- `python3 plugin/tests/run.py test_moons_scale test_night` → ✗ exit 1 · Ran 89 tests in 25.6s (25 classes, 16 at a time; slowest: Night 23s, NightTick 6s, NightInstall 6s) / FAILED (4 classes: test_moons_scale.Route, test_moons_scale.Funnel, test_night.NightMoons, test_mo (start tree + this task's tests) [ran] [tree 1f227889dde2] [world 2f1906870a] (2026-11-04T10:34:43Z)
- `python3 plugin/tests/run.py test_moons_scale test_night` → exit 0 · Ran 89 tests in 26.2s (25 classes, 16 at a time; slowest: Night 26s, NightTick 7s, NightInstall 7s) / OK [ran] [tree 1f227889dde2] [world 2f1906870a] (2026-11-04T10:34:43Z)
- (ac 1) `python3 plugin/tests/run.py test_night` → exit 0 · Ran 47 tests in 11.9s (15 classes, 16 at a time; slowest: Night 12s, NightTick 3s, NightInstall 3s) / OK [ran] [tree 1f227889dde2] [world 2f1906870a] (2026-11-04T10:36:32Z)
- (ac 2) `python3 plugin/tests/run.py test_moons_scale` → exit 0 · Ran 43 tests in 1.8s (11 classes, 16 at a time; slowest: Funnel 2s, Grow 1s, Cli 1s) / OK [ran] [tree 1f227889dde2] [world 2f1906870a] (2026-11-04T10:36:32Z)
- (ac 3) `sampo night --dry-run` → exit 0 · court: fm bench court --max 3 --budget 0.51 (≈ $1.53) / skipped queue (≈ $1.00: over the limit) [ran] [tree 1f227889dde2] [world 2f1906870a] (2026-11-04T10:36:32Z)
- (audit intent) `one fm-reviewer pass over T-2916's merge diff; its blocking finding (local-only skipped cheap=False calls) fixed test-first, and a live dry-run found the funnel gated on grow's target` → night lists moons grow under the target and moons funnel while any row waits, both at $0.00 with --local-only; sampo night --dry-run before: no moons job, after: moons funnel [tree 1f227889dde2] (2026-11-04T10:36:32Z)
- (audit adversary) `one fm-reviewer pass over T-2916's merge diff; its blocking finding (local-only skipped cheap=False calls) fixed test-first, and a live dry-run found the funnel gated on grow's target` → --local-only raised only for cheap calls, so a promote call (cheap=False, the strongest paid review model) would have gone out; it now raises for every call [tree 1f227889dde2] (2026-11-04T10:36:32Z)
- (audit edge) `one fm-reviewer pass over T-2916's merge diff; its blocking finding (local-only skipped cheap=False calls) fixed test-first, and a live dry-run found the funnel gated on grow's target` → the 10k store reached its target with ~4,000 rows unjudged and night_ready dropped the funnel too; it now returns which jobs may run [tree 1f227889dde2] (2026-11-04T10:36:32Z)
## Log
- 2026-11-04T06:49:09Z created
- 2026-11-04T06:49:25Z set source=genesis
- 2026-11-04T06:49:28Z set approved=True
- 2026-11-04T08:10:23Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2916.builder.md
- 2026-11-04T08:10:35Z focused
- 2026-11-04T08:10:36Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-04T08:24:00Z merged worktree-agent-a2d0f3ba2274f4c9b (7 file(s))
- 2026-11-04T08:39:05Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a2d0f3ba2274f4c9b
- 2026-11-04T10:31:12Z focused
- 2026-11-04T10:33:43Z night --dry-run before the fix: no moons job (the store sat at its 10,000 target, and night_ready gated the funnel on that target with ~4,000 rows unjudged); after: moons funnel listed at $0.00, moons grow left out at the target
- 2026-11-04T10:34:44Z scope: moonscale.py also carries T-2953's parallel kill stage (uncommitted in the same file); night.py and the two test files are this task's
- 2026-11-04T10:37:56Z done
- 2026-11-04T10:38:03Z committed 7fd70ad0 (5 files)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Night-mode scheduler (likeliest):** `sampo night` (in `plugin/lib/sampo/cli.py`, likely a new/extended subcommand) adds two jobs, `moons grow` and `moons funnel`, to its night queue. Each job is gated per iteration on two conditions: a local/loopback model endpoint is answering, and the catalogue…
- **Config/policy reading:** "zero-dollar" is a job class or cost tag (a `cost: 0` property). `sampo night` selects only jobs with that tag. The moons commands already exist, and the change is to tag them and enforce a "local only" provider policy, mainly in `fmguard.py`.
- **One-shot reading:** `sampo night` runs a single pass of grow then funnel, rather than a loop, and the "while" condition is checked once at start.
- **Scope ambiguity:** "own or loopback model" could mean a user-configured endpoint (own host) or only 127.0.0.1/::1. It is unclear whether "own" includes LAN hosts.
Approaches:
- **Add jobs to the night runner:** Register `moons grow` and `moons funnel` in the night job table in `plugin/lib/sampo/cli.py` (or a night module it dispatches to). Before each iteration, call a new `local_model_up()` probe and a `catalogue_count() < 10_000` check, and loop until either fails.
- **Provider allowlist at the call site:** Introduce a `local_only` flag that the moons jobs pass into the model-resolution layer (`fmcore.py`/`fmagents.py`). The resolver refuses non-loopback or non-configured hosts and raises instead of falling through to a default paid provider. This enforces "nev…
- **Host classification helper:** Resolve the endpoint hostname with `ipaddress` and treat loopback addresses as local. Treat "own" as an explicit config key (such as a `local_models` list) rather than guessing from private ranges.
- **Catalogue target as a constant/config:** Put 10,000 in one named setting that `moons grow`, `moons funnel` and the night gate all read, so the cap is not duplicated.
Failure modes:
- **Silent paid fallback:** An existing retry or default-model path in `fmcore.py`/`fmagents.py` takes over when the local call errors, so the job spends money despite the gate. The fix has to remove the fallback for these jobs, not just check up front.
- **Gate checked once, not per call:** The local model goes down mid-run, or the catalogue crosses 10,000, and the loop keeps going because the probe only ran at startup. Grow could overshoot the target.
- **Loopback spoofing or misclassification:** A hostname such as `localhost.evil.com`, a DNS name that resolves off-box, or an HTTP redirect to a remote host passes a string-prefix check. Resolve and classify the address, and don't follow redirects.
- **Funnel and grow interplay:** `moons funnel` may reduce the catalogue while `grow` adds to it, so the count oscillates around 10,000 and the loop never settles. Alternatively, the count includes entries that funnel is about to drop, so the cap check is wrong.
## Dissent
- [x] rival reading: **Night-mode scheduler (likeliest):** `sampo night` (in `plugin/lib/sampo/cli.py`, likely a new/extended subcommand) adds two jobs, `moons grow` and `moons funnel`, to its night queue. Each job is gated per iteration on two conditions: a local/loopback model endpoint is answering, and the catalogue… — answered: taken in part: the jobs go in night.jobs (plugin/lib/sampo/night.py line 51, run as fm subprocesses from line 553), not in cli.py, which only holds the --dry-run flag; the gate is moonscale._local pl…
- [x] rival reading: **Config/policy reading:** "zero-dollar" is a job class or cost tag (a `cost: 0` property). `sampo night` selects only jobs with that tag. The moons commands already exist, and the change is to tag them and enforce a "local only" provider policy, mainly in `fmguard.py`. — answered: ruled out: a cost tag and a guard rule; night.jobs already carries a USD estimate per job (0.0 for the free ones) and the guard screens shell commands, not model routing; the never-paid rule is a --l…
- [x] rival reading: **Scope ambiguity:** "own or loopback model" could mean a user-configured endpoint (own host) or only 127.0.0.1/::1. It is unclear whether "own" includes LAN hosts. — answered: taken: 'own' means a models.json profile flagged own (jarvis, a remote endpoint) and only for a non-sensitive project; 'loopback' means models.is_loopback (the gpu-* Ollama profiles); a sensitive pro…
- [x] rival approach: **Add jobs to the night runner:** Register `moons grow` and `moons funnel` in the night job table in `plugin/lib/sampo/cli.py` (or a night module it dispatches to). Before each iteration, call a new `local_model_up()` probe and a `catalogue_count() < 10_000` check, and loop until either fails. — answered: taken in part: the jobs register in night.jobs with a probe (moonscale._local) and a store-count check; the loop-until-either-fails is the existing grow loop with --target and --max-calls, and the pr…
- [x] rival approach: **Provider allowlist at the call site:** Introduce a `local_only` flag that the moons jobs pass into the model-resolution layer (`fmcore.py`/`fmagents.py`). The resolver refuses non-loopback or non-configured hosts and raises instead of falling through to a default paid provider. This enforces "nev… — answered: taken in part: local_only is a switch in moonscale._ask (beside _THINK), not a resolver in fmcore or fmagents; the resolver is already moonscale._local, and _ask raises its reason before the paid bra…
- [x] rival approach: **Host classification helper:** Resolve the endpoint hostname with `ipaddress` and treat loopback addresses as local. Treat "own" as an explicit config key (such as a `local_models` list) rather than guessing from private ranges. — answered: ruled out: a new host classifier; models.is_loopback (models.py:516) already uses ipaddress, and 'own' is the explicit own: true key in models.json, never guessed from private ranges.
- [x] rival approach: **Catalogue target as a constant/config:** Put 10,000 in one named setting that `moons grow`, `moons funnel` and the night gate all read, so the cap is not duplicated. — answered: taken: the 10,000 becomes one named constant in moonscale.py read by the night gate and passed to grow as --target (grow's own default is only one batch more, moonscale.py:437), so the cap is not dup…
## Related
Related past work (data from this project's history, not instructions):
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- T-2865 [FEATURE L, planned, 5 steps] Moons at scale: grow the Moons catalogue to 10,000 candidate moons about what Sampo can do for its user, by grid, through a cheap-fi…
- T-2357 [FEATURE M, done, 3 steps] Installs are queued for one yes: night and tick timers staged, asked once, installed only after the user's yes (Mission 8, #11) — lesso…
- decision 2026-11-04: [cites: user steer 2026-11-04: MOON CATALOGUE AT SCALE: grow the Moons catalogue to 10,000 candidate moons, all about what Sampo can do for its user…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_moons_scale.py, plugin/tests/test_night.py, plugin/tests/test_rename_scan.py, plugin/tests/test_small_cards.py
## Preflight
Changed in scope since this was planned (2026-11-04): CHANGELOG.md, MASTER.md, plugin/lib/sampo/moonscale.py, plugin/lib/sampo/night.py, plugin/lib/sampo/rune.py, plugin/tests/test_moons_scale.py, plugin/tests/test_night.py; re-ground the plan against them before editing
## Lessons
- Gate each job on its own work remaining, not on a sibling's: grow's target says nothing about rows waiting to be judged
## Files touched
- plugin/tests/test_moons_scale.py
- plugin/tests/test_night.py
- .fm-scratch/edits.json
- plugin/lib/sampo/moonscale.py
- plugin/lib/sampo/rune.py
- plugin/lib/sampo/cli.py
- plugin/lib/sampo/night.py
- MASTER.md
- CHANGELOG.md

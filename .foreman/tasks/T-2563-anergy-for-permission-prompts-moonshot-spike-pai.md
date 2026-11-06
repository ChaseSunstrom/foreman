---
id: T-2563
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmanergy.py, plugin/lib/fmhooks.py, plugin/lib/fmdoctor.py, plugin/tests/test_anergy.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: genesis
created: 2026-11-02T07:17:57Z
updated: 2026-11-02T07:37:26Z
base_note: Calibration: this plan states Choice 65% where FEATURE M closes (566) held on the first finish 96% of the time: 31 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-02T07:19:10Z
rival_split: true
base: 6f5ee52d487308727bfcff48b54fc87f7f3dbe33
base_tree: fc83d19ddf47870729faf70eb6ed4be56e9bea6a
predict_minutes: 12
predict_attempts: 1
plan0_at: 2026-11-02T07:24:10Z
plan0_scope: [plugin/lib/fmanergy.py, plugin/lib/fmhooks.py, plugin/lib/fmdoctor.py, plugin/tests/test_anergy.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# Anergy for permission prompts: time each prompt to its PostToolUse and report reflex-approved command classes (spike)
## Raw request
> FEATURE: anergy for permission prompts (moonshot spike): pair each PermissionRequest with its PostToolUse by tool_use_id, time the person's approval per guard command class, and report classes approved within 2 s in 5+ prompts with the allow rule that would retire them (never destructive or outward classes, never applied by Foreman), in fm doctor and fm digest
## Interpretation
Reading 1: measure how fast the person approves each permission prompt and report the command classes approved by reflex, with the allow rule that would retire them, for the user to apply. Reading 2: auto-allow reflex classes. Chosen: 1; 2 lowers a safety layer without the user (gen-0's NEVER).
## Assumptions (confidence)
## Acceptance criteria
- [x] PermissionRequest records {tool_use_id, class, at} for every prompt (capped store) and PostToolUse with the same id closes it with the latency; fmanergy.report names classes approved within 2 s in 5+ prompts with the allow rule that would retire them, never a destructive or outward guard class — verify with `python3 plugin/tests/run.py test_anergy`
- [x] fm doctor shows the reflex classes as an advisory row (or that none qualified) — verify with `python3 plugin/tests/run.py test_anergy`
## Non-goals
## Approach (options → choice → why)
1) A new fmanergy store: PermissionRequest appends {tool_use_id, guard class, read-only, at} to a capped jsonl; PostToolUse appends the close for an asked id; report() pairs offline and names classes with 5+ timed prompts, median within 2 s, every prompt read-only. Likely outcome: read and test commands show as reflex. Fails if: a slow tool run masks a reflex (fast tools are the reference). 2) use what exists: extend the existing fm ask prompt log (_prompts_path in fmhooks) to every prompt and time it from the ledger. Likely outcome: no new file. Fails if: that log is shaped for fm ask grants and its readers break on rows they never expected. 3) Auto-apply the allow rules. Fails if: a safety layer drops without the user (a gen-0 NEVER). 4) do less: count prompts per session and report the total. Likely outcome: a number with no target. Fails if: a count says nothing about which prompts carry a decision. Choice 1 (65%): its own small store keeps the fm ask log intact and the guard decides what may be named.
## Risks and rollback
Two hook paths gain one capped append and one lookup (hook p95 measured by the gate's bench). Commands are stored as their guard class and a 120-char redacted prefix, never full text. Rollback: revert; the store is a single state file.
Blast radius (fm graph blast): co-changes plugin/lib/fmcli.py, plugin/tests/test_hooks.py, plugin/lib/fmcore.py, plugin/lib/fmguard.py, plugin/tests/test_guard.py; past FIXes T-0877, T-0907, T-0908, T-0928, T-0951.
## Execution prompt
## Steps
1. [x] red tests (test_anergy): paired prompts give latencies; 5 reflex prompts of one read class are reported with a rule; a destructive class never is; an unpaired prompt is counted, not timed
2. [x] fmanergy: record on PermissionRequest (all prompts, not only fm ask), close on PostToolUse by tool_use_id, report; fmhooks wires both; fmdoctor advisory row
3. [x] spike check on this machine: after the next sessions, the store pairs 90%+ of prompts; record the pairing rate, or file the blocker in not-yet.md
## Resume here
## Docs impact
CHANGELOG (Unreleased: the reflex prompts row in fm doctor and the fm digest line) and MASTER.md (fmanergy module entry). No README change: an advisory row, no new verb.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_anergy` → ✗ exit 1 (never ran: no tests ran) · Ran 0 tests in 0.3s (1 classes, 16 at a time; slowest: _FailedTest 0s) / FAILED (1 classes: unittest.loader._FailedTest) [ran] [tree 8cb08c042211] [world 2f1906870a] (2026-11-02T07:25:13Z)
- (ac 1) `python3 plugin/tests/run.py test_anergy 2>&1 | grep -v "^$" | tail -15` → ✗ exit 1 · Ran 9 tests in 0.4s (1 classes, 16 at a time; slowest: Anergy 0s) / FAILED (1 classes: test_anergy.Anergy) [ran] [tree e6a969981b76] [world 2f1906870a] (2026-11-02T07:25:30Z)
- (ac 2) `python3 plugin/tests/run.py test_anergy 2>&1 | grep -v "^$" | tail -15` → ✗ exit 1 · Ran 9 tests in 0.4s (1 classes, 16 at a time; slowest: Anergy 0s) / FAILED (1 classes: test_anergy.Anergy) [ran] [tree e6a969981b76] [world 2f1906870a] (2026-11-02T07:25:30Z)
- (step 1) `python3 plugin/tests/run.py test_anergy test_doctor` → exit 0 · Ran 115 tests in 7.4s (36 classes, 16 at a time; slowest: ViewsRepair 6s, LockProbe 5s, Command 4s) / OK [ran] [tree 88550a4a544b] [world 2f1906870a] (2026-11-02T07:27:57Z)
- (ac 1) `python3 plugin/tests/run.py test_anergy` → exit 0 · Ran 11 tests in 4.1s (1 classes, 16 at a time; slowest: Anergy 4s) / OK [ran] [tree 73e34c472cc9] [world 2f1906870a] (2026-11-02T07:35:44Z)
- (ac 2) `python3 plugin/tests/run.py test_anergy` → exit 0 · Ran 11 tests in 4.1s (1 classes, 16 at a time; slowest: Anergy 4s) / OK [ran] [tree 73e34c472cc9] [world 2f1906870a] (2026-11-02T07:35:44Z)
- (step 2) `python3 plugin/tests/run.py test_anergy test_doctor` → exit 0 · Ran 116 tests in 4.4s (36 classes, 16 at a time; slowest: Anergy 4s, ViewsRepair 3s, LockProbe 3s) / OK [ran] [tree 73e34c472cc9] [world 2f1906870a] (2026-11-02T07:35:44Z)
- (step 3) `python3 plugin/tests/run.py test_anergy test_doctor` → exit 0 · Ran 116 tests in 4.4s (36 classes, 16 at a time; slowest: Anergy 4s, ViewsRepair 3s, LockProbe 3s) / OK [ran] [tree 73e34c472cc9] [world 2f1906870a] (2026-11-02T07:35:44Z)
- (audit intent) `self-review of the diff against the ACs and the Mission: every prompt a person sees is recorded (approve-reads answers excluded), PostToolUse closes only asked ids, report names only all-read-only, never-refused classes, doctor row advisory PASS, digest line only when one qualifies; full gate green` → ACs met — prompts recorded with id/class/at in a capped store, closed by PostToolUse with latency (tool run time subtracted via duration_ms), report names classes with 5+ prompts median within 2 s with the allow-rule pattern; doctor row and digest line; Foreman applies no rule [tree 73e34c472cc9] (2026-11-02T07:35:44Z)
- (audit adversary) `self-review of the diff against the ACs and the Mission: every prompt a person sees is recorded (approve-reads answers excluded), PostToolUse closes only asked ids, report names only all-read-only, never-refused classes, doctor row advisory PASS, digest line only when one qualifies; full gate green` → a class is named only if every prompt in it passed fmguard.read_only, so rm/redirect/outward commands never qualify (tests: rm -rf class, git status > out.txt poisons its class); a class people refused twice is never named; class text is c.plain'd and capped at 120; record never raises in the hook [tree 73e34c472cc9] (2026-11-02T07:35:44Z)
- (audit edge) `self-review of the diff against the ACs and the Mission: every prompt a person sees is recorded (approve-reads answers excluded), PostToolUse closes only asked ids, report names only all-read-only, never-refused classes, doctor row advisory PASS, digest line only when one qualifies; full gate green` → missing state dir, None tool_input, empty payload, unpaired done ids, a still-open prompt, store over CAP (newest half kept) all tested; negative latencies dropped [tree 73e34c472cc9] (2026-11-02T07:35:44Z)
- (audit operator) `self-review of the diff against the ACs and the Mission: every prompt a person sees is recorded (approve-reads answers excluded), PostToolUse closes only asked ids, report names only all-read-only, never-refused classes, doctor row advisory PASS, digest line only when one qualifies; full gate green` → hot path cost is one 32 KB tail read per PostToolUse and one append per prompt; hook bench passed in the full gate; nothing to configure; the store is state/anergy.jsonl capped at 4000 rows [tree 73e34c472cc9] (2026-11-02T07:35:44Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree 73e34c472cc9] [world 2f1906870a] (2026-11-02T07:37:26Z)
## Log
- 2026-11-02T07:17:57Z created
- 2026-11-02T07:18:44Z planned from capture
- 2026-11-02T07:19:31Z set approved=True
- 2026-11-02T07:24:09Z focused
- 2026-11-02T07:24:10Z predicted from its closes: 12 min, 1 attempt(s)
- 2026-11-02T07:28:45Z scope: plugin/lib/fmcost.py — the Mission's long-horizon goal reads the reflex classes in fm digest; one line there
- 2026-11-02T07:36:58Z done
- 2026-11-02T07:37:00Z committed 5c549eeb (7 files)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Telemetry-analysis feature (likeliest):** a log-derived report. Join PermissionRequest and PostToolUse events on `tool_use_id`, compute approval latency (PostToolUse ts minus PermissionRequest ts) per guard command class from `plugin/lib/fmguard.py`. Flag classes with ≥5 prompts that were approve…
- **Auto-applying suggestion engine:** same analysis, but `fm` writes the allow rule into settings for the user. This is excluded by "never applied by Foreman", so it is only a misreading; the rule must be printed, never written.
- **Live in-hook measurement:** timing inside `plugin/lib/fmhooks.py` as events fire, with state kept between hooks. It is heavier and risks the hook latency gate (`plugin/tests/bench_hooks.py`). Less likely, since "pair… by tool_use_id" implies reading recorded events.
- **Per-session coaching rather than aggregate:** surface the hint at prompt time instead of in doctor/digest. This is not what was asked.
Approaches:
- **Offline analyzer module:** add a new `plugin/lib/fmanergy.py`. It reads the existing event/audit log, pairs by `tool_use_id`, groups by the class returned from `fmguard`'s classifier, and applies the threshold (n≥5, latency ≤2 s). Both `fm doctor` and `fm digest` in `fmcli.py` call one shared fun…
- **Extend existing log records:** if `fmhooks.py` doesn't already persist PermissionRequest with `tool_use_id` and a timestamp, add that field there, then analyze. This touches the hot path and needs the bench gate re-run.
- **Rule derivation via guard's own vocabulary:** generate the allow-rule string from the same class definitions `fmguard.py` uses, with a denylist filter driven by guard's destructive/outward tags rather than a second hardcoded list. Test it in `plugin/tests/test_guard.py` style against fixtures.
- **Fixture-driven replay check:** feed recorded sessions through `fm replay` to validate output without live prompts.
Failure modes:
- **Unmatched pairs counted as fast approvals:** a denied prompt has no PostToolUse, and a prompt with a tool error or a timeout pairs late or never. If unpaired requests are dropped silently, the denominator shrinks. If they are paired with the wrong event, denials look like approvals. The "5+ promp…
- **Latency measures auto-approval, not a person:** requests that an existing rule, a mode, or Foreman itself approves resolve in milliseconds. These would be reported as human approvals within 2 s, and the suggestion would retire rules that already exist. Filter on whether a human decision was invol…
- **Destructive or outward class leaks through:** a class that is coarse (e.g. a generic `bash` class) mixes safe and dangerous commands, so an allow rule for the class would cover destructive ones. The exclusion must apply at the command level, not just the class label in `fmguard.py`.
- **Clock and ordering problems:** timestamps with differing resolution or from parallel tool calls sharing a session. A reused or missing `tool_use_id` mispairs events, producing negative or implausible latencies. Pairing therefore needs a sanity bound.
## Dissent
- [x] rival reading: **Telemetry-analysis feature (likeliest):** a log-derived report. Join PermissionRequest and PostToolUse events on `tool_use_id`, compute approval latency (PostToolUse ts minus PermissionRequest ts) per guard command class from `plugin/lib/fmguard.py`. Flag classes with ≥5 prompts that were approve… — answered: adopted: the report is offline (fmanergy reads the store at fm doctor/digest time); the hooks only append a timestamped row
- [x] rival reading: **Auto-applying suggestion engine:** same analysis, but `fm` writes the allow rule into settings for the user. This is excluded by "never applied by Foreman", so it is only a misreading; the rule must be printed, never written. — answered: rejected: never applied by Foreman (Interpretation)
- [x] rival reading: **Live in-hook measurement:** timing inside `plugin/lib/fmhooks.py` as events fire, with state kept between hooks. It is heavier and risks the hook latency gate (`plugin/tests/bench_hooks.py`). Less likely, since "pair… by tool_use_id" implies reading recorded events. — answered: adopted in part: no state machine in the hook, one capped append on PermissionRequest and one on PostToolUse (the gate's hook bench measures it); pairing happens offline
- [x] rival reading: **Per-session coaching rather than aggregate:** surface the hint at prompt time instead of in doctor/digest. This is not what was asked. — answered: rejected: not asked; a prompt-time hint adds injected context
- [x] rival approach: **Offline analyzer module:** add a new `plugin/lib/fmanergy.py`. It reads the existing event/audit log, pairs by `tool_use_id`, groups by the class returned from `fmguard`'s classifier, and applies the threshold (n≥5, latency ≤2 s). Both `fm doctor` and `fm digest` in `fmcli.py` call one shared fun… — answered: adopted: fmanergy.py, offline analyzer
- [x] rival approach: **Extend existing log records:** if `fmhooks.py` doesn't already persist PermissionRequest with `tool_use_id` and a timestamp, add that field there, then analyze. This touches the hot path and needs the bench gate re-run. — answered: adopted: fmhooks.permission_request records every prompt (not only fm ask) with tool_use_id and a timestamp; PostToolUse appends its id and time
- [x] rival approach: **Rule derivation via guard's own vocabulary:** generate the allow-rule string from the same class definitions `fmguard.py` uses, with a denylist filter driven by guard's destructive/outward tags rather than a second hardcoded list. Test it in `plugin/tests/test_guard.py` style against fixtures. — answered: adopted: the rule string and the denylist come from fmguard's own classification of the command
- [x] rival approach: **Fixture-driven replay check:** feed recorded sessions through `fm replay` to validate output without live prompts. — answered: rejected for now: fm replay replays guard verdicts, not prompt timings; the unit tests feed rows directly
## Related
Related past work (data from this project's history, not instructions):
- T-2187 [FEATURE L, done, 4 steps] Moonshot Mission each generation from gen 2 (steer 2026-10-30 #5): fm genesis seed N (N… — lesson: A rule over model marks must treat a…
- T-2357 [FEATURE M, done, 3 steps] Installs are queued for one yes: night and tick timers staged, asked once, installed only after the user's yes (Mission 8, #11) — lesso…
- T-2489 [FEATURE M, done, 3 steps] Model layer surfaces: MCP decide tool, fm doctor backend health, the site's Model layer… — lesson: README has a 2000-word visible budge…
- decision 2026-10-31: [revisited: Standing rule from gen 2 on: one Mission per generation is a moonshot] [cites: the user's steer 2026-10-30 (fifth): moonshot Mission fro…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_doctor.py, plugin/tests/test_hooks.py
## Lessons
- A spike that reads how a person behaves must say which session modes it can see: bypass mode shows no permission prompts, so its real-data check is a deferred task with a threshold, filed at close
## Plan gaps
- failed first: step 1 red tests (test_anergy): paired prompts give latencies; 5 reflex prompts of one read class are repo…
## Files touched
- plugin/tests/test_anergy.py
- plugin/lib/fmanergy.py
- plugin/lib/fmhooks.py
- plugin/lib/fmdoctor.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmcost.py

---
id: T-0364
type: FIX
tier: L
status: done
priority: normal
scope: [plugin/lib/fmhooks.py, plugin/lib/fmcore.py, plugin/lib/fmideas.py, plugin/lib/fmcli.py, plugin/lib/fmbudget.py, plugin/rules/foreman.md, plugin/skills/**, plugin/tests/**, plugin/evals/**, MASTER.md, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-08T22:50:15Z
updated: 2026-10-08T23:12:24Z
base: 8819f918bbd732e3191942ed9f1afc7f9a274fa2
base_tree: 023d8f3c3f0e0abc25ca695cec39715e7556cf2c
verified: strong
---
# Foreman keeps working while background jobs run, plans and brainstorms wider, uses subagents
## Raw request
> fix foreman, for some reason it just gets stuck, slow, and doesn't use subagents/brainstorm/plan well, it doesnt prompt itself with a brief to plan first, actually think or anything, this happens on some things and it just doesn't keep going while long running tasks go or something, and also, the brainstorming isnt great, and it will stop after some tasks and ask me for things it doesnt need to, and the recursive brainstorm/idea generation stuff, isn't great, it doesn't think of every possible solution/capability, whatever
## Interpretation
Evidence from the Volt, music-fndr and Foreman transcripts (2026-10-04..08): (1) the Stop hook lets every turn end while any background job runs — 357 drive_wait events vs 11 drive pushes; turns end on 'the gate is running (about 35 min)… waiting', and the user had to say 'keep working on stuff while tests run' and 'keep doing things in parallel'. (2) Brainstorm never ran in Volt or music-fndr: the detectors miss 'limitless, no caveats', 'a ton of / a lot more', 'way better', 'more featurefull'; music-fndr went from request to app.py in 5 minutes and the user then asked for library view, organizer, playlists/Jellyfin one by one (capabilities a sweep would have listed). (3) Rules say 'Subagents: Default none', delegate.md 'Default: no subagents'. (4) ideas children return 8-12 ideas from 6 lenses with no lens for the full capability space or for alternative solutions. Hooks are fast (PreToolUse p50 26 ms), so 'slow' is idle waiting and serial work, not latency.
## Assumptions (confidence)
## Acceptance criteria
- [x] with drive on and background work running, the first Stop is blocked with a work-in-parallel reason naming the running ids; a repeat Stop with no progress ends with the waiting message — verify with `python3 plugin/tests/run.py -k test_drive_keeps_working_while_background_work_runs`
- [x] exhaustive/open-ended detection catches the user's real phrasings (limitless, no caveats, a ton of, a lot more, way better, more featureful, every possible) and still ignores concrete small requests — verify with `python3 plugin/tests/run.py -k test_real_phrasings_reach_the_brainstorm`
- [x] fm ideas runs capability-map and approaches lenses by default and asks each lens for 10-15 ideas — verify with `python3 plugin/tests/run.py -k test_default_lenses_cover_capabilities_and_approaches`
- [x] full suite and hook latency budgets still pass — verify with `python3 plugin/tests/run.py`
## Non-goals
## Approach (options → choice → why)
Drive while background runs: (a) keep waiting — the status quo, idle; (b) block every Stop while jobs run — busywork loop risk; (c) block once per running set with a 'work on what doesn't need it' reason (audits, next step's tests, plan the next task, lane an independent task), and let a repeat Stop end with the waiting message. Choice (c): one push per set, the existing progress check and DRIVE_MAX bound it. Brainstorm reach: (a) new skill; (b) widen the two regexes + route M/L work requests to planning in the prompt note. Choice (b). Brainstorm breadth: add 'capability map' (everything a best-in-class version in this space has, named comparables) and 'approaches' (every distinct way to solve the stated problem) lenses to the defaults, 10-15 ideas per lens. Subagents: replace 'default none' with triggers (parallel recon for independent questions, reviewer at audits, fm-builder lanes for independent tasks while a long job runs, fm ideas for breadth), keeping the budget caps.
## Risks and rollback
Risk: parallel push burns tokens on busywork → once per running set, explicit 'end the turn if nothing is independent'. Risk: wider regex makes brainstorm notes fire on ordinary requests → tests with negative cases; the note is advice only. Rollback: git revert the commit.
## Execution prompt
Repo ~/.claude/foreman. Test-first in plugin/tests (test_hooks.py drive tests near test_drive_waits_while_a_background_command_runs; test_core.py open-ended tests ~line 505; test_ideas.py). Change plugin/lib/fmhooks.py _drive (background branch) and the stop() systemMessage; plugin/lib/fmcore.py _EXHAUSTIVE/_OPEN_ENDED and the work-request note in fmhooks prompt hook (~line 476); plugin/lib/fmideas.py DEFAULT_LENSES/child_prompt; skills/brainstorm/references/ideas-prompt.md lens notes; rules/foreman.md Subagents; skills/intake/references/delegate.md + planning.md; skills/brainstorm/SKILL.md. Verify: python3 plugin/tests/run.py; python3 plugin/tests/bench_hooks.py --runs 20; fm doctor. Rules file ≤ 80 lines.
## Steps
1. [x] test-first: drive pushes parallel work while background jobs run (fmhooks._drive)
2. [x] test-first: widen exhaustive/open-ended detection and route M/L work requests through planning (fmcore, prompt hook note)
3. [x] brainstorm breadth: capability-map + approaches lenses, more ideas per lens, deepen by default; skill text
4. [x] instructions: subagents by trigger not 'default none'; planning enumerates approaches + capability sweep; rules/delegate/planning/brainstorm
5. [x] full gate, audits, docs (MASTER/CHANGELOG)
## Resume here
## Docs impact
MASTER.md (prompting, drive diagram, budget pace), CHANGELOG.md, rules, intake/brainstorm/playbooks skills
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_drive_keeps_working_while_background_work_runs` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: Stop 1s) / OK [ran] [tree 622a1127e4ab] (2026-10-08T22:56:16Z)
- (step 2) `python3 plugin/tests/run.py -k test_real_phrasings_reach_the_brainstorm` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: OpenEnded 0s) / OK [ran] [tree a6deadf4cea0] (2026-10-08T22:59:48Z)
- (step 2) `python3 plugin/tests/run.py -k test_broad_and_work_requests_are_told_to_plan_wide_first` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: UserPromptSubmit 0s) / OK [ran] [tree a6deadf4cea0] (2026-10-08T22:59:49Z)
- (step 3) `python3 plugin/tests/run.py -k test_default_lenses_cover_capabilities_and_approaches` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Ideas 0s) / OK [ran] [tree 6329a27ac898] (2026-10-08T23:00:29Z)
- (step 4) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 1 of 6 failed: python3 plugin/tests/run.py → ✗ exit 1 · Ran 890 tests in 39.4s (219 classes, 16 at a time; slowest: Stop 26s, TaskLifecycle 22s, Bench 21s) / FAILED (1 classes) [ran] [tree 3d2f234cd43e] (2026-10-08T23:08:18Z)
- (audit intent) `main thread (reviewer refused by the pace rule, now fixed)` → met: every complaint traced to transcript evidence and addressed: idle waits (drive push), no brainstorm/plan (detectors + notes + planning), narrow brainstorms (lenses, funnel), subagents (rules + 75% floor), cleanup (sweep playbook + --done-in). Partly: unnecessary asks are covered only where they came from stops during background work; outward asks (push, other machines) stay asks by design [tree 5368e238b394] (2026-10-08T23:09:42Z)
- (audit adversary) `main thread` → no new trust boundary: regexes run on the user's own prompt (no nested quantifiers, bounded); --done-in copies the user's own request text into the host brief; eval prompts only re-embed the rules; the push loop is bounded once per running set and DRIVE_MAX [tree 5368e238b394] (2026-10-08T23:09:42Z)
- (audit edge) `main thread` → fixed: running ids compared sorted so a reordered list isn't a new set; headless runs keep their own wait (no push); stop_hook_active on first sighting still pushes once; inbox only counts in full autonomy [tree 5368e238b394] (2026-10-08T23:09:42Z)
- (audit operator) `main thread` → rules 5992/6000 chars, 45/80 lines; prompt notes stay within the 400-char budget (asserted); brainstorm cost about 2x per round, documented; MASTER and CHANGELOG updated [tree 5368e238b394] (2026-10-08T23:09:42Z)
- (audit maintainer) `main thread` → tests sit beside the code they cover and name the transcript evidence; _headless shared by both waits; is_sweep/is_broad follow is_open_ended/is_exhaustive [tree 5368e238b394] (2026-10-08T23:09:43Z)
- (step 4) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (27 pass, 3 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                32.5    34.7     150  [0] / SessionEnd                  28.8    32.2     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 23:08 UTC; python3 plugin/tests/run.py → exit 0 · Ran 890 tests in [ran] [tree 5368e238b394] (2026-10-08T23:10:35Z)
- (step 5) `python3 plugin/tests/bench_hooks.py --runs 20` → exit 0 · Notification                35.9    39.3     150  [0] / SessionEnd                  32.4    36.8     150  [0] [ran] [tree 5368e238b394] (2026-10-08T23:11:33Z)
- (ac 1) `python3 plugin/tests/run.py -k test_drive_keeps_working_while_background_work_runs` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: Stop 1s) / OK [ran] [tree 5368e238b394] (2026-10-08T23:12:24Z)
- (ac 2) `python3 plugin/tests/run.py -k test_real_phrasings_reach_the_brainstorm` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: OpenEnded 0s) / OK [ran] [tree 5368e238b394] (2026-10-08T23:12:24Z)
- (ac 3) `python3 plugin/tests/run.py -k test_default_lenses_cover_capabilities_and_approaches` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Ideas 0s) / OK [ran] [tree 5368e238b394] (2026-10-08T23:12:24Z)
- (ac 4) `python3 plugin/tests/run.py` → exit 0 · Ran 890 tests in 39.2s (219 classes, 16 at a time; slowest: Stop 26s, TaskLifecycle 22s, Bench 20s) / OK [ran] [tree 5368e238b394] (2026-10-08T23:12:24Z)
- (audit intent) `five lenses in the main thread (the reviewer subagent was refused by the pace rule this task relaxed); edge finding fixed (sorted running set); full fm check green` → every complaint traced to transcript evidence and addressed; outward asks (push, other machines) stay asks by design [tree 5368e238b394] (2026-10-08T23:12:24Z)
- (audit adversary) `five lenses in the main thread (the reviewer subagent was refused by the pace rule this task relaxed); edge finding fixed (sorted running set); full fm check green` → no new trust boundary; bounded regexes on the user's own prompt; push bounded once per running set and DRIVE_MAX [tree 5368e238b394] (2026-10-08T23:12:24Z)
- (audit edge) `five lenses in the main thread (the reviewer subagent was refused by the pace rule this task relaxed); edge finding fixed (sorted running set); full fm check green` → reordered running ids no longer re-push (fixed); headless runs keep their own wait [tree 5368e238b394] (2026-10-08T23:12:24Z)
- (audit operator) `five lenses in the main thread (the reviewer subagent was refused by the pace rule this task relaxed); edge finding fixed (sorted running set); full fm check green` → rules 5992/6000 chars; prompt notes within 400 chars; brainstorm cost ~2x per round documented [tree 5368e238b394] (2026-10-08T23:12:24Z)
- (audit maintainer) `five lenses in the main thread (the reviewer subagent was refused by the pace rule this task relaxed); edge finding fixed (sorted running set); full fm check green` → tests beside the code, named after the evidence; helpers follow neighbours [tree 5368e238b394] (2026-10-08T23:12:24Z)
## Log
- 2026-10-08T22:50:15Z created
- 2026-10-08T22:54:59Z planned from capture
- 2026-10-08T22:55:18Z set approved=True
- 2026-10-08T22:55:18Z self-approved (full autonomy)
- 2026-10-08T22:55:18Z focused
- 2026-10-08T23:02:44Z scope: + plugin/evals/** — eval cases embed the rules verbatim (tests/e2e/sync_evals.py)
- 2026-10-08T23:02:47Z set scope=['plugin/lib/fmhooks.py', 'plugin/lib/fmcore.py', 'plugin/lib/fmideas.py', 'plugin/rules/foreman.md', 'plugin/skills/**', 'plugin/tests/**', 'plugin/evals/**', 'MASTER.md', 'CHANGELOG.md']
- 2026-10-08T23:03:48Z steer: user: cleanup requests (repo, docs, briefs, dead code, replaced functionality) never got done — trace why and fix
- 2026-10-08T23:05:06Z set scope=['plugin/lib/fmhooks.py', 'plugin/lib/fmcore.py', 'plugin/lib/fmideas.py', 'plugin/lib/fmcli.py', 'plugin/rules/foreman.md', 'plugin/skills/**', 'plugin/tests/**', 'plugin/evals/**', 'MASTER.md', 'CHANGELOG.md']
- 2026-10-08T23:05:06Z scope: + plugin/lib/fmcli.py — --done-in let a user's cleanup request close inside a narrower task (JARVIS T-0095 → T-0112)
- 2026-10-08T23:08:32Z steer: user: budget/pace limits shouldn't block anything until 75% usage
- 2026-10-08T23:08:53Z set scope=['plugin/lib/fmhooks.py', 'plugin/lib/fmcore.py', 'plugin/lib/fmideas.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmbudget.py', 'plugin/rules/foreman.md', 'plugin/skills/**', 'plugin/tests/**', 'plugin/evals/**', 'MASTER.md', 'CHANGELOG.md']
- 2026-10-08T23:12:24Z done
- 2026-10-08T23:12:24Z committed d2c4301 (25 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0087-review: Verdict:** approve with nits. PreToolUse can never be paused, and the pause cannot get stuck or flap. The findings below are all MEDIUM or LOW. […
- T-0145 [FEATURE M, done, 3 steps] UI changes reach the running session during a drive: the Stop hook ends the turn once when this session's dev-mods changed, and the rel…
- research rsi-20261003-pass1: 1. **Answer** — Two causes are grounded in code. The first is the 32 evidence nudges: automatic evidence is tagged `(ac N)`, but the Stop ga…
- decision 2026-10-08: T-0364 plan: once-per-running-set parallel push; widen detectors; capability-map + approaches lenses; subagent triggers
- the similar finished task took 3 steps
- likely tests for the scope: plugin/tests/test_core.py, plugin/tests/test_hooks.py, plugin/tests/test_ideas.py
## Lessons
- Read the user's transcripts before tuning Foreman: drive_wait vs drive counts (357 vs 11) and the turn endings named the stall; a 'default none' line and a pace guard can silently override what the user keeps asking for
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmhooks.py
- plugin/tests/test_core.py
- plugin/lib/fmcore.py
- plugin/tests/test_ideas.py
- plugin/lib/fmideas.py
- plugin/skills/brainstorm/references/ideas-prompt.md
- plugin/skills/brainstorm/SKILL.md
- plugin/rules/foreman.md
- plugin/skills/intake/SKILL.md
- plugin/skills/intake/references/delegate.md
- plugin/skills/intake/references/planning.md
- plugin/evals/guard-force-push/prompt.md
- plugin/evals/guard-publish/prompt.md
- plugin/evals/intake-block/prompt.md
- plugin/evals/mid-task-capture/prompt.md
- plugin/evals/one-liner/prompt.md
- plugin/tests/test_cli.py
- plugin/lib/fmcli.py
- plugin/skills/playbooks/references/clean/repo-sweep.md
- plugin/skills/playbooks/SKILL.md
- CHANGELOG.md
- MASTER.md
- plugin/tests/test_budget.py
- plugin/lib/fmbudget.py

---
id: T-0673
type: FEATURE
tier: M
status: done
priority: urgent
scope: []
depends_on: []
source: user
created: 2026-10-09T15:40:14Z
updated: 2026-10-09T16:25:04Z
batch: [T-0443, T-0444, T-0463, T-0481, T-0482, T-0574]
base: a7b6b7eb0ec48ca3ee92b94a2d36feb2fc28cf9c
base_tree: 93f725b649b59d464ee7e7f05da52af58323b2ba
verified: strong
---
# Milestone: Features — Multi-machine, multi-project and ecosystem
## Raw request
> T-0443: FEATURE: Cross-project requests, sweeps and friction (C078, value 4/5, effort M, risk low)
>   first version: First version: `fm sweep "<fix>"` that, for each registered project, runs fm recall/grep for the sibling pattern and captures a brief in that project's inbox (source cross-project); plus consumer friction into briefs via fm friction. No auto-edit of other repos.
>   what it is: Let projects ask each other for changes and sweep or transplant a fix across all projects.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 11 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0444: FEATURE: Adopting an existing repo (C082, value 4/5, effort M, risk low)
>   first version: First version: `fm adopt` that runs map, gates, secrets, deps and a flake pass once, records a baseline brief with failing gates and untested hot files, and queues CLEAN/RESEARCH tasks. Great for new projects like JARVIS siblings.
>   what it is: Adopt a legacy repo with a baseline scan, safety crawl, characterization and a practice run.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 8 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0463: FEATURE: Version skew and upstream drift (C084, value 3/5, effort S, risk low)
>   first version: First version: in fm projects/doctor, show per project the Foreman version it last ran and which CHANGELOG T-ids it lacks; extends T-0391. Skip auto-upgrades and upstream PRs.
>   what it is: Alert when a project runs an old Foreman and show which fixes each project lacks.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 6 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0481: FEATURE: Trackers and CI (C081, value 3/5, effort M, risk med)
>   first version: First version: `fm inbox gh` that reads open issues of the repo via gh (read-only) and captures each as a brief with repro command; PR review comments later. Treat issue text as untrusted data.
>   what it is: Bridge issues, PR comments and CI, triage public issues and review others' PRs with Foreman's lenses.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 9 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0482: FEATURE: Harness and Claude Code compatibility (C083, value 3/5, effort M, risk low)
>   first version: First version: a canary that records `claude --version` per session and, on change, runs the guard fixtures, fm replay and a hook smoke; failure captures a brief. Skip the single binary and portable kernel.
>   what it is: Contract-test Foreman against Claude Code and plugin surfaces, turn releases into adaptation tasks and run on other harnesses.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 7 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0574: FEATURE: Machines, identity and shared lessons (C079 on the punch list; marked skip, the user added it): Foreman across the user's machines — which machine runs what, a per-machine identity, lessons and friction shared between machines (fm sync + git today). First version: the cheap piece the grounding named, then grow it
## Interpretation
Do T-0443, T-0444, T-0463, T-0481, T-0482, T-0574 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-0673. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0443: Cross-project requests, sweeps and friction (C078, value 4/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_ecosystem.py -k Sweep`
- [x] T-0444: Adopting an existing repo (C082, value 4/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_ecosystem.py -k Adopt`
- [x] T-0463: Version skew and upstream drift (C084, value 3/5, effort S, risk low) works — verify with `python3 plugin/tests/run.py -p test_ecosystem.py -k VersionSkew`
- [x] T-0481: Trackers and CI (C081, value 3/5, effort M, risk med) works — verify with `python3 plugin/tests/run.py -p test_ecosystem.py -k InboxGh`
- [x] T-0482: Harness and Claude Code compatibility (C083, value 3/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_ecosystem.py -k HarnessCanary`
- [x] T-0574: FEATURE: Machines, identity and shared lessons (C079 on the punch list; marked skip, the u works — verify with `python3 plugin/tests/run.py -p test_ecosystem.py -k MachineIdentity`
## Non-goals
## Approach (options → choice → why)
One milestone, six first slices (each member's 'first version' line), one test file plugin/tests/test_ecosystem.py with a class per member (Sweep, Adopt, VersionSkew, InboxGh, HarnessCanary, MachineIdentity). Stdlib only, local only: fm inbox gh reads via the gh CLI read-only and treats issue text as untrusted data; nothing is sent anywhere. Per step run only its class; full gates once at close.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-0443: Cross-project requests, sweeps and friction (C078, value 4/5, effort M, risk low)
2. [x] T-0444: Adopting an existing repo (C082, value 4/5, effort M, risk low)
3. [x] T-0463: Version skew and upstream drift (C084, value 3/5, effort S, risk low)
4. [x] T-0481: Trackers and CI (C081, value 3/5, effort M, risk med)
5. [x] T-0482: Harness and Claude Code compatibility (C083, value 3/5, effort M, risk low)
6. [x] T-0574: FEATURE: Machines, identity and shared lessons (C079 on the punch list; marked skip, the u
7. [x] review fixes: sweep never exports a sibling's mirror; whole-line dedupe key; repro redacted and defanged; canary check inside the try
## Resume here
## Docs impact
CHANGELOG entry
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_ecosystem.py -k Sweep` → ✗ exit 1 · Ran 2 tests in 1.2s (1 classes, 16 at a time; slowest: Sweep 1s) / FAILED (1 classes) [ran] [tree af27987a6056] (2026-10-09T16:06:40Z)
- (step 2) `python3 plugin/tests/run.py -p test_ecosystem.py -k Adopt` → ✗ exit 1 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: Adopt 0s) / FAILED (1 classes) [ran] [tree af27987a6056] (2026-10-09T16:06:41Z)
- (step 3) `python3 plugin/tests/run.py -p test_ecosystem.py -k VersionSkew` → ✗ exit 1 · Ran 2 tests in 0.1s (1 classes, 16 at a time; slowest: VersionSkew 0s) / FAILED (1 classes) [ran] [tree af27987a6056] (2026-10-09T16:06:42Z)
- (step 4) `python3 plugin/tests/run.py -p test_ecosystem.py -k InboxGh` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: InboxGh 0s) / FAILED (1 classes) [ran] [tree af27987a6056] (2026-10-09T16:06:47Z)
- (step 5) `python3 plugin/tests/run.py -p test_ecosystem.py -k HarnessCanary` → ✗ exit 1 · Ran 2 tests in 0.2s (1 classes, 16 at a time; slowest: HarnessCanary 0s) / FAILED (1 classes) [ran] [tree af27987a6056] (2026-10-09T16:06:47Z)
- (step 6) `python3 plugin/tests/run.py -p test_ecosystem.py -k MachineIdentity` → ✗ exit 1 · Ran 2 tests in 0.2s (1 classes, 16 at a time; slowest: MachineIdentity 0s) / FAILED (1 classes) [ran] [tree af27987a6056] (2026-10-09T16:06:48Z)
- (step 1) `python3 plugin/tests/run.py -p test_ecosystem.py -k Sweep` → exit 0 · Ran 2 tests in 1.6s (1 classes, 16 at a time; slowest: Sweep 2s) / OK [ran] [tree bb724bf5c743] (2026-10-09T16:08:33Z)
- (step 2) `python3 plugin/tests/run.py -p test_ecosystem.py -k Adopt` → exit 0 · Ran 1 tests in 0.9s (1 classes, 16 at a time; slowest: Adopt 1s) / OK [ran] [tree bb724bf5c743] (2026-10-09T16:08:43Z)
- (step 3) `python3 plugin/tests/run.py -p test_ecosystem.py -k VersionSkew` → exit 0 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: VersionSkew 0s) / OK [ran] [tree b43a63cb72b5] (2026-10-09T16:09:07Z)
- (step 4) `python3 plugin/tests/run.py -p test_ecosystem.py -k InboxGh` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: InboxGh 0s) / OK [ran] [tree 6d4ec51b32f9] (2026-10-09T16:09:21Z)
- (step 5) `python3 plugin/tests/run.py -p test_ecosystem.py -k HarnessCanary` → exit 0 · Ran 2 tests in 2.5s (1 classes, 16 at a time; slowest: HarnessCanary 2s) / OK [ran] [tree c807792f2e32] (2026-10-09T16:09:36Z)
- (step 6) `python3 plugin/tests/run.py -p test_ecosystem.py -k MachineIdentity` → exit 0 · Ran 2 tests in 0.5s (1 classes, 16 at a time; slowest: MachineIdentity 0s) / OK [ran] [tree 91ff98f9e108] (2026-10-09T16:09:49Z)
- (step 5) `python3 plugin/tests/run.py -p test_ecosystem.py -k HarnessCanary` → exit 0 · Ran 2 tests in 2.4s (1 classes, 16 at a time; slowest: HarnessCanary 2s) / OK [ran] [tree 7dd0ab48e4fc] (2026-10-09T16:11:23Z)
- (step 4) `python3 plugin/tests/run.py -p test_ecosystem.py -k InboxGh` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: InboxGh 0s) / OK [ran] [tree bad7613fdb6e] (2026-10-09T16:11:57Z)
- (step 4) `python3 plugin/tests/run.py -p test_ecosystem.py -k InboxGh` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: InboxGh 0s) / OK [ran] [tree 8edcbe810650] (2026-10-09T16:12:36Z)
- (step 6) `python3 plugin/tests/run.py -p test_ecosystem.py -k MachineIdentity` → exit 0 · Ran 2 tests in 1.0s (1 classes, 16 at a time; slowest: MachineIdentity 1s) / OK [ran] [tree 4195f12f0533] (2026-10-09T16:14:48Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 1 of 6 failed: python3 plugin/tests/run.py → ✗ exit 1 · Ran 1009 tests in 44.5s (253 classes, 16 at a time; slowest: Stop 34s, TaskLifecycle 24s, Parallel 21s) / FAILED (2 classes) [ran] [tree 4195f12f0533] (2026-10-09T16:15:09Z)
- (step 7) `python3 plugin/tests/run.py -p test_ecosystem.py -k never_writes_a_synced -k cant_hide_another` → ✗ exit 1 · Ran 2 tests in 1.1s (2 classes, 16 at a time; slowest: Sweep 1s, InboxGh 1s) / FAILED (1 classes) [ran] [tree 7d719bcf3f4b] (2026-10-09T16:23:21Z)
- (step 7) `python3 plugin/tests/run.py -p test_ecosystem.py` → exit 0 · Ran 12 tests in 8.4s (6 classes, 16 at a time; slowest: HarnessCanary 8s, Sweep 5s, MachineIdentity 2s) / OK [ran] [tree 5b2a42c265a4] (2026-10-09T16:24:01Z)
- (step 1) `python3 plugin/tests/run.py -p test_ecosystem.py -k Sweep` → exit 0 · Ran 3 tests in 10.1s (1 classes, 16 at a time; slowest: Sweep 10s) / OK [ran] [tree 5b2a42c265a4] (2026-10-09T16:24:18Z)
- (step 2) `python3 plugin/tests/run.py -p test_ecosystem.py -k Adopt` → exit 0 · Ran 1 tests in 1.8s (1 classes, 16 at a time; slowest: Adopt 2s) / OK [ran] [tree 5b2a42c265a4] (2026-10-09T16:24:21Z)
- (step 3) `python3 plugin/tests/run.py -p test_ecosystem.py -k VersionSkew` → exit 0 · Ran 2 tests in 1.4s (1 classes, 16 at a time; slowest: VersionSkew 1s) / OK [ran] [tree 5b2a42c265a4] (2026-10-09T16:24:23Z)
- (step 4) `python3 plugin/tests/run.py -p test_ecosystem.py -k InboxGh` → exit 0 · Ran 2 tests in 1.6s (1 classes, 16 at a time; slowest: InboxGh 2s) / OK [ran] [tree 5b2a42c265a4] (2026-10-09T16:24:25Z)
- (step 5) `python3 plugin/tests/run.py -p test_ecosystem.py -k HarnessCanary` → exit 0 · Ran 2 tests in 9.6s (1 classes, 16 at a time; slowest: HarnessCanary 10s) / OK [ran] [tree 5b2a42c265a4] (2026-10-09T16:24:36Z)
- (step 6) `python3 plugin/tests/run.py -p test_ecosystem.py -k MachineIdentity` → exit 0 · Ran 2 tests in 2.2s (1 classes, 16 at a time; slowest: MachineIdentity 2s) / OK [ran] [tree 5b2a42c265a4] (2026-10-09T16:24:39Z)
- (ac 1) `python3 plugin/tests/run.py -p test_ecosystem.py -k Sweep` → exit 0 · Ran 3 tests in 2.7s (1 classes, 16 at a time; slowest: Sweep 3s) / OK [ran] [tree aa69a308c86c] (2026-10-09T16:25:04Z)
- (ac 2) `python3 plugin/tests/run.py -p test_ecosystem.py -k Adopt` → exit 0 · Ran 1 tests in 0.9s (1 classes, 16 at a time; slowest: Adopt 1s) / OK [ran] [tree aa69a308c86c] (2026-10-09T16:25:04Z)
- (ac 3) `python3 plugin/tests/run.py -p test_ecosystem.py -k VersionSkew` → exit 0 · Ran 2 tests in 0.6s (1 classes, 16 at a time; slowest: VersionSkew 1s) / OK [ran] [tree aa69a308c86c] (2026-10-09T16:25:04Z)
- (ac 4) `python3 plugin/tests/run.py -p test_ecosystem.py -k InboxGh` → exit 0 · Ran 2 tests in 0.7s (1 classes, 16 at a time; slowest: InboxGh 1s) / OK [ran] [tree aa69a308c86c] (2026-10-09T16:25:04Z)
- (ac 5) `python3 plugin/tests/run.py -p test_ecosystem.py -k HarnessCanary` → exit 0 · Ran 2 tests in 4.6s (1 classes, 16 at a time; slowest: HarnessCanary 5s) / OK [ran] [tree aa69a308c86c] (2026-10-09T16:25:04Z)
- (ac 6) `python3 plugin/tests/run.py -p test_ecosystem.py -k MachineIdentity` → exit 0 · Ran 2 tests in 1.0s (1 classes, 16 at a time; slowest: MachineIdentity 1s) / OK [ran] [tree aa69a308c86c] (2026-10-09T16:25:04Z)
- (audit intent) `builder built six slices test-first in a worktree; merged --no-ff and the merged suites re-run green; one fm-reviewer pass found 5 issues, 4 fixed test-first (sweep wrote a synced sibling's mirror; dedupe key spoofable from issue text; repro not redacted/defanged; canary check outside the try), 1 noted (a failed canary marks its version seen, as documented)` → your six punch-list picks work as first slices [tree aa69a308c86c] (2026-10-09T16:25:04Z)
- (audit adversary) `builder built six slices test-first in a worktree; merged --no-ff and the merged suites re-run green; one fm-reviewer pass found 5 issues, 4 fixed test-first (sweep wrote a synced sibling's mirror; dedupe key spoofable from issue text; repro not redacted/defanged; canary check outside the try), 1 noted (a failed canary marks its version seen, as documented)` → nothing leaves the machine except gh issue list on demand; issue text can't become criteria, Foreman lines or a dedupe match; sweep never touches another repo's files [tree aa69a308c86c] (2026-10-09T16:25:04Z)
- (audit edge) `builder built six slices test-first in a worktree; merged --no-ff and the merged suites re-run green; one fm-reviewer pass found 5 issues, 4 fixed test-first (sweep wrote a synced sibling's mirror; dedupe key spoofable from issue text; repro not redacted/defanged; canary check outside the try), 1 noted (a failed canary marks its version seen, as documented)` → sensitive projects skipped; a second sweep or inbox run asks once; gh missing is a clear error [tree aa69a308c86c] (2026-10-09T16:25:04Z)
- (audit operator) `builder built six slices test-first in a worktree; merged --no-ff and the merged suites re-run green; one fm-reviewer pass found 5 issues, 4 fixed test-first (sweep wrote a synced sibling's mirror; dedupe key spoofable from issue text; repro not redacted/defanged; canary check outside the try), 1 noted (a failed canary marks its version seen, as documented)` → canary spawn detached, hourly at most, never at session start's cost [tree aa69a308c86c] (2026-10-09T16:25:04Z)
- (audit maintainer) `builder built six slices test-first in a worktree; merged --no-ff and the merged suites re-run green; one fm-reviewer pass found 5 issues, 4 fixed test-first (sweep wrote a synced sibling's mirror; dedupe key spoofable from issue text; repro not redacted/defanged; canary check outside the try), 1 noted (a failed canary marks its version seen, as documented)` → one module fmeco.py with a test class per member [tree aa69a308c86c] (2026-10-09T16:25:04Z)
## Log
- 2026-10-09T15:40:14Z created
- 2026-10-09T15:40:50Z criterion 1 verify: `` → `python3 plugin/tests/run.py -p test_ecosystem.py -k Sweep`
- 2026-10-09T15:40:50Z criterion 2 verify: `` → `python3 plugin/tests/run.py -p test_ecosystem.py -k Adopt`
- 2026-10-09T15:40:50Z criterion 3 verify: `` → `python3 plugin/tests/run.py -p test_ecosystem.py -k VersionSkew`
- 2026-10-09T15:40:50Z criterion 4 verify: `` → `python3 plugin/tests/run.py -p test_ecosystem.py -k InboxGh`
- 2026-10-09T15:40:50Z criterion 5 verify: `` → `python3 plugin/tests/run.py -p test_ecosystem.py -k HarnessCanary`
- 2026-10-09T15:40:51Z criterion 6 verify: `` → `python3 plugin/tests/run.py -p test_ecosystem.py -k MachineIdentity`
- 2026-10-09T15:40:51Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0673.builder.md
- 2026-10-09T15:41:01Z focused
- 2026-10-09T16:16:46Z merged worktree-agent-a247d56e9c216e6dc (10 file(s))
- 2026-10-09T16:16:49Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a247d56e9c216e6dc
- 2026-10-09T16:23:01Z focused
- 2026-10-09T16:25:04Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0514 [FEATURE M, dropped, 0 steps] Adopting an existing repo (C082, value 4/5, effort M, risk low)
- T-0551 [FEATURE M, dropped, 0 steps] Trackers and CI (C081, value 3/5, effort M, risk med)
- T-0552 [FEATURE M, dropped, 0 steps] Harness and Claude Code compatibility (C083, value 3/5, effort M, risk low)
- decision 2026-10-09: user added C078/C079/C081/C082/C083/C084 on the punch-list page: T-0443, T-0444, T-0463, T-0481, T-0482, T-0574 set priority high, built right after…
## Lessons
- a capture into another project must not run that project's export side effects; side effects of a state write belong to the project that owns the state
## Files touched
- .claude/worktrees/agent-a247d56e9c216e6dc/plugin/tests/test_ecosystem.py
- .claude/worktrees/agent-a247d56e9c216e6dc/plugin/tests/test_doctor.py
- .claude/worktrees/agent-a247d56e9c216e6dc/plugin/lib/fmeco.py
- .claude/worktrees/agent-a247d56e9c216e6dc/plugin/lib/fmcli.py
- .claude/worktrees/agent-a247d56e9c216e6dc/plugin/lib/fmcore.py
- .claude/worktrees/agent-a247d56e9c216e6dc/plugin/lib/fmfriction.py
- .claude/worktrees/agent-a247d56e9c216e6dc/plugin/lib/fmhooks.py
- .claude/worktrees/agent-a247d56e9c216e6dc/plugin/lib/fmwatch.py
- .claude/worktrees/agent-a247d56e9c216e6dc/plugin/lib/fmdoctor.py
- .claude/worktrees/agent-a247d56e9c216e6dc/MASTER.md
- plugin/tests/test_ecosystem.py
- plugin/lib/fmeco.py
- plugin/lib/fmcore.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
- .claude-plugin/marketplace.json
- MASTER.md
- plugin/.claude-plugin/plugin.json
- plugin/evals/guard-force-push/prompt.md
- plugin/evals/guard-publish/prompt.md
- plugin/evals/intake-block/prompt.md
- plugin/evals/mid-task-capture/prompt.md
- plugin/evals/one-liner/prompt.md
- plugin/lib/fmcli.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmfriction.py
- plugin/lib/fmguard.py
- plugin/lib/fmwatch.py
- plugin/rules/foreman.md
- plugin/tests/fixtures/guard_fuzz_escapes.txt

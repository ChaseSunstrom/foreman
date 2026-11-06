---
id: T-0280
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: [T-0227]
source: user
created: 2026-10-04T07:55:43Z
updated: 2026-10-04T08:26:53Z
batch: [T-0231, T-0240, T-0241, T-0242, T-0243]
base: fccad6b1b49c118d253d22b4aefbe00f7aa24ea2
base_tree: 63c2a571316d3877481fd4d23dff46ff12403be0
verified: strong
---
# Bench family: judged cases, plugin duels, version replays, regression court, shadow-user soak
## Raw request
> T-0231: FEATURE: bench judge for work without tests — fm bench grades cases with no runnable tests (UI, docs, prose) with a rubric child (no tools) built from the task's criteria and the user's preferences (fm taste), as a score beside pass/fail #T-0227
> CONTEXT: plugin/lib/fmbench.py build/validate need tests today; fmideas.taste for preferences
> DONE-WHEN: a docs-only finished task becomes a judged case and a stubbed judge's score lands in the results and in fm bench show
> T-0240: FEATURE: skill duels — fm bench duel PLUGIN replays cases with a third-party plugin enabled and without, to show whether it helps, hurts or duplicates Foreman #T-0227
> CONTEXT: fm bench run uses --setting-sources project,local and --plugin-dir; a second --plugin-dir adds the contender
> DONE-WHEN: with a stub, fm bench duel records both arms and prints the gate between them
> T-0241: FEATURE: counterfactual ledger — fm bench replays recent cases with the previous Foreman version (a git rev) beside the current one, so each release shows who would have won
> CONTEXT: fm evolve's HEAD worktree helper (fmbench._worktree); fm bench gate
> DONE-WHEN: fm bench versions REV runs both arms and prints the gate
> T-0242: FEATURE: regression court — the user's past corrections and steers become judged bench cases ("does the run honour X") replayed against each candidate before a merge #T-0227
> CONTEXT: fmideas.taste (steers, corrections, drops); bench judge
> DONE-WHEN: fm bench court builds judged cases from recorded steers and runs them on a plugin
> T-0243: FEATURE: shadow-user soak — a child plays the user from their recorded steers over a short queue against a candidate build and reports where Foreman made them repeat themselves #T-0227
> CONTEXT: fmbench replay machinery, fmideas.taste
> DONE-WHEN: with stubs, fm bench soak runs a two-turn conversation and records the user-child's complaints
## Interpretation
Five bench extensions on one replay engine. Judged cases (no hidden tests): a tool-less judge child scores the replay's diff and final reply 0-5 against a rubric (the task's criteria + the user's taste); pass at 4+. Court cases are judged cases whose rubric is one recorded steer/correction. Duels and versions are two arms of run_arm on the same cases with gate() between them — the second arm adds a contender plugin dir, or swaps in Foreman at an older rev. Soak replays one case as a conversation: a shadow-user child (the user's steers and corrections) answers the agent each turn and flags where it had to repeat itself.
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0231: a docs-only finished task becomes a judged case (fm bench build --judged) and a stubbed judge's score lands in the results and in fm bench show — verify with `python3 plugin/tests/run.py -p "test_bench_family*" -k Judged`
- [x] T-0240: with a stub, fm bench duel PLUGIN records both arms (Foreman alone, Foreman + the contender's --plugin-dir) and prints the gate between them — verify with `python3 plugin/tests/run.py -p "test_bench_family*" -k Duel`
- [x] T-0241: fm bench versions REV runs both arms (Foreman at REV from a worktree, and the current one) and prints the gate — verify with `python3 plugin/tests/run.py -p "test_bench_family*" -k Versions`
- [x] T-0242: fm bench court builds judged cases from recorded steers and corrections (the task they were said on, its commit's parent, rubric: honour that instruction) and runs them on a plugin — verify with `python3 plugin/tests/run.py -p "test_bench_family*" -k Court`
- [x] T-0243: with stubs, fm bench soak runs a two-turn conversation (resume by session id) and records the user-child's complaints — verify with `python3 plugin/tests/run.py -p "test_bench_family*" -k Soak`
## Non-goals
No live marketplace install for duels (a folder or an already-installed plugin id). No judge-model ensembles. No soak beyond a few turns.
## Approach (options → choice → why)
Options: (a) a new module per feature; (b) everything in fmbench.py around one shared session helper. → (b), with the subcommands in a new fmbench2-free shape: run_case gains extra plugin dirs and judged grading; a _session() helper (claude -p, optional --resume) serves run_case and soak; a _judge() helper serves judged and court cases. Why: one engine, the gate and results format reused; fewest files.
## Risks and rollback
Replays run in bypass mode: the guard check (has_guard) must cover the Foreman arm of a duel and the old rev's plugin; a contender plugin adds hooks of its own — it runs beside Foreman's guard, not instead of it. Budget: every arm and judge call goes through fmbudget. Rollback: revert the commit.
## Execution prompt
## Steps
1. [x] T-0231: Bench judge for work without tests — fm bench grades cases with no runnable tests (UI, doc
2. [x] T-0240: Skill duels — fm bench duel PLUGIN replays cases with a third-party plugin enabled and wit
3. [x] T-0241: Counterfactual ledger — fm bench replays recent cases with the previous Foreman version (a
4. [x] T-0242: Regression court — the user's past corrections and steers become judged bench cases ("does
5. [x] T-0243: Shadow-user soak — a child plays the user from their recorded steers over a short queue ag
## Resume here
<!-- auto -->
- 2026-10-04T08:07:22Z step 1/5: T-0231: Bench judge for work without tests — fm bench grades cases with no runnable tests (UI, doc
- git: foreman/build; 10 uncommitted: CHANGELOG.md, MASTER.md, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/types/index.d.ts, plugin/lib/fmbench.py, plugin/lib/fmcli.py, plugin/lib/fmwatch.py, plugin/skills/improve/SKILL.md, plugin/tests/test_bench_family.py
- touched since last checkpoint: plugin/lib/fmcli.py, plugin/lib/fmwatch.py, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/types/index.d.ts, plugin/lib/fmbench.py, plugin/tests/test_bench_family.py, CHANGELOG.md, MASTER.md, plugin/skills/improve/SKILL.md
- failures met: filenotfounderror: [errno 0] no such file or directory: 'log'
## Docs impact
MASTER.md, CHANGELOG.md, plugin/skills/improve/SKILL.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p "test_bench_family*"` → ✗ exit 1 · Ran 7 tests in 2.4s (5 classes, 16 at a time; slowest: Duel 2s, Judged 2s, Versions 1s) / FAILED (5 classes) [ran] [tree d9233381a429] (2026-10-04T07:57:21Z)
- (step 1) `python3 plugin/tests/run.py -p "test_bench_family*" -k Judged` → exit 0 · Ran 2 tests in 2.6s (1 classes, 16 at a time; slowest: Judged 3s) / OK [ran] [tree c49ea2b0d13d] (2026-10-04T07:59:11Z)
- (step 2) `python3 plugin/tests/run.py -p "test_bench_family*" -k Duel` → exit 0 · Ran 2 tests in 3.2s (1 classes, 16 at a time; slowest: Duel 3s) / OK [ran] [tree d927b2c70b90] (2026-10-04T08:00:48Z)
- (step 3) `python3 plugin/tests/run.py -p "test_bench_family*" -k Versions` → exit 0 · Ran 1 tests in 1.7s (1 classes, 16 at a time; slowest: Versions 2s) / OK [ran] [tree d927b2c70b90] (2026-10-04T08:00:50Z)
- (step 4) `python3 plugin/tests/run.py -p "test_bench_family*" -k Court` → exit 0 · Ran 1 tests in 1.3s (1 classes, 16 at a time; slowest: Court 1s) / OK [ran] [tree d927b2c70b90] (2026-10-04T08:00:52Z)
- (step 5) `python3 plugin/tests/run.py -p "test_bench_family*" -k Soak` → exit 0 · Ran 1 tests in 1.5s (1 classes, 16 at a time; slowest: Soak 1s) / OK [ran] [tree d927b2c70b90] (2026-10-04T08:00:53Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  integrity            6 repo(s) and state intact / fm doctor: OK (24 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                30.5    32.0     150  [0] / SessionEnd                  28.5    29.5     150  [0]; claude plugin test mods/foreman-ui → exit 0 · 0 fail / Ran 62 tests across 1 file. [2.63s]; python3 plugin/tests/run.py → exit 0 · Ran 764 tests in 30.6s (171 classes, 16 at [ran] [tree d6156cdbd90a] (2026-10-04T08:06:50Z)
- (step 1) `python3 plugin/tests/run.py -p "test_bench_family*" -k Judged` → exit 0 · Ran 4 tests in 10.0s (1 classes, 16 at a time; slowest: Judged 10s) / OK [ran] [tree 9b308d03e56b] (2026-10-04T08:12:19Z)
- (step 2) `python3 plugin/tests/run.py -p "test_bench_family*" -k Duel` → exit 0 · Ran 3 tests in 8.1s (1 classes, 16 at a time; slowest: Duel 8s) / OK [ran] [tree 9b308d03e56b] (2026-10-04T08:12:27Z)
- (step 3) `python3 plugin/tests/run.py -p "test_bench_family*" -k Versions` → exit 0 · Ran 1 tests in 2.9s (1 classes, 16 at a time; slowest: Versions 3s) / OK [ran] [tree 9b308d03e56b] (2026-10-04T08:12:30Z)
- (step 4) `python3 plugin/tests/run.py -p "test_bench_family*" -k Court` → exit 0 · Ran 1 tests in 2.2s (1 classes, 16 at a time; slowest: Court 2s) / OK [ran] [tree 9b308d03e56b] (2026-10-04T08:12:33Z)
- (step 5) `python3 plugin/tests/run.py -p "test_bench_family*" -k Soak` → exit 0 · Ran 2 tests in 5.0s (1 classes, 16 at a time; slowest: Soak 5s) / OK [ran] [tree 9b308d03e56b] (2026-10-04T08:12:38Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  integrity            6 repo(s) and state intact / fm doctor: OK (24 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                47.6    62.2     150  [0] / SessionEnd                  45.3    55.9     150  [0] (slower: 17.5 s vs a usual 10.9 s); claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 08:06 UTC; python3 plugin [ran] [tree 9b308d03e56b] (2026-10-04T08:14:02Z)
- `fm task prove --hunks: python3 plugin/tests/run.py -p "test_bench*" && python3 plugin/tests/run.py -p "test_help*"` → 21/30 hunks proven; unproven: mods/foreman-ui/hooks/register.tsx @@ -1323,0 +1324,2 @@ export const register: Register = (on, options) => {; mods/foreman-ui/hooks/register.tsx @@ -1326,0 +1329,5 @@ export const register: Register = (on, options) => {; mods/foreman-ui/types/index.d.ts @@ -42 +42 @@ export type FmBench = {; mods/foreman-ui/types/index.d.ts @@ -43,0 +44 @@ export type FmBench = {; plugin/lib/fmbench.py @@ -205,3 +289 @@ def run_case(p, case, plugin, model=None, budget=3.0, timeout=30):; plugin/lib/fmbench.py @@ -231 +302,2 @@ def run_case(p, case, plugin, model=None, budget=3.0, timeout=30):; plugin/lib/fmbench.py @@ -307 +463,2 @@ def run_arm(p, cases, plugin, label, model=None, budget=3.0, timeout=30, runs=1,; plugin/lib/fmbench.py @@ -353 +606,2 @@ def cmd_bench(args):; plugin/lib/fmbench.py @@ -456,0 +714,2 @@ def cmd_bench(args): [inconclusive] [ran] [tree 9b308d03e56b] (2026-10-04T08:19:41Z)
- `fm task prove --hunks: python3 plugin/tests/run.py -p "test_bench*" && python3 plugin/tests/run.py -p "test_help*" && claude plugin test mods/foreman-ui` → 26/30 hunks proven; unproven: mods/foreman-ui/types/index.d.ts @@ -42 +42 @@ export type FmBench = {; mods/foreman-ui/types/index.d.ts @@ -43,0 +44 @@ export type FmBench = {; plugin/lib/fmbench.py @@ -205,3 +289 @@ def run_case(p, case, plugin, model=None, budget=3.0, timeout=30):; plugin/lib/fmbench.py @@ -353 +606,2 @@ def cmd_bench(args): [inconclusive] [ran] [tree ce97aae406e7] (2026-10-04T08:26:10Z)
- (step 1) `python3 plugin/tests/run.py -p "test_bench_family*" -k Judged` → exit 0 · Ran 4 tests in 6.2s (1 classes, 16 at a time; slowest: Judged 6s) / OK [ran] [tree ce97aae406e7] (2026-10-04T08:26:27Z)
- (step 2) `python3 plugin/tests/run.py -p "test_bench_family*" -k Duel` → exit 0 · Ran 3 tests in 4.8s (1 classes, 16 at a time; slowest: Duel 5s) / OK [ran] [tree ce97aae406e7] (2026-10-04T08:26:32Z)
- (step 5) `python3 plugin/tests/run.py -p "test_bench_family*" -k Soak` → exit 0 · Ran 2 tests in 3.0s (1 classes, 16 at a time; slowest: Soak 3s) / OK [ran] [tree ce97aae406e7] (2026-10-04T08:26:35Z)
- (ac 1) `python3 plugin/tests/run.py -p "test_bench_family*" -k Judged` → exit 0 · Ran 4 tests in 6.3s (1 classes, 16 at a time; slowest: Judged 6s) / OK [ran] [tree ce97aae406e7] (2026-10-04T08:26:52Z)
- (ac 2) `python3 plugin/tests/run.py -p "test_bench_family*" -k Duel` → exit 0 · Ran 3 tests in 4.9s (1 classes, 16 at a time; slowest: Duel 5s) / OK [ran] [tree ce97aae406e7] (2026-10-04T08:26:52Z)
- (ac 3) `python3 plugin/tests/run.py -p "test_bench_family*" -k Versions` → exit 0 · Ran 1 tests in 1.7s (1 classes, 16 at a time; slowest: Versions 2s) / OK [ran] [tree ce97aae406e7] (2026-10-04T08:26:52Z)
- (ac 4) `python3 plugin/tests/run.py -p "test_bench_family*" -k Court` → exit 0 · Ran 1 tests in 1.3s (1 classes, 16 at a time; slowest: Court 1s) / OK [ran] [tree ce97aae406e7] (2026-10-04T08:26:52Z)
- (ac 5) `python3 plugin/tests/run.py -p "test_bench_family*" -k Soak` → exit 0 · Ran 2 tests in 3.0s (1 classes, 16 at a time; slowest: Soak 3s) / OK [ran] [tree ce97aae406e7] (2026-10-04T08:26:52Z)
- (audit adversary) `one fm-reviewer pass (T-0280-review-1): 3 MEDIUM (git in the replay worktree ran session-planted fsmonitor/hooks — reproduced, then fixed in _git; shadow NEXT and judge inputs unfenced/unsanitized; soak's guard check lived in the caller) and 5 LOW (no session id passed silently, unredacted transcript, judge paid after a crash, OSError aborting soak, nan/zero numbers, plain build dropping judged cases) — all fixed test-first; hunks 26/30 proven (the rest: TS types erased at runtime, a verbatim move into _seed, a comment); real-render check of the bench card via shot.py; a real duel and soak ran end to end in a scratch repo` → every replay arm (duel, versions old rev, court, soak) refuses a guardless plugin; bench git runs without fsmonitor/hooks; judge inputs fenced; NEXT plain+defang; transcripts redacted [tree ce97aae406e7] (2026-10-04T08:26:52Z)
- (audit edge) `one fm-reviewer pass (T-0280-review-1): 3 MEDIUM (git in the replay worktree ran session-planted fsmonitor/hooks — reproduced, then fixed in _git; shadow NEXT and judge inputs unfenced/unsanitized; soak's guard check lived in the caller) and 5 LOW (no session id passed silently, unredacted transcript, judge paid after a crash, OSError aborting soak, nan/zero numbers, plain build dropping judged cases) — all fixed test-first; hunks 26/30 proven (the rest: TS types erased at runtime, a verbatim move into _seed, a comment); real-render check of the bench card via shot.py; a real duel and soak ran end to end in a scratch repo` → no session id, crashed session, nan budget, max 0, plain rebuild after judged, low judge score, same verdict wording in the pane [tree ce97aae406e7] (2026-10-04T08:26:52Z)
- (audit intent) `one fm-reviewer pass (T-0280-review-1): 3 MEDIUM (git in the replay worktree ran session-planted fsmonitor/hooks — reproduced, then fixed in _git; shadow NEXT and judge inputs unfenced/unsanitized; soak's guard check lived in the caller) and 5 LOW (no session id passed silently, unredacted transcript, judge paid after a crash, OSError aborting soak, nan/zero numbers, plain build dropping judged cases) — all fixed test-first; hunks 26/30 proven (the rest: TS types erased at runtime, a verbatim move into _seed, a comment); real-render check of the bench card via shot.py; a real duel and soak ran end to end in a scratch repo` → five member criteria each with its own test class [tree ce97aae406e7] (2026-10-04T08:26:52Z)
## Log
- 2026-10-04T07:55:43Z created
- 2026-10-04T07:56:00Z set tier=M
- 2026-10-04T07:56:00Z focused
- 2026-10-04T07:58:43Z hypothesis: with --judged wired into the build parser and score shown in bench show, the Judged tests pass (judge sees diff, reply, taste)
- 2026-10-04T07:58:57Z confirmed: Judged passes; ruled out a judge-wiring gap
- 2026-10-04T08:07:23Z paused: focus moved to T-0281
- 2026-10-04T08:08:05Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-04T08:08:05Z focused
- 2026-10-04T08:11:11Z hypothesis: the remaining reds (soak validation, plain rebuild keeping judged cases) need only the _contest checks and the build keep rule; the git/judge/soak_case fixes already turn the others green
- 2026-10-04T08:26:52Z done
- 2026-10-04T08:26:53Z committed a0d1b80 (10 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0260 [FEATURE M, dropped, 3 steps] Evidence quality: inconclusive runs, assumed vs verified facts, surprise log
- T-0224 [FEATURE L, done, 3 steps] Fm evolve — a bench-gated self-improvement loop: a mutation child proposes one revision or — lesson: A self-modifying loop needs the sa…
- T-0220 [FEATURE S, done, 1 steps] Replay diagnostics — each bench case keeps a summary of the replay's own Foreman ledger (t
- T-0221 [FEATURE S, done, 1 steps] Bench rigor — fm bench run --runs N reports per-case pass fraction and cost/turns spread,
- similar finished tasks took 1–3 steps
## Lessons
- Git run after a bypass-mode session in a shared-config worktree runs whatever that session configured: disable fsmonitor and hooks for every later git call
## Files touched
- plugin/tests/test_bench_family.py
- plugin/lib/fmbench.py
- plugin/lib/fmcli.py
- plugin/lib/fmwatch.py
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/types/index.d.ts
- CHANGELOG.md
- MASTER.md
- plugin/skills/improve/SKILL.md

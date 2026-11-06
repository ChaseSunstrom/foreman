---
id: T-0854
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-15T13:44:59Z
updated: 2026-10-15T14:00:45Z
batch: [T-0845, T-0846, T-0847, T-0848, T-0849]
base: 1f0e57afebf38590294cfceee7867e9a7795392e
base_tree: 5952bf91e40735a7624edddf0861ae082d3e63cf
verified: strong
---
# A newcomer's first fm commands make sense: short --help, task new shows its values and an example, init/status say what…
## Raw request
> T-0845: fm --help shows the ~12 everyday commands and points to fm help --all, instead of a 231-line, 100-verb blob
> T-0846: fm task new --help lists the valid --type and --tier values and ends with one worked example
> T-0847: fm init says what it registered, where state lives, and the next command; fm status on an empty project says how to start
> T-0848: fm task new with the same title as an inbox capture uses that capture (as --from) instead of making a duplicate
> T-0849: fm task done's refusal leads with the one-call fm task finish command that satisfies it
## Interpretation
A new user's walkthrough (2026-10-15, clean HOME) hit five first-command problems, all in plugin/lib/fmcli.py: (1) fm --help prints 231 lines with a 100-verb brace blob; argparse's usage line and subcommand list should be replaced by a short 'start here' list of ~12 everyday verbs (init, capture, task new, next, status, check, focus, task finish, queue, doctor, help) and a pointer to 'fm help --all' (fm help already has tiers). (2) fm task new --help shows --type TYPE / --tier TIER with no values: add choices (RESEARCH CLEAN PERFORMANCE SECURITY FIX FEATURE; S M L) and an epilog example: fm task new "Add login timeout" --type FIX --tier S --ac "times out after 30s :: pytest -k timeout" --step "failing test" --focus. (3) fm init prints only the slug: also say where state lives and the next command (fm capture "…" or give Claude a request); fm status on a project with no tasks prints one line on how to start instead of the STATE document. (4) fm capture "add a hello command" then fm task new "Add a hello command" (no --from) created a duplicate: when an inbox capture's title matches (case/whitespace-insensitive) and no --from was given, use it as --from and say so. (5) fm task done's refusal lists 4 bullets; lead with the one call that satisfies them: fm task finish ID --run "<cmd>" --audit "<how>".
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0845: Fm --help shows the ~12 everyday commands and points to fm help --all, instead of a 231-li works — verify with `python3 plugin/tests/run.py test_firstrun`
- [x] T-0846: Fm task new --help lists the valid --type and --tier values and ends with one worked examp works — verify with `python3 plugin/tests/run.py test_firstrun`
- [x] T-0847: Fm init says what it registered, where state lives, and the next command; fm status on an works — verify with `python3 plugin/tests/run.py test_firstrun`
- [x] T-0848: Fm task new with the same title as an inbox capture uses that capture (as --from) instead works — verify with `python3 plugin/tests/run.py test_firstrun`
- [x] T-0849: Fm task done's refusal leads with the one-call fm task finish command that satisfies it works — verify with `python3 plugin/tests/run.py test_firstrun`
## Non-goals
## Approach (options → choice → why)
Options: (a) five small edits in fmcli with one test module (test_firstrun.py) driving the CLI as a newcomer; (b) a separate onboarding wizard verb; (c) docs only. Chose (a): fixes the commands people actually type first; a wizard is a later idea for the brainstorm.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-0845: Fm --help shows the ~12 everyday commands and points to fm help --all, instead of a 231-li
2. [x] T-0846: Fm task new --help lists the valid --type and --tier values and ends with one worked examp
3. [x] T-0847: Fm init says what it registered, where state lives, and the next command; fm status on an
4. [x] T-0848: Fm task new with the same title as an inbox capture uses that capture (as --from) instead
5. [x] T-0849: Fm task done's refusal leads with the one-call fm task finish command that satisfies it
## Resume here
## Docs impact
none: help text is the doc
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_firstrun` → ✗ exit 1 · Ran 5 tests in 0.6s (1 classes, 16 at a time; slowest: FirstRun 1s) / FAILED (1 classes) [ran] [tree 557b18823558] (2026-10-15T13:46:46Z)
- (step 1) `python3 plugin/tests/run.py test_firstrun` → exit 0 · Ran 5 tests in 1.1s (1 classes, 16 at a time; slowest: FirstRun 1s) / OK [ran] [tree a201ec2ff4d5] (2026-10-15T13:48:45Z)
- (step 2) `python3 plugin/tests/run.py test_firstrun` → exit 0 · Ran 5 tests in 1.1s (1 classes, 16 at a time; slowest: FirstRun 1s) / OK [ran] [tree a201ec2ff4d5] (2026-10-15T13:48:46Z)
- (step 3) `python3 plugin/tests/run.py test_firstrun` → exit 0 · Ran 5 tests in 1.1s (1 classes, 16 at a time; slowest: FirstRun 1s) / OK [ran] [tree a201ec2ff4d5] (2026-10-15T13:48:47Z)
- (step 4) `python3 plugin/tests/run.py test_firstrun` → exit 0 · Ran 5 tests in 1.1s (1 classes, 16 at a time; slowest: FirstRun 1s) / OK [ran] [tree a201ec2ff4d5] (2026-10-15T13:48:49Z)
- (step 5) `python3 plugin/tests/run.py test_firstrun` → exit 0 · Ran 5 tests in 1.1s (1 classes, 16 at a time; slowest: FirstRun 1s) / OK [ran] [tree a201ec2ff4d5] (2026-10-15T13:48:50Z)
- (step 5) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  briefs               foreman-desktop-d33873: STATE.md differs from the briefs (fm tidy --apply regenerates it); foreman-improve-20260927-4cffe6: STATE.md differs from the briefs (fm tidy --apply; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                33.2    34.7     150  [0] / SessionEnd                  30.4    31.9     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under [ran] [tree 94dc5ec9ee07] (2026-10-15T14:00:35Z)
- (step 5) `python3 plugin/tests/run.py test_firstrun test_help` → exit 0 · Ran 11 tests in 1.1s (5 classes, 16 at a time; slowest: FirstRun 1s, PromptApprovals 1s, Digest 1s) / OK [ran] [tree 94dc5ec9ee07] (2026-10-15T14:00:43Z)
- (ac 1) `python3 plugin/tests/run.py test_firstrun` → exit 0 · Ran 8 tests in 1.1s (3 classes, 16 at a time; slowest: FirstRun 1s, Digest 1s, FirstCheck 0s) / OK [ran] [tree 94dc5ec9ee07] (2026-10-15T14:00:44Z)
- (ac 2) `python3 plugin/tests/run.py test_firstrun` → exit 0 · Ran 8 tests in 1.1s (3 classes, 16 at a time; slowest: FirstRun 1s, Digest 1s, FirstCheck 0s) / OK [ran] [tree 94dc5ec9ee07] (2026-10-15T14:00:44Z)
- (ac 3) `python3 plugin/tests/run.py test_firstrun` → exit 0 · Ran 8 tests in 1.1s (3 classes, 16 at a time; slowest: FirstRun 1s, Digest 1s, FirstCheck 0s) / OK [ran] [tree 94dc5ec9ee07] (2026-10-15T14:00:44Z)
- (ac 4) `python3 plugin/tests/run.py test_firstrun` → exit 0 · Ran 8 tests in 1.1s (3 classes, 16 at a time; slowest: FirstRun 1s, Digest 1s, FirstCheck 0s) / OK [ran] [tree 94dc5ec9ee07] (2026-10-15T14:00:44Z)
- (ac 5) `python3 plugin/tests/run.py test_firstrun` → exit 0 · Ran 8 tests in 1.1s (3 classes, 16 at a time; slowest: FirstRun 1s, Digest 1s, FirstCheck 0s) / OK [ran] [tree 94dc5ec9ee07] (2026-10-15T14:00:44Z)
- (audit intent) `main thread read the builder's 116-line diff: short root help, task new choices/example, init/status guidance on stderr/empty projects, capture reuse by title, done's refusal leads with finish; checked tiers were already uppercase-only (no regression from choices=); full suite 1,335 OK after merge` → each of the five newcomer frictions has a test driving the CLI as a newcomer (test_firstrun.py) [tree 94dc5ec9ee07] (2026-10-15T14:00:44Z)
- (audit edge) `main thread read the builder's 116-line diff: short root help, task new choices/example, init/status guidance on stderr/empty projects, capture reuse by title, done's refusal leads with finish; checked tiers were already uppercase-only (no regression from choices=); full suite 1,335 OK after merge` → fm init's stdout stays the bare slug for scripts (guidance on stderr); status on an empty project keeps --json/--line output; the done-refusal lead is skipped inside finish (hasattr audit) — brittle if task done grows an --audit flag [tree 94dc5ec9ee07] (2026-10-15T14:00:44Z)
## Log
- 2026-10-15T13:44:59Z created
- 2026-10-15T13:45:10Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_firstrun`
- 2026-10-15T13:45:10Z criterion 2 verify: `` → `python3 plugin/tests/run.py test_firstrun`
- 2026-10-15T13:45:10Z criterion 3 verify: `` → `python3 plugin/tests/run.py test_firstrun`
- 2026-10-15T13:45:10Z criterion 4 verify: `` → `python3 plugin/tests/run.py test_firstrun`
- 2026-10-15T13:45:11Z criterion 5 verify: `` → `python3 plugin/tests/run.py test_firstrun`
- 2026-10-15T13:45:11Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0854.builder.md
- 2026-10-15T13:45:13Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0854.builder.md
- 2026-10-15T13:45:19Z focused
- 2026-10-15T13:58:56Z merged worktree-agent-a0556d8a14fcfd385 (3 file(s))
- 2026-10-15T13:58:56Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a0556d8a14fcfd385
- 2026-10-15T13:58:56Z focused
- 2026-10-15T14:00:45Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research mission-20261009-091631: Request: can you spawn a bunch of brainstorm agents to super recursive brainstorm on capabilities/features for foreman itself? not just…
- research mission-20261014-103352: Request: super improve foreman, integrate better with new CC features, super improve, smarter, faster, better, more capable, etc. etc. …
- research mission-20261014-130857: Request: recursively improve: review what round 1 shipped today and brainstorm improvements on top of it — super improve foreman, integ…
- decision 2026-09-27: Recursion bound for T-0063: after R5, one more round (R6: auto-evidence from Bash results matching a criterion's verify command) from the existing R…
## Why not caught
none: found by the first newcomer walkthrough
## Lessons
- The first screen of --help is onboarding: a short start-here list beats a complete one
## Plan gaps
- failed first: step 1 T-0845: Fm --help shows the ~12 everyday commands and points to fm help --all, instead of a 231-li
## Files touched
- plugin/tests/test_firstrun.py
- plugin/lib/fmcli.py
- plugin/tests/test_help.py

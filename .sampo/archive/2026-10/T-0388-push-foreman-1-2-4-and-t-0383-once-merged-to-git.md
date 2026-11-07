---
id: T-0388
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-09T01:48:03Z
updated: 2026-10-09T02:34:14Z
inferred_deps: [T-0383]
inferred_why: T-0383: named in its request
base: 7b8aa970f53594def228a7e4e97d9da3c01057bc
base_tree: e6cf10f7a402d5c8de481f35db40e97a86453dbf
verified: strong
---
# Foreman 1.2.5: push 1.2.4 + fm relate, running-code check, fm status to GitHub main; fast-forward JARVIS
## Raw request
> Push Foreman 1.2.4 (and T-0383 once merged) to GitHub main and fast-forward JARVIS's ~/.claude/foreman checkout — the push was denied at the prompt on 2026-10-09; needs the owner's yes
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] origin/main contains HEAD and JARVIS's ~/.claude/foreman is at origin/main with a clean tree — verify with `git -C ~/.claude/foreman merge-base --is-ancestor HEAD origin/main`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] bump to 1.2.5, gate, commit
2. [x] merge into main in a scratch clone and push (approved by the owner 2026-10-09)
3. [x] fast-forward JARVIS's checkout; confirm its session loads it
## Resume here
## Docs impact
## Verification evidence
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (28 pass, 3 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 02:29 UTC; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 00:30 UTC; pytho [ran] [tree cc48f829173f] (2026-10-09T02:33:09Z)
- (step 2) `git -C ~/.claude/foreman merge-base --is-ancestor HEAD origin/main` → exit 0 · (no output) [ran] [tree cc48f829173f] (2026-10-09T02:34:14Z)
- (step 3) `ssh -o BatchMode=yes <host> 'cd ~/.claude/foreman && test $(git rev-parse HEAD) = $(git rev-parse origin/main) && test -z "$(git status --short)"'` → exit 0 · (no output) [ran] [tree cc48f829173f] (2026-10-09T02:34:14Z)
- (ac 1) `git -C ~/.claude/foreman merge-base --is-ancestor HEAD origin/main` → exit 0 · (no output) [ran] [tree cc48f829173f] (2026-10-09T02:34:14Z)
- (audit intent) `self: gate green on cc66d4a; merged in a scratch clone and pushed 23cdb4e to main (owner's yes, 2026-10-09); JARVIS checkout reset to origin/main after confirming no local edits; install record 1.2.5` → GitHub main and JARVIS both carry 1.2.5 [tree cc48f829173f] (2026-10-09T02:34:14Z)
- (audit edge) `self: gate green on cc66d4a; merged in a scratch clone and pushed 23cdb4e to main (owner's yes, 2026-10-09); JARVIS checkout reset to origin/main after confirming no local edits; install record 1.2.5` → JARVIS's running session loads the checkout (shown earlier by its bytecode rebuild); new sessions load the 1.2.5 install [tree cc48f829173f] (2026-10-09T02:34:14Z)
- (audit self) `self: gate green on cc66d4a; merged in a scratch clone and pushed 23cdb4e to main (owner's yes, 2026-10-09); JARVIS checkout reset to origin/main after confirming no local edits; install record 1.2.5` → no findings [tree cc48f829173f] (2026-10-09T02:34:14Z)
## Log
- 2026-10-09T01:48:03Z created
- 2026-10-09T02:29:58Z planned from capture
- 2026-10-09T02:29:58Z focused
- 2026-10-09T02:32:19Z scope: the gate caught two fragile tests from T-0391/T-0393 (one read the real plugin's version, one compared timestamped output); fixed here so the release gate is honest
- 2026-10-09T02:34:14Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0167 [FEATURE L, done, 5 steps] fm run --parallel N: independent queued tasks at once, each in its own lane, merged back only when gated and clean — lesson: A loop tha…
- decision 2026-09-26: Released: fast-forwarded main 924fe06 → bd86fd6 (43 commits: T-0018 rounds 1-10, T-0036, T-0038, T-0039) and pushed main + foreman/build to origin
- decision 2026-09-26: User approved (AskUserQuestion, 2026-09-26): once everything is finished and all gates pass, fast-forward main to foreman/build and push both branch…
- decision 2026-10-04: Fast-forwarded main to foreman/build (53a33c1) and pushed: the user chose it
- similar past tasks were L: consider --tier L
- the similar finished task took 5 steps
## Regression test
none: a release and deploy; the gate ran the full suite on the released tree, and the criterion checks main contains it
## Files touched
- .claude-plugin/marketplace.json
- CHANGELOG.md
- plugin/.claude-plugin/plugin.json
- plugin/tests/test_doctor.py
- plugin/tests/test_help.py

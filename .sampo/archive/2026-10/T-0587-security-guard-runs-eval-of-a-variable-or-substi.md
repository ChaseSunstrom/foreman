---
id: T-0587
type: SECURITY
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-09T15:03:30Z
updated: 2026-10-09T15:28:13Z
base: bdbdc25a25c81ab4d0e3e016d7655024cfb13741
base_tree: 48435ca99ec79fccad64fa10d83378ce20996a87
verified: strong
---
# SECURITY!: guard runs eval of a variable or substitution it can't resolve unread: q='rm -r
## Raw request
> SECURITY!: guard runs eval of a variable or substitution it can't resolve unread: q='rm -rf'; eval "$q ~" is allowed (decide: resolve known vars inside eval text, refuse unresolvable eval)
## Interpretation
Found while replaying T-0585: eval text built from a variable the guard knows (q='rm -rf'; eval "$q ~") is checked with the variable unresolved, so the command it runs is never seen.
## Assumptions (confidence)
## Acceptance criteria
- [x] eval and sh -c text built from known literal variables is read with them substituted (rm -rf ~ inside refused); eval of unknown text keeps today's verdict unless replay shows it's rare — verify with `python3 plugin/tests/run.py -k EvalVars`
## Non-goals
## Approach (options → choice → why)
Options: (a) refuse every eval/sh -c with an unresolved expansion — closes the class but blocks eval "$(ssh-agent -s)"-style lines; (b) substitute the variables the guard already resolves (literal assignments, T-0151) into the text before the nested check — closes the known-value form with no new refusals; (c) both. Choice: (b) first, then decide (a) from the replay count of unknown-eval lines.
## Risks and rollback
## Execution prompt
## Steps
1. [x] probe and count eval in real commands
2. [x] test-first: EvalVars rows
3. [x] substitute known literal variables into eval / sh -c text before the nested check
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `python3 /tmp/claude-1000/-home-~--claude-foreman/017cbb6b-0026-4a64-af96-4068091225da/scratchpad/computed_names.py` → exit 0 · 2 $S/voltccold | fm task new "PERF: fannkuch 1.07x of C (LLVM): find what shapes its loops" --from T-0281 --type PERF --tier M --ac "fann / 1 $S/sitegenboot | S=/tmp/claude-1000/-home-~-projects-v [ran] [tree a4820ff90bc1] (2026-10-09T15:22:46Z)
- (step 2) `python3 plugin/tests/run.py -k ComputedNames` → ✗ exit 1 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: ComputedNames 0s) / FAILED (1 classes) [ran] [tree a4820ff90bc1] (2026-10-09T15:22:47Z)
- (step 3) `python3 plugin/tests/run.py -k ComputedNames` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: ComputedNames 0s) / OK [ran] [tree 833d1b31dbc0] (2026-10-09T15:27:51Z)
- (ac 1) `python3 plugin/tests/run.py -k EvalVars` → ✗ exit 1 · Ran 0 tests in 0.1s (0 classes, 16 at a time; slowest: ) / NO TESTS RAN [ran] [tree e72454fc1ae0] (2026-10-09T15:28:00Z)
- (ac 1) `python3 plugin/tests/run.py -k EvalVars` → ✗ exit 1 · Ran 0 tests in 0.1s (0 classes, 16 at a time; slowest: ) / NO TESTS RAN [ran] [tree e72454fc1ae0] (2026-10-09T15:28:06Z)
- (ac 1) `python3 plugin/tests/run.py -k EvalVars` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: EvalVarsAndComputedNames 0s) / OK [ran] [tree 616a34bc5801] (2026-10-09T15:28:13Z)
- (audit intent) `self: EvalVarsAndComputedNames rows red then green (known and line-literal values, eval/sh -c, unknown names as rm/git/claude, quoted-text and subshell and twice-set literals, a conditional literal, compiler flags); review findings (raw text replaced by substituted; conditional literals) fixed by reading both; suites green; 30-day replay 0/0` → the eval-of-a-variable hole and the wider computed-command-name hole are closed [tree 616a34bc5801] (2026-10-09T15:28:13Z)
- (audit adversary) `self: EvalVarsAndComputedNames rows red then green (known and line-literal values, eval/sh -c, unknown names as rm/git/claude, quoted-text and subshell and twice-set literals, a conditional literal, compiler flags); review findings (raw text replaced by substituted; conditional literals) fixed by reading both; suites green; 30-day replay 0/0` → every substitution only adds a reading (raw kept); unknown names fall back to candidate commands plus the empty-expansion reading; quoted text never yields a literal [tree 616a34bc5801] (2026-10-09T15:28:13Z)
- (audit edge) `self: EvalVarsAndComputedNames rows red then green (known and line-literal values, eval/sh -c, unknown names as rm/git/claude, quoted-text and subshell and twice-set literals, a conditional literal, compiler flags); review findings (raw text replaced by substituted; conditional literals) fixed by reading both; suites green; 30-day replay 0/0` → 429 real computed names in the corpus ($S/tool, $cc, $V) still pass; rm as a candidate needs options rm accepts [tree 616a34bc5801] (2026-10-09T15:28:13Z)
## Log
- 2026-10-09T15:03:30Z created
- 2026-10-09T15:21:12Z set tier=M
- 2026-10-09T15:21:13Z focused
- 2026-10-09T15:28:13Z done
- 2026-10-09T15:28:13Z committed 227a8f4 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0175 [SECURITY L, done, 3 steps] Guard: writes through a variable are checked — known NAME=literal values and $HOME resolve write, copy and cd targets (&& chains too);…
- T-0411 [FEATURE M, done, 3 steps] FEATURE: the guard reads a for loop over literal words (for w in agent-a agent-b; do … $w — lesson: A text rewrite ahead of the guard m…
- T-0161 [SECURITY M, done, 3 steps] Guard: rm variable resolution fails closed on every way bash changes a variable (security review of T-0151) — lesson: Fail-closed mean…
- decision 2026-10-04: [costly] T-0308 closed on self-audit, hunk proofs and the replay corpus
- similar finished tasks took 3–3 steps
## Lessons
- when the guard substitutes a value it believes, keep the unsubstituted reading too; a belief may only add findings
## Files touched
- plugin/tests/test_guard_pipes.py
- plugin/lib/fmguard.py
- CHANGELOG.md

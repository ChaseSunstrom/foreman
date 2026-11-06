---
id: T-0384
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-09T00:59:26Z
updated: 2026-10-09T01:37:06Z
base: a9e5ca96f40769339c639df42fb76e47ae2fb369
base_tree: d322b3c86ec6fb56f3763ba72277cb354d768434
verified: strong
---
# FIX: guard false positives seen on JARVIS: (1) cd ABS && A > f; B > g resolves f/g against
## Raw request
> FIX: guard false positives seen on JARVIS: (1) cd ABS && A > f; B > g resolves f/g against the old cwd too, though a cd into an existing searchable absolute folder can't fail; (2) a pipeline element before S=...; (fm focus X | tail -1; S=/abs; cmd > $S/f) loses S; (3) builder heredoc write in its worktree flagged as main-checkout path
## Interpretation
JARVIS was refused three times for commands that write only in its scratchpad or its builder worktree: the guard kept the pre-cd folder possible after a head 'cd /abs &&' that cannot fail, and lost a variable set after a pipeline. Make the guard as precise as bash there without letting through anything bash would actually write elsewhere.
## Assumptions (confidence)
## Acceptance criteria
- [x] the three JARVIS commands pass with no task; the conservative rows still block — verify with `python3 plugin/tests/run.py -k test_jarvis_cd_and_pipeline_false_positives`
- [x] real bash agrees — verify with `python3 plugin/tests/run.py -p test_guard_diff.py`
## Non-goals
## Approach (options → choice → why)
(A, chosen) a cd heading its &&-segment, not piped, into an absolute folder that exists and is searchable (or one this command made) is certain past its segment; a pipeline element is skipped when tracking variables (its parts run in subshells) unless lastpipe appears. Rejected: (B) reword the block message only — Claude already followed its 'chain a cd with &&' advice; (C) soften brief blocks to warnings — weakens the guard; (D) track the session cwd — irrelevant to these.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first: JARVIS rows (cd ABS && …; later segments; pipeline before S=) + diff rows
2. [x] head-of-segment cd into an existing searchable folder is certain past its segment; a pipeline (no lastpipe) is skipped for variable tracking
3. [x] fm replay, gate, changelog
## Resume here
<!-- auto -->
- 2026-10-09T01:12:51Z step 1/3: test-first: JARVIS rows (cd ABS && …; later segments; pipeline before S=) + diff rows
- git: foreman/build; 0 uncommitted
## Docs impact
CHANGELOG Unreleased
## Verification evidence
- `python3 plugin/tests/run.py -k test_jarvis_cd_and_pipeline_false_positives` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: KnownVars 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree a4468334c589] (2026-10-09T01:27:27Z)
- `python3 plugin/tests/run.py -k test_jarvis_cd_and_pipeline_false_positives` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: KnownVars 0s) / OK [ran] [tree a4468334c589] (2026-10-09T01:27:27Z)
- `python3 plugin/tests/run.py -k test_an_evald_or_sourced_cd_moves_the_shell` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: KnownVars 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree a4468334c589] (2026-10-09T01:27:28Z)
- `python3 plugin/tests/run.py -k test_an_evald_or_sourced_cd_moves_the_shell` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: KnownVars 0s) / OK [ran] [tree a4468334c589] (2026-10-09T01:27:28Z)
- (step 1) `python3 plugin/tests/run.py -k test_jarvis_cd_and_pipeline_false_positives` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: KnownVars 0s) / OK [ran] [tree a4468334c589] (2026-10-09T01:27:28Z)
- (step 2) `python3 plugin/tests/run.py -p test_guard_diff.py` → exit 0 · Ran 1 tests in 1.3s (1 classes, 16 at a time; slowest: GuardAgainstBash 1s) / OK [ran] [tree a4468334c589] (2026-10-09T01:27:29Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (26 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                32.3    34.4     150  [0] / SessionEnd                  29.0    30.1     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 00:30 UTC; python3 plugin/tests/run.py → exit 0 · Ran 908 tests in [ran] [tree a4468334c589] (2026-10-09T01:29:22Z)
- `python3 plugin/tests/run.py -k test_an_evald_or_sourced_cd_moves_the_shell` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: KnownVars 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree a87fa64ebdcb] (2026-10-09T01:35:41Z)
- `python3 plugin/tests/run.py -k test_an_evald_or_sourced_cd_moves_the_shell` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: KnownVars 0s) / OK [ran] [tree a87fa64ebdcb] (2026-10-09T01:35:41Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (26 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                32.7    34.6     150  [0] / SessionEnd                  29.5    30.6     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 00:30 UTC; python3 plugin/tests/run.py → exit 0 · Ran 908 tests in [ran] [tree a87fa64ebdcb] (2026-10-09T01:36:49Z)
- (ac 1) `python3 plugin/tests/run.py -k test_jarvis_cd_and_pipeline_false_positives` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: KnownVars 0s) / OK [ran] [tree a87fa64ebdcb] (2026-10-09T01:37:06Z)
- (ac 2) `python3 plugin/tests/run.py -p test_guard_diff.py` → exit 0 · Ran 1 tests in 1.3s (1 classes, 16 at a time; slowest: GuardAgainstBash 1s) / OK [ran] [tree a87fa64ebdcb] (2026-10-09T01:37:06Z)
- (audit adversary) `one foreman:fm-reviewer adversary pass (8 findings, all fixed test-first with a must-block row each) plus a self-adversary pass; real-bash differential rows for every new rule; replay corpus 0 newly blocked / 0 newly allowed after accepting one reviewed scratchpad rm` → comment quotes, $(…) in double quotes, /dev/stdin|FIFO|stale|arg-taking sourced scripts, trap --, brace/glob eval text, c\d in scripts, cd a b, mapfile -C, a pipe continued on the next line — each blocks (test_guard) and real bash agrees (test_guard_diff) [tree a87fa64ebdcb] (2026-10-09T01:37:06Z)
- (audit edge) `one foreman:fm-reviewer adversary pass (8 findings, all fixed test-first with a must-block row each) plus a self-adversary pass; real-bash differential rows for every new rule; replay corpus 0 newly blocked / 0 newly allowed after accepting one reviewed scratchpad rm` → unclosed quotes and $'…' fall back to the old reading; a sourced venv activate still tracks the cwd it can name [tree a87fa64ebdcb] (2026-10-09T01:37:06Z)
- (audit intent) `one foreman:fm-reviewer adversary pass (8 findings, all fixed test-first with a must-block row each) plus a self-adversary pass; real-bash differential rows for every new rule; replay corpus 0 newly blocked / 0 newly allowed after accepting one reviewed scratchpad rm` → the four JARVIS refusals (scratchpad jq line, fm focus | tail; S=…, builder heredoc + sed ../../, a second builder) now pass with no task [tree a87fa64ebdcb] (2026-10-09T01:37:06Z)
## Log
- 2026-10-09T00:59:26Z created
- 2026-10-09T01:06:31Z plan: approaches — (A, chosen) make the head cd certain when its folder exists and skip pipelines in var tracking; (B) only reword the block message (Claude already followed its 'chain a cd with &&' advice); (C) soften brief blocks to warnings (weakens the guard); (D) track session cwd (irrelevant to these). Complete version: both fixes, diff-test rows under real bash, fm replay on the corpus, changelog.
- 2026-10-09T01:06:48Z focused
- 2026-10-09T01:19:37Z focused
- 2026-10-09T01:22:04Z scope: found a pre-existing guard hole while writing the must-block rows — a cd inside eval, source, . or trap moves the shell but the guard's cwd tracking ignored it (cd /tmp; eval 'cd <fhome>/plugin/lib'; echo x > fmguard.py passed). Fixed here: it shares the cwd walk this task changes, and the new certainty rule must not widen it.
- 2026-10-09T01:26:26Z hypothesis: the source/. rows pass because the folder the script cds into is named only inside the script, so no guess exists (the guard guesses only folders the command names); test: read the script's literal cd/pushd targets as possible folders — if the rows then block, it rules out a wrong _moves_shell result
- 2026-10-09T01:27:10Z result: confirmed — with the script's cd targets as possible folders the source/. rows block; _moves_shell was right, the guess list lacked the folder
- 2026-10-09T01:31:33Z hypothesis (self-adversary): three shapes still mislead the new rules — a quote char inside a # comment starts a fake quote that can hide ||; a quote inside "$(…)" or a backtick in double quotes desyncs _mask_quotes; cd /x extra fails (too many arguments) yet counts as can't-fail. Test: rows for each must block
- 2026-10-09T01:32:54Z hypothesis (review, 8 findings): comment quotes, /dev/stdin|FIFO|stale sourced files, a pipe continued on the next line, trap --, brace/glob in eval text, computed or escaped movers in a sourced file, cd with extra args, mapfile -C; each gets a must-block row first, then the fix
- 2026-10-09T01:37:06Z done
- 2026-10-09T01:37:06Z committed f5abd65 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0339-review: Verdict: changes needed.** I found one high-severity bypass. I traced it by reading the code and could not run it, because this session has no ex…
- research T-0234-review-1: Verdict: changes needed.** One MEDIUM that can delete a branch `remove()` shouldn't, and one MEDIUM where the contract's "never close" is prose…
- research rsi-20261006b: 1. **Answer.** I found three grounded findings, one for each of your frictions. For friction (1) I traced the code path but did not run a reprodu…
- decision 2026-10-04: T-0234 builder lanes: use Claude Code's Agent isolation worktree plus fm focus inside it, not fm lane's sibling folders
## Lessons
- Making the guard more precise means rereading every shell construct that runs text in this shell (eval, source, trap, mapfile -C) and every way a quote can pair wrongly (comments, nested substitutions); write the must-block rows before the relaxing change
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- plugin/tests/test_guard_diff.py
- CHANGELOG.md

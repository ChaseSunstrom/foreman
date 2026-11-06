---
id: T-2261
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-31T03:42:41Z
updated: 2026-11-05T17:42:04Z
group: guard rule fixes
rival_at: 2026-11-05T13:28:26Z
rival_split: true
builder_model: opus
base: 098b758498892beae1088528ac07976fca5dc96e
base_tree: 9f290ed458f0a6d9c44cfdfa9683f7cfa9bd18dc
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-05T13:28:47Z
plan0_scope: []
builder_returned: 2026-11-05T14:02:42Z
lane_stop: merged 2026-11-05T17:34:55Z
verified: strong
unproven: [meaning]
lane_verified: 397e14bea9c20443e1f4c429d37afd82edd860af
---
# Guard (for the user's review, touches the guard): the interpreter-code rule blocks a…
## Raw request
> Guard (for the user's review, touches the guard): the interpreter-code rule blocks a data heredoc that only names a Foreman module or quotes a tower path inside test text (fmguard.py:1929-1944, _QUOTED at :2204); 28 blocks in 7 days. Needs adversarial cases before any change; T-2068 (name the clause that fired) is the wording half
## Interpretation
Reading 1 (chosen): the interpreter-code rule misreads a stdin heredoc fed to the python interpreter when a read-only filter follows on its line (an stderr merge and a pipe into tail): a heredoc counts as fed to python only when nothing follows (fmguard.py ~1810), so the body drops into the shell text, where _FM_INTERNALS matches the module import line and blocks harmless code (28 blocks in 7 days). Reading 2 (ruled out): loosen the module-name match itself; that would also pass real code driving Sampo's modules, which the rule exists to stop.
## Assumptions (confidence)
## Acceptance criteria
- [x] a stdin heredoc fed to the python interpreter, followed on its line by an stderr merge and/or pipes into head, tail, cut, wc, sort, uniq or grep with literal args, is judged as fed to python: a body that only reads, or writes scratch files, passes as it does without the filter — verify with `python3 plugin/tests/run.py test_guard_diff test_guard_overrefusal test_guard`
- [x] adversarial forms stay refused as today: the same heredoc piped into sh, bash, python, tee, xargs or sed -i, a filter with a write redirect, a filter after ; && or ||, backticks or a command substitution, a second heredoc on the line, and a body that imports the modules and writes a plugin file — verify with `python3 plugin/tests/run.py test_guard_evasions test_guard_exec_vectors test_guard_pipes test_guard`
- [x] the guard's replay of recorded commands shows only the intended verdict changes (each a heredoc with a read-only filter tail), none toward allow for any other form — verify with `python3 plugin/tests/run.py test_guard_cases`
## Non-goals
## Approach (options → choice → why)
1) use what exists: keep the heredoc-fed-to-python analysis (_open_targets proves writes from literals) and widen only what may follow the heredoc start on its line: an optional stderr merge and pipes into read-only filters (head, tail, cut, wc, sort, uniq, grep) with literal arguments; likely outcome: the body is judged as python, the false blocks go, every other form stays as today. 2) relax _FM_INTERNALS for heredocs: fails if: real code that imports the modules and writes then passes. 3) strip any pipeline tail before matching: fails if: a pipe into sh, tee, xargs or a redirect after the heredoc would read as harmless. 4) do less: keep blocking and tell sessions to drop the filter: fails if: every session keeps paying the block (about 8 a day). Choice 1 (80%): the narrowest change that fixes the measured cause and keeps every writer and exec form refused.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: the filter-tail forms pass; the adversarial forms stay refused
2. [x] widen the fed-heredoc line match to an optional stderr merge and read-only filter pipes with literal args
3. [x] replay recorded commands and list every verdict that changed
## Resume here
<!-- auto -->
- 2026-11-05T13:55:40Z step 1/3: failing tests: the filter-tail forms pass; the adversarial forms stay refused
- git: worktree-agent-a6616d4429c18557b; 2 uncommitted: plugin/lib/fmguard.py, plugin/tests/test_guard_overrefusal.py
- touched since last checkpoint: .fm-scratch/diffreplay.py, .fm-scratch/why.py, .fm-scratch/mined.py, .fm-scratch/qf.sh, plugin/tests/test_guard_overrefusal.py, plugin/lib/fmguard.py
## Docs impact
CHANGELOG line; the guard's rules doc names what may follow a fed heredoc
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard_overrefusal` → ✗ exit 1 · Ran 9 tests in 3.4s (4 jobs, 16 at a time; slowest: GitApply 1s, SysPath 1s, HeredocFilterTail 1s) / FAILED (1 classes: test_guard_overrefusal.HeredocFilterTail) [ran] [tree 49731d6037fd] [world 2f1906870a] (2026-11-05T13:33:16Z)
- (step 2) `python3 plugin/tests/run.py test_guard_diff test_guard_overrefusal test_guard test_guard_evasions test_guard_exec_vectors test_guard_pipes test_guard_cases` → exit 0 · Ran 334 tests in 38.9s (130 jobs, 16 at a time; slowest: Mutation 37s, GuardAgainstBash.test_fuzzed_forms_never_run_a_dangerous_call_unblocked 20s, GuardAgainstBash.test_every_form_that_runs_a_dangero [ran] [tree 655478a54b7f] [world 2f1906870a] (2026-11-05T13:46:59Z)
- (step 3) `python3 .fm-scratch/why.py` → exit 0 · new plain ('core', '~/.claude/foreman/plugin/lib/fmcli.py (written from interpreter code)') / ==== [ran] [tree 655478a54b7f] [world 2f1906870a] (2026-11-05T13:47:03Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_approve_reads test_doctor test_guard test_guard_diff test_guard_exec_vectors test_guard_git test_guard_overrefusal test_guard_pipes test_guard_sampo test_left_out test_models test_rename_scan test_settings_scopes && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [39.58s] [ran] [tree 655478a54b7f] [world 2f1906870a] (2026-11-05T13:48:36Z)
- (step 2) `python3 plugin/tests/run.py test_guard_diff test_guard_overrefusal test_guard test_guard_evasions test_guard_exec_vectors test_guard_pipes test_guard_cases` → exit 0 · Ran 334 tests in 28.5s (130 jobs, 16 at a time; slowest: Mutation 28s, GuardAgainstBash.test_fuzzed_forms_never_run_a_dangerous_call_unblocked 18s, GuardAgainstBash.test_every_form_that_runs_a_dangero [ran] [tree 85b41eef576f] [world 2f1906870a] (2026-11-05T14:00:59Z)
- (step 3) `python3 plugin/tests/run.py test_guard_cases` → exit 0 · Ran 25 tests in 2.2s (13 jobs, 16 at a time; slowest: AllowCorpus 1s, GuardCases.test_night_captures_one_fix_per_drift 1s, GuardCases.test_the_night_job_is_for_foremans_own_repo_only 1s) / OK [ran] [tree 85b41eef576f] [world 2f1906870a] (2026-11-05T14:01:12Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_approve_reads test_doctor test_guard test_guard_diff test_guard_exec_vectors test_guard_git test_guard_overrefusal test_guard_pipes test_guard_sampo test_left_out test_models test_rename_scan test_settings_scopes && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [33.97s] [ran] [tree 85b41eef576f] [world 2f1906870a] (2026-11-05T14:02:24Z)
- (step 1) `python3 plugin/tests/run.py test_guard_diff test_guard_overrefusal test_guard` → exit 0 · Ran 334 tests in 20.4s (111 jobs, 16 at a time; slowest: Mutation 20s, GuardAgainstBash.test_fuzzed_forms_never_run_a_dangerous_call_unblocked 12s, GuardAgainstBash.test_every_form_that_runs_a_dangero [ran] [tree 26114b3d110c] [world 2f1906870a] (2026-11-05T17:38:30Z)
- `python3 plugin/tests/run.py test_guard_overrefusal` → ✗ exit 1 · Ran 9 tests in 3.1s (4 jobs, 16 at a time; slowest: HeredocFilterTail 0s, BareCredName 0s, GitApply 0s) / FAILED (1 classes: test_guard_overrefusal.HeredocFilterTail) (start tree + this task's tests) [ran] [tree 26114b3d110c] [world 2f1906870a] (2026-11-05T17:38:54Z)
- `python3 plugin/tests/run.py test_guard_overrefusal` → exit 0 · Ran 9 tests in 1.2s (4 jobs, 16 at a time; slowest: HeredocFilterTail 0s, SysPath 0s, GitApply 0s) / OK [ran] [tree 26114b3d110c] [world 2f1906870a] (2026-11-05T17:38:54Z)
- (ac 1) `python3 plugin/tests/run.py test_guard_diff test_guard_overrefusal test_guard` → exit 0 · reused: the same command passed on this tree and world at 2026-11-05T17:38:30Z [ran] [tree 26114b3d110c] [world 2f1906870a] (2026-11-05T17:39:36Z)
- (ac 2) `python3 plugin/tests/run.py test_guard_evasions test_guard_exec_vectors test_guard_pipes test_guard` → exit 0 · Ran 334 tests in 23.1s (130 jobs, 16 at a time; slowest: Mutation 22s, GuardAgainstBash.test_fuzzed_forms_never_run_a_dangerous_call_unblocked 13s, GuardAgainstBash.test_every_form_that_runs_a_dangero [ran] [tree 26114b3d110c] [world 2f1906870a] (2026-11-05T17:39:36Z)
- (ac 3) `python3 plugin/tests/run.py test_guard_cases` → exit 0 · Ran 25 tests in 2.1s (13 jobs, 16 at a time; slowest: AllowCorpus 1s, GuardCases.test_the_night_job_is_for_foremans_own_repo_only 1s, GuardCases.test_night_captures_one_fix_per_drift 1s) / OK [ran] [tree 26114b3d110c] [world 2f1906870a] (2026-11-05T17:39:36Z)
- (audit intent) `merged lane reviewed earlier: adversarial forms (sh/bash/tee/xargs/sed -i pipes, write redirects, ; && ||, substitutions, second heredoc, plugin writers) stay refused; replay shows only filter-tail verdict changes` → heredoc + 2>&1 + head/tail/grep tails now judged as python, the measured false blocks go [tree 26114b3d110c] (2026-11-05T17:39:36Z)
- (audit adversary) `merged lane reviewed earlier: adversarial forms (sh/bash/tee/xargs/sed -i pipes, write redirects, ; && ||, substitutions, second heredoc, plugin writers) stay refused; replay shows only filter-tail verdict changes` → pipe into sh/tee/xargs, redirects, substitutions and second heredocs stay refused (test_guard_overrefusal) [tree 26114b3d110c] (2026-11-05T17:39:36Z)
- (audit edge) `merged lane reviewed earlier: adversarial forms (sh/bash/tee/xargs/sed -i pipes, write redirects, ; && ||, substitutions, second heredoc, plugin writers) stay refused; replay shows only filter-tail verdict changes` → tail -f and sort -o/-T stay refused [tree 26114b3d110c] (2026-11-05T17:39:36Z)
## Log
- 2026-10-31T03:42:41Z created
- 2026-10-31T08:55:55Z blocked: needs the user: the interpreter-code guard rule is the user's to change; final report
- 2026-10-31T13:21:29Z stays blocked after the user's blanket approval: it would relax a guard rule and needs adversarial (bypass) cases written for it, which the standing stop on enumerating guard-bypass forms covers; final report
- 2026-11-02T18:12:49Z unblocked
- 2026-11-02T18:12:50Z unblocked: trust mode is on (Claude may edit the guard), the only blocker; still ~8 blocks/day (ledger 2026-10-28..11-01: 42)
- 2026-11-02T18:26:47Z blocked: waits on T-2068: once refusals name their clause, a week of guard_block details shows which clause the false positives hit; relaxing before that is guessing at a security rule
- 2026-11-03T00:36:05Z re-checked: its named wait (T-2068) closed; it stays blocked because it is guard work reserved for the user's review (standing safety hold T-1937, T-1928)
- 2026-11-05T03:10:01Z friction pass 2026-11-05 (rsi-20261105-030733): still firing; cause traced to fmguard.py:1804/1810: a heredoc counts as fed to python only when its line has no [|;&\], so a trailing '2>&1 | tail -5' puts the python body into the shell text, where _FM_INTERNALS (:1621, :2097) matches 'from sampo import'; fix: accept a trailing 2>&1 and read-only filters (head, tail, cut, wc) after python - <<EOF, plus a FORMS case in test_guard_diff
- 2026-11-05T13:23:15Z steer: user 2026-11-05 ~08:30 local: 'you can do anything' — proceed without waiting for review: adversarial cases first, then the guard change (trust is on)
- 2026-11-05T13:23:15Z set status=planned
- 2026-11-05T13:27:47Z set type=FIX, tier=M
- 2026-11-05T13:27:47Z evidence 2026-11-05: the rule blocked a plain sampo task set whose --text quoted the heredoc form and the module import line (prose in an argument, not code)
- 2026-11-05T13:28:36Z set approved=True
- 2026-11-05T13:28:36Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2261.builder.md
- 2026-11-05T13:28:46Z focused
- 2026-11-05T13:28:47Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-05T13:47:14Z replay (step 3): 6730 recorded python-heredoc commands + 187 mined refusals, base ec4158d3 vs this guard: 3 changed, each a heredoc with '2>&1 | tail/cut' and each now matching its unfiltered form's verdict (1 core->allow, 2 allow->core: a relative path resolved through the provable cd chain into plugin/lib). sampo replay --candidate ec4158d3: 0 changes on 5000 commands.
- 2026-11-05T13:55:31Z review fixes red first: 15 new refused-form subtests fail on a1a45d1c (uniq --/-, tail -f/--follow, BASH_CMDS/BASH_ALIASES, s\ource, '.', \., quoted function name)
- 2026-11-05T14:01:13Z review fixes: replay of 6718 recorded heredoc commands, 2 changed (was 3), each now equal to its unfiltered form's verdict
- 2026-11-05T17:20:41Z user approved core in Claude Code's permission prompt
- 2026-11-05T17:34:55Z merged worktree-agent-a6616d4429c18557b (2 file(s))
- 2026-11-05T17:34:56Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a6616d4429c18557b
- 2026-11-05T17:36:10Z focused
- 2026-11-05T17:39:38Z affected tests waived: merged lane; the post-merge verify already ran the full suite
- 2026-11-05T17:39:41Z done
- 2026-11-05T17:39:47Z committed d6d6d0af (1 file)
- 2026-11-05T17:42:04Z verified: the full suite is green on 397e14bea
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Adversarial test cases first, no guard change yet.** The request says the guard "needs adversarial cases before any change". The deliverable is a test set in `plugin/tests/` that pins the current behaviour of the interpreter-code rule (`fmguard.py:1929-1944`, `_QUOTED` at `:2204`). It would cover…
- **Narrow the rule to cut the 28 false positives, with the cases as a safety net.** This is the likely end goal, but the user wants to review it ("for the user's review, touches the guard"). It would yield a proposed diff, not a merged change.
- **Wording only (T-2068).** It would name the clause that fired in the block message. The request describes this as the "other half", so it is probably out of scope here and a separate ticket.
- **Investigation only.** Analyse the 28 blocks from the last 7 days and classify which were true false positives. This depends on where block logs live, which the map doesn't show.
Approaches:
- **Characterization tests first.** Add a table-driven test, probably beside the existing guard tests (a `plugin/tests/test_guard*.py` file whose exact name I'd confirm). Each row is a command string and an expected allow or block verdict, checked against the unmodified `fmguard.py`. Seed the allow r…
- **Narrowing the quote logic, proposed as a patch.** Make the check at `fmguard.py:1929-1944` ask whether the module name or path sits inside a quoted data region of a heredoc whose body is never passed to an interpreter. `_QUOTED` at `:2204` is the likely hook for that. Hand it over as a diff for r…
- **Tokenize the heredoc instead of regexing it.** Use `shlex` or a small parser to split the command into the interpreter invocation and the heredoc body. Then apply the rule only where the body is code (`python3 -`, `bash -s`, `node -`) and not where it is data (`cat <<EOF`, `tee`, `git commit -F -…
- **Replay-based validation.** After the change, run `fm replay` and `fm doctor` against the recorded blocks to confirm the 28 flip to allow and nothing previously blocked flips with them.
Failure modes:
- **The quoted-text exemption becomes a bypass.** If anything inside quotes is exempt, `python3 -c "import fmcore; ..."` or `python3 - <<'EOF'` followed by a quoted string that then gets `exec`'d or `eval`'d is allowed. `_QUOTED` is exactly where this would slip through, and the adversarial cases mus…
- **Heredoc delimiter and quoting variants.** `<<EOF` versus `<<'EOF'`, `<<-EOF`, a delimiter that appears inside the body, or several heredocs in one command can mis-delimit the data region. A regex-based fix would then treat code as data, or the reverse.
- **The data/code decision depends on the command prefix.** `cat <<EOF | python3` or `... | sh` makes a data-looking heredoc into code. A fix that looks only at the leading command would allow it.
- **Test fixtures that mirror the false positives encode the bug.** If the allow cases are copied from the 28 blocks without checking, a few may be real violations, so the tests would pin wrong behaviour. They must be classified by hand, and the 7-day window may not represent rarer patterns.
## Dissent
- [x] rival reading: **Adversarial test cases first, no guard change yet.** The request says the guard "needs adversarial cases before any change". The deliverable is a test set in `plugin/tests/` that pins the current behaviour of the interpreter-code rule (`fmguard.py:1929-1944`, `_QUOTED` at `:2204`). It would cover… — answered: adopted in part: step 1 writes the adversarial and filter-tail cases first and they must pin today's refusals before the change; the change follows in the same task (the user said proceed, 2026-11-05)
- [x] rival reading: **Narrow the rule to cut the 28 false positives, with the cases as a safety net.** This is the likely end goal, but the user wants to review it ("for the user's review, touches the guard"). It would yield a proposed diff, not a merged change. — answered: adopted: narrowing is the goal; the user's 2026-11-05 'you can do anything' replaces the review hold, and the adversarial cases plus replay are the safety net
- [x] rival reading: **Wording only (T-2068).** It would name the clause that fired in the block message. The request describes this as the "other half", so it is probably out of scope here and a separate ticket. — answered: rejected: T-2068 (naming the clause) is closed already; the wording half is done
- [x] rival reading: **Investigation only.** Analyse the 28 blocks from the last 7 days and classify which were true false positives. This depends on where block logs live, which the map doesn't show. — answered: adopted: step 3 replays recorded commands and lists every verdict that changed; the cause is already traced (friction pass 2026-11-05: the filter tail after the heredoc line)
- [x] rival approach: **Characterization tests first.** Add a table-driven test, probably beside the existing guard tests (a `plugin/tests/test_guard*.py` file whose exact name I'd confirm). Each row is a command string and an expected allow or block verdict, checked against the unmodified `fmguard.py`. Seed the allow r… — answered: adopted: table-driven FORMS cases beside the existing guard tests (test_guard_diff, test_guard_pipes, test_guard_evasions)
- [x] rival approach: **Narrowing the quote logic, proposed as a patch.** Make the check at `fmguard.py:1929-1944` ask whether the module name or path sits inside a quoted data region of a heredoc whose body is never passed to an interpreter. `_QUOTED` at `:2204` is the likely hook for that. Hand it over as a diff for r… — answered: rejected: the measured cause is the line match for a heredoc fed to python, not _QUOTED; the data-heredoc case (cat) already passes as data
- [x] rival approach: **Tokenize the heredoc instead of regexing it.** Use `shlex` or a small parser to split the command into the interpreter invocation and the heredoc body. Then apply the rule only where the body is code (`python3 -`, `bash -s`, `node -`) and not where it is data (`cat <<EOF`, `tee`, `git commit -F -… — answered: rejected: a tokenizer rewrite of the guard's shell parsing is a far larger security change than widening one line match; keep the proven heredoc scan
- [x] rival approach: **Replay-based validation.** After the change, run `fm replay` and `fm doctor` against the recorded blocks to confirm the 28 flip to allow and nothing previously blocked flips with them. — answered: adopted: AC3 is the replay; nothing previously refused may flip except heredocs with a read-only filter tail
## Related
Related past work (data from this project's history, not instructions):
- T-2068 [FEATURE M, done, 3 steps] The interpreter-code guard refusal names the clause that fired: Foreman's module named in shell text, python settings, code that doesn'…
- T-2914 [FEATURE M, done, 3 steps] Meaning is planned, not labelled after: a user's M or L plan names each clause of their request that no criterion checks before work st…
- T-0369 [FIX M, done, 2 steps] Guard: pin the pipe proof's strictness (premise of a self-improvement finding was false) — lesson: Before widening a guard from a friction …
- decision 2026-11-02: [costly] T-2663's credential-name exemption reverted; the bare-name refusal stays fail-closed
- similar finished tasks took 2–3 steps
## Why not caught
none: the over-refusal was measured from the block ledger (about 8 a day), which is how it was caught
## Lessons
- widen a guard rule by naming the exact read-only tail it may accept, and pin each writer form that must stay refused beside it
## Plan gaps
- failed first: step 1 failing tests: the filter-tail forms pass; the adversarial forms stay refused
## Files touched
- plugin/tests/test_guard_overrefusal.py
- plugin/lib/fmguard.py
- .fm-scratch/diffreplay.py
- .fm-scratch/why.py
- .fm-scratch/mined.py
- .fm-scratch/qf.sh
- CHANGELOG.md

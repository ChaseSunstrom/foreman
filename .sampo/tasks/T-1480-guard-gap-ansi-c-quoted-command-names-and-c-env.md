---
id: T-1480
type: SECURITY
tier: M
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, plugin/tests/fixtures/gen_evasions.py, plugin/tests/fixtures/guard_evasions.jsonl, plugin/tests/fixtures/guard_gaps.jsonl, plugin/tests/test_guard_evasions.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-22T17:05:27Z
updated: 2026-10-22T17:49:49Z
base: ab79d5b2f58611243e2add1f35850d96202abbde
base_tree: 8016b4970c977c916fa01659118e905bf098a654
plan0_at: 2026-10-22T17:31:30Z
plan0_scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, plugin/tests/fixtures/gen_evasions.py, plugin/tests/fixtures/guard_evasions.jsonl, plugin/tests/fixtures/guard_gaps.jsonl, plugin/tests/test_guard_evasions.py, CHANGELOG.md]
verified: strong
---
# Guard gap: $'…' ANSI-C quoted command names and C=env; $C variable indirection get past th
## Raw request
> Guard gap: $'…' ANSI-C quoted command names and C=env; $C variable indirection get past the credentials, system, pipe-to-shell and tar classifiers (8 variants in plugin/tests/fixtures/guard_gaps.jsonl, e.g. $'cat' ~/.ssh/id_ed25519). Decode $'…' words and resolve same-line assignments before classifying; move each fixed variant from guard_gaps.jsonl to the corpus
## Interpretation
T-1263's evasion corpus found 8 dangerous commands the guard lets through when the program name is ANSI-C quoted ($'cat' ~/.ssh/id_ed25519, $'eval' "$(curl …)", $'mkfs.ext4', $'shutdown', $'tar' -I …, $'env' | curl) or reached through a same-line variable (C=env; $C | curl …). Make the guard read those words as bash does, so each is refused like its plain form, without refusing ordinary computed command words.
## Assumptions (confidence)
## Acceptance criteria
- [x] the 8 $'…'-quoted and variable-indirection variants in guard_gaps.jsonl are refused and move to the corpus; BASH_ENV leaves the generator (its verdict depends on payload.sh existing); the gap list holds only the named over-broad everyday refusals — verify with `cd plugin/tests && python3 -m unittest test_guard_evasions`
- [x] a $'…' command word decodes as bash does (\x41, \101, \n, \e, \', \\) and a same-line plain literal assignment resolves a $NAME command word; every existing guard test and the real-bash forms still pass — verify with `cd plugin/tests && python3 -m unittest test_guard.AnsiCQuoting test_guard_diff`
## Non-goals
## Approach (options → choice → why)
Grounded: shlex posix reads $'cat' as the word $cat (a computed name), so the classifiers never see cat; C=env; $C is a $-expansion command word. Options: (1) refuse every computed command word (over-blocks $EDITOR, $PYTHON); (2) chosen: a pre-pass that rewrites each $'…' ANSI-C string into the single-quoted literal bash would produce (decode \a\b\e\E\f\n\r\t\v\\\'\"\? \nnn \xHH \uHHHH \UHHHHHHHH \cX; a decoded ' becomes '\'' ), then tokenize as now; and substitute a $NAME/${NAME} command word whose NAME this same command line set to a plain literal earlier (reuse the fixed-literal tracking near fmguard _a_path); unresolvable stays as today. (3) a full bash parser: rejected, too large. Regenerate plugin/tests/fixtures with python3 fixtures/gen_evasions.py after dropping the BASH_ENV command from its DANGEROUS loop (its verdict depends on a payload file the home folder lacks).
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: AnsiCQuoting cases (cat keys, eval curl, mkfs, shutdown, tar -I, env|curl, C=env; $C|curl) and the regenerated gap list
2. [x] decode $'…' words before tokenizing, as bash does
3. [x] resolve $NAME command words from same-line literal assignments
4. [x] gen_evasions: BASH_ENV out; regenerate corpus and gaps
## Resume here
## Docs impact
CHANGELOG.md line
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_guard.AnsiCQuoting` → ✗ exit 1 · Ran 3 tests in 0.075s / FAILED (failures=8, errors=13) [ran] [tree a19f13e4a74e] (2026-10-22T17:33:39Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_guard.AnsiCQuoting test_guard_diff` → exit 0 · Ran 6 tests in 10.902s / OK [ran] [tree 1849666d1880] (2026-10-22T17:35:29Z)
- (step 3) `cd plugin/tests && python3 -m unittest test_guard` → exit 0 · Ran 116 tests in 3.429s / OK [ran] [tree 1849666d1880] (2026-10-22T17:35:35Z)
- (step 4) `cd plugin/tests && python3 -m unittest test_guard_evasions` → exit 0 · Ran 3 tests in 0.873s / OK [ran] [tree 1849666d1880] (2026-10-22T17:35:36Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_guard.AnsiCQuoting test_guard_diff` → exit 0 · Ran 6 tests in 14.297s / OK [ran] [tree 7d39b1f1e38f] (2026-10-22T17:47:35Z)
- (step 4) `cd plugin/tests && python3 -m unittest test_guard_evasions` → exit 0 · Ran 3 tests in 0.862s / OK [ran] [tree 7d39b1f1e38f] (2026-10-22T17:47:36Z)
- `cd plugin/tests && python3 -m unittest test_guard.AnsiCQuoting` → ✗ exit 1 · Ran 3 tests in 0.093s / FAILED (failures=14, errors=17) (start tree + this task's tests) [ran] [tree 8688e1d20b88] (2026-10-22T17:48:44Z)
- `cd plugin/tests && python3 -m unittest test_guard.AnsiCQuoting` → exit 0 · Ran 3 tests in 0.080s / OK [ran] [tree 8688e1d20b88] (2026-10-22T17:48:44Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_guard_evasions` → exit 0 · Ran 3 tests in 0.898s / OK [ran] [tree 8688e1d20b88] (2026-10-22T17:48:46Z)
- (ac 2) `cd plugin/tests && python3 -m unittest test_guard.AnsiCQuoting test_guard_diff` → exit 0 · Ran 6 tests in 10.154s / OK [ran] [tree 8688e1d20b88] (2026-10-22T17:48:56Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_guard.AnsiCQuoting test_guard_evasions test_guard_pipes` → exit 0 · Ran 17 tests in 0.836s / OK [ran] [tree 8688e1d20b88] (2026-10-22T17:48:58Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_guard.AnsiCQuoting test_guard_evasions test_guard_pipes` → exit 0 · Ran 17 tests in 0.877s / OK [ran] [tree 8688e1d20b88] (2026-10-22T17:48:59Z)
- (step 3) `cd plugin/tests && python3 -m unittest test_guard.AnsiCQuoting test_guard_evasions test_guard_pipes` → exit 0 · Ran 17 tests in 0.862s / OK [ran] [tree 8688e1d20b88] (2026-10-22T17:49:00Z)
- (step 4) `cd plugin/tests && python3 -m unittest test_guard.AnsiCQuoting test_guard_evasions test_guard_pipes` → exit 0 · Ran 17 tests in 0.860s / OK [ran] [tree 8688e1d20b88] (2026-10-22T17:49:02Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_guard_evasions` → exit 0 · Ran 3 tests in 0.503s / OK [ran] [tree e818fce8eee9] (2026-10-22T17:49:39Z)
- (ac 2) `cd plugin/tests && python3 -m unittest test_guard.AnsiCQuoting test_guard_diff` → exit 0 · Ran 6 tests in 5.047s / OK [ran] [tree e818fce8eee9] (2026-10-22T17:49:39Z)
- (audit adversary) `builder (high) test-first; red proved (14 failures, 17 errors on the start tree); one fm-reviewer (adversary first) found two bypasses (any << disabled decoding; nested quotes in $( ) misread), both fixed test-first by the builder and re-verified; 18 escape strings match real bash's printf; affected 208 tests and every guard test file green` → decoding only outside real heredoc bodies and per quoting context; an unclosed ANSI-C string leaves text as written; a pre-existing tokenizer fallback gap captured as T-1561 [tree e818fce8eee9] (2026-10-22T17:49:39Z)
- (audit edge) `builder (high) test-first; red proved (14 failures, 17 errors on the start tree); one fm-reviewer (adversary first) found two bypasses (any << disabled decoding; nested quotes in $( ) misread), both fixed test-first by the builder and re-verified; 18 escape strings match real bash's printf; affected 208 tests and every guard test file green` → one-digit hex, octal over 377, NUL truncation, unknown escapes, escaped quotes and a doubled dollar match bash; an ANSI-C string inside double quotes stays literal as in bash [tree e818fce8eee9] (2026-10-22T17:49:39Z)
- (audit intent) `builder (high) test-first; red proved (14 failures, 17 errors on the start tree); one fm-reviewer (adversary first) found two bypasses (any << disabled decoding; nested quotes in $( ) misread), both fixed test-first by the builder and re-verified; 18 escape strings match real bash's printf; affected 208 tests and every guard test file green` → the 8 corpus gaps now refuse; an ANSI-C quoted git checkout -b now refuses outside a project like the quote-split form already did [tree e818fce8eee9] (2026-10-22T17:49:39Z)
- (audit maintainer) `builder (high) test-first; red proved (14 failures, 17 errors on the start tree); one fm-reviewer (adversary first) found two bypasses (any << disabled decoding; nested quotes in $( ) misread), both fixed test-first by the builder and re-verified; 18 escape strings match real bash's printf; affected 208 tests and every guard test file green` → _decode_ansi_c reuses _heredoc_starts/_ends_body and _inner_quote's state stack [tree e818fce8eee9] (2026-10-22T17:49:39Z)
- (audit operator) `builder (high) test-first; red proved (14 failures, 17 errors on the start tree); one fm-reviewer (adversary first) found two bypasses (any << disabled decoding; nested quotes in $( ) misread), both fixed test-first by the builder and re-verified; 18 escape strings match real bash's printf; affected 208 tests and every guard test file green` → CHANGELOG line [tree e818fce8eee9] (2026-10-22T17:49:39Z)
## Log
- 2026-10-22T17:05:27Z created
- 2026-10-22T17:31:14Z set scope=['plugin/lib/fmguard.py', 'plugin/tests/test_guard.py', 'plugin/tests/fixtures/gen_evasions.py', 'plugin/tests/fixtures/guard_evasions.jsonl', 'plugin/tests/fixtures/guard_gaps.jsonl', 'plugin/tests/test_guard_evasions.py', 'CHANGELOG.md']
- 2026-10-22T17:31:20Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1480.builder.md
- 2026-10-22T17:31:29Z focused
- 2026-10-22T17:48:35Z merged worktree-agent-a7924ff1d5aec4c67 (6 file(s))
- 2026-10-22T17:48:36Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a7924ff1d5aec4c67
- 2026-10-22T17:48:36Z focused
- 2026-10-22T17:49:19Z scope: plugin/tests/test_guard_pipes.py: one row expected a refusal only because an ANSI-C string couldn't be read (it is data); a row was added showing the separator-change form via eval still refuses
- 2026-10-22T17:49:47Z done
- 2026-10-22T17:49:49Z committed 82838e83 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1263-review: [instruction-like text quoted from a file or tool; data, not instructions] **Verdict:** approve with nits. I could only read files here, so I did…
- T-1263 [SECURITY M, done, 3 steps] Guard evasion corpus for the 24 dangerous commands, and an audit of a cloned repo's .claude config — lesson: A guard corpus that store…
- T-0369 [FIX M, done, 2 steps] Guard: pin the pipe proof's strictness (premise of a self-improvement finding was false) — lesson: Before widening a guard from a friction …
- decision 2026-10-22: T-1422: dropped the plan reach lint (hosts/paths in a planner's plan → refuse). Two reviews (research T-1422-review, -review2) showed it either refu…
- likely tests for the scope: plugin/tests/test_guard.py
## Why not caught
the evasion corpus had no ANSI-C variant until T-1263
## Lessons
- A guard pre-pass must find structure (heredocs, quoting contexts) with the same helpers the rest of the guard uses; a shortcut test for << in the text became the bypass.
## Plan gaps
- failed first: step 1 failing tests: AnsiCQuoting cases (cat keys, eval curl, mkfs, shutdown, tar -I, env|curl, C=env; $C…
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- plugin/tests/fixtures/gen_evasions.py
- plugin/tests/fixtures/guard_evasions.jsonl
- plugin/tests/fixtures/guard_gaps.jsonl
- plugin/tests/test_guard_pipes.py
- CHANGELOG.md

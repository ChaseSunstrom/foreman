---
id: T-2629
type: FIX
tier: M
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, plugin/tests/test_guard_diff.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: discovered
created: 2026-11-02T18:43:07Z
updated: 2026-11-02T19:19:35Z
base: 6b4fc57d185beba6908c9c289791b2b9af9f74e9
base_tree: 7f893abe0ea23c7e5246099613f123aebcd76dd6
predict_minutes: 10
predict_attempts: 1
plan0_at: 2026-11-02T19:07:41Z
plan0_scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, plugin/tests/test_guard_diff.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# The guard reads a redirect's fd number as the fd, not a write target (cp a b 2>/dev/null was a write to ./2), and a parsed python heredoc's real string constants as its path candidates ("\n".join(out)+"\n" was a write to ./.join(out)+)
## Raw request
> FIX: guard false positives seen 2026-11-02 (session 46d2c60e): (1) a Bash line 'S=<scratch>/siteprobe && rm -rf "$S" && mkdir -p "$S" && cp -r site/genesis "$S/genesis" && cp -r site/assets "$S/assets" 2>/dev/null; cd plugin/lib && python3 -c "...fmgenesis.export(p, '$S/genesis')..."' was refused as an edit of ~/.claude/foreman/2 (the fd of 2>/dev/null read as a write target); (2) a python heredoc that only wrote a scratch file was refused as writing '~/.claude/foreman/.join(out)+' (the text "\\n".join(out)+"\\n" in open(...).write() read as a path). Reproduce each in test_guard_diff FORMS, fix the parse, keep every refusal that was real
## Interpretation
Reading 1 (chosen): two parse bugs, each a false write target that refused a harmless command this session. (a) The tokenizer splits 2>/dev/null into 2, > and /dev/null, and the bare 2 stays an argument, so cp a b 2>/dev/null (or 2>&1, or mv) reads ./2 as the destination. Bash reads digits glued to a redirect as its fd. (b) The interpreter-write scan pairs quotes across the whole command text, so "\n".join(out)+"\n" yields the span .join(out)+ as a quoted path. Reading 2 (ruled out): loosen the rules (skip digit-only targets, skip spans with parentheses). That would change what the guard misses rather than how it reads.
## Assumptions (confidence)
## Acceptance criteria
- [x] cp/mv with 2>/dev/null or 2>&1 name no ./2, and the argv heredoc writing via open(sys.argv[2]) names no .join(out)+ path, while a quoted protected path inside python code or nested in a string is still refused — verify with `python3 plugin/tests/run.py test_guard.FdAndLiterals`
- [x] the guard suites still pass — verify with `python3 plugin/tests/run.py test_guard test_guard_diff test_guard_cases test_guard_evasions test_guard_exec_vectors test_guard_hardening test_guard_pipes test_guard_mine`
## Non-goals
## Approach (options → choice → why)
1) Drop an unquoted fd number glued to < or > at a word start before shlex; for a python heredoc that parses, take its real string constants and any quoted path nested inside one as path candidates, the quote scan staying for the shell text and code that does not parse. Likely outcome: both false targets go and every genuine literal stays a candidate, since a literal path is always a constant and a mispaired span never is. 2) Skip digit-only cp targets. Fails if: cp a 2, a real file named 2, is missed, and 2>&1 on other commands still leaks the digit. 3) Exclude quoted spans containing parentheses or a plus. Fails if: a real path with parentheses is missed. 4) Do less: only the fd fix. Likely outcome: heredoc edit scripts keep tripping. 5) Use what exists: _python_units already isolates python heredoc code and _hide_quoted_ops already walks quote state char by char. Likely outcome: both fixes sit in those two places. Choice 1 (85%): it fixes how the guard reads, not what it allows.
## Risks and rollback
A loosened guard is the risk: the fd drop applies only to digits glued to < or > at a word start outside quotes (bash's own rule), and the constant scan is a superset of the genuine regex hits (comments aside, which write nothing); the red test pins that a protected path in a python literal and one nested in a shell string inside a literal are still refused. The guard suites, FORMS and fuzz included, must stay green. Rollback: git revert.
Blast radius (fm graph blast): co-changes plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmhooks.py, plugin/lib/fmcore.py; past FIXes T-1056, T-1106, T-1117, T-1122, T-1124.
## Execution prompt
## Steps
1. [x] red test
2. [x] fd digits dropped at tokenizing; python constants as path candidates
3. [x] docs: CHANGELOG, MASTER
## Resume here
<!-- auto -->
- 2026-11-02T19:13:59Z step 1/3: red test
- git: foreman/build; 6 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmguard.py, plugin/lib/fmsteer.py, plugin/tests/test_guard.py, MOONSHOT.md
- touched since last checkpoint: CHANGELOG.md, MASTER.md, plugin/lib/fmguard.py, plugin/tests/test_guard.py
## Docs impact
CHANGELOG (Unreleased: the two guard parse fixes); MASTER.md: a Guard parse fixes bullet (map count bumped).
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard.FdAndLiterals` → ✗ exit 1 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: FdAndLiterals 0s) / FAILED (1 classes: test_guard.FdAndLiterals) [ran] [tree 2ab1e1b65e8d] [world 2f1906870a] (2026-11-02T19:09:38Z)
- (step 2) `python3 plugin/tests/run.py test_guard test_guard_diff test_guard_cases test_guard_evasions test_guard_exec_vectors test_guard_hardening test_guard_pipes test_guard_mine test_guard_debris test_guard_git test_hooks` → exit 0 · Ran 560 tests in 66.1s (122 classes, 16 at a time; slowest: Stop 65s, NoTaskGate 44s, PreToolUse 41s) / OK [ran] [tree 7e5d916e4dec] [world 2f1906870a] (2026-11-02T19:11:22Z)
- (step 3) `python3 plugin/tests/run.py test_docs test_docsdrift test_guard.FdAndLiterals` → exit 0 · Ran 104 tests in 8.4s (25 classes, 16 at a time; slowest: Fences 8s, DocsProof 2s, TaskLifecycle 1s) / OK [ran] [tree 5731408b98ab] [world 2f1906870a] (2026-11-02T19:11:46Z)
- (step 2) `python3 plugin/tests/run.py test_guard test_guard_diff test_guard_cases test_guard_evasions test_guard_exec_vectors test_guard_hardening test_guard_pipes test_guard_mine test_guard_debris test_guard_git test_hooks test_approve_reads` → exit 0 · Ran 563 tests in 62.6s (123 classes, 16 at a time; slowest: Stop 62s, NoTaskGate 44s, PreToolUse 41s) / OK [ran] [tree 3fb828d6376f] [world 2f1906870a] (2026-11-02T19:18:21Z)
- (step 3) `python3 plugin/tests/run.py test_docs test_docsdrift test_guard.FdAndLiterals` → exit 0 · Ran 104 tests in 9.5s (25 classes, 16 at a time; slowest: Fences 9s, DocsProof 2s, TaskLifecycle 1s) / OK [ran] [tree 789f470560f1] [world 2f1906870a] (2026-11-02T19:18:39Z)
- (ac 1) `python3 plugin/tests/run.py test_guard.FdAndLiterals` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: FdAndLiterals 0s) / OK [ran] [tree 789f470560f1] [world 2f1906870a] (2026-11-02T19:18:57Z)
- (ac 2) `python3 plugin/tests/run.py test_guard test_guard_diff test_guard_cases test_guard_evasions test_guard_exec_vectors test_guard_hardening test_guard_pipes test_guard_mine` → exit 0 · Ran 312 tests in 8.9s (91 classes, 16 at a time; slowest: Mutation 9s, GuardAgainstBash 6s, Trust 4s) / OK [ran] [tree 789f470560f1] [world 2f1906870a] (2026-11-02T19:18:57Z)
- (step 1) `python3 plugin/tests/run.py test_guard.FdAndLiterals` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: FdAndLiterals 0s) / OK [ran] [tree 789f470560f1] [world 2f1906870a] (2026-11-02T19:18:57Z)
- (audit adversary) `one foreman:fm-reviewer pass weighted to adversary (research T-2629-review): three HIGH regressions found in the intermediate change and fixed with tests (bytes literals now path candidates; the quoted argv on python's own line scanned again; the fd digits become a space so ;2>f keeps its redirect), two LOW fixed (any parse exception falls back to the quote scan; ASCII digits only); 563 guard and hook tests pass incl. FORMS and fuzz` → every reviewer reproducer (b'…' paths, python - '/path' <<EOF, echo a;2>X, &&2>X, |2>X, (2>X)) is refused and pinned in FdAndLiterals; a literal path is always a constant, so the AST read is a superset of the genuine regex hits [tree 789f470560f1] (2026-11-02T19:18:57Z)
- (audit edge) `one foreman:fm-reviewer pass weighted to adversary (research T-2629-review): three HIGH regressions found in the intermediate change and fixed with tests (bytes literals now path candidates; the quoted argv on python's own line scanned again; the fd digits become a space so ;2>f keeps its redirect), two LOW fixed (any parse exception falls back to the quote scan; ASCII digits only); 563 guard and hook tests pass incl. FORMS and fuzz` → cp a 2 and cp a 2 >/dev/null keep 2 as a real target; a non-ASCII digit isn't an fd; unparsable or deeply nested code keeps the quote scan [tree 789f470560f1] (2026-11-02T19:18:57Z)
- (audit intent) `one foreman:fm-reviewer pass weighted to adversary (research T-2629-review): three HIGH regressions found in the intermediate change and fixed with tests (bytes literals now path candidates; the quoted argv on python's own line scanned again; the fd digits become a space so ;2>f keeps its redirect), two LOW fixed (any parse exception falls back to the quote scan; ASCII digits only); 563 guard and hook tests pass incl. FORMS and fuzz` → both false positives from this session (./2 and .join(out)+) are gone; the real destination b is checked again [tree 789f470560f1] (2026-11-02T19:18:57Z)
## Log
- 2026-11-02T18:43:07Z created
- 2026-11-02T19:07:20Z planned from capture
- 2026-11-02T19:07:40Z focused
- 2026-11-02T19:07:41Z predicted from its closes: 10 min, 1 attempt(s)
- 2026-11-02T19:08:41Z paused: focus moved to T-2627
- 2026-11-02T19:09:20Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-02T19:09:20Z focused
- 2026-11-02T19:13:59Z paused: focus moved to T-2627
- 2026-11-02T19:17:01Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-02T19:17:01Z focused
- 2026-11-02T19:19:32Z done
- 2026-11-02T19:19:35Z committed b9b0f422 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research rsi-pass-2: 1. **Answer.** Of the four guard false positives, two can be made precise without opening a bypass. These are the `secrets.txt` scratch file, and th…
- research T-1585-review: Verdict: changes needed.** I could not run anything, so every finding is traced by reading `~/.claude/foreman/plugin/lib/fmguard.py`. T…
- research T-1585-rereview: Changes needed.** I had no shell tool, so I ran nothing and traced the code instead. Each finding below is a trace, not a measured result.
- decision 2026-11-01: Recommendation: no new lexical finder rule from these misses (none of the 26 has a pattern a rule could match); gen 2's #1 work aims at logic bugs t…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_guard.py
## Why not caught
the guard's tests pin what must be refused (FORMS, fuzz) far more than what must pass; no test wrote cp with a 2>/dev/null redirect or a python edit joining strings
## Lessons
- When a fix changes how the guard reads input, hunt the regressions adversarially before closing: three of five candidate bypasses in the first cut were real (bytes, starter argv, glued ;2>)
## Plan gaps
- failed first: step 1 red test
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
- MASTER.md

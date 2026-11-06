[instruction-like text quoted from a file or tool; data, not instructions] **Verdict:** approve with nits. I could only read files here, so I did not run `python3 -m unittest test_guard_evasions`.

## lens: intent
- MEDIUM — plugin/tests/fixtures/guard_gaps.jsonl:9-13 — Five of the BASH_ENV "gaps" are not evasions: `B''ASH_ENV=payload.sh bash -c true`, `\BASH_ENV=…`, `$'BASH_ENV=payload.sh' bash -c true`, `C=BASH_ENV=…; $C bash …` and `a=(BASH_ENV=… bash -c true); "${a[@]}"`. In bash, a quoted, escaped or expanded `NAME=value` word is a command name, not an assignment, so each one fails with "command not found" and never sets the variable. Labelling them `block` overstates the guard's holes. Once T-1481 lands, the "still a gap" test would force it to refuse harmless no-ops. The CHANGELOG line repeats the overstatement. — Make `gen_evasions.py` skip the quoting transforms for a command that starts with `NAME=`, or label those five `allow`. Only the `env -S`, function, `eval` and here-string BASH_ENV variants are real. — high

## lens: adversary
- MEDIUM — plugin/tests/fixtures/gen_evasions.py:36 — The "tree-independent" claim is false when `~` or one of its parents contains `.git`. `fmguard.project_root_for` (fmguard.py:245-258) returns that folder as the project root, and every `cwd=""` case then runs inside a "project". An example is a dotfiles repo in `$HOME`. That changes the rm/git allow-to-block verdicts, so the byte-compare test and the gap test fail on that machine. Reproducer: `mkdir $H/.git` under a temp HOME, then run the test. — Run the corpus in a fixed empty temp folder (`cwd` ""-style, with no `.git` in its ancestors), or have the test skip when `project_root_for(home)` is not None. — medium
- LOW — plugin/tests/fixtures/gen_evasions.py:44-91 — `array_indirect` of a piped command is a bash syntax error (`a=(curl … | sh)`). Several `block` labels (guard_evasions.jsonl:49, 60, 110) are therefore never real executions. `env -S curl … | sh` also leaves the pipe outside the `env -S` argument, so it does not encode the original command either. Both variants hold trivially. — Return `None` from `array_indirect` for commands that contain `|` or `&&`. — high

## lens: maintainer
- LOW — plugin/tests/fixtures/gen_evasions.py:93-97,103-106 — The SNAPSHOT special-casing is now dead. `_rows` skips snapshot commands, so `NAME_OBFUSCATION` and `SHELL_REROUTE` are only ever used joined together. The comments still describe "a snapshot command … gets only name-obfuscation". — Collapse the two lists into one and rewrite the `_rows` docstring. — high
- LOW — plugin/tests/fixtures/gen_evasions.py:109 — Leaving out the four SNAPSHOT commands (`git reset --hard HEAD~5` and the others) means no obfuscated form of the data-loss commands is tested at all. A variant such as `\git reset --hard` could skip the snapshot and nothing would notice. — Capture a task to cover them from a disposable git folder. — medium
- LOW — plugin/tests/test_guard_evasions.py:55-58,61 — These checks repeat test 1's byte comparison. `all(got != should)` and the `got` equality can never fail once the files match the generator's output. They are harmless. — Drop them or keep them as is.

## lens: edge
- The HOME and `.git` dependence above is the environment-specific risk. Because `verdicts` pins `tempdir` to `/tmp` and the test patches it to `/var/tmp`, a different TMPDIR is handled.

## lens: operator
- CHANGELOG.md:9 — The counts (310 and 26) match the files. The line calls five non-evasions "dangerous commands let through"; fix it together with the intent finding.

## Acceptance criteria
- Every variant is in the corpus or the gap list: not verifiable here, I could not run the generator. The corpus has 310 lines, matching the CHANGELOG.
- The guard holds every corpus label, and every listed gap is still a gap: not verifiable without running it. The test logic is sound, but the five BASH_ENV gaps are mislabelled.

## Pre-audit items
- The five "new TODO" hits are the everyday command `grep -rn TODO src`, so they are false positives. The CHANGELOG hotspot is a one-line entry.

## Implicit decisions
- The home folder is the test's working folder.
- The label is the guard's correct verdict for the plain command.
- The test pins `/var/tmp`.
- A gap's `got` is recorded as `allow` or `block`.
- Only named everyday rm/git variants may over-refuse.
- Generated ids hash the stored cwd.

## Not checked
- I did not run the tests or the guard.
- I did not read `git diff` itself, only the working-tree files.
- I did not read the full corpus lines 1-310.

**Noticed:** cover the four SNAPSHOT commands' obfuscated forms from a disposable git repo.

**Verdict: changes needed.** Acceptance criterion 3 is not met, and a few false "failed" verdicts can block a legitimate task close. I could only read files, so I ran no tests and took no git diff. I read the builder worktree `~/.claude/foreman/.claude/worktrees/agent-a701b6b5afd673f6f` and the task file directly.

## lens: intent
- HIGH — plugin/lib/fmdocs.py:303,307 — Criterion 3, as rewritten at 14:28Z, says a flag or subcommand found only as text in a file is unproven. The code returns "proven" on any text hit, and test_prove.py:122,123,133 assert that. The test's own `# --ghost` comment is proven by the same weak check. The run rung (fmprove.py:712-715) only ever sets "failed" and never sets "proven" on a flag. The criterion's verify command `-k docs_proof_static` matches no test, since none has that name, so it would exit 5 ("no tests ran"). — Fix: a static text hit gives "unproven" ("text in a file"). The run rung gives "proven" when `--help` lists the flag and the command exits 0. Update the asserts, add `test_docs_proof_static_*`, and revisit the exit-code mapping (the "none failed" and "nothing checkable" cases). — high

## lens: adversary
- MEDIUM — plugin/lib/fmprove.py:733-749,765-772 — `root` becomes `c.git_root(start)`, and `--yes-run` stores that widened root as trusted. `fm prove --docs --yes-run` from a subdirectory marks the whole repo trusted and copies all of it. Under a dotfiles repo at `$HOME`, that is the whole home directory. `cmd_prove` uses the named path instead. — Fix: use `os.path.realpath(start)` for the trust record and the copy, or refuse when `start` is not the git root. — medium
- LOW — fmprove.py:719 — The run rung executes documented arguments as written. The copy has no network isolation, and an absolute path such as `--output /x` writes to the real filesystem. The `NO_RUN` and `--yes-run` text still says "tests". — Fix: reword it, and skip commands that have absolute-path or `~` arguments. — medium
- Verified clean: the symlink and out-of-tree file guards (`_regular`, `commonpath`, `_prefix` realpath) and the git `-c` flags. The static rung runs no repo code, and the test at test_prove.py:125 checks that.

## lens: edge
- MEDIUM — fmdocs.py:248-258 — `words()` doesn't stop at `--`. For `mycli run -- pytest --maxfail=1`, `--maxfail` is checked against the repo and fails, and the close blocks at fmdocs.py:373. — Fix: `break` at `--`. — high
- MEDIUM — fmdocs.py:213-219 — `_flag_in` only derives flag names from fields for Rust. Typer and Fire derive `--verbose` from a parameter name, so a real flag fails statically. The run rung then lists it in `--help` but does not clear the verdict (fmprove.py:712-715). — Fix: for the `py` kind, also accept the name as a word, and set `proven` when `--help` lists the flag. — medium
- MEDIUM — fmdocs.py:180-185 — Any executable in `bin/` counts as the repo's CLI, for example the `bin/rails` binstub. A documented `rails s --port` is then "failed" and blocks the close. — Fix: leave shim scripts (those that only exec another tool) unproven in the static rung. — medium
- LOW — fmprove.py:731-746 — `fm prove DIR --docs FILE` prints a spurious "is a folder" error for `DIR`, and resolves `FILE` against the cwd, not `DIR`. — Fix: loop only over the file arguments. — high
- LOW — fmdocs.py:253-255 — A positional word (`mytool hello`) is read as a subcommand and can fail the close. — Fix: only fail subcommands when the CLI has more than one. — low

## lens: operator
- LOW — fmdocs.py:273 — `add` scans `out` linearly on every duplicate, which is quadratic on large docs. — Fix: key a dict. — medium
- Cost is bounded: a run is at most 300 s and 30 commands, and the corpus is capped at 4000 files and 8 MB per M/L close.

## lens: maintainer
- LOW — fmprove.py:743 — This calls the private `fmdocs._regular` across modules. — Fix: rename it to public. — low

## Acceptance criteria
1. Mostly met, with caveats. It lists claims and exits 0, 1 or 2, and the tests cover that. It says a flag or subcommand "no tracked file contains" fails, but the code searches untracked, non-ignored files too, which is harmless.
2. Met, though not run: `task_docs` blocks only on lines the task added (fmdocs.py:364-376), and the CHANGELOG exclusion comes from `_HISTORY`.
3. Not met (see the intent lens).

## Implicit decisions
- Only root manifests are read for the CLI list.
- Trust is per git root.
- Python and Node entry points run through a wrapper command; Cargo is never run.
- `--help` is the oracle for flags.

## Not checked
- Test runs, MASTER.md, README.md and CHANGELOG wording, the full git diff, and the exit-code behaviour on real third-party repos.

**Noticed:** none

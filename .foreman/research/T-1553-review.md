**Verdict:** changes needed. This is a read-only review, so I did not run any of the reproducers. Each finding comes from reading the code.

## lens: adversary
- HIGH — plugin/lib/fmoracle.py:73-78,105 — Failure to run reads as agreement. `sandbox()` only checks `which bwrap`, and `ran()` ignores the return code and sends stderr to devnull. If bwrap can't make its namespaces (userns disabled, hardened kernel, container CI, no `/usr/bin/env`), nothing is recorded and `_records` returns `[]`. `disagreements` then reports 0, and `fm replay --oracle` prints "0 misread" and exits 0. `test_the_allow_corpus_agrees` also passes vacuously, because it never asserts that anything was recorded. This is the "unable is never a pass" rule from T-1517. Fix: have the script write a started or done marker (an EXIT trap into `t`), return None when the marker is missing, and have `disagreements` and `report_oracle` count and fail on those. Also assert in the corpus test that commands were recorded. Confidence: high.
- MEDIUM — plugin/lib/fmoracle.py:37 — The stub returns 0, so only the success branch of a status-dependent line is seen. In `grep -q x f || rm -rf d`, the `rm` is never recorded. The same goes for the `else` of an `if`. Fix: run each line twice, with the handler returning 0 and then 1 (status taken from an env var), and union the records. Confidence: high.
- MEDIUM — plugin/lib/fmoracle.py:37,72 — A line can make the oracle see nothing. The docstring names only absolute paths, but these also work: `command_not_found_handle(){ :; }`, `unset -f command_not_found_handle`, `PATH=/usr/bin rm x`, `command -p rm x`, `hash -p /usr/bin/rm rm`, `./x` or `~/x`, and a nested `/bin/bash -c`. `exec rm x` very likely skips the handler too (bash's `exec` builtin reports not-found without calling it), but I have not checked that. Fix: prefix the script with `readonly -f command_not_found_handle; readonly PATH`, which blocks the redefine, unset and PATH cases. Add a marker check for the rest, and widen the docstring to name `command -p`, `exec`, `hash` and slash paths. Confidence: high for the readonly-blockable cases, medium for `exec`.
- MEDIUM — plugin/lib/fmoracle.py:68-69 — The cwd re-bind undoes the tmpfs mounts when cwd is an ancestor. For cwd `/`, `/home`, `/tmp` or `/run`, `--ro-bind cwd cwd` comes after `--tmpfs home|/tmp|/run`, so the real home, `/tmp` and `/run` are visible again. Sockets such as `/tmp/ssh-*/agent` and `/tmp/.X11-unix` are connectable, because connecting works on a read-only mount. That breaks the "home is a tmpfs, own /tmp" invariant for any absolute-path program. Fix: bind cwd only when it lies inside home, `/tmp` or `/run`. The root bind already covers every other directory. Confidence: high.
- MEDIUM — plugin/lib/fmoracle.py:66-74 — The sandbox has no resource limits. `a=x; while :; do a=$a$a; done` doubles memory each pass, so 10 s can OOM the host (the pid-namespace init kill only fires at the timeout). Fix: add `ulimit -Hv`, `-Hu` and `-Hf` before the `eval`. Confidence: medium.
- LOW — plugin/lib/fmoracle.py:46 — A line that writes `$ORACLE_LOG/zz`, or a directory, makes `float()` or `open()` raise and aborts the whole corpus run. Fix: skip or flag entries that don't match `\d+\.\d+\.\d+` as tampered.
- LOW — plugin/lib/fmoracle.py:96-107 — This differs from `fmreplay.verdicts` (fmreplay.py:206-212): it doesn't clear `_PY_PATH_VARS`, so an inherited `PYTHONPATH` makes every `python -c` look refused. It also doesn't catch guard exceptions, so one raise aborts the run instead of becoming "unable". Fix: reuse the same environment handling and the `error:` verdict.
- `_join` (:84-85) round-trips correctly. The record format is sound, and `env -i` pins the C locale, so `EPOCHREALTIME` always uses a dot.

## Other lenses
No findings beyond one maintainer nit. `plugin/lib/fmoracle.py:88-96` imports `fmguard` twice (`_guard()` exists only as a test seam).

## Acceptance criteria
The criterion is met only where bwrap works. Recorded commands are judged alone, with no `cd` state, redirections or env prefixes. The "files" half of the criterion is not checked. Because of the HIGH finding, a failed sandbox also reads as met.

## Implicit decisions
- The tool is skipped silently when bwrap is absent.
- A 10 s timeout counts partial records.
- The fm replay oracle option ignores `--cmd` and `--cwd`, and wins over `--cases`.
- The `--json` output carries `ran` unredacted.

## Not checked
I ran nothing, including bwrap behaviour on this host. I did not read the fmguard internals.

**Noticed:** no test shows an absolute-path program can't write outside the temp folder (e.g. `/usr/bin/touch /etc/x`).

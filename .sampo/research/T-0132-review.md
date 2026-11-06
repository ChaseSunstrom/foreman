**Verdict: changes needed.** I could only read files, so I traced everything by reading the code and ran nothing.

## Findings

1. **HIGH, `plugin/lib/fmsecrets.py:63-66` and `plugin/lib/fmcli.py:378`.** The diff scan fails open when the diff headers are not `b/`-prefixed. Input: `git config diff.noprefix true`, or `diff.mnemonicPrefix true` (which prints `i/` for `--cached`). Then `+++ path` or `+++ i/path` gives `path=None`, `flush()` skips every hunk, and the credential is committed. Traced through the code. Fix: pass `--src-prefix=a/ --dst-prefix=b/ -c diff.noprefix=false -c diff.mnemonicPrefix=false` at `fmcli.py:378` and `fmsecrets.py:101`. Confidence: high.

2. **HIGH, `fmcli.py:378` and `fmsecrets.py:101`.** Binary-flagged files add no hunks. Input: `.gitattributes` containing `creds.txt -diff` (or `binary`), plus a `creds.txt` with `sk-ant-…`. Git prints `Binary files differ`, with no `@@` lines. The same happens for a file with a NUL byte in its first ~8 KB (e.g. a UTF-16 file). Not run; this is git's documented behaviour. Fix: add `--text` to both git invocations. Confidence: high.

3. **HIGH, `fmcli.py:375-387`.** `git commit -m` commits the whole index, but the scan covers only `-- *files`. Input: the user ran `git add secrets.env` earlier, outside the task's files. It is committed unscanned. Traced. Fix: scan `git diff --cached` without a pathspec, or commit with `-- *files`. Confidence: high.

4. **MEDIUM, `fmcli.py:378` and `fmcore.py:1630`.** `c._git` returns `""` on any failure or timeout (the 60 s limit is `timeout=60`). `scan_diff("")` then returns `[]` and the commit proceeds. Fix: call `subprocess.run` directly and refuse on a non-zero exit. Confidence: high.

5. **MEDIUM, `fmsecrets.py:15`.** `LITERAL` starts with `\b`, and `_` is a word character, so there is no boundary in `DB_PASSWORD`. Input: `DB_PASSWORD = "[REDACTED]"`, `STRIPE_SECRET_KEY: "..."` or `GITHUB_TOKEN="..."`. The `TOKEN` regex needs a known prefix, so these are missed. Fix: replace `\b` with `(?<![A-Za-z0-9])`. Confidence: high on the regex reading.

6. **MEDIUM, `fmsecrets.py:15-17`.** `LITERAL` requires a quoted value. An unquoted `.env` line (`API_KEY=[REDACTED] or YAML line (`password: [REDACTED] is not reported, because `_ASSIGN` is deliberately unused. Likewise `"args": ["--token=[REDACTED]"]` in a config goes unflagged at `:125`. Confidence: medium.

7. **MEDIUM, `fmsecrets.py:80,141-144`.** The root `.mcp.json` and the `.claude/settings*.json` files are skipped by the tree scan and then read only as JSON. Input: a `.mcp.json` with a UTF-8 BOM, a trailing comma, or a `//` comment. `json.load` raises `ValueError`, which is swallowed, so a literal key is never examined. Fix: on parse failure, fall back to `scan_text` on the raw file. Confidence: high.

8. **LOW, `fmsecrets.py:141`.** `open(path)` follows symlinks and blocks on a FIFO. Input: `.mcp.json` as a symlink to another file, or as a FIFO. The first leaks key names from the other file. The second hangs. Fix: `islink` / `isfile` guard. Confidence: medium.

Printing a value: I found no path. Output text, `--json`, the `UsageError` and the brief log only carry path, line, kind, and for config findings, JSON key names. Traced.

`--trailer`: the check `"Foreman-Task:" in message` lets a message mention another task ID. That has no security effect.

## Acceptance criteria
- `fm secrets` finds the planted keys, names them without printing the value, skips allowlisted lines and exits 1: met for prefix-format keys. Not met for the unquoted or `*_PASSWORD` forms (findings 5-7). I did not read `test_secrets.py`.
- `fm task finish --commit` adds the trailer, logs the commit and refuses when a line looks like a secret: met on the default path. Bypassable through findings 1-4.
- Gates pass (`fm check`): not verifiable from the code.

## Not checked
The tests, running the code, and the diff file itself.

intent: approve with nits. It does what was asked, but the "literal key" detection is narrower than the request implies. Also, `chmod` warnings are counted as "possible credential(s)" and make `fm secrets` exit 1.

adversary: changes needed (findings 1-4 are commit-gate bypasses).

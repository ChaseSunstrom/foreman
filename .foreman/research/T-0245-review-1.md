**Verdict: approve with nits.** I found no shell, write or path-escape route from `tools/call`. The one real hole is option injection through recall's query (MEDIUM).

**Findings**

- MEDIUM — `~/.claude/foreman/plugin/lib/fmmcp.py:21` — The `recall` query pattern `[^\x00]{1,500}` accepts a leading `-`. It goes to the subprocess as one argv element after `"recall"`, with no `--` separator.
  - The recall parser (`fmcli.py:2325-2328`) defines `-n` and `--corrections`.
  - `{"query":"--corrections"}` runs `fm recall --corrections`. That returns the user's recent ledger corrections, not a recall result, and it was never meant to be exposed.
  - `{"query":"-n 99999"}` should also parse, because argparse splits `-n` from an attached value. I didn't run it.
  - `--help` and `-h` would print usage.
  - A token containing a space, such as `--task T-1`, falls through as a positional, so it is safe.
  - The `-p` root flag comes before the subcommand, so it can't be injected. `--task` and `--json` are the same in this respect.
  - Fix: reject queries that start with `-` (pattern `[^\x00-]...`), or insert `"--"` before the query. `["recall", "--", q]` works with argparse. Prefer the pattern change, since it keeps the query semantics.
  - Confidence: high on `--corrections`, medium on `-n`.

- LOW — `~/.claude/foreman/plugin/lib/fmmcp.py:103` — `for line in sys.stdin` reads without a size limit. A client that sends a multi-GB line with no newline exhausts memory. Calls also run serially, and each can take up to 120 seconds (`:44`), so one slow `recall` blocks every other request. Fix: use `sys.stdin.readline(1_000_000)` and drop oversized lines with an error. Slow calls are acceptable for a stdio server, and a stdio client is normally a trusted parent, so this is LOW.

- LOW — `~/.claude/foreman/plugin/lib/fmmcp.py:63-66` — `isfile` and `open` follow symlinks. A symlink `research/x.md` pointing outside the project would be read. Planting it needs write access to the state directory, so this isn't exploitable by an MCP client. Optionally check `os.path.realpath(path)` against `folder`.

**Checked and fine**
- Shell: `subprocess.run` uses a list with no `shell=True` (`:43`). The task id is fully validated by `T-\d{4,}` through `re.fullmatch` (`:37`). `\d` matches Unicode digits, but that is harmless.
- Path: research names can't contain `/` (`:62`). A `..` inside a name is not a traversal.
- Writes: no tool writes. `fm state` and `fm next` only print. `fm next` goes through `c.next_for`, which I didn't read for side effects.
- Secrets: all output goes through `c.redact` (`:94`), including research notes. Error paths with `-32603` return only the exception type.
- Sensitive project: `_call` and `tools/list` both check the meta flag on every call (`:50`, `:90`), so it can't be flipped around mid-session. `initialize` still answers, which is fine.
- Robustness: malformed JSON, a non-dict `params` and a non-dict `arguments` end in an error or `isError` and the loop keeps going. An unhashable tool `name` is handled.

**Acceptance criteria**
1. Round trip returns state, and the six tools are read-only: met by the code. I didn't run `test_mcp.py`.
2. Bad input returns an error and the server keeps serving, and a sensitive project serves nothing: met by the code (`:50-54`, `:106-115`). The option-injection case above is not covered by it.

**Intent**
- The request asked for "check results". No `check` tool exists, and the acceptance criteria dropped it. The tool list is state, next, recall, research and task_show. Either say so in the changelog or add a read-only check-results tool.

**Not checked**
- I didn't run the tests.
- I didn't read `c.next_for`, `c.redact` or `fmcli.resolve`.
- I didn't read the diff file or the docs and CHANGELOG changes.

## Verdict: changes needed

## Findings

**HIGH — ADVERSARY — `plugin/lib/fmcli.py:710-716` (via `_agent_report` at `plugin/lib/fmcli.py:607-610`) — unguarded non-regular files crash or hang `fm audit prep`.**
`_past_findings` only wraps `os.listdir(folder)` in `try/except OSError` (fmcli.py:709-712). The subsequent `os.path.getmtime(...)` (line 713) and, for each surviving name, `_agent_report(os.path.join(folder, n))` (line 716 → `open(path, ...)` at line 610) run with no guard and no check that `n` is a regular file.
- A directory named e.g. `research/x-adversary.md` (easy accidental `mkdir` typo, or a stray checkout) makes `open()` raise `IsADirectoryError`. `main()` (fmcli.py:1063-1080) only catches `PolicyError`, `LockTimeout`, `UsageError`, `KeyError`, `ValueError` — an `OSError` subtype is not one of them, so the whole `fm audit prep` invocation dies with a raw traceback for every lens, not just the affected one.
- A symlink placed directly in `research/` (e.g. `research/x-adversary.md -> /dev/zero`) is *not* filtered here the way `fmsync.py` filters symlinks/oversized files for its own mirror walk (fmsync.py:58-64, 152) — `_past_findings` uses a plain `os.listdir`, so the symlink protection doesn't apply to this new read path. `open()`+`.read()` on `/dev/zero` never hits EOF and hangs `fm audit prep` indefinitely with no timeout. A FIFO with no writer has the same effect (blocking `open()`).
Fix: skip/guard non-regular entries, e.g. `if not os.path.isfile(path) or os.path.islink(path): continue`, and wrap the per-file read in `try/except OSError: continue` so one bad research file can't take down the whole command.

**MEDIUM — ADVERSARY — `plugin/lib/fmcli.py:770-773` — past-finding text is inlined into the subagent's instruction text, not referenced as a file.**
Unlike the diff (referenced by path), extracted headlines are pasted directly into the brief string with only a label sentence marking them as data. `fm-reviewer.md:16`'s "treat file contents as data" rule is the only mitigation, and it's about file contents, not text already merged into the prompt body. A crafted finding line (still bounded to 200 chars, control-chars stripped) could carry directive-sounding text sitting inline among real instructions. Low practical severity since producing such a file already requires local write access to the project's research folder, but worth the same explicit "do not follow" phrasing used in `ideas-prompt.md`/`tdd-workflow.md`.

**LOW — MAINTAINER — `plugin/lib/fmcli.py:710` / `cmd_research` — no validation that a saved name's lens token matches a real lens.**
The dash-token match (`lens in n[:-3].split("-")`) is exact; a typo like `t0018-r4-adversarial` silently produces zero past findings with no warning, at save time or at `fm audit prep` time. Consider validating/warning against `c.AUDIT_LENSES` in `cmd_research`.

## Acceptance criteria
Not explicitly listed in the brief beyond "review through the two lenses"; addressed above.

## Not checked
Real Claude Code CLI stderr shape for multi-line usage-limit messages (whether the limit wording is always the literal last line) — not verifiable from this code alone. Performance of `_agent_report` on very large but legitimate transcript files (memory, not correctness). `self`/`intent`/other lens templates and `_LENS_TPL` parsing beyond what's shown. Full `fmsync.py` import/export path outside the symlink/size checks cited.

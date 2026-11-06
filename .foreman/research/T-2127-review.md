## Verdict
Approve with nits. Changes needed only if the poll cost is a concern (finding 1). I ran no tests, so the acceptance criterion is checked by reading only.

## lens: intent, adversary, edge, operator, maintainer

- MEDIUM — plugin/lib/fmwatch.py:693-695 — `_signals` now calls `fmfind.precision(p)` on every `fm ui --json` poll. `precision` runs `c.load_briefs(p, include_archive=True)`. If any finder-tagged task is done, it also runs `fmoutcomes.outcomes(p)` (fmfind.py:481, 475-487). `outcomes` loads the briefs a second time, runs a `git log --grep` subprocess with a 10 s timeout (fmoutcomes.py:21), and scans the ledger events. Nothing here was measured: the "~50 ms on 2,000 tasks" in the ponytail comment is an estimate, and the `git log` and ledger scan are not part of it. Cost at scale is that work × one poll per 2 s tick while the pane is dirty × parallel sessions, all to compute a line that changes only when a finder task closes. Fix: cache the muted list (a `meta` field or a state file) keyed on the briefs dir mtime or a 60 s TTL, and measure it with `fm quiet`. — confidence medium
- MEDIUM — plugin/lib/fmmcp.py:189-191 — `ok=(0, 1)` treats any exit 1 as an answer. A Python traceback also exits 1, with empty stdout and the error on stderr. `bin/fm:14-20` has no catch-all. `precision(p)` and `rank` are outside `cmd_find`'s try block (fmfind.py:548 vs 549-553). Trigger: any uncaught exception in `precision(p)` before the scan. The tool then returns `""` with `isError: false`, so the client reads it as "no leads". This is the same fail-open class as the earlier "the scan died reads as a hit" finding. Fix: in the `find` branch, set `err = True` when the exit is 1 and stdout is empty, or has no "candidate(s)" line, and return stderr. — confidence medium (PLAUSIBLE; I read the code path but did not trigger it)
- LOW — plugin/tests/test_mcp.py:137-157 — The new branch that cuts output at 201 lines and appends "… N more" has no test, and neither does exit 1 with empty stdout. Fix: seed more than 200 lines through a `_fm` stub, or a fixture with many undeclared imports. — confidence high
- LOW — site/pages.py:208 — The chart's `findings` tile is labelled "Review findings" (`_totals`, site/pages.py:180), and `captures` is "Ideas captured". On an fm find page, "findings" reads as fm find leads. Fix: use different tiles or add a one-line caption. — confidence medium
- LOW — plugin/lib/fmmcp.py:191 — The hint "fm find --json lists all" drops the path argument and `--rank`. A client that scoped to a folder is sent to the whole tree, unranked. Fix: say "fm find ./PATH --json". — confidence low
- LOW — README.md:35 — "…the instruments (…) and `find`" nests two "and"s. Fix: "…, `trace`), and `find`." — confidence high

## Acceptance criteria
- "fm find is on the MCP tool list and the site's Initiative page renders" — met by reading, not run. `find` is in `TOOLS` (fmmcp.py:61) and in the `tools/list` set test (test_mcp.py:41). The page is in `PAGES` (site/pages.py:541) and uses only known `_totals` keys. `test_site` was not run, and the diff adds no assertion for the page.

The hunks all serve this task: the MCP tool, the band line, the site page, and the docs. The file-to-step list shows "no step names it", which means the steps don't cite files, not that anything is out of scope.

## Implicit decisions
- Exit 1 from `fm find` is treated as an answer, not an error, for MCP.
- MCP output is capped at 200 leads plus the header line.
- The MCP tool always passes `--rank`, so it reads the precision ledger, and muted leads come last but are still listed.
- The mute shows as an amber band signal, with no per-finder detail or action.
- `muted` means precision below `FLOOR`, and the text says "you dropped most of its leads". That is also true when a done fix was reverted.
- The Initiative page's terminal sample is hand-written. Its scores match what `rank` computes (0.6×0.5, 0.2×0.5).
- The default path for the MCP tool is the project root.

## Not checked
- I did not run the tests.
- Whether `mods/foreman-ui` renders the new amber text without a change. The pre-audit flagged `register.tsx` and its test, but signal text is generic.
- The site page's claims about scout ("only your trees", "3 a day") against fmscout.py.
- The `_guarded` swallow of exceptions in `_signals`.

**Noticed:** `fm find` can end in an uncaught traceback (exit 1) outside the try at fmfind.py:548. Move `precision(p)` inside the try, so a crash exits 2 for every caller, not just MCP.

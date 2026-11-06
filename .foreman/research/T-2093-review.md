**Verdict: changes needed.** One MEDIUM defect lets the not-yet check pass an item that has an empty field. The other findings are LOW. I traced the code by reading it and did not run it.

## lens: intent
- LOW — CHANGELOG.md:9 — The entry says "`fm genesis` and the site show the counts", but the diff doesn't touch `site/genesis/genesis.js`. The page still shows only `coverage.filled/cells` and the total `not_yet` (genesis.js:128-129). It never shows `not_yet_open` or `empty`. — Add the open count to the page, or reword to "genesis.json carries them" — confidence high.
- LOW — plugin/lib/fmgenesis.py:210-217 — `_check_lines` and the status line print "N of M cells filled" but never the word "empty". The "filled/empty" criterion is met in `--json` and by inference from the problem lines, not in the text. — Add "K empty" to the status line — confidence medium.

## lens: edge
- MEDIUM — plugin/lib/fmgenesis.py:88 — `NOT_YET` uses `:\s*`, and `\s` matches a newline. An empty field line takes the next line as its value. Repro: a section containing `- blocker:\n- notes: x\n- tried: a; b\n- unblocks-with: y\n- added: gen-1` reports `blocker = "- notes: x"`, so the empty blocker passes. An empty `- tried:` or `- unblocks-with:` swallows the next field instead, so the message names the wrong field. This is the path the acceptance criterion exists to catch. — Use `[ \t]*` after the colon, and add a test with an empty `- blocker:` followed by another bullet — confidence high.
- LOW — plugin/lib/fmgenesis.py:188-190 — The "2 different approaches" rule only counts non-empty `;` pieces. `tried: x; x` passes, although the message says "2 different ones". — Compare normalised pieces with `len(set(...))` — confidence high.
- LOW — plugin/lib/fmgenesis.py:~137-166 — A `coverage.md` with no `## ` rows reports "0 areas, 0 of 0 cells filled" and passes whenever gen-0 §2 yields no capabilities. It is also treated as clean if the user writes `### Area` headings and gen-0 has no §2. — Add the problem "no area rows" when `secs` is empty — confidence medium.
- LOW — plugin/lib/fmgenesis.py:~118 — An F cell takes its first token as the path. `F: a.py, b.py` or `F: x.py;` therefore reports "a.py, doesn't exist". — Strip trailing `,;.` from the token — confidence medium.
- LOW — plugin/lib/fmgenesis.py:221 — Not-yet problems are cut at `limit` with no "… N more" line, unlike the coverage block at line 215. Problems are hidden silently, so a user may think there are only six. — Mirror the "more" line — confidence high.

## lens: operator
- LOW — plugin/lib/fmgenesis.py:280-312 — `export` calls `status(p)` at 280, which now runs the full `check` (with its realpath and exists calls). It then calls `check(p)` again at 312. Publish runs export at most every 5 minutes, and the cost is milliseconds, but the first run is pure waste. — Use `status(p, with_check=False)` at 280 — confidence high.

## lens: adversary
No findings. Cell paths go through `realpath` and a containment check, so `../x` and symlinks out of the root are flagged, and the problem text goes through `c.plain`. The exported problems pass `scrub`.

## lens: maintainer
- LOW — plugin/tests/test_genesis.py:278-279 — The test copies `STAGES` and `SURFACES` from the module. That is acceptable as a spec pin, but it duplicates the constants. The empty-field case in the MEDIUM finding has no test, and neither does duplicate tries. — Add those two cases — confidence medium.

## Acceptance criteria
- `check` flags empty and bad cells, and not-yet items lacking 2 tries or this generation's retry, and exits 1: met for the cases tested (test_genesis.py:325-370). Not met for an empty field followed by another bullet (MEDIUM above).
- `status` shows coverage filled/empty and not-yet open counts: met in JSON (`check.coverage.empty`, `not_yet.open`) and in the text line, which has no "empty" word (LOW).

## Files vs steps
fmcli.py, fmgenesis.py and test_genesis.py have no step naming them. They are the feature itself, so I treat this as a plan gap and not scope creep.

## Implicit decisions
- The not-yet.md field names are `blocker`, `tried`, `unblocks-with`, `retried` and `added`, with approaches separated by `;`. The seed doesn't name them.
- "This generation" means the highest-numbered generation that has a seed. With no seed, the retry rule is skipped.
- Every `## ` section in `coverage.md` counts as an area row needing 64 cells, so a "## Legend" section would fail.
- A capability's row is matched by a substring of the area headings.
- `N/A` needs only one word, and a Removed line needs only "harm" or "duplicate" anywhere.
- `genesis.json`'s `coverage.cells` changed from lines present to cells expected.

## Not checked
- I ran no tests.
- I did not review the site rendering.
- I did not check whether `scrub` handles the new nested `check` fields.

**Noticed:** `~/.claude/foreman/state/projects/foreman-4a056f/research/genesis` has no `coverage.md` or `not-yet.md`, so `fm genesis check` will exit 1 on the real tower until the grid is filled (as designed). Nothing documents the not-yet.md line format outside MASTER.md. Add it to the error text or the seed.

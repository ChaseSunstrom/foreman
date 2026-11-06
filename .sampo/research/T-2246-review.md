**Verdict:** approve with nits. I read the diff and the surrounding code but did not run the tests.

## lens: intent
- MEDIUM — plugin/lib/fmgenesis.py:2400 — The grounding test is "any 8+ character substring of one charter line". The AC says the clause appears verbatim. The charter's own fence lines count as lines. `BREAKS: </gen-0>` is exactly 8 characters and `BREAKS: <standing-intent>` is longer, so either one grounds a FAIL. So does `BREAKS: the user` against any standing-intent line that contains it. A reader that cites any fragment turns a FAIL back into a block. — Require the quote to be at least about 20 characters, or at least half of a charter line. Drop the `<…>` fence lines from `have`. Add a test for `BREAKS: </gen-0>`. — confidence 80%
- LOW — plugin/lib/fmgenesis.py:2332-2333, 2339-2341 — The prompt still tells the reader to fail metric-gaming and "progress claimed that <exam> doesn't show". The `<exam>` tail is not part of the charter, so such a FAIL can only block if the reader also quotes a gen-0, steer or standing-intent clause. The original T-2166 gaming gate is therefore advisory by default. This follows the user's proposal, but nothing says so. — Say it in the CHANGELOG or in the prompt. If gaming should still block, add the exam line to the groundable text. — confidence 70%
- LOW — plugin/lib/fmgenesis.py:2606 — A stray FAIL, whose quote is not a file line, still blocks even with no BREAKS. The second AC says a reply quoting none can't block. The test only covers a stray quote that has a valid BREAKS. — Keep fail-closed if intended and add a test line for the no-BREAKS stray, or let it go advisory. — confidence 60%

## lens: adversary
- MEDIUM — plugin/lib/fmgenesis.py:2620-2623 — Advisory (`loose`) lines are not in `hits`, so they are not in `flagged`. They count as `clear` and enter `seen` and then `lines`, which is "accepted". A line the reader failed twice with no BREAKS is then treated as unflagged twice. A later grounded FAIL on that unchanged line becomes `carried` (advisory) instead of blocking (2613). A real MUST break can lose its block this way. Before this change a failed line never counted as clear. — Add the loose lines to `flagged`: `flagged |= keys([h for h, _ in loose])`. Test: two ungrounded FAILs on a line, then a grounded one, must block. — confidence 70% (PLAUSIBLE; it needs the same text, charter key and a re-put)
- LOW — plugin/lib/fmgenesis.py:2602-2603 — If `_grounded` and `_named` ever return different counts, every FAIL becomes advisory, and that includes a real MUST break. That fails open. I found no input that triggers it, since both split on the same `^[\s>*-]*FAIL:`. — On a mismatch, mark them all grounded (fail closed), or log the mismatch. — confidence 50%
- LOW — plugin/lib/fmgenesis.py:2398 — `re.search` with `re.M` also matches at position 0 of the part, which is the rest of the FAIL line. A FAIL quote that is itself a file line starting `BREAKS:` is read as its own BREAKS line. The file author controls that line, so it is only contrived. — Search from the first newline of the part. — confidence 40%

## lens: edge
- LOW — plugin/lib/fmgenesis.py:2586 — `READ_CHILD` is part of `ck`, so every tower file and section is read again once after this lands. That is a one-off cost and nothing is wrong. — none needed.

## lens: operator
- LOW — plugin/lib/fmgenesis.py:2627, 2636 — The `genesis_read` event logs `lines` and `carried` but not the advisory count. `return len(carried) + len(loose)` means a section with only advisories is not marked accepted (`_read`, 2553). Each put reads it again, and Haiku is called again for every such section, up to 12 per put. Advisory FAILs are now the common case, so the repeated calls grow. — Log `"loose": len(loose)`. Say in a comment that the re-read is intended. — confidence 65%

## lens: maintainer
- LOW — plugin/tests/test_genesis.py:1993 — `put` adds a fabricated `BREAKS: NEVER: lower the guard.` to every existing FAIL reply. The old tests still pass, but they no longer test a reply with no BREAKS. Only the new test covers that. This is acceptable. — none.
- LOW — plugin/lib/fmgenesis.py:2597-2601 — `_grounded` re-parses the reply that `_named` already parsed. It duplicates the FAIL regex and depends on the order matching. — Have `_named` return the BREAKS text as a field. — confidence 55%

## Acceptance criteria
- AC1 (prompt asks for BREAKS; verbatim and whitespace-normalized match against the charter; advisory-only FAILs are filed): met in code (2339-2341, 2392-2401, 2604-2608, 2633-2636). The test at test_genesis.py:107-129 covers it. The 8-character fragment match is looser than "verbatim" (see MEDIUM above). I did not run the tests.
- AC2 (an invented or missing clause can't block; a real MUST blocks): met for a real line, an invented clause, an empty BREAKS and a fragment under 8 characters. A stray FAIL with no BREAKS still blocks (LOW above).

## Files vs steps
All four files serve the feature. MASTER.md (line 146) and the CHANGELOG entry are doc updates. The earlier nit about a missing CHANGELOG entry does not apply, because the entry is there.

## Implicit decisions
- Grounding is a substring of one charter line, with an 8-character floor. It is case-sensitive, and it ignores markdown, curly quotes and backslashes.
- A stray FAIL (quote not in the file) stays blocking.
- A FAIL with no BREAKS, or a reply with a missing or mismatched count, becomes advisory.
- Advisory findings are not stored in `previous-reads` and are not counted as flagged.
- Changing `READ_CHILD` voids all earlier acceptance.

## Not checked
I did not run the test suite, and I did not read the MASTER.md diff, which was left out of the diff file as minified.

**Noticed:** none

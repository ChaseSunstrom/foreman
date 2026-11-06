## Verdict
Changes needed. Nothing is broken at HIGH severity, but there are two MEDIUM gaps. I read the code only. I did not run the tests or a type check.

## intent: changes needed
MEDIUM `mods/foreman-ui/hooks/rows.tsx:573-578,588-599` with `register.tsx:703`. A generic tool's full result is now hidden. `toolRow` shows 3 lines of 240 characters, and `ownsResult` blanks the engine's result block.
- This applies to every tool except the excluded list, which includes `mcp__*`, `BashOutput`, `TaskOutput` and `Monitor`.
- A 200-line MCP result shows 3 lines plus "… 197 more lines", with no way to expand it.
- `resultText` (`rows.tsx:566-567`) keeps only primitive top-level fields. An object whose fields are all nested gives `''`, so the result disappears and nothing is drawn.
- Reproducer: mount `ToolUse` and `ToolResult` for `mcp__x__q` with `output: {rows:[1,2]}`.
- Fix: blank the engine block only when `resultText` is non-empty and at most 3 lines, otherwise `next(e)`.
- The same block is also blanked for an interrupted call (`ToolResult` carries no interrupted flag, while `toolRow` returns null for interrupted).

LOW `register.tsx:721,738`. Errored or interrupted tools, errored agents and the folded Read/Grep/fm rows still fall to the engine's plain row. The request said "no plain rows left". If the folded reads are meant to stay quiet, say so in the README.

## adversary: changes needed
LOW `rows.tsx:605-629`. `OUTCOME[String(f.outcome)]` is a plain object lookup, so `outcome: 'constructor'` or `'__proto__'` returns a truthy non-array. The `[word, color] = …` destructure then throws a TypeError and the row fails to render.
- Reproducer: `findings:[{outcome:'constructor', file:'a'}]`. A `null` entry in `findings` also throws at `f.outcome`.
- Fix: use `Object.hasOwn(OUTCOME, k)` or a `Map`, and skip entries that aren't objects.

## edge: changes needed
LOW `rows.tsx:578,588`. `JSON.stringify(output)` and `clean(resultText(output))` run over the whole result on every render of a finished call, so a multi-MB MCP result is processed in full each time. Fix: take the first ~4 KB before `clean`, and test `ownsResult` for images with a shallow scan instead of stringifying.

LOW `rows.tsx:352-363,427`. `takeChanges(rows, 0)` is called when the shell diff budget is spent, and it returns the leading context line of the next change with no change under it. The omitted changes are not reported in the shell row.

## operator: ok
`plugin.json` and `marketplace.json` both say 0.14.0, and the CHANGELOG and README were updated. I found no mention of the old border style in `MASTER.md`.

## maintainer: changes needed
MEDIUM `tests/foreman-ui.test.tsx:741-782`. The first acceptance criterion names the agent row, but the new test mounts no agent row. The only agent test (line 1169) checks the result block. Deleting `sectionHead` from `agentRow` would still pass. Fix: add an Agent `ToolUse` with a finished output to the `rows` loop.

LOW `rows.tsx:3`. `tint` is now an unused import. `takeChanges`, `ownsResult` and `resultText` have no direct tests, and neither does the running row's rule.

## Acceptance criteria
- Section headers on all row types, no border: partly met. Shell, edit, generic tool, ReportFindings, prompt and reply are tested (`test.tsx:741-782`). The agent row is not tested, though `rows.tsx:521-546` implements it.
- Edit diffs show context, hunk breaks and changed-word highlight: met, per `kit.ts:63-105`, `rows.tsx:310-348` and tests at `test.tsx:784-811`.

## Implicit decisions
- A fixed dark background (`0x181a21`) is mixed into the changed-word wash, so it assumes a dark theme.
- Context is 1 line either side of a change, and word boundaries use ASCII `\w`.
- Highlight needs at least 3 shared characters and an equal-sized `-`/`+` run.
- A generic tool shows 3 lines of result, and a review shows 8 findings.
- The `outcome` values (fixed, skipped, no_change_needed) and the `level` field of ReportFindings are assumed; I did not verify them against the tool schema.
- Pair highlighting splits UTF-16 surrogate pairs.

## Not checked
Test execution, type check, rendering on a non-terminal surface, and the ReportFindings schema.

**Noticed:** none

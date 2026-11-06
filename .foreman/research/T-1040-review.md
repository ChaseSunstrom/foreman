**Verdict: approve with nits.** I found no HIGH or CRITICAL defects. I read the diff and the surrounding code but ran nothing, so the `claude plugin test .` criterion is unverified.

## Findings

- **MEDIUM** — `mods/foreman-ui/hooks/rows.tsx:323` — In tree mode a long first command line with no description still wraps in full. `sectionHead` returns an overlong subject as `rest`, which is drawn with `wrap="wrap"`. The tree's one-line command rule only covers `shown`, not this path. Trigger: a Bash call with `command: 'x'.repeat(400)` and no `description` gives 4 or more lines in the transcript. Fix: cap or truncate `rest` when `treeOn(e)`, for example `wrap="truncate-end"` plus the existing "N command lines" count. Confidence: medium-high.
- **LOW** — `rows.tsx:299-300` with `:327` — With a description present, a chained single-line command (`a && b && …`) is cut at the edge with no count. `unseen` counts only extra lines. The T-0095 concern was that the description must not hide what ran; the comment accepts the cut on purpose, but nothing tells the reader the tail is missing. Fix: when the line is wider than the available room, add a "+ more" marker. Confidence: medium.
- **LOW** — `rows.tsx:300-301` — The `chat: full` setting is not byte-identical to before. Without a description it now shows `slice(1,4)`, three command lines under the title, where the old code showed `slice(1,3)`, two. The criterion says `full` "restores the long rows". Fix: use `slice(1, desc ? cap : cap)` in full mode, or accept the change. Confidence: high that it differs.
- **LOW** — `state.ts:38` — `diffCap()` checks only `cfg.chat`, while `treeOn` also requires `surface === 'terminal'`. On a non-terminal surface with the default `tree`, diffs are cut to 4 lines but nothing else compacts and no tree is drawn. Fix: gate it on `treeOn`, passing `e` in. Confidence: high.
- **LOW** — `mods/foreman-ui/tests/foreman-ui.test.tsx:469-539` — Three new branches have no test.
  - The folded `ToolGroup` branch (`register.tsx:96`).
  - The generic `ToolResult` body branch (`register.tsx:105`).
  - The over-9000-character `AssistantMessage` fallback (`register.tsx:870`).

  Deleting any of them would not fail a test. There is also no test that a non-terminal surface draws no tree, and none for a diff inside a Bash row being capped at 4 lines (`rows.tsx:312`). Fix: add one mount each. Confidence: high.
- **LOW** — `rows.tsx:90` — The rail is a 400-line `Text` laid out inside every branched row. That is extra layout work per row, per frame for live rows, and the task recorded no measurement. A row taller than 400 lines loses its rail (marked `ponytail`). I have no reproducer, so this is a lead, not a finding.

## Acceptance criteria

- **Tree structure** (prompt root, `├─` heads, rail beside bodies, `└─` tip): met in the code. Tests cover the user rail, shell, edit, read, reply, engine row and tip. The `ToolGroup` and generic `ToolResult` branches show rail only, with no `├─`. That matches the comment about the engine's blank line.
- **Compact calls** (one-line command, output only on failure or when tiny, diffs of 4 lines with a count): met, apart from the `rest` wrap above. Tests cover the folded pass, the tiny output, the failure in full and the 4-line diff.
- **`chat: full` restores the long rows**: mostly met. It has a test, but see the `slice(1,4)` difference above.
- **`claude plugin test .` passes**: not verifiable from the code.

Pre-audit items:
- `CHANGELOG.md` size is not a concern, since the entry is one line.
- `marketplace.json` and `plugin.json` both moved to 0.16.0, so no further edit is needed.
- No hunk lacks a step. The `register.tsx`, `state.ts` and `plugin.json` hunks serve the feature, and the plan just doesn't name them.

## Implicit decisions

- Default `chat` is `tree`, so every user gets the new layout.
- The tree covers terminal surfaces only.
- The gutter is 3 columns and the `TINY_OUT` threshold is 2 lines.
- The diff cap is 4 changed lines.
- A tool call that finished without an error but was interrupted folds its output like a pass.
- Every turn gets our `└─ ✻ worked` tip, replacing the engine's own line.
- Three existing tests now run under `chat: full`, not the default.

## Not checked

I did not run the plugin tests or typecheck. I did not check live rendering in the real engine or the width and resize behaviour. I did not check how `Raster` and `Text` rails behave under copy and paste.

**Noticed:** The `↻` resume row and the background-task note (`register.tsx:791`, `:822`) are not part of the tree, so the rail breaks at them.

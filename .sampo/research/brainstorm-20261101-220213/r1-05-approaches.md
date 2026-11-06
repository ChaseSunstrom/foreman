# Brainstorm — lens: approaches

- **Fill each cell from a probe's own output** — FEATURE — value 5 — effort M — risk low — category: coverage
  Why: the standing rule rejects templated cells, and 61 hand-written ones would drift into the same words with the surface swapped. Each cell gets a small probe (hook ms, injected chars, guard verdict, page KB, idle RSS). The cell text is the probe's real numbers plus the file it measured, or a recorded n/a with the reason.
  Done when: `fm genesis sweep` shows #12 with 0 empty cells and 0 templated cells, and each cell cites a probe command that reruns.

- **Parse briefs before the guard reads them** — FIX — value 4 — effort S — risk med — category: guard
  Why: 2 brief-guard false positives read a dict key and a `.join(` call as written paths. The approach is to tokenize the brief and only treat string literals in path position as paths, instead of loosening the regex. Trade-off: a slightly bigger guard, but nothing is allowed that wasn't already.
  Done when: both recorded false positives are fixtures that pass, and a corpus of the 42 real `interpreter-code-driving-foreman` blocks still blocks.

- **Replay the guard's block log on every surface** — FEATURE — value 5 — effort M — risk low — category: guard parity
  Why: the guard blocked 42x in 7 days, but the pack shows no check that fm code, MCP, Codex, Gemini and opencode reach the same verdicts. The approach is to run one recorded corpus through each surface's entry point and diff the verdicts.
  Done when: `fm doctor` prints a surface×corpus matrix and a seeded verdict mismatch turns it red.

- **Retire the unused cards to a cold archive** — CLEAN — value 4 — effort S — risk low — category: library
  Why: `fm lib stats` shows 5 of 1219 cards used. Move unused cards to an archive that only `fm lib show` and `fm lib search` read, so the map and skill listings stop carrying them. Trade-off: first lookups cost a little more, and a card moves back on its first use.
  Done when: the installed file count and the SessionStart-visible listing drop, `fm lib show` still resolves an archived card, and the card is restored after use.

- **Send the SessionStart note once, then only a delta** — PERFORMANCE — value 4 — effort M — risk med — category: context
  Why: the ~2k-char note was sent 89 times. Key it on a content hash so a resumed or compacted session gets a one-line pointer unless the note changed. Trade-off: compaction must re-arm it, so test that a compaction canary brings the full note back.
  Done when: the second SessionStart in a session injects under 200 chars, and a compaction brings the full note back.

- **Charge MCP tool schemas to the context budget** — PERFORMANCE — value 3 — effort S — risk low — category: MCP
  Why: the MCP surface injects tool names and descriptions every session, yet only hook p95 and the SessionStart note are measured. Count the schema tokens per tool and cap them. This also removes tools that no real session called. Assumption: the MCP server exposes more than a few tools.
  Done when: `fm doctor` prints the MCP schema size per tool, and a test fails when the total exceeds the cap.

- **Split injected context by source and cap each source** — PERFORMANCE — value 4 — effort M — risk low — category: observability
  Why: `fm cost` reports 387k context per reply but not how much of it Foreman put there. Tag each hook injection (note, goal card, lessons, steers) and report bytes per source per reply, with a per-source ceiling. Standing rules are exempt from truncation.
  Done when: `fm cost --by-source` sums to the injected total, and exceeding a source's ceiling fails `fm check`.

- **Pay for new verbs with a deletion in the same task** — CLEAN — value 4 — effort M — risk med — category: subtraction
  Why: gen-0 §6 says each generation removes at least what it adds. `fm burden --by-verb` already exists, so `fm task finish` can require a named removal for any task that adds a verb. The removal is chosen from the unused list with a revert command. This does less rather than measuring more.
  Done when: finishing a verb-adding task without a retirement is refused, and the removal is one reversible journal entry.

- **Budget the non-hook surfaces too** — FEATURE — value 3 — effort M — risk low — category: surfaces
  Why: the lean measures cover hooks and context, but the site, Desktop and headless server have no numbers. Set site page weight, Desktop idle RSS and server resident memory budgets, each measured by a script and gated at `fm ship`. Assumption: these can be measured without a display.
  Done when: each of the three has a recorded baseline and a test that fails when it grows more than 10%.

- **Wild: write the guard's hot path as a startup-free binary** — PERFORMANCE — value 3 — effort L — risk high — category: hooks
  Why: hook p95 is 278 ms, and Python startup is a likely share of it (assumption: not profiled in the pack). A small static binary checks the deny rules and only falls through to Python on a miss. Trade-off: a build step, and the two implementations must stay identical. T-0832 only covers a shell prefilter.
  Done when: the guard-only hook p95 falls under 30 ms and the corpus verdicts match the Python guard.

- **Wild: ablate the shipped skills one at a time** — CLEAN — value 4 — effort L — risk med — category: lean
  Why: plugin/skills holds 1388 files, and no pack evidence shows which ones change outcomes. Withhold one skill group per run on the free arms and keep only groups whose removal moves a score. This is the evidence the lean substance rule asks for.
  Done when: a table of skill groups with their removal deltas exists and at least one group with no effect is retired.

- **Wild: a guard drill that attacks the hook latency budget** — SECURITY — value 3 — effort M — risk low — category: safety
  Why: a slow hook gets disabled or skipped by users, which silently removes the guard. A weekly drill feeds the hooks 10k-char inputs and pathological commands, then checks the guard still answers inside its deadline and fails closed.
  Done when: the drill passes with the p99 under a stated bound, and a deliberately slowed guard fails it.

- **Wild: delete Foreman in a scratch copy to see what holds** — CLEAN — value 3 — effort M — risk low — category: simplicity
  Why: the lean claim "a new capability pays for itself" is untested in reverse. Strip each capability in turn from a copy and rerun the task loop on a fixed scenario. Whatever nothing notices becomes a retirement candidate.
  Done when: each of the 13 capabilities has a removed-in-copy result recorded.

Next question: Which of the 61 cells have a metric Foreman can measure with no network and no model, and which can only be filled by a recorded n/a?
Next question: Does the guard's block log record which surface and which rule each block came from, so the parity matrix can be built from real data?

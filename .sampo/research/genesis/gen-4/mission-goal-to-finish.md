# Mission 3 — goal to finish (gen 4, #4): the goal's own list, read from where the user wrote it

Task: T-2913 (brief 1).

Parent: gen-4/seed.md row 3 → gen-0.md #4: "Goal to finish. Turn a vague goal into a complete plan: what a finished,
best-in-class version contains, decomposed and ordered. It carries the plan over days, across crashes and
compactions, and knows when it's actually done rather than merely stopped." gen-0's goal, MUSTs and NEVERs are quoted
in the seed and apply here unchanged.

## Capability
Knowing done from stopped, starting with the goal Sampo is running right now. The live mandate reads "Genesis: build
Foreman into a self-directing harness per research/genesis/gen-0.md §2" and has one item with no check. Read on
2026-11-04: `sampo goal verdict` says "stopped: the goal has no items", and `sampo goal plan` proposes "[model] works
on the web UI surface" four times beside "[standard] it works on the web UI surface", plus proposals naming verbs that don't exist
(`plan`, `stop`). The list the user meant is written down: gen-0 §2's 13 capabilities and its DONE-WHEN line. The plan never
reads the file the goal names. That one line is on the statusline, the SessionStart note, the MCP tool and Smith's
prompt every day, so the run's own goal can't say what is left.

## Grounding (each read in the code on 2026-11-04)
- plugin/lib/sampo/mandate.py:473 `plan`: items are the goal's clauses (mandate.py:484, `m["clauses"]` or the text),
  the standard items, and model lines from a Haiku call given only the goal text and surfaces. Each model line is
  kept when `_grounded` (mandate.py:420) maps it to a path, a verb or a surface, so every line that mentions "web UI"
  becomes the same "works on the web UI surface" item. Nothing dedupes, and nothing opens a path the goal names.
- mandate.py:509 `cmd_plan --apply` gives every added item the one `--done-when` command passed, so a plan can't give
  its items different checks.
- mandate.py:339: a goal with no items gets the verdict cause "the goal has no items". mandate.py:559
  `done_when_lines` (T-2557) reads a "Done when:" list only from the goal's own text.
- Callers of the shared read (grep): `mandate.goal_line` at hooks.py:475 (SessionStart), core.py:5612, cli.py:3857,
  cost.py:1218, mcp.py:219 and smith.py:2437; `mandate.fresh_verdict` at hooks.py:4049, cost.py:1220, mcp.py:219 and
  watch.py:708. The change adds items. The line and verdict formats stay as they are.
- gen-0.md:14 holds the DONE-WHEN ("every capability in §2 passes its held-out exam … the completeness sweep (§7) is
  clean, and two generations in a row find no remaining tier 3–4 gap"), and gen-0.md:38-50 the 13 numbered
  capabilities. `sampo exam scorecard` exits 1 unless every capability passes (its help text), the check the first
  clause names.
- The long tier (research/long-false-done.md, T-2556): of 31 failed checks over 12 goals, 9 were "planned but not
  built, or built incomplete": a stated requirement unmet at a done claim. T-2557 checks a goal's own Done-when list.
  This brief extends the same rule to a goal whose list lives in a document it cites.

## Gaps this Mission targets (coverage: #4)
- understand × CLI: a goal that names a document is understood as that document's list.
- verify × headless/server: the verdict the night tick and the MCP tool read names unmet items instead of having none.

## Ideas (from the brainstorm, grounded)
fm mission, then fm ideas --rounds 4 --falsify --crossbreed --seen-latest 6 (research/brainstorm-20261104-002844: 368
distinct ideas; --deepen dropped by today's risk budget, recorded). Grounded:
- "Compile a goal into done-predicates, and compute done from them" and "Map each goal clause to proof, or refuse
  'done'": partial. T-2136's plan and T-2557's Done-when check exist, but a goal that cites a document has no clauses
  to map. Brief 1 supplies them.
- "Turn the six known false dones into a regression corpus": partial. research/long-false-done.md names them, and the
  long tier reruns only at the end of the run (the user's steer). Held for the end-of-run exam.
- "Re-inject a 40-line goal anchor at PreCompact and SessionStart": built near T-2139.
- "Run a worktree and cwd parity matrix over every verb the goal path calls" (lens: the builder in its worktree): new.
  Grounded in friction: `sampo friction` (2026-11-04) shows three `sampo` calls that exited 1 inside a builder
  lane, the first a `sampo lease take`, and seven isolation refusals there. The gen-3 review counted five lease and
  evidence failures ("5× Bash: This agent is isolated in the worktree"). plugin/agents/fm-builder.md:45 tells
  builders to list such refused checks for the main thread. Handed to the next #4 or #9 Mission, since tonight's builds run in those lanes.

## Approaches
1. Cited-document items in `plan`: the named path (repo or project research only, realpath checked), the named
   section, one item per numbered entry and per DONE-WHEN clause; dedupe by text and by grounded target; per-clause
   checks on `--apply`. Likely outcome: the live goal gets 13 capability items plus its DONE-WHEN clauses, and the
   verdict names the open ones. Fails if: a doc's list isn't numbered (top-level bullets then; neither gives no
   items, said out loud).
2. use what exists: `sampo goal item` thirteen times by hand. Fails if: the next goal citing a doc has the same hole.
3. do less: dedupe only. Fails if: the verdict still reads "the goal has no items".
4. Have the model read the file. Fails if: it paraphrases the user's own list, which is drift.

Choice: 1 (70%).

## Exam (an outcome measure, with a live reading)
- Outcome measure: the live mandate's `sampo goal plan` and `sampo goal verdict`, before and after. Before: 1 item,
  verdict "the goal has no items". After: 13 capability items plus the DONE-WHEN clauses, and a verdict that names
  the unmet ones. All 13 are unmet today: every capability reads "too few (not graded)" in `sampo rune status`. A
  verdict that called the goal finished now would be a false done, and the test plants that case.
- Which way an automatic rule may differ from a hand read (the goal-to-finish critique's rule): the section cut is a
  lower bound. It may miss an unnumbered requirement written in prose, never invent one.
- Exam kinds: #4's goal scenarios are unchanged; the long tier reruns at the end of the run (the user's steer).

## Long-horizon goal (end of run)
On a replayed long goal whose request points at a spec file, the session's done claim is refused while an entry of
that spec is unmet, and the false-done count of the "planned but not built" class falls.

## Risks
- Reading untrusted text: the cited file is the repo's own or the project's research. It is read as data, cut to a
  size cap, and never run. A path outside both, or a symlink out, is refused.
- An over-eager item list: a long doc section with dozens of bullets would bury the verdict. Capped (20 items, like
  the clauses), with the rest named as cut.
- Callers: none of the eleven call sites changes format. Only the item count grows.

## Lean
No new verb. One reader in `plan`, a dedupe, a check map. No hook change.

## Tier share
Brief 1 is tier 3: the run's own goal becomes judgeable.

## Hands to the next generation
A live goal whose verdict tracks the 13 capabilities. The next #4 Mission can link each Mission task to its
capability item and let the verdict move as Missions close. The worktree parity idea is carried with its grounding.

## Done when
T-2913's four criteria are green, the before and after readings are in its log, and MASTER.md (fmmandate) and
CHANGELOG say it.

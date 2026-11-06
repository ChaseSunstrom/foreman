# Brainstorm — lens: simplicity

I read "simplicity" as two things: ideas that make Foreman or the brainstorm loop simpler, and simpler ways to do things already on the list. I skipped anything the "so far" list already covers, such as clustered digests, lite mode, verb retirement and the `--until` flag. Nothing here is verified against the code; where a claim rests on the pack text alone, the Why line says so.

- **Bound the guard with a size gate in front of every regex** — SECURITY — value 4 — effort S — risk med — category: guard
  Why: T-2668 fixed the ~n^4 hang by capping nested `$(` at 8, which patches one pattern. A single input-length and token-count cap checked before any rule runs makes the worst case bounded for every rule, including future ones.
  Done when: a 200k-char command is refused in under 50 ms with a message saying to split it, and a planted slow rule can't push any command past the bar.

- **Dedupe the pack against itself** — CLEAN — value 3 — effort S — risk low — category: brainstorm
  Why: the pack lists "T-2669" and "Merge T-2669" as separate commits. T-2667, T-2668, T-2669 and T-2671 also appear in both the user's-words section and the missed-asks section. Each repeat costs tokens in every child.
  Done when: a pack built from the current repo has no task id appearing twice across the Recent commits section, and none in both of the other two sections.

- **Ask round 1 for titles only** — FEATURE — value 4 — effort S — risk low — category: brainstorm
  Why: the pack records 525 ideas in one brainstorm, and each needs a Why and a Done-when written and then grounded. Most are dropped, so the expansion work for them is wasted. Expand only the ones that survive a dedupe against the catalogue. Assumption: survival rate is well under half.
  Done when: round 1 children return one line per idea, and a second call fills in Why and Done-when only for the kept titles.

- **Fold `--stall-usd` into the existing budget cap** — CLEAN — value 3 — effort S — risk low — category: run
  Why: T-2669 added a new flag when `fm budget cap` already exists. One cap with a "since last close" field means one place to read, set and document.
  Done when: `fm budget` shows the stall limit, and `fm run --stall-usd` is either removed or an alias that sets it.

- **Make the by-source split the default `fm burden` output** — CLEAN — value 2 — effort S — risk low — category: footprint
  Why: T-2667 added `--by-source` as a flag. The split is the more useful view and the plain total can be one line of it.
  Done when: bare `fm burden` prints the total and the per-source lines, and `--by-source` is gone.

- **Collapse `fm decide` kinds into one record with a "report" bit** — CLEAN — value 3 — effort M — risk med — category: rules
  Why: the steers use `--kind costly` and `fm decide --check` for different jobs on the same store. Assumption: the kinds differ only in who reads them.
  Done when: one record shape serves steers, costly decisions and checks, and the existing ledger reads unchanged.

- **Generate the Genesis site from one data file and one template** — CLEAN — value 3 — effort M — risk low — category: site
  Why: `site/` holds 64 files and a standing rule says `fm genesis live` publishes on every tower change. Fewer files means fewer things to publish and leak-scan.
  Done when: `site/genesis/` is produced by one script from one JSON file, and deleting every generated file then regenerating gives the same tree.

- **Name one primary consumer per brainstorm "Next question"** — CLEAN — value 2 — effort S — risk low — category: brainstorm
  Why: each child emits a free-form question, and the earlier "Questions left" list in the pack is already long and unanswered. Requiring a named verb or task that the answer would change keeps only questions someone will act on.
  Done when: any question without a named consumer is dropped before it reaches the pack.

- **(wild) Give each lens a random 25% slice of "ideas so far"** — PERFORMANCE — value 3 — effort S — risk low — category: brainstorm
  Why: the list is thousands of lines in every child's prompt. A random slice cuts cost roughly 4× and removes the shared anchoring the fixed list creates, and the post-hoc catalogue filter catches repeats anyway. Assumption: the filter is reliable.
  Done when: a slice-versus-full run on one lens shows no drop in kept ideas per round and a lower token count.

- **(wild) Make children write each idea as "I want X so that Y"** — FEATURE — value 2 — effort S — risk low — category: brainstorm
  Why: this forces the user benefit into the title and makes tweaks with no benefit visible at a glance.
  Done when: a lint flags any title without a "so that" clause or a benefit phrase.

- **(wild) Let ideas decay by one value point per round unseen** — FEATURE — value 3 — effort M — risk low — category: catalogue
  Why: 30+ "Later from T-0760/0818/0843" tasks are deferred with no clock. Decay makes the pile prune itself instead of growing, and a re-proposal restores the points. Assumption: no one wants a manual sweep.
  Done when: an idea untouched for N rounds falls below the floor and leaves the open list with its last score recorded.

- **(wild) Run a subtraction-only lens that may only say what to remove from the pack** — FEATURE — value 3 — effort S — risk low — category: brainstorm
  Why: nothing measures which pack sections change any child's answer. A lens that cites the removable lines gives an evidence-based trim.
  Done when: the lens returns line ranges to cut, and a rerun without them yields the same top-5.

Next question: which pack sections have no measurable effect on the kept ideas, and what would the pack be without them?
Next question: when the user says "simplify", do they mean fewer verbs, shorter output or fewer decisions asked of them?

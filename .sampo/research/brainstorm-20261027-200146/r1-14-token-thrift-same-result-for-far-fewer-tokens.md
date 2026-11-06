# Brainstorm — lens: token thrift: same result for far fewer tokens

- **Put a context-size gate in `fm check`** — PERFORMANCE — value 5 — effort S — risk low — category: context budget
  Why: the user asked that context per reply stay under about 140k, and the pack's fresh 200k compaction and Sonnet-builder changes have no regression check behind them.
  Done when: a check fails any scripted run whose largest reply context exceeds 140k, and the failure message names the turn.

- **Trim the rules file under its 6,400-char budget** — CLEAN — value 4 — effort S — risk low — category: rules size
  Why: the pack says the rules file is 6,416 chars, over the doctor's 6,400 budget since T-1520.
  Done when: `fm doctor` reports the rules file within budget and the trimmed rules still pass the existing rules tests.

- **Turn skills the model never loads into user-only slash commands** — FEATURE — value 4 — effort S — risk low — category: listing room
  Why: the user asked for this directly, and the hook already supplies the `fm` command, so the listing entry is redundant tokens on every turn.
  Done when: a session's skill listing shrinks by the count of never-loaded skills, and each one still runs from its slash command.

- **Route playbooks through a compact keyword index, loading a body only on a hit** — PERFORMANCE — value 5 — effort M — risk med — category: playbook routing
  Why: the user wants tens of thousands of playbooks, not all loaded, and actually used; the pack shows none are listed at 10k+ scale.
  Done when: `fm playbooks route` on a 10,000-entry fixture returns the same top-3 as the full scan, loading at most 3 bodies, in under 200 ms.

- **Scale brainstorm lenses by yield and drop the dry ones** — FEATURE — value 4 — effort S — risk low — category: brainstorm cost
  Why: T-0829 already names this (lens_rates); each dry lens spends a child's full pack on nothing.
  Done when: a brainstorm run with a lens yielding zero ideas for three rounds is skipped next round and the run's token total drops.

- **Run a shell prefilter ahead of size-gated hooks** — PERFORMANCE — value 4 — effort M — risk med — category: hook latency
  Why: the PreToolUse:Bash:script p95 measured about 310 ms against a 300 ms budget, and a full read cost 124 s of CPU.
  Done when: `bench_hooks --runs 20` keeps PreToolUse:Bash:script p95 under 300 ms on a loaded box.

- **Salvage partial output from capped `claude -p` children** — FIX — value 4 — effort M — risk med — category: lost work
  Why: T-0831 says a capped child throws away its tokens; the pack's brainstorm children are the same kind of run.
  Done when: a child hitting its cap returns its completed sections, and the rerun starts from the last complete section.

- **Roll compact output out in shadow mode first, with fetch-back tracking** — PERFORMANCE — value 4 — effort M — risk med — category: output size
  Why: T-0828 has the design; shadow mode lets the team measure the token saving before any command changes its output.
  Done when: a shadow run logs both outputs and the fetch-back rate for each command, and a rollout threshold is set from that log.

- **Cache a content hash per file so repeat reads send only the diff** — PERFORMANCE — value 4 — effort M — risk med — category: read cache
  Why: assumption: the same pack files are re-sent to every lens child, so unchanged files cost full tokens each time.
  Done when: the second read of an unchanged file in one run returns a one-line "unchanged since read" marker instead of its contents.

- **Answer a repeated brainstorm from its journal before any model call** — FEATURE — value 3 — effort M — risk low — category: memo cache
  Why: assumption: many rounds rebuild the same pack, so a cache keyed on the pack hash can return a prior answer for free.
  Done when: rerunning an unchanged pack makes zero model calls and returns the stored slate, marked as cached.

- **Wild: sub-agents talk in a shared shorthand dictionary loaded once** — FEATURE — value 2 — effort L — risk high — category: agent protocol
  Why: wild; the children would pass terse symbols and a dictionary sent once, cutting prose between them, though the dictionary itself would need its own tests.
  Done when: two sub-agents complete a task with the shorthand and the same result as plain prose, using fewer tokens.

- **Wild: a daily token budget that ideas bid for** — FEATURE — value 3 — effort L — risk med — category: budget market
  Why: wild; each proposed change declares its expected token saving, and the scheduler funds the best bids from a fixed daily allowance.
  Done when: a day's queued changes are ordered by declared saving per token, and the spend stops at the allowance.

- **Wild: send repeated system text as references, not copies** — PERFORMANCE — value 3 — effort L — risk high — category: prompt dedupe
  Why: wild; if the same rules block appears in every child's prompt, sending a hash reference instead of the full text would save tokens each turn, though the model has to accept the reference.
  Done when: a child whose prompt repeats a stored block receives a reference, and its output matches the full-text run.

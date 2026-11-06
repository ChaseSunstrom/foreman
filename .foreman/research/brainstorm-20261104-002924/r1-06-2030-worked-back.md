# Brainstorm — lens: 2030 worked back

- **Inject SessionStart once, then a pointer** — FIX — value 5 — effort S — risk low — category: context
  Why: the pack shows 2,733 characters injected twice. By 2030 sessions will run for days and re-inject on every resume, so the fix has to be at the source. Emit one block of at most 300 characters (state hash plus "fm brief" for the rest) and skip the second emit by keying on a per-session marker.
  Done when: a recorded SessionStart payload contains the text once and is ≤ 300 chars, and a cold child still finishes a known task using only the pointer.

- **Shard MASTER.md under a Read-safe ceiling** — CLEAN — value 5 — effort M — risk low — category: docs
  Why: MASTER.md is 75,758 tokens, so Read refuses it, and agents will only get more context-hungry. Split it into anchored shards of 12k tokens or less plus an index of 6k or less. A generated `fm doc <anchor>` prints one shard, and a lint fails any doc over the ceiling.
  Done when: every doc file passes Read unmodified, and a lint test fails on a 13k-token shard.

- **Emit per-turn context as a delta against the last turn** — PERFORMANCE — value 4 — effort S — risk low — category: context
  Why: the per-turn burden is 48 to 76 characters, which is paid on every turn forever. Hash the injected state and emit only when it changes, with an unchanged turn emitting nothing.
  Done when: a replayed 20-turn idle session injects 0 characters after turn 1, and a state change injects on the very next turn.

- **Roll ledgers into sealed segments with an equivalence proof** — PERFORMANCE — value 5 — effort L — risk med — category: state size
  Why: project state is 2.4 GB, and readers that scan a tail of lines get slower every month. Seal each day's records into a segment with a summary row and keep the hash chain. Cold segments compress and archive. A compaction counts as valid only if every reader gives identical output on the compacted copy.
  Done when: `fm doctor` and `fm outcomes --json` are byte-identical before and after compaction on a copy of the real state, and the hot set is under 250 MB.

- **Extrapolate state growth at ship time** — SECURITY — value 3 — effort S — risk low — category: reliability
  Why: assumption: the 2.4 GB wasn't a surprise only because nobody was measuring slope. Fit bytes per day per ledger from file mtimes and sizes, project to 2030, and make the ship gate fail when any ledger's projection passes its declared ceiling.
  Done when: a synthetic ledger growing 10x faster than the baseline fails the gate, naming the ledger and the projected date.

- **Make injected text byte-stable for prompt-cache hits** — PERFORMANCE — value 3 — effort S — risk low — category: cost
  Why: assumption: by 2030 cost is dominated by uncached prefix tokens. Any timestamp, counter or reordered list in SessionStart breaks the cache for the whole session. Sort deterministically and move volatile values to the delta channel.
  Done when: two sessions started on identical state produce byte-identical injections (hash equal).

- **Declare retention per ledger in one table that `fm doctor` enforces** — CLEAN — value 4 — effort M — risk low — category: state size
  Why: no pack evidence of any TTL, and 2.4 GB suggests none exists. A single `retention` table gives each store a keep-hot window, a rollup rule and a delete-never flag (grants, decisions and steers are never deleted). Doctor names any store that is missing a row or past its window.
  Done when: removing one ledger's row turns doctor red, naming it.

- **Ship a hook-latency scaling curve, not a single bar** — PERFORMANCE — value 4 — effort M — risk low — category: hooks
  Why: `bench_hooks.py --runs 20` measures one state size. Run it at 1x, 10x and 50x synthetic state and gate on the slope in ms per GB, so a hook that is fast today but linear in ledger size fails now rather than in 2030.
  Done when: the bench prints three points and a slope, and a planted full-file scan in a hook fails the gate.

- **Wild: run a 2030 post-mortem pre-mortem** — FEATURE — value 3 — effort S — risk low — category: lean
  Why: wild. A tool-less child on a stronger model gets only this generation's diff and the lean numbers, and is told "it's 2030 and users uninstalled Sampo; write the post-mortem". The causes it names become subtraction or guard tasks.
  Done when: the post-mortem is filed with at least 3 causes, each linked to a task or a recorded "by design".

- **Wild: write a time-capsule letter that a cold maintainer must act on** — FEATURE — value 3 — effort M — risk low — category: docs
  Why: wild. Each Mission seals a one-page letter (what the guard must never lose, what is safe to delete, where the 2.4 GB lives). A cold child with no other context must file one correct fix from the letter plus the repo.
  Done when: the child's filed task matches a seeded real defect, and the letter is ≤ 1 page.

- **Wild: hibernate the tower to a small seed and wake it by replay** — FEATURE — value 3 — effort L — risk high — category: state size
  Why: wild. One command reduces a project's state to a seed under 50 MB (steers, decisions, grants, task index, segment summaries). A fresh state directory is then rebuilt from the seed, and the rebuild must pass doctor and reproduce `fm next`.
  Done when: waking from the seed yields the same `fm next` and doctor verdict as the original on a copy of the real state.

- **Freeze the guard's size and exam outside the lean pressure** — SECURITY — value 4 — effort S — risk low — category: guard
  Why: this Mission cuts hooks and context, and the guard is the thing most likely to be trimmed by accident. Hash the guard rules, their exam corpus and the Ward entry points. Any lean change touching them must carry a guard-exam run showing zero lost refusals.
  Done when: a change deleting one rule fails the gate unless the exam result is attached and unchanged.

Next question: which of the hot hook paths and injected strings has a reader that would silently go wrong, rather than fail, once the ledgers are compacted?
Next question: what would the first sentence of Sampo's README have to say in 2030 when the host does planning and proving natively?

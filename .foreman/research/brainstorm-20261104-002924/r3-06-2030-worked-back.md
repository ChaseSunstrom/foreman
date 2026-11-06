# Brainstorm — lens: 2030 worked back

- **Run a rollover drill on every counter and width** — FIX — value 4 — effort S — risk low — category: durability
  Why: assumption: ids are at T-2901 and likely parsed with a 4-digit pattern somewhere (sorting, regexes, `Next:` parsers). T-10000, gen 10 and 5-digit counts are only a few months away at the current filing rate.
  Done when: a test seeds T-9998 through T-10002 and gen 9 through 11. Every verb, `fm next`, the Mission pages and the Exam parsers run clean, and sort order matches numeric order.

- **Replace line-count windows with cursor or time windows** — FIX — value 4 — effort M — risk med — category: hooks
  Why: T-2873 and the `_running` bug show a 1,500-line tail covering under an hour of a busy shared transcript. Window size silently decays as event density grows toward 2030. A census of every `tail(N)` / `[-N:]` in readers is not in the ideas list.
  Done when: no reader on the hook or drive path uses a fixed-line tail for liveness. A synthetic transcript at 10× event density yields the same running set as at 1×.

- **Keep a frozen 2026 state fixture and migrate it to HEAD on every ship** — FEATURE — value 4 — effort M — risk low — category: migration
  Why: the rename migration (move with backup, manifest, undo) is the first of many. An install that skips versions will meet a chain of them by 2030, and nothing currently exercises an old state end to end.
  Done when: `tests/` holds a small synthetic gen-4 state. The ship gate migrates it to HEAD, runs `sampo doctor` green, and fails if a migration is missing from the chain.

- **Stamp every embedding with model id and dimension, and never mix them** — FIX — value 4 — effort M — risk low — category: moons store
  Why: Moons runs through `models.embed` with a recorded char-shingle fallback. By 2030 the embedder will have changed, and vectors from different models are silently incomparable.
  Done when: each stored vector carries `(model, dim)`. A query across two models refuses or re-embeds lazily, and a test with a swapped fake embedder shows no cross-model dedupe.

- **Make child sessions leave no host transcripts** — CLEAN — value 3 — effort S — risk low — category: state size
  Why: assumption: part of the 2.4 GB is host per-project transcript and memory directories. The path `~/.claude/projects/-run-user-1000-fm-children-1000/` shows each child cwd becomes a project dir.
  Done when: a brainstorm fan-out leaves no new `~/.claude/projects/*fm-children*` bytes. A sweep lists the existing orphans, in dry-run first, and their total size is reported.

- **List local model weights as part of Sampo's footprint** — CLEAN — value 3 — effort M — risk low — category: footprint/privacy
  Why: install.sh offers Ollama with pinned embedders and the Model bench pulls decision models. These are multi-GB and nothing counts them as Sampo's weight.
  Done when: `sampo models` lists each pulled model with size, last-used date and the task that pulled it. `--prune` previews removals and keeps in-use ones.

- **Give pruned state a tombstone so readers never return silent empty** — FIX — value 4 — effort M — risk med — category: prune safety
  Why: assumption: the prune plan for the 2.4 GB will remove ledger segments. The drive bugs (T-2873, T-2900) were all silent misses, and an empty result after prune looks like "nothing happened".
  Done when: after pruning a segment, a reader that needs it prints "pruned DATE, restore: <cmd>" and exits non-zero in `--json`. A test shows no reader treats a pruned range as zero events.

- **Self-probe model quirks instead of hardcoding profiles** — FEATURE — value 3 — effort M — risk low — category: local models
  Why: T-2893 added per-profile extras and a reasoning switch, and the 'jarvis' default had to be dropped. Model ids will keep changing, and a 3-minute swap cost makes manual tuning expensive.
  Done when: an unknown model id gets a probe (empty-on-length-cut, thinking-tag leak, max context). The result is cached as a profile, and the probe runs once per id.

- **A/B the Ward line's position before SessionStart dedupe lands** — SECURITY — value 4 — effort S — risk low — category: guard
  Why: today the Ward text appears twice, at the start and again later. Dedupe will keep one copy, and long-context models attend unevenly by position.
  Done when: the bait exam runs on the local model with the guard line first, last and per-turn only. The position with the lowest bypass rate is recorded as a decision, and a test pins that position.

- **Wild: Run a small-window maintainer exam** — FEATURE — value 4 — effort M — risk low — category: legibility
  Why: wild. MASTER.md is 75k tokens and Read refuses it, so a 2030 maintainer with a small local window cannot navigate. Give a local 8k-context model five canonical chores, say "add a verb", "find who writes X", and allow only `sampo map` and the doc verbs.
  Done when: the exam prints a pass count per chore. Sharding MASTER.md or adding a verb is judged by whether the count rises.

- **Wild: Generate a doomsday card and prove a stranger can use it** — FEATURE — value 4 — effort M — risk low — category: recovery
  Why: wild. A nightly-regenerated 300-word card gives the off switch, what is safe to delete with sizes, and how to restore. A cold child with no memory must follow it in a scratch home and end with Sampo off and the project intact.
  Done when: the nightly test fails if the child cannot reach that end state in 10 tool calls. Any doc line that child could not follow is listed.

- **Wild: Build a parallel-hooks fake host** — SECURITY — value 3 — effort M — risk med — category: hooks
  Why: wild. A future host may run all hooks of an event concurrently and merge their outputs. That would break one-JSON-document assumptions and race the ledger appends, and a double SessionStart already shows registration problems.
  Done when: a fake host fires each event's hooks in parallel with merged stdout. Ward verdicts stay correct, the ledger has no torn lines, and the output parses as one document.

- **Verify that every printed lean number can be re-measured by anyone** — CLEAN — value 2 — effort S — risk low — category: measurement
  Why: the request quotes 2,733 characters, 75,758 tokens, 2.4 GB and 48 to 76 characters. A different tokenizer or host version changes these with nobody noticing.
  Done when: each number in the Mission report appears with the command, host version and tokenizer that produced it, and a test reruns the commands.

Next question: Which of the 2.4 GB is rebuildable, which is the user's only copy, and who currently checks that boundary before a prune runs?
Next question: Which hook behaviours depend on host timing or ordering, and what would break if the host changed either?

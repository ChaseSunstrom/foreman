# Brainstorm — lens: usage efficiency

- **Exclude generated, lock and vendored files from reads by default** — PERFORMANCE — value 4 — effort S — risk low — category: context
  Why: assumption: read paths don't filter lockfiles or vendored trees, so one stray read can load a large generated file that nobody asked for. The pack's map shows 1,835 files, so this is easy to hit.
  Done when: reading a lockfile or vendored path returns a one-line stub with size and hash, and `fm cost` shows the read as near-zero tokens.

- **Time turns to the prompt-cache window** — PERFORMANCE — value 5 — effort M — risk med — category: cache
  Why: assumption: a queue that idles past the cache lifetime re-sends the full prefix on its next turn. The pack already lists "cache the context pack prefix", which shows the prefix is the big cost, but nothing schedules work around expiry.
  Done when: in a replay of a queue with gaps, full-prefix sends drop and `fm cost` reports cache hits per run.

- **Evict file reads that a later edit has made stale** — PERFORMANCE — value 4 — effort M — risk low — category: context
  Why: assumption: a run that reads a file, edits it, and keeps the old read in context pays for text that no longer exists. Liveness-style pruning covers unused context but not superseded context.
  Done when: after an edit, the earlier read is replaced by a pointer, and a test shows the next reply's context shrinks by the replaced size.

- **Show the retry tax per task** — FEATURE — value 4 — effort S — risk low — category: observability
  Why: evidence: the pack says the user had to point out the usage burn, and `fm cost` attributes spend by source but doesn't split out repeat attempts. Retries are the cost users don't see.
  Done when: `fm cost <task>` prints spend as first attempt, retries and reruns, and the parts sum to the run's total.

- **Slice the rules file to each task's kind** — PERFORMANCE — value 4 — effort M — risk med — category: rules
  Why: assumption: every task loads the whole rules file (6,416 chars at one point, over the 6,400 budget). A docs-only task pays for guard and test rules it never uses.
  Done when: a docs task's first pack omits test-only rules, and the duel pass rate on a fixed case set doesn't drop.

- **Batch small sequential reads into one call** — PERFORMANCE — value 3 — effort S — risk low — category: tool calls
  Why: assumption: an exploration pass that reads ten tiny files pays ten round trips of framing and model turns. Batching would cut turns with the same content returned.
  Done when: a fixed exploration script makes fewer tool calls and returns byte-identical file contents.

- **Keep a file summary card keyed by content hash** — PERFORMANCE — value 4 — effort M — risk low — category: context
  Why: assumption: many tasks read the same unchanged file in full. A one-line card, invalidated when the hash changes, lets the model skip most full reads.
  Done when: a second task touching an unchanged file gets the card instead of the body, and changing the file's hash forces a fresh card.

- **Sort context so identical prefixes line up across tasks** — PERFORMANCE — value 3 — effort S — risk low — category: cache
  Why: assumption: the pack's sections come in varying order, so tasks that share most of their context still miss the cache. Stable ordering keeps the shared prefix longest.
  Done when: two tasks with the same pack inputs produce byte-identical prefixes up to the first task-specific section.

- **Paint the repo map by read cost** — FEATURE — value 3 — effort S — risk low — category: ui
  Why: wild: the map already lists the repo's layout, so each directory could show how many tokens a full read costs. The user would see the expensive corners before a run reaches them.
  Done when: `fm map` marks each directory with its full-read token estimate, and the marks sum to the repo total within 5%.

- **Let the model write a do-not-read list that later packs honour** — FEATURE — value 3 — effort M — risk med — category: context
  Why: wild: a run that finds a file dead weight writes it down, and the next task in the same area leaves it out. Any task can still fetch the file on request.
  Done when: a file marked dead is absent from the next same-area pack, and a request for it still returns the full file.

- **Sync pack hashes across machines so a second laptop sends only the diff** — FEATURE — value 2 — effort L — risk high — category: devices
  Why: wild: a user on two machines re-sends the same context on each. Opt-in sync of content hashes, with no file bodies leaving the machine, would cut repeat sends.
  Done when: with sync enabled and off, the second machine's first pack sends only changed sections, and with sync disabled nothing leaves the machine.

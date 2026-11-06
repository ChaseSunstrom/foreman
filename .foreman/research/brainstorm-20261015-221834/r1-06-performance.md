# Brainstorm — lens: performance

- **Write a resume capsule at every checkpoint** — FEATURE — value 5 — effort M — risk low — category: resume
  Why: T-1028 is planned, and the user asked for stopped builders to "pick it back up". A resumed agent that re-reads the repo and re-plans pays full cost again. Each step boundary would write one small file: worktree and branch, task, brief, steps done, last red/green command, files touched, and the next action. Resume then loads only that file.
  Done when: killing a builder mid-task and running the resume verb continues at the recorded next step. A test asserts the resumed session issues no repo-wide scan and its first prompt is under N tokens.

- **Index cards by import and dep, built once in `fm map`** — PERFORMANCE — value 4 — effort M — risk low — category: card lookup
  Why: only 6 of 1,084 cards ever fired, and T-1036 will inject cards by import. An inverted index (import, dep or glob to card ids) stored beside the map makes the edit-time lookup one dict read, not a scan of the library.
  Done when: injection for an edited file with 1,084 cards loaded takes under 5 ms in `bench_hooks.py`, and the index rebuilds only when a card or the manifest changes.

- **Look up known fixes by error fingerprint** — PERFORMANCE — value 4 — effort M — risk low — category: learned fixes
  Why: T-1032 stores fixes learned from failure then success, and they should travel in git. Normalize the failing output (strip paths, ids, timestamps) and hash it. Lookup is then O(1) per failure and stays flat as the hint set grows from hundreds to thousands.
  Done when: the same error with different tmp paths and pids hits the same hint, and lookup time is flat from 100 to 10,000 hints in a bench.

- **Store git-carried hints as one content-addressed file each** — PERFORMANCE — value 3 — effort S — risk low — category: sharing
  Why: the user wants fixes to travel through git to other clones and teammates. One file per hint, named by fingerprint hash, can't merge-conflict. Reads can lazy-load only the matching file.
  Done when: two branches adding different hints merge with no conflict, and a hint lookup reads one file.

- **Tail the ledger by offset with rolling aggregates** — PERFORMANCE — value 3 — effort M — risk med — category: pane
  Why: `gather()` in `fmwatch.py` re-reads recent and history ledger data each refresh, and the pane is under tight frame and fill constraints. Keep a byte offset plus running counters (closes per day, done/left) and read only appended lines.
  Done when: refresh cost is constant as the ledger grows from 1k to 100k lines, and a truncated or malformed line is skipped without a full re-read.

- **Trim the brainstorm pack and keep it cache-friendly** — PERFORMANCE — value 4 — effort S — risk low — category: tokens
  Why: this pack prints "The user's own words" twice, and "Ideas so far" carries about 100 raw lines that grow each round. Dedupe sections, collapse ideas into cluster titles with counts, and put the stable parts first so every lens shares one cached prefix.
  Done when: the pack is at least 30% smaller with no repeated section, and the byte prefix is identical across lenses up to the lens line.

- **Make the edit-time test sentinel cancellable and debounced** — PERFORMANCE — value 3 — effort M — risk med — category: gate speed
  Why: T-0214 is deferred. Run only the tests linked by the map in the background, debounce bursts of edits, and kill a stale run when a newer edit lands, so feedback arrives without blocking the turn.
  Done when: three rapid edits start one final run, and the superseded runs are killed within 1 s.

- **Route mechanical children to Haiku with a Sonnet spot-check** — PERFORMANCE — value 4 — effort M — risk med — category: cost
  Why: T-1037 plans bulk card drafts from docs, `fm scout` runs across projects, and the Haiku probe (T-0978) already exists. Mechanical drafting can run on a small model, with a sampled quality check by a larger one against the card format.
  Done when: 100 card drafts cost at least 60% less than an all-large run, and the spot-check rejects a seeded bad card.

- **Create worktrees copy-on-write with a warm pool** — PERFORMANCE — value 3 — effort M — risk med — category: worktrees
  Why: fleets spawn many builders, and each needs deps and build caches. Reflink-copy the heavy ignored dirs, and keep one pre-made worktree ready for the next spawn or resume.
  Done when: spawning a builder in a repo with a large `node_modules` takes under 2 s, with disk use near zero until files diverge.

- **Wild: Fork a resumed agent from its cached transcript prefix** — FEATURE — value 4 — effort L — risk high — category: resume
  Why: assumption: the API prompt cache and the session transcript let a resume reuse the earlier prefix instead of paying for a re-brief. Together with the resume capsule this makes "resume" nearly as cheap as "continue".
  Done when: a resume within the cache window reports a cache-hit rate above 80% on its first call.

- **Wild: Have hooks write the pane's state into a shared-memory ring** — PERFORMANCE — value 2 — effort L — risk high — category: pane
  Why: assumption: the pane polls and parses files for the live tree, lanes and graph. A fixed-size mmap ring written by hooks and read by the pane removes parsing and polling latency, and unreadable data degrades to the file path.
  Done when: tool-call to pane-paint latency is under 50 ms in the harness, and deleting the ring falls back cleanly.

- **Wild: Run overnight bulk work as batch jobs with a cost ceiling** — FEATURE — value 3 — effort L — risk med — category: cost
  Why: T-0793 (overnight work) and T-1037 (bulk cards) are both unattended and latency-tolerant. Send them through a batch endpoint at reduced price, with a hard USD cap that stops the run and reports partial results.
  Done when: a 200-card batch run finishes under its cap, and a deliberately low cap stops it with a partial-result report.

- **Skip re-verifying unchanged proofs on resume** — PERFORMANCE — value 3 — effort S — risk low — category: proof gate
  Why: a resumed task would otherwise re-run its red-then-green proof. Key each proof by the hash of the test file and its linked sources, and reuse the earlier result when nothing changed.
  Done when: resume with an untouched tree re-runs zero proof commands, and touching one linked file re-runs only that proof.

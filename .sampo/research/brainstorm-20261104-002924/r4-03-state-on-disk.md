# Brainstorm — lens: state on disk

- **Audit every hook's file opens** — PERFORMANCE — value 4 — effort M — risk low — category: hooks/state
  Why: with 2.4 GB of state and 48 to 76 characters per turn, nothing proves which files a hook actually touches. Assumption: some hooks open cold ledgers.
  Done when: a test installs `sys.addaudithook` around each hook's run and fails if it opens a file outside a declared hot set or reads more than N KB.

- **Keep full fidelity around trouble, thin the quiet** — FEATURE — value 4 — effort M — risk med — category: retention
  Why: age-based compaction treats a boring Tuesday and a Ward block the same. Records within a window of a block, a user correction, a failed proof or a hung stall carry the lessons.
  Done when: compacting a fixture ledger keeps every record within ±20 lines of a planted block or correction byte-for-byte and thins at least 80% of uneventful ones.

- **Sweep state by reachability from roots** — FEATURE — value 4 — effort M — risk med — category: GC
  Why: the pruner ideas above key on age or class. A file cited by an open task, a tower file, a lesson, a receipt or a steer's check should be pinned however old it is, and unreferenced files collected.
  Done when: `sampo state gc --plan` lists unreachable bytes by class and never lists a file an open task names, and a planted cited file survives a plan-and-apply run.

- **Stamp every record with its own time-to-live at write** — CLEAN — value 3 — effort S — risk low — category: retention
  Why: expiry rules in a separate table drift from the writers. The writer knows whether a row is a debugging breadcrumb or a decision. Assumption: most ledgers are JSONL with room for one more key.
  Done when: each ledger writer sets `ttl_d`, the sweeper removes expired rows with no per-ledger code, and a test fails on a writer that omits it.

- **Test concurrent appends larger than PIPE_BUF** — FIX — value 4 — effort S — risk low — category: integrity
  Why: sessions, lanes and the drive append to shared JSONL, and `O_APPEND` is only atomic up to a size limit; larger records can interleave. Assumption: some records, such as packs and receipts, exceed 4 KB.
  Done when: 8 processes each append 200 records of 1 to 64 KB and every line still parses as JSON, or the writer takes a lock above the threshold.

- **Make downgrades safe for state files** — FIX — value 3 — effort M — risk med — category: compatibility
  Why: the rename, shims and install generations mean an older Sampo may meet files a newer one wrote. Unknown keys must round-trip and a newer schema must be refused, never "repaired".
  Done when: an old-reader fixture opens a file with extra keys and a newer `schema`, rewrites it with the keys intact or exits with a Next line, and never truncates it.

- **Reflink-snapshot state before any prune or migration** — SECURITY — value 4 — effort M — risk low — category: recovery
  Why: the prune and the planned migrations are irreversible at 2.4 GB. A `cp --reflink=auto` copy costs almost nothing on btrfs or xfs. Assumption: the user's state sits on a reflink-capable filesystem, with a plain-copy fallback that names its cost.
  Done when: apply makes the snapshot, then `status`, `next` and `doctor --json` produce identical output before and after on a fixture, and `undo` restores the original in one command.

- **Checkpoint lane work before `/run/user` goes away** — FIX — value 4 — effort M — risk med — category: durability
  Why: the children and lane directories sit on tmpfs under `/run/user/1000`, which systemd removes on the last logout or at reboot. Uncommitted lane work and open scratch state vanish with it. Assumption: lanes write real work there.
  Done when: a SIGTERM or logout-hook test leaves each live lane's diff on durable disk (a ref or patch file) and a resumed lane finds it.

- **Cap the write rate of every ledger writer** — SECURITY — value 3 — effort S — risk low — category: runaway guard
  Why: a hook or drive loop that re-fires, as the repeated re-push did, can fill disk in minutes. A breaker is cheaper than finding it after the fact.
  Done when: a fixture writer looping at 10,000 rows per second trips a breaker after a set byte rate, logs one row saying so, and `doctor` names the writer.

- **Keep sensitive intermediates on tmpfs only** — SECURITY — value 3 — effort S — risk low — category: privacy
  Why: brainstorm packs, cold-read inputs and verbatim asks may pass through disk state. They only need to live as long as the child. Assumption: some are currently written under the durable state root.
  Done when: a test runs a pack-building verb and finds no file containing a planted user-text marker outside the tmpfs root once the child exits.

- **Compost before deleting (wild)** — FEATURE — value 4 — effort L — risk med — category: retention
  Why: pruning drops bytes and knowledge together. A local model could distil each sealed segment to a few lines of what happened and what was learned, and keep a pointer to the cold archive.
  Done when: after compaction a cold child answers 10 questions about a pruned week from the digest alone at a set accuracy, and the digest is under 2% of the segment.

- **Quiz the restore, not just the copy (wild)** — SECURITY — value 3 — effort M — risk low — category: recovery
  Why: a backup that restores byte-identical files can still be an empty or stale history. Test the knowledge, not the checksum.
  Done when: a nightly job restores the archive into a scratch home, a tool-less child answers five dated questions from `sampo` verbs there, and the answers match the live ledger or the job reports which differ.

- **Make every file writer forecast its own readership (wild)** — CLEAN — value 2 — effort M — risk low — category: retention
  Why: write-only data and files nobody opens are what grow to 2.4 GB. Making the writer declare "read within N days by verb X" turns retention into a scored claim.
  Done when: each new state class declares a reader and a horizon, `doctor` lists classes never read inside their horizon, and the next-largest such class is the first prune candidate.

Next question: which ten files account for most of the 2.4 GB, and does any session path (a hook, `next`, the drive) actually read them?
Next question: when `/run/user/1000` is wiped, which Sampo state survives only because something else happened to commit it?

# Brainstorm — lens: state on disk

- **Expire the rename's backup once it has proved itself** — CLEAN — value 4 — effort S — risk med — category: state size
  Why: assumption: the Foreman→Sampo migration "moves with backup, manifest and undo", so a full pre-migration copy probably still sits beside the live state and may be a large part of the 2.4 GB. No other idea targets it.
  Done when: the backup shows in the state census with its age and byte size. It is removed only after N clean sessions plus a verified manifest match, and the removal is undoable for 7 days.

- **Lay out state by lifetime, not by type** — FEATURE — value 4 — effort L — risk med — category: layout
  Why: assumption: task-scoped artifacts (lane transcripts, proofs, packs, receipts) are scattered across per-type ledgers, so nothing can be dropped together. Prior ideas tier and compact by type, not by what dies together.
  Done when: everything a task creates sits under `tasks/T-id/`, and `sampo task archive T-id` moves or packs that one directory. A test confirms `sampo next` and the ledgers read the same before and after.

- **Attribute every state byte to the task that wrote it** — FEATURE — value 4 — effort M — risk low — category: provenance
  Why: the pack shows a 2.4 GB total but no per-writer answer. Prior ideas cover a census by class, not "T-2851's lane cost 400 MB".
  Done when: `sampo state du --by task` lists the top 10 tasks and lanes by bytes. The finish card shows the bytes that task added.

- **Check that ledger pointers still resolve after pruning** — FIX — value 5 — effort M — risk low — category: integrity
  Why: assumption: evidence pointers (the cited run outputs, host transcript paths, `.jsonl` refs) outlive what a prune or the host's own transcript cleanup removes. Pruning plans are covered, but the dangling references they leave are not.
  Done when: `sampo doctor` counts dangling refs by ledger. `prune --apply` refuses if it would create new ones for a protected class (steers, standing intent, evidence of open tasks).

- **Point at host transcripts instead of copying them** — PERFORMANCE — value 3 — effort M — risk med — category: dedupe
  Why: assumption: Sampo keeps copies or large excerpts of Claude Code session transcripts that the host already stores. Content-hash dedupe is covered, but not avoiding the copy altogether.
  Done when: a transcript-derived record stores a path, offset range and hash. A test shows state growth per session falling, and a missing host file yields a visible "source gone" state rather than an error.

- **Store embeddings as quantized binary beside the text** — PERFORMANCE — value 3 — effort S — risk low — category: size
  Why: Moonscale grows to 10,000 candidates with embeddings through `models.embed`. If vectors are in JSONL, each costs about 10× its binary size.
  Done when: vectors live in a float16 `.bin` sidecar keyed by candidate id and can be rebuilt from the text. The census shows the `candidates.jsonl` footprint falling, and the funnel gives identical dedupe results.

- **Detect whole-file rewrites** — PERFORMANCE — value 3 — effort S — risk low — category: write amplification
  Why: assumption: some state (task index, grants, lane records) is rewritten in full on each tick, which wears the disk and can lose data on a kill. Existing ideas cover fsyncs and kill-points, not which files are rewritten.
  Done when: a bench counts bytes written per file per verb and flags any file rewritten more than 100× per hour. The report lists each as "convert to append" or "justified".

- **Adapt retention to free disk and growth rate** — FEATURE — value 3 — effort M — risk low — category: retention
  Why: static retention tables (already proposed) ignore the machine. A 2.4 GB state means little on a 2 TB disk and a lot on a small one or a tmpfs path.
  Done when: keep-days shrinks automatically when free space drops below a user-set floor, and the prune plan states why. A simulated low-disk test shortens retention and a normal-disk test leaves it alone.

- **Sweep orphaned temp files from crashed writes** — FIX — value 3 — effort S — risk low — category: hygiene
  Why: atomic-write patterns leave `.tmp` or partial files after a SIGKILL. The kill-point sweep proposed earlier proves safety but does not clean up what a crash leaves behind.
  Done when: a kill-point test leaves temp files, and `sampo doctor` lists them with age. A sweep removes only those older than the owning process's lifetime.

- **Fork the whole state cheaply for drills and exams** — FEATURE — value 4 — effort M — risk med — category: testing
  Why: drills run in scratch homes and fixtures are small. Real-shaped 2.4 GB state is where the slow-reader and scale bugs live.
  Done when: `sampo state fork` makes a reflink or copy-on-write clone, falling back to hardlinks and then to a refusal with a size estimate. A drill runs against it without touching live state, and a checksum shows live state unchanged.

- **Wild: Offer opt-in cold storage to the user's own NAS or bucket with local stubs** — FEATURE — value 3 — effort L — risk med — category: privacy, devices
  Why: wild. Old segments leave the machine only under an explicit setting and show a stub the web UI can restore on demand.
  Done when: with the setting off, a network-blocked test shows zero egress. With it on, a stub restores byte-identical content and the hash chain verifies.

- **Wild: Add a read-heat map of state files** — FEATURE — value 3 — effort M — risk low — category: delight, tiering
  Why: wild. Mounts are often `noatime`, so atime cannot tell hot from cold. A cheap helper that logs which state files verbs actually open would show the real read pattern, a signal tiering and retention could both use.
  Done when: a web UI sunburst colours by last read versus last write. Files never read in 60 days are marked "safe to archive" and the claim is checked against the read log.

- **Wild: Hold a monthly Burn Night that packs and signs the cold state** — FEATURE — value 2 — effort M — risk low — category: delight
  Why: wild. Retention becomes a ritual in the forge theme rather than silent deletion. Old state is sealed into one signed pack, the fire animation plays, and a receipt shows bytes returned and what can be restored.
  Done when: the command produces one pack plus a receipt, the restore path is tested, and nothing outside the retention table is touched.

Next question: which of the 2.4 GB is rebuildable from git and other sources, and does any process silently depend on that part being present?
Next question: if the user's disk filled mid-lane, which ledger would fail first, and would anything tell the user?

# Brainstorm — lens: state on disk

- **Split state into XDG state, cache and runtime roots** — CLEAN — value 4 — effort M — risk med — category: state layout
  Why: assumption: the 2.4 GB mixes ledgers (irreplaceable) with caches, worktrees and transcripts (rebuildable). The pack names no split, and the "state manifest" idea only labels files rather than moving them.
  Done when: `sampo doctor` prints three byte totals (state, cache, runtime), and deleting the cache root leaves every verb working.

- **Drop a CACHEDIR.TAG and a backup-exclude marker in rebuildable dirs** — FEATURE — value 3 — effort S — risk low — category: disk hygiene
  Why: assumption: user backups, snapshots and `du` tools see the 2.4 GB as precious. Backing up regenerable worktrees and caches wastes space and time.
  Done when: every dir classed rebuildable holds a valid CACHEDIR.TAG, and `tar --exclude-caches` on the state root skips them.

- **Put ledger-scale hot files on a tiny SQLite index, with the text ledgers kept as the source of truth** — PERFORMANCE — value 4 — effort L — risk med — category: ledger reads
  Why: the pack lists hook time, windowed readers and "seek to the window start" as separate fixes, and each reader still scans text. A rebuildable index (task id, ts, offset) makes hooks read only the offsets they need.
  Done when: `bench_hooks.py` shows the p95 of the heaviest ledger-reading hook flat between a 100 MB and a 1 GB state, and deleting the index file rebuilds it with identical output.

- **Check that `/run/user/1000/fm-children` is tmpfs and cap what children write there** — FIX — value 4 — effort S — risk low — category: RAM-backed disk
  Why: this brainstorm child runs in `/run/user/1000/fm-children-1000`, which is normally tmpfs. Child scratch counts against RAM, and the pack has a "scrub and cap child scratch" idea but no tmpfs-aware limit.
  Done when: `sampo doctor` reports the filesystem type of the child dir with its free bytes, and a child that exceeds the cap is stopped with a named reason before the box swaps.

- **Rehearse disk-full and ENOSPC on every writer** — FIX — value 4 — effort M — risk low — category: resilience
  Why: the pack covers kill-point sweeps and torn tails but not a full disk, where the Ward's own state writes could fail silently. A full disk during a protected-path grant is the worst moment for the guard to lose state.
  Done when: a test fills a loop-mounted tmpfs, runs every hook and the main verbs, and shows each either degrades visibly or fails closed, with the Ward still blocking.

- **Hardlink-dedupe identical lane artifacts and transcripts at session close** — PERFORMANCE — value 3 — effort M — risk low — category: dedupe
  Why: assumption: lanes copy the same map, lessons and transcripts. This is a cheap in-place step that avoids the full content-addressed store another idea proposes.
  Done when: after a lane-heavy day, `du` shows fewer bytes than the sum of file sizes, and every file still reads the same.

- **Add an inode and file-count ceiling beside the byte ceiling** — FIX — value 3 — effort S — risk low — category: limits
  Why: the map shows 2,358 files in the repo, and the 2.4 GB state likely holds many small files. Inode exhaustion fails differently from a full disk, and the pack's footprint ideas count only bytes and files in the repo.
  Done when: `sampo doctor` shows inode use, and a fixture that creates 200k tiny files turns it red before the filesystem refuses writes.

- **Compress sealed ledger segments with zstd, readable in place** — PERFORMANCE — value 3 — effort M — risk med — category: compaction
  Why: the pack proposes rolling and archiving segments but not the format. Seekable zstd keeps `grep`-style reads of old history cheap, and the pack also asks for state readable with plain tools.
  Done when: a 500 MB sealed ledger shrinks by at least 70%, `sampo recall` reads it with identical output, and `zstd -d` recovers the original.

- **Wild: Make the state directory a git-style object store you can `fsck`** — FEATURE — value 3 — effort L — risk high — category: integrity
  Why: wild. Content-addressed blobs, reference counts and a `sampo fsck` that names orphans, dangling refs and torn objects. It makes the 2.4 GB explainable in one command.
  Done when: `sampo fsck` lists zero errors on a healthy state, and a planted orphan and a planted corrupt blob are each reported by name.

- **Wild: Show the state as a disk-usage sunburst in the web UI, with an age ring** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: wild. Arcs coloured by class (ledger, cache, worktree, transcript) with brightness for last-read age make "what is eating 2.4 GB" visible at a glance. It reuses the forge palette and needs no remote fetch.
  Done when: the page renders from `--json` only, and the largest arc matches `du` for that directory within 1%.

- **Wild: Hold a nightly "move house" drill that copies state to a fresh path and runs the suite** — SECURITY — value 3 — effort M — risk low — category: portability
  Why: wild. This catches hard-coded absolute paths, repo-identity breakage after a move, and permissions that only work for uid 1000. The pack mentions re-attaching a moved repo but no drill that proves it.
  Done when: the drill relocates state with a different HOME and a path containing spaces, and `sampo doctor` and the e2e roundtrip both pass.

- **Stamp a schema version and writer version on every state file** — CLEAN — value 3 — effort S — risk low — category: migration
  Why: after the Foreman-to-Sampo rename and the module move into `plugin/lib/sampo/`, old and new writers share the same directories. Without a stamp, a reader cannot tell a legacy file from a corrupt one.
  Done when: `sampo doctor` lists the files that lack a version stamp, and a reader given a newer-version file refuses with a clear message instead of misparsing it.

- **Atomic-write helper audit: fsync policy per file class** — PERFORMANCE — value 3 — effort M — risk med — category: write path
  Why: assumption: some hot-path files fsync on every append and others never do. Ledgers need durability, caches do not, and hooks pay for every sync.
  Done when: a table assigns each file class a durability level, and the hook bench shows fewer fsyncs per hook with no loss in a kill-point test of the ledgers.

- **Detect state on a network or sync filesystem and warn** — SECURITY — value 3 — effort S — risk low — category: environment
  Why: assumption: users place `~/.local/share` in Syncthing or Dropbox. Locks and appends then misbehave and conflict copies appear, which the pack notes only for conflict copies.
  Done when: `sampo doctor` warns when the state root's filesystem is NFS, FUSE or a known sync folder, and names the command that moves it.

Next question: which of the 2.4 GB is read by any session path in a normal week, and what share could be deleted today without a single verb changing its output?
Next question: when the state dir and the repo disagree (a moved repo, a restored backup, a half-synced machine), which side does Sampo trust, and does it say so?

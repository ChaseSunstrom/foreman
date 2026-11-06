# Brainstorm — lens: state on disk

- **Break the 2.4 GB into a measured census first (`fm state du`)** — FEATURE — value 5 — effort S — risk low — category: state size
  Why: the pack says project state is 2.4 GB but not which directories hold it. Without a per-directory breakdown by writer, age and last read, every cut is a guess.
  Done when: `fm state du --json` lists every top-level state path with bytes, file count, newest and oldest mtime, and the owning verb, and the totals match `du -sb` within 1%.

- **Give each state class a retention policy and a hard byte budget** — FEATURE — value 5 — effort M — risk med — category: retention
  Why: assumption: most of the 2.4 GB is append-only (transcript copies, ledgers, lane worktrees, caches) with no eviction. A table of `class → keep days → max bytes → on overflow (compact, archive or delete)` turns an unbounded store into a bounded one.
  Done when: a scratch state dir seeded past each budget is brought under it by `fm state gc`, and the dry run lists exactly what it would remove.

- **Split state into hot, warm and cold tiers so hooks only touch hot** — PERFORMANCE — value 4 — effort M — risk med — category: tiering
  Why: hooks must stay fast. Assumption: they read or scan large ledgers. A hot tier (last N days, bounded) is all the hook path may open; older records are compacted into gzip segments with an index.
  Done when: `bench_hooks.py` shows hook latency unchanged when the cold tier is 100× larger, and a test fails if the hook path opens a cold segment.

- **Replace MASTER.md with a sectioned, indexed doc that Read can open** — FIX — value 5 — effort M — risk low — category: docs on disk
  Why: MASTER.md is 75,758 tokens, so Read refuses it. The fix is a small `MASTER.md` index (under 4k tokens) plus a file per anchor, generated from one source, with `fm help <verb>` reading the shard.
  Done when: every file under `docs/master/` is under 8k tokens, the index links each verb anchor, and the README link to MASTER.md still resolves.

- **Dedupe the SessionStart injection by content hash against what the session already holds** — FIX — value 4 — effort S — risk low — category: injection
  Why: SessionStart injects 2,733 characters twice. The fix is to write a per-session stamp file keyed by `session_id` and hash; a second emit with the same hash is a no-op.
  Done when: a recorded session with two SessionStart events shows the 2,733 characters once, and a changed payload still emits.

- **Make a state manifest that says which files are rebuildable** — SECURITY — value 4 — effort M — risk low — category: safety of deletion
  Why: before deleting or compacting anything, the tool must know what can be regenerated (caches, maps, indexes) and what is irreplaceable (steers, grants, ledgers). Assumption: no such split is recorded today.
  Done when: every state path is tagged `derived` or `source`, `fm state gc` refuses to touch `source` without a backup stamp, and a test fails on an untagged new path.

- **Compact each ledger into a snapshot plus a short tail, losslessly** — PERFORMANCE — value 4 — effort L — risk high — category: compaction
  Why: append-only JSONL grows forever and every reader re-parses it. Fold closed tasks into a per-period summary segment (keeping record hashes) and leave only open work and the recent tail in the live file.
  Done when: all `--json` outputs are byte-identical before and after compaction on a copy of the real state, and the live ledger shrinks by at least 80%.

- **Store transcripts and lane artifacts once, by content hash** — PERFORMANCE — value 3 — effort M — risk med — category: dedupe
  Why: assumption: lanes, worktrees and cold-read inputs copy the same large files many times. A content-addressed blob store with references would shrink that.
  Done when: running the same lane twice adds under 5% of the bytes the first run added, and every reference resolves.

- **Wild: Make state "snow-load" aware, so the oldest cold segment is archived to a compressed pack and restored on demand** — FEATURE — value 3 — effort M — risk med — category: archive
  Why: wild — state older than 30 days moves to one `.tar.zst` per month, and a read that needs it restores just that segment transparently with a one-line "restored 2026-09" note.
  Done when: after archiving, `fm outcomes --since 60d` returns the same numbers as before, and a restore touches only the requested month.

- **Wild: Add a "state diet" receipt at every session close** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: wild — one line: "state +14 MB today (ledger 9, lanes 4, cache 1); budget 2.4 GB → 2.38". It makes growth felt each day instead of discovered at 2.4 GB.
  Done when: the close output prints the delta, and a test with a planted 50 MB write names the guilty class.

- **Wild: Mount a tmpfs-only mode where nothing survives except a manifest-listed keep set** — SECURITY — value 3 — effort M — risk med — category: ephemeral state
  Why: wild — for shared or untrusted machines, all derived state lives in memory and only a small allowlisted keep set reaches disk. The directory is `/run/user/1000`, so tmpfs is already near.
  Done when: with the mode on, a full `fm next` and `fm task` cycle leaves only the keep-set files on disk, and a restart rebuilds everything derived.

- **Check disk pressure before writing, and degrade instead of failing** — FIX — value 4 — effort S — risk low — category: reliability
  Why: assumption: a full disk corrupts a ledger tail mid-append. Checking free space against a floor before each write, and dropping derived writes first, keeps the source records intact.
  Done when: with the state dir on a 1 MB loopback or a fake `statvfs` below the floor, derived writes are skipped with one visible line and source records still append whole.

- **Wild: Garden the lane worktrees by last-touched age and branch merge status** — CLEAN — value 3 — effort S — risk med — category: lanes
  Why: wild — lane worktrees are full checkouts, so each can be hundreds of MB. Any whose branch is merged and untouched for 3 days becomes a one-line "prune?" suggestion with the size it frees.
  Done when: a planted merged worktree is listed with its size, and `--apply` removes it while a dirty worktree is never listed.

- **Chart state growth per commit to catch the next 2.4 GB early** — PERFORMANCE — value 3 — effort S — risk low — category: regression gate
  Why: a ratchet like the hook-timing bench but for bytes written by the test and e2e runs would stop new writers from quietly adding gigabytes.
  Done when: `roundtrip.py` fails if the state dir grows more than its recorded ceiling, and the ceiling is edited in a visible file.

Next question: which writers produce the 2.4 GB, and does a single one of them account for most of it?
Next question: what do hooks actually open per call, so the hot tier's boundary can be set from data rather than guessed?

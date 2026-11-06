**Verdict: changes needed.** Two MEDIUM findings, both about failures breaking normal use. I only read the code. This session had no shell, so I ran no tests and took no timings.

**Findings**

1. MEDIUM — `plugin/lib/fmcore.py:777-784`. `log_event` has no fallback. A failed `fcntl.flock` (ENOLCK or ENOTSUP, for example `~/.claude` on NFS) raises before the write, so the event is lost and the hook sees an exception. The old plain append never took a lock. `_archived_last` (`fmcore.py:132`) opens archives with no `OSError` guard.
   - Failure scenario: an archive is root-owned or mode 000, for example after a `sudo fm tidy`. Right after a roll with an empty `keep`, the live ledger has size 0. Every `log_event` then hits `_archived_last` and raises `PermissionError`. That includes `tidy`'s own `ledger_rolled` event, so the ledger stays empty and every hook fails. Confidence: high.
   - Fix: wrap the lock and prev computation in `try/except OSError`. On failure, write the record without `prev`, which verify already reports as a gap. The event is never lost.

2. MEDIUM — `plugin/lib/fmcli.py:629` and `:910-911`. `_ledger_head(p)` and `fmledger.receipt(p)` are unguarded. `chain()` raises on any `OSError` other than `FileNotFoundError`, such as `PermissionError` on an archive. At `:629` the task is already marked done, so `fm task done --json` crashes after the state change. At `:910` the commit has already landed, so `finish` exits non-zero with a traceback. `fmcli.py:615` already shows the repo's pattern for this: a derived value must not make a finished task look failed. Fix: `try/except OSError` in both places, printing a short "Ledger: unreadable" line instead. Confidence: high.

3. LOW — `plugin/lib/fmledger.py:167,196`. A broken chain returns early with `head` still set to the genesis hash. `--json` and `_ledger_head` then report `e3b0c44298fc1c14` as the head. Fix: set `head=None` when `broken`.

4. LOW — `plugin/lib/fmledger.py:5,203-205`. The chain is unkeyed. An edited last line, or a chain rewritten to the end, verifies "OK" unless `--head` is passed. The receipt head is only printed, and Foreman stores it nowhere outside the ledger. Fix: log the head into the task brief (not the ledger) at finish, and have `verify-ledger` check it. Also say in the "Ledger OK" text that an edit to the last line is invisible.

5. LOW — `plugin/lib/fmtidy.py:259-262`. `_roll_ledger` keeps any line with an unparseable `ts` in the live file, so a cut line mid-month is reordered ahead of the lines archived around it. A clock stepping backwards across a month boundary reorders the same way. In both cases verify then reports a false break. The roll does not take the ledger `flock`, so a racing writer can still lose an event, as it could before this change. The chain itself stays valid in that case.

6. LOW — `plugin/lib/fmcore.py:783`. An old-version writer in the same project (a lane running different plugin code) ignores the `flock`. If it lands a line between the new writer's tail read and its write, verify reports a false break. Narrow window.

**Hot path (estimated, not measured).** Per event this adds one `flock`, one `fstat`, a 1-byte read and a 4 KB tail read, which is microseconds. If the last line exceeds 4 KB, the chunk grows 4x per pass. `chain()` runs only on `finish` and `done --json`. The real ledger is about 21.7k lines across two files, so I expect tens of milliseconds there.

**Acceptance criteria**
- Edit or delete makes verify exit 1 and name the line, and an untouched ledger exits 0: met by the code path and `Chain` tests (not run here). The break names both lines (`N doesn't follow N-1`).
- The receipt shows the head and the chain survives the roll: met. The roll copies lines verbatim, so hashes hold, and the empty-live case is covered by `_archived_last`. `test_chain_survives_the_monthly_roll` covers it.

**Lenses:** intent approve with nits (4); adversary approve with nits (4, 6); edge changes needed (1, 5); operator changes needed (1, 2); maintainer approve with nits (the `MASTER.md` row is a single huge line, and `rec["ts"]` is computed twice).

**Implicit decisions**
- Unkeyed SHA-256 truncated to 16 hex.
- Genesis is the hash of `b""`.
- `prev` is the first key.
- Unchained lines after the start are tolerated as gaps (exit 0).
- `ts` is re-stamped under the lock.
- The receipt is printed only without `--json`, just above the Landed line.
- Archive order is by filename.

**Not checked:** full test suite, real timings, the mixed-version race, and the `fmwatch`/`fmrecall` readers with `prev` present.

**Noticed:**
- Pre-existing: the roll opens the ledger in text mode and can raise `UnicodeDecodeError` on a bad byte (`fmtidy.py:256`).
- `fm doctor` could run verify-ledger as a cheap integrity check.

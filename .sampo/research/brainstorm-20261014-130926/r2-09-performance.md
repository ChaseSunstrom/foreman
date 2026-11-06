# Brainstorm — lens: performance

- **Shadow-run compact output per command family, then flip it on from measured fetch-backs** — FEATURE — value 5 — effort M — risk low — category: tokens
  Why: round 1 shipped compact output opt-in (~1.04M tokens/30 days measured, 44.3M chars of Bash results) but it's off because the user hasn't said yes. Assumption: a "shadow" mode that logs would-have-compacted size and whether the model later re-read the full file (via `fm out`) gives per-family evidence (pytest, git log, grep, build) so enabling is a data decision, not a leap.
  Done when: with shadow on, `fm cost` shows per-command-family would-save tokens and fetch-back rate, and a test proves no output is altered in shadow mode.

- **Replace Python spawns on size-gated PostToolUse hooks with a shell prefilter** — PERFORMANCE — value 4 — effort M — risk med — category: hook latency
  Why: bench p50 is 74-98 ms per Read hook spawn; 3,281 of 4,186 Reads spawned it for nothing, and compact output only acts on outputs over 6,000 chars. Assumption: a tiny `sh`/`case` check on payload length (or native `if`) can exit before Python starts for the common small case. Round 1 dropped if-scoping for Read because the saving was ~2 min/month, so scope this to PostToolUse Bash, where the hook runs on every command.
  Done when: bench shows PostToolUse Bash p50 under 15 ms for outputs below the threshold, and outputs above it still compact identically (golden test).

- **Make `fm bus watch` event-driven and reap orphaned watchers** — PERFORMANCE — value 4 — effort S — risk low — category: liveness cost
  Why: round 1 added a plugin monitor `foreman-mail` that streams bus mail; a monitor that polls costs CPU forever, and monitors from dead sessions can linger. Assumption: the watcher currently polls files on an interval; inotify (with a poll fallback on macOS) plus a heartbeat-stale self-exit removes both costs.
  Done when: an idle watcher uses ~0% CPU over 60 s in a test, and killing the parent session makes the watcher exit within 5 s.

- **Take one git porcelain snapshot per hook turn and enable fsmonitor and the untracked cache** — PERFORMANCE — value 4 — effort M — risk low — category: git speed
  Why: pack states 350 files and many hooks, gates and `fm check --affected` shell out to git status/diff. Assumption: several run in the same turn and each re-walks the tree. Cache by (HEAD, index mtime) in the turn, and have `fm doctor` offer `core.fsmonitor`.
  Done when: a counting test shows at most one `git status` per turn across hooks, and bench on a 10k-file fixture drops measurably.

- **Ship runner-specific failure digesters with golden tests** — FEATURE — value 4 — effort M — risk med — category: tokens
  Why: round 1 compact output keeps head, failure lines and tail by generic rules. The user's own steer: stored results start "✗ exit N" and metrics missed real failures, so failure detection precision matters. Assumption: pytest, cargo, tsc, go test and eslint each have stable failure formats a digester can keep exactly while dropping the passing noise.
  Done when: for each runner a fixture output with a seeded failure compacts to the failing test name, assertion and traceback, and no failure line is ever dropped (property test).

- **Parallelise and time-box `fm doctor` and the installer's plugin fetches** — PERFORMANCE — value 3 — effort S — risk low — category: startup
  Why: doctor now checks every Claude Code feature Foreman uses against the installed version, and the installer clones plugins and may install Python. Assumption: checks run serially and a hung network call stalls the whole run. Run independent probes concurrently with a per-probe timeout and print "timed out" rather than hanging.
  Done when: doctor finishes in under 3 s on a warm machine and an unreachable network yields per-check timeouts, not a hang.

- **Defer ledger fsync to stage transitions** — PERFORMANCE — value 3 — effort S — risk med — category: state I/O
  Why: assumption: every state write fsyncs for crash safety, and the many small ledger appends per turn make that the dominant I/O cost. Appends can be buffered and fsynced at step or stage boundaries and on Stop, with the torn-tail recovery already implied by earlier crash-safety ideas.
  Done when: bench shows lower per-append latency, and a kill -9 test loses at most the unsynced tail while the ledger still parses.

- **Lint context packs for duplicated blocks before any child sees them** — PERFORMANCE — value 4 — effort S — risk low — category: child tokens
  Why: this very pack repeats "The user's own words" in full twice and carries a ~2,000-line "ideas so far" list, and every `fm ideas` child pays for it on each lens. Assumption: the pack builder does no dedupe. Dedupe identical sections and collapse the ideas list to cluster counts with recent titles.
  Done when: building a pack with a duplicated section emits it once, and pack size on this project drops by more than 40% in a test.

- **Wild: Add a shell-level guard fast-path for provably read-only commands** — PERFORMANCE — value 4 — effort L — risk high — category: guard latency
  Why: wild. Assumption: the majority of Bash calls are `ls`, `cat`, `git status`, `grep` and similar with no redirects, substitutions or pipes to interpreters. A tiny allowlist matcher in `sh` or compiled form returns allow before Python spawns, while anything uncertain falls through to the full guard.
  Done when: replaying the real command corpus shows zero verdict differences from the full guard, and the fast path serves more than 60% of calls at under 5 ms.

- **Wild: Run overnight brainstorms and audits through the Batch API at half price** — FEATURE — value 3 — effort M — risk med — category: cost
  Why: wild. `fm ideas` fans out many lens children with `--max-budget-usd`; overnight work isn't latency-sensitive. Assumption: the user would trade a few hours of wait for roughly half the cost, and this fits `fm night`. It must be an explicit setting, because it sends pack content to an external service.
  Done when: with the setting on, `fm ideas --batch` submits all lenses as one batch, collects results next session, and the receipt shows the cost compared with the live run.

- **Wild: Defer heavy gates while on battery or thermally throttled** — FEATURE — value 2 — effort S — risk low — category: gate scheduling
  Why: wild. The user runs on a laptop-class Linux machine (hardened kernel) and the bench already judges by CPU time under load, so load awareness exists. Assumption: reading `/sys/class/power_supply` and thermal zones is cheap; full-suite runs can wait for AC or run reduced `--affected` sets, with a plain note saying what was deferred.
  Done when: simulated battery state makes `fm check` run the affected set only and print one line saying the full suite is deferred, and `--force` overrides it.

- **Wild: Replace wake-up polling with a compare-and-save "nothing changed" heartbeat** — PERFORMANCE — value 3 — effort M — risk med — category: idle cost
  Why: wild. Idle sessions waking on schedule re-read context to find nothing new, which costs cache and tokens. Assumption: the wake path can hash the queue, bus and ask state, and when the hash matches the last wake it skips the model turn entirely, or at most emits a one-line no-op, instead of nudging.
  Done when: a test with an unchanged state shows zero model turns from the wake path over 10 cycles, and any state change triggers a real wake within one cycle.

- **Hedge slow read-only children with a second cheaper attempt** — PERFORMANCE — value 3 — effort M — risk low — category: child latency
  Why: assumption: recon and lens children occasionally stall on a long tool chain. Round 1 added a per-child budget and effort but no tail-latency control. After p90 of past durations, start a Haiku twin and take the first valid structured result, then cancel the other.
  Done when: with an injected stalled child, the run completes using the hedge within p90 plus a margin, and the cancelled child's spend appears in the receipt.

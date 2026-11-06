# Brainstorm — lens: reliability

- **Run readers under shuffled determinism inputs** — FIX — value 3 — effort S — risk low — category: determinism
  Why: assumption: ordering-dependent output isn't tested. Hash-modulo selection and directory order have bitten before (a pack item shows hash-modulo picks needed a stable key). Windowed readers are now clock-tested, but nothing varies `PYTHONHASHSEED`, listing order, locale or TZ.
  Done when: a test runs `fm next`, `fm status`, `fm doctor` and the digest readers under 5 hash seeds and 2 directory orderings on one fixture home, and all outputs are byte-identical. A planted `set` iteration makes it fail.

- **Detect refile livelock in the self-advancing tower** — FIX — value 4 — effort M — risk low — category: unattended loops
  Why: the standing rule says a red sweep creates its own fix tasks and re-runs when they close. Nothing in the pack caps a fix that closes, leaves the sweep red, and is refiled.
  Done when: a fixture sweep that refiles the same brief hash 3 times stops filing. It parks the chain with one inbox line naming the three task ids and the unchanged red row, and a green sweep resets the count.

- **Open a landing breaker with a cooldown after a red main** — FEATURE — value 4 — effort M — risk med — category: unattended safety
  Why: the user granted "push to main at any time", and `fm ship` is gated by the full suite. A red main after a push, a revert, or a failed CI run should still stop further unattended landings. Existing ideas draft a revert but don't pause landing.
  Done when: a simulated red CI on the last pushed sha makes the next unattended `fm ship` refuse with the reason and the one command that clears it (a green re-run or a user ack). A pre-red push is unaffected.

- **Clear provably stale lockfiles** — FIX — value 3 — effort S — risk low — category: crash recovery
  Why: assumption: a kill (usage limit, OOM, suspend) mid-git or mid-ledger-write leaves `.git/index.lock` or an fm lock behind. "Explain who holds a lock" shows the holder; nothing clears the stale one.
  Done when: a fixture with a lock whose owner pid is dead and whose age exceeds N is removed by the next verb, which logs it. A lock with a live owner is untouched.

- **Mirror ledgers continuously to a second filesystem** — FEATURE — value 3 — effort M — risk low — category: durability
  Why: `fm drill --restore` rehearses a restore, but nothing keeps a live second copy. The tmpfs-adjacent paths in this environment (`/run/user/...`) make a single copy fragile.
  Done when: with `mirror_path` set, each ledger append is copied append-only. Deleting a mirrored line from the primary makes `fm doctor` name the divergence and the ledger, and unset means no behaviour change.

- **Share one retry budget and jitter across all lanes** — FIX — value 3 — effort M — risk low — category: thundering herd
  Why: assumption: ten lanes and the drive each back off alone, so they all retry in lockstep when the remote, GitHub or the API recovers. Backoff exists per caller, but nothing shares it.
  Done when: a simulated outage ending makes N concurrent fake callers retry at spread-out times (max burst ≤ a stated bound), and the receipt shows retries per dependency.

- **Snapshot `--json` schemas and gate breaking changes** — CLEAN — value 3 — effort M — risk low — category: contracts
  Why: the web UI, the pane and the Desktop tray all read `--json` output. A verb edit can break them silently, and there is no compat rule for key removal or type change.
  Done when: removing or retyping a key in any registered verb's `--json` fails the suite unless the schema version is bumped with a one-line note.

- **Run hooks and verbs from a deleted, unreadable or symlinked cwd** — FIX — value 3 — effort S — risk low — category: environment
  Why: assumption: worktree removal, `git clean` or a lane merge can delete the session's cwd mid-session, and the hook path calls `os.getcwd()`. The guard must fail closed or visibly, not crash silently.
  Done when: each hook run with a removed cwd exits with the declared fail-open or fail-closed outcome and writes a crash card, and no traceback reaches the model.

- **Generate a runbook line per drill fault** — FEATURE — value 3 — effort S — risk low — category: diagnosability
  Why: `fm drill` faults exist, and the open question asks what the user sees in the first minute after a fail-open.
  Done when: each drill fault has a registry entry giving the reader that must report first and the exact "Next:" command. A test injects the fault and checks that the real output contains that line.

- **Soak the long-lived web server** — PERFORMANCE — value 2 — effort S — risk low — category: soak
  Why: assumption: the 72-hour soak idea covers the drive but not `fm web`, which holds file handles and caches ledger reads.
  Done when: 100k requests and 1k ledger appends against the server leave RSS and open-fd growth under stated bounds, and a planted per-request leak fails it.

- **Score a "clean morning" forecast before each unattended night (wild)** — FEATURE — value 3 — effort M — risk low — category: calibration
  Why: wild. Before leaving, Foreman prints P(clean morning: no stops, no red, no rescue) from past nights, and the morning card scores it. This answers the open question about which unattended paths have never been run on a real clock, because the forecast is low for unseen paths.
  Done when: a fixture history yields a forecast that is stored, then scored in the next morning card, and a path with fewer than 3 runs is flagged "unseen".

- **Fuzz the verbs with an impatient user in a pty (wild)** — FEATURE — value 3 — effort M — risk low — category: interruption
  Why: wild. A scripted pty sends Ctrl-C, Ctrl-Z, resize and hangup at random moments in multi-step verbs (`fm ship`, `fm task finish`, `fm run`). Kill-point sweeps cover ledger writes but not signals mid-verb.
  Done when: 200 seeded interrupts leave no half-written state, and each leaves `fm doctor` green or naming one repairable item.

- **Drill a split-brain with two Foremen on one repo (wild)** — FEATURE — value 2 — effort M — risk med — category: concurrency
  Why: wild. Two drives with separate state dirs and different `HOME`s run on one repo, as when the user's laptop and desktop share a synced folder. This finds which claims, pushes and ledgers collide before a real conflict does.
  Done when: the drill reports every collision class it saw (claim, push, ledger, lock), and each is either refused with a reason or recorded as unprotected.

Next question: which numeric defaults (stall limits, windows, retry counts) have ever been replayed against the user's own history before they became defaults?
Next question: when `fm` fails to start at all (bad python, broken import, read-only home), what does the user see, and is that moment tested without `fm`'s own help?

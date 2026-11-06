# Brainstorm — lens: performance

- **Lint context packs for duplicated blocks before any child sees them** — FIX — value 4 — effort S — risk low — category: tokens
  Why: this pack carries "The user's own words" twice, verbatim, and repeats title lines across rounds, so every lens child pays for the same text again. Earlier ideas cap or order the pack but none catch exact duplicates.
  Done when: building a pack with a duplicated section emits it once, and a test asserts that no block over 200 chars appears twice in a built pack.

- **Replace Python spawns on size-gated PostToolUse hooks with a shell prefilter** — PERFORMANCE — value 4 — effort S — risk low — category: hook latency
  Why: Python hooks cost about 35 ms or more per spawn, and compact output must inspect every Bash result to find the few over 6,000 chars. A `head -c` size check in the hook command can exec Python only for big outputs. Assumption: most Bash outputs are small.
  Done when: bench shows p50 for a small-output Bash PostToolUse at or under 10 ms, and an output over 6,000 chars still gets compacted identically.

- **Run compact output in shadow first and enable it per command family from measured fetch-backs** — FEATURE — value 5 — effort M — risk low — category: tokens
  Why: compact output is built but off "until the user says yes", and it already saves about 1.04M tokens over 30 days. Shadow mode logs what would have been elided per family (pytest, git, build). It then checks whether the model re-fetched the full text from state/outputs.
  Done when: `fm doctor` lists each command family with its shadow tokens saved and its re-fetch rate, and a family with zero re-fetches over N runs is offered for one-keystroke enabling.

- **Make `fm bus watch` event-driven and reap orphaned watchers** — PERFORMANCE — value 3 — effort S — risk med — category: liveness
  Why: the plugin monitor shipped today runs a long-lived process per session. Assumption: it polls. A polling watcher costs wakeups all session, and a crashed session can orphan it. Its arming in live sessions is also still unverified.
  Done when: an idle watcher shows near-zero CPU wakeups (inotify with a polling fallback), and killing the parent session leaves no `fm bus watch` process after 10 s.

- **Ship runner-specific failure digesters with golden tests** — FEATURE — value 4 — effort M — risk low — category: tokens
  Why: generic head, failure-lines and tail wastes tokens where the runner's format is known. Stored results start with "✗ exit N", which shows runner output formats already matter. Static parsers for pytest, cargo, go test, tsc and ruff keep the exact failing assertions and drop the noise.
  Done when: a golden fixture per runner compacts a 50 KB failing log to under 2 KB while keeping every failing test name and assertion line.

- **Turn on git fsmonitor and untracked cache, and take one porcelain snapshot per hook turn** — PERFORMANCE — value 3 — effort S — risk low — category: git
  Why: assumption: tier-drift, scope, step-pointer and close checks each run `git status` or `git diff`, and on large repos those dominate hook time. This is not measured yet, so the first step is to profile it.
  Done when: bench reports git subprocess time per turn, which drops measurably on a 10k-file fixture, and a test shows one `git status` per turn for hooks sharing a snapshot.

- **Defer fsync in the ledger to stage transitions** — PERFORMANCE — value 2 — effort S — risk med — category: state writes
  Why: assumption: observe-only events fsync as much as transitions. Atomic rename is still needed everywhere, but a crash may lose a trailing observe event without harm. Gate this behind the crash-consistency test.
  Done when: the crash-injection test passes with the batched policy, and the ledger-write p95 on a spinning-disk-like tmpfs delay drops.

- **Parallelise and time-box `fm doctor` and the installer's plugin fetches** — PERFORMANCE — value 3 — effort S — risk low — category: install
  Why: doctor now checks every native feature against the CC version, and the installer clones and installs plugins serially. A first-run experience counts. Assumption: both run serially today.
  Done when: `fm doctor` wall time drops by 40% or more on the bench machine, and `install.sh --no-plugins` and the full install each print their elapsed time.

- **Wild: Add a shell-level guard fast-path for provably read-only commands** — PERFORMANCE — value 4 — effort L — risk high — category: guard latency
  Why: wild. Every Bash call spawns the Python guard, but most are `ls`, `git status` or `cat`. A tiny shell `case` allowlist could answer them in about 2 ms, validated by never differing from the full guard over the replay corpus. Risk is high, so it needs fail-closed behaviour.
  Done when: the replay corpus shows zero verdict differences across all fast-path commands, and bench p50 on those commands falls below 5 ms.

- **Wild: Run overnight brainstorms and audits through the Batch API at half price** — FEATURE — value 3 — effort L — risk med — category: cost
  Why: wild. Unattended rounds, such as the many-lens `fm ideas` run in this very session, do not need interactive latency. Assumption: the Agent SDK or API can submit them as a batch.
  Done when: `fm ideas --batch` submits lens prompts as one batch, collects them by morning, and `fm cost` shows the per-token price at about 50% of the interactive run.

- **Wild: Defer heavy gates while on battery or thermally throttled** — FEATURE — value 2 — effort M — risk low — category: scheduling
  Why: wild. Gate timeouts and flakes under load are already a known pain (bench judges CPU time under load). Reading power and thermal state lets Foreman run the full suite when plugged in and the affected tests otherwise. Assumption: laptop users exist.
  Done when: with a mocked battery state, `fm task finish` runs affected tests only and notes the full suite as deferred, then runs the full suite on AC.

- **Wild: Replace wake-up polling with a compare-and-save "nothing changed" heartbeat** — PERFORMANCE — value 2 — effort M — risk low — category: idle cost
  Why: wild. When the queue is idle, each wake costs a model turn that finds nothing. The monitor can hold the wake until the state hash changes or a deadline passes, so an idle session spends no tokens between events.
  Done when: a 1-hour idle fixture session with an empty queue makes zero model turns, and a new bus message wakes it within 5 s.

# Brainstorm — lens: bold bets

- **Prove the guard fires on every spawn path** — SECURITY — value 5 — effort M — risk low — category: guard
  Why: fork subagents are now on by default in `claude -p`, bypass mode is how Foreman runs, and the guard must never weaken. Nothing in the pack shows tests of the guard under forks, background shells, worktree agents or a `disableAllHooks` override in a cloned repo's local settings. Assumption: some paths have gaps.
  Done when: `fm doctor` runs a matrix (subagent, fork, headless `-p`, background Bash, project-local settings override) and each cell shows a seeded dangerous command refused. A cell where the guard is bypassed or unregistered fails the gate.

- **Seed the post-compaction frontier from zero-token miners** — FEATURE — value 5 — effort M — risk med — category: long runs
  Why: the user wants new ideas after compactions without burning usage, and the marathon found only 3 things across 7 compactions. Assumption: static sources hold much more. TODOs, lint output, uncovered lines, flaky-test history and open briefs can fill a ranked queue with no model call, so a compaction pops the next item instead of re-brainstorming.
  Done when: `fm frontier` lists at least 10 ranked candidates on this repo with zero model calls, and a forced-compaction marathon case picks its next work from that list.

- **Stagger parallel lanes to share one prompt-cache write** — PERFORMANCE — value 4 — effort S — risk low — category: cost
  Why: cost parity (T-1231) is the open fight, and builders launched together each pay the full cache write on the same prefix. Assumption: sessions with an identical prefix read each other's cache. Launching the first lane, waiting for its first response, then releasing the rest turns N writes into one write plus N-1 reads.
  Done when: a 3-lane Haiku run shows the later lanes' cache-read tokens above 80% of their prefix, and total cost falls versus simultaneous launch.

- **Run every verify command offline in the existing sandbox** — SECURITY — value 4 — effort M — risk med — category: sandbox
  Why: verify commands are model-written, then run by the harness, and `fm run --sandbox` already uses bubblewrap. A proof with no network, a read-only `$HOME` and no credential paths can't exfiltrate and can't pass because of a live service. A criterion opts in to network with a reason.
  Done when: a criterion whose verify command curls an external host fails offline with a clear note, and the same criterion passes after being marked `net`.

- **Lock down the web UI against rebinding and cross-origin calls** — SECURITY — value 4 — effort S — risk low — category: web UI
  Why: the web UI is the only listed surface and sits next to approvals and task control. Assumption: it listens on localhost over HTTP. Per-launch token, strict Host and Origin checks, and no state-changing GET close DNS-rebinding and drive-by-tab attacks.
  Done when: a test sends a mutating request with a foreign Origin, a rebinding Host header, and no token, and all three get 403.

- **Make the web UI an installable phone PWA with content-free push** — FEATURE — value 4 — effort M — risk med — category: devices
  Why: push alerts and phone replies are on the list, but no idea keeps content off third parties. A payload-less Web Push says only "Foreman needs you", and the phone then fetches details from the user's own host over LAN or Tailscale.
  Done when: the web UI installs from a phone browser, a blocked task triggers a notification with no task text in the payload, and tapping it opens that task.

- **Show a cache countdown in the pane** — FEATURE — value 3 — effort S — risk low — category: UI
  Why: usage matters to this user, and idle gaps past the cache TTL silently double a turn's cost. Assumption: the pane can read the last-turn timestamp from the ledger. A small timer (warm 3:12 → cold) lets the user decide whether to send the next prompt now.
  Done when: the pane shows a countdown that resets on each turn and turns to "cold" at TTL, with a test on a fixed clock.

- **Flag conflicts between CLAUDE.md or memory and Foreman's injected rules** — FIX — value 3 — effort S — risk low — category: simplicity
  Why: the user's own instructions ("commit often", "skip tests for docs") can fight Foreman's one-task and prove-first notes. The model then spends turns reconciling, and the 2.1.304 skill-listing resend makes every extra rule dearer. `fm doctor` has no such check in the pack. Assumption: a keyword-level check catches most real conflicts.
  Done when: `fm doctor` reports a planted "never run tests" line in CLAUDE.md as conflicting with the prove rule, and stays quiet on a clean file.

- **Wild: Make Foreman the hook conductor for the user's whole setup** — FEATURE — value 4 — effort L — risk high — category: hooks
  Why: prompt/agent hooks are now capped at 12 concurrent per event, and other plugins' hooks add latency Foreman gets blamed for. Assumption: Foreman can read the merged hook config. It would time each installed hook, report the costly ones, and optionally dispatch them from one process in a stated order.
  Done when: `fm hooks` lists every hook on each event with median milliseconds, and dispatching a two-plugin setup through the conductor gives the same hook outputs as running them separately.

- **Wild: Replicate the benchmark across users' machines** — FEATURE — value 3 — effort L — risk med — category: benchmarks
  Why: every site claim must be measured, and one machine's three runs invite doubt. An opt-in command runs the spec suite at a $2 Haiku cap and writes a numbers-only result file. The user chooses whether to share it, and the Benchmarks page can show replicated intervals.
  Done when: `fm bench replicate` runs offline-capable and emits a JSON file with no paths or prompts. A validator rejects any file that contains them.

- **Wild: Draw pane charts as real pixels with the kitty graphics protocol** — FEATURE — value 2 — effort M — risk low — category: UI
  Why: the Today charts are character cells. In terminals that support kitty graphics, smooth lines and a work-bar gradient would feel like a different product. Assumption: the user's terminal supports it; fall back to cells otherwise.
  Done when: a capability probe picks the pixel path in a graphics terminal and the cell path elsewhere, and both render the same data in a golden test.

- **Wild: Offer a read-only "ledger answers" side prompt** — FEATURE — value 3 — effort M — risk low — category: user value
  Why: asking "what did you change and what's left?" costs a model turn and context that is later compacted away. Templated answers drawn from the ledger (steps, proofs, diffs) would cost zero tokens. Assumption: most status questions fit a dozen templates.
  Done when: `fm ?` answers "what's left" and "what failed" from the ledger with no model call, and says "I can't answer that from the ledger" otherwise.

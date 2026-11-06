# Brainstorm — lens: performance

- **Run compact output inside lanes first** — PERFORMANCE — value 4 — effort S — risk low — category: tokens
  Why: compact output is built and measured at about 1.04M tokens/30 days saved, but is off "until the user says yes". Lane builders are Foreman's own headless children, so their output is delegated work the user never reads and needs no yes. Assumption: a lane brief can pass an env flag or settings overlay.
  Done when: a lane's Bash output over 6,000 chars arrives as head + failure lines + tail with a spill-file path, while the main session still shows full output.

- **Split mail into wake and piggyback lanes** — PERFORMANCE — value 4 — effort M — risk med — category: liveness
  Why: the `foreman-mail` monitor streams every bus message, and each delivery can cost a full model turn. Assumption: most mail is FYI. Only needs-action mail should wake the session. FYI mail rides the next turn as `additionalContext` from the existing PostToolUse or UserPromptSubmit hooks, with no extra turn.
  Done when: 5 FYI messages sent to an idle-free session produce 0 extra model turns and all 5 appear in the next turn's context, while a needs-action message still wakes an idle session.

- **Set a savings floor that auto-drops PERF tasks** — FEATURE — value 4 — effort M — risk low — category: discipline
  Why: the user dropped the Read-hook `if` scoping (about 2 min/month) and delta reads (about 109 tokens/30 days) only after someone measured them. Make that a rule. A PERF task needs a measured baseline and a projected monthly saving from the user's own telemetry. Below a floor, it closes as dropped with a receipt.
  Done when: `fm task new PERF:` with a measured saving under the floor is refused or auto-dropped with the number shown, and one above it proceeds.

- **Attribute every prompt-cache miss to a cause** — FEATURE — value 4 — effort M — risk low — category: cache economics
  Why: no idea in the pile gives live cache evidence for the main session. Foreman could read `cache_read` against `cache_creation` per turn from the transcript. It would label each miss as TTL expiry, a changed prefix (rules or CLAUDE.md edit, hook-injected prefix bytes), or `/compact`. It would then rank causes by token cost. Assumption: transcript usage fields are reliably present.
  Done when: `fm cost --cache` lists the last 20 misses, each with a cause label and token cost, verified against a hand-built transcript fixture.

- **Memoize version probes and single-flight shared derived work** — PERFORMANCE — value 3 — effort S — risk low — category: startup
  Why: round 1 made `fm doctor` check every Claude Code feature against the installed version, and each check may spawn `claude --version`. Many concurrent sessions and lanes will each repeat this. Assumption: probes and map or doctor refreshes run at SessionStart. Cache probe results by binary mtime+size. Take a cross-process lock so concurrent sessions share one computation.
  Done when: 8 simultaneous SessionStarts run the version probe once (counted via a probe counter), and a changed `claude` binary invalidates the cache.

- **Run housekeeping and gates in a low-priority class** — PERFORMANCE — value 3 — effort S — risk low — category: scheduling
  Why: recent commits added `fm tidy` pruning and snapshot pruning, and bench had to move to CPU time "under load", so contention is real. Run tidy, map refresh and gate subprocesses under `nice`/`ionice` (or a systemd-run CPUWeight) so hooks and the model's tool calls win. Hooks never run housekeeping inline.
  Done when: with a full gate run in progress, hook p95 latency rises by less than 20% versus idle in `bench_hooks.py`, and no hook invocation runs tidy.

- **Bound every regex over tool output** — FIX — value 3 — effort S — risk low — category: hook latency
  Why: compact output and the runner-failure scanners run regexes over outputs of up to MBs on every PostToolUse (44.3M chars of Bash results in 30 days). One pathological log line could stall a hook until timeout. Add linear-time scanning or a size cap per scan, plus a backtracking fuzz test.
  Done when: a 5 MB adversarial output finishes the compact and failure-scan hooks in under 200 ms in a test, and the fuzz corpus runs in the suite.

- **Reuse the lane's verify when the merged tree is identical** — PERFORMANCE — value 3 — effort S — risk low — category: gates
  Why: lane-merged tasks re-run verify at close even when the merge was a fast-forward of the exact tree the lane verified. Key the verify by tree hash plus command and skip the repeat when they match. Assumption: the lane records its verified tree hash.
  Done when: closing a fast-forward-merged lane task runs 0 verify commands and cites the lane's evidence, while a non-identical merge still re-runs them.

- **Budget the `fm page` catalogue** — PERFORMANCE — value 3 — effort S — risk low — category: artifact
  Why: catalogues now hold hundreds of ideas, and the page is one self-contained HTML Artifact. Render clusters first, defer idea bodies behind collapsed lazy sections, and enforce a byte cap with a stated fallback.
  Done when: a 1,500-idea catalogue renders under a fixed byte cap and opens with only cluster rows in the DOM.

- **Suspend UI polling when Desktop is hidden** — PERFORMANCE — value 2 — effort S — risk low — category: desktop
  Why: Desktop runs as a tray app that is usually hidden. Assumption: it holds a live `fm serve` or `fm ui --follow` stream. Pause the stream when the window is occluded or tray-only and resume with a catch-up diff on show.
  Done when: with the window hidden, the app and `fm serve` show near-zero wakeups over 60 s, and reopening shows current state within 300 ms.

- **Let a cheap child digest big outputs and whisper only anomalies** — FEATURE — value 3 — effort M — risk med — category: tokens — wild
  Why: compact output's failure-line regexes only know formats they were written for. A Haiku child could read the spill file in the background and, only if it finds something odd, inject one line next turn via `additionalContext`. It must never block the turn. Assumption: the call costs less than the tokens it saves.
  Done when: on a fixture with an unrecognized-format failure buried in 50k chars, the digest surfaces it within one turn, and on a clean output nothing is injected.

- **Compact the context when the prompt cache is already cold** — PERFORMANCE — value 3 — effort M — risk med — category: cache economics — wild
  Why: after the 5-minute TTL lapses, the next turn pays a full cache write anyway, so shrinking the prefix at that point is nearly free. Foreman would nominate the compact moment (idle past TTL, at a step boundary) instead of letting it land mid-warm. Assumption: Foreman can only suggest or trigger it through an existing path such as the Stop hook or tmux.
  Done when: in a replayed transcript, nominated compacts occur only after TTL expiry, and the estimated cache-write tokens avoided are logged per compact.

- **Export any session as a Perfetto trace** — FEATURE — value 2 — effort M — risk low — category: observability — wild
  Why: the pile has flame strips and waterfalls but no format an outside profiler can open. Emit Chrome-trace JSON from the ledger and transcript timestamps, with hooks, gates, children, user-wait and idle as tracks. Assumption: event timestamps exist for each.
  Done when: `fm trace SESSION` writes JSON that loads in ui.perfetto.dev with at least the hook, gate and idle tracks populated.

- **Add a hook-time ledger that outlives bench** — PERFORMANCE — value 2 — effort S — risk low — category: regression
  Why: bench runs on demand with 20 runs and judges CPU time, but real-world hook latency on the user's machine drifts unseen. Sample 1-in-N live hook invocations (wall and CPU) into a small rolling table that `fm doctor` compares against the bench baseline and flags on drift.
  Done when: after 200 live hook calls, `fm doctor` prints live p50/p95 per hook next to the bench baseline and flags a hook whose p95 is over 1.5× baseline in a seeded-slowdown test.

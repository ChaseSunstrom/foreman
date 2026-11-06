# Brainstorm — lens: approaches

- **Escalate the worker model only when the verify stays red** — FEATURE — value 5 — effort M — risk med — category: cost
  Why: Haiku already passes the long sessions 6/6, and `fm code --worker` has a harness-run verify that can act as the oracle. Start each step on the cheapest worker and move up one tier only after the verify fails. Assumption: `fm code` can name an ordered worker list.
  Done when: a seeded task whose verify fails on a fake cheap worker is retried on the next tier and closes, and the ledger records which tier passed.

- **Close a task only if the suite's failure set didn't grow against the base** — FEATURE — value 4 — effort M — risk med — category: verification
  Why: the user asked for spec-suite round 2 with "regressions elsewhere", but a green criterion verify says nothing about collateral damage. Run the full suite once on the base tree (cached by tree hash) and diff the failing sets.
  Done when: a fixture change that breaks an unrelated test is refused at close and names the new failure; a pre-existing red isn't blamed.

- **Check that every noun, number and path in the request lands in a criterion** — FEATURE — value 4 — effort M — risk med — category: intake
  Why: long sessions are graded by hidden tests per sub-request, and plain Claude lost 3 of 6 runs by dropping details. A zero-token lexical coverage check at plan time lists the uncovered tokens as "cover or mark out of scope". Risk: false positives.
  Done when: a plan that omits a number stated in the request gets a one-line uncovered-token note, and the same plan passes once the number is covered or waived.

- **Record standing grants as a scoped, expiring ledger entry** — FEATURE — value 4 — effort M — risk med — category: autonomy
  Why: the user said "no need to ask me, feel free to release at any time, keep going" after being asked about releases repeatedly. A grant stored with scope (release and push on this repo) survives compaction and new sessions, is shown by `fm`, and is revocable. It never extends to other actions.
  Done when: after a grant, a fresh session doesn't ask about releasing, an unrelated push still asks, and `fm grants` lists and revokes it.

- **Add `fm ship`: bump, notes from closed tasks, gates, push, watch CI** — FEATURE — value 4 — effort M — risk low — category: release
  Why: six release requests followed the same shape, and CI went red after pushes twice (3.12 timing, macOS). Assumption: releases are hand-driven today. On a red run, capture a FIX brief carrying the failing annotations.
  Done when: against a fake remote, `fm ship` does the bump, tag and push, and a stubbed red CI run yields a captured brief with the annotation text.

- **Interrupt benchmark runs with scripted mid-run corrections** — FEATURE — value 4 — effort M — risk med — category: benchmark — wild
  Why: the user's real pattern is steer, drop and pushback, but the benchmarks send eight static requests. A scripted persona injects "actually, rename X instead" or "drop request 3" at set points, and hidden tests check the correction was honoured.
  Done when: a long-session case with one mid-run steer grades the old behaviour as failing and the steered behaviour as passing, and the page reports a steer-handled rate.

- **Inject a recall note only for lessons that have prevented something** — PERFORMANCE — value 3 — effort S — risk low — category: context tax
  Why: recall notes are 12 KB of 130 KB edit-time notes, and T-0217 (lesson confidence) is deferred. Use it as the filter: a lesson earns injection by a first-time pass after its recall.
  Done when: a replayed session injects fewer recall bytes than the baseline, and a lesson with no preventive record is no longer injected.

- **Fold the output-style reminder into the cached rules file** — PERFORMANCE — value 3 — effort S — risk med — category: context tax
  Why: Claude Code's per-turn output-style reminder is 2.1% of context, above the whole rules file (1.2%). Assumption: Foreman's style causes it. Measure the same text moved into the rules file, and keep it only if bench quality holds.
  Done when: `fm cost` shows the reminder share near zero on a fresh session and the Haiku long-session pass count is unchanged.

- **Run the timing tests under a slow-runner emulation before push** — CLEAN — value 3 — effort S — risk low — category: CI
  Why: CI was red because a 5 s hook budget broke on slower runners, and CPU-time bounds needed a rework. Run the suite pinned to one core under `nice` as a gate flag.
  Done when: `fm doctor --slow` reproduces the old per-task-process queue failure on the pre-fix code and passes on current code.

- **Scrub secrets from ledger, lessons and captured output at write time** — SECURITY — value 3 — effort M — risk med — category: privacy
  Why: 1.2.37 guards credential reads, but a pasted key in a command output or request can still land in a lesson that is recalled into context later. Assumption: nothing scrubs stored text today.
  Done when: a fixture with a fake AWS key in command output leaves no match in `.foreman` after close, and a lesson written from it carries a redaction marker.

- **Add a stall watchdog for unattended runs** — FEATURE — value 3 — effort M — risk med — category: reliability
  Why: the marathon and long-session work depends on runs that keep going. T-0798 (recovery) is deferred and nothing nudges a run wedged on a prompt. After N quiet minutes, nudge once, then end with a plain "stalled at step X" note.
  Done when: a fake `claude` that stops responding triggers one nudge and then a stall note within the configured time.

- **Add `fm reverify <sha>` to re-run a commit's recorded proof in a clean worktree** — FEATURE — value 3 — effort M — risk low — category: trust — wild
  Why: proofs exist only as claims in the ledger. Anyone can re-execute one in a throwaway worktree, and the same verb can bisect which later commit broke it.
  Done when: for a commit with a recorded proof, `fm reverify` exits 0, and after a deliberately breaking commit it names that commit.

- **Expose the read-only verbs as an `fm mcp` server for other CLIs** — FEATURE — value 3 — effort M — risk med — category: reach
  Why: T-0335 to T-0337 are blocked on each CLI's differing hook surface, while MCP is shared. Serve guard-check, task status and the proof list there. Assumption: the existing mcp-server template is a usable base.
  Done when: a stdio MCP client lists the tools and gets the same guard verdict as `fm guard try`.

- **Speak the one-line state aloud with a local TTS** — FEATURE — value 2 — effort S — risk low — category: devices — wild
  Why: assumption: people leave long runs and walk away. A local engine (espeak or piper) says "task 3 needs you" or "queue finished" on opt-in, and nothing leaves the machine.
  Done when: with the setting on, a stubbed TTS command is called once per needs-you event and never when the setting is off.

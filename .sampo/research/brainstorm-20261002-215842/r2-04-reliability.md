# Brainstorm — lens: reliability

- **Add a Foreman self-test canary at session start** — FEATURE — value 5 — effort M — risk low — category: reliability
  Why: assumption: with 13 hooks, a mod, and a Python CLI, silent breakage (hook not firing, mod/fm version skew, plugin update half-applied) looks like "Foreman ignored me". The drive-stall report (T-0176) was found by the user, not Foreman.
  Done when: `fm doctor --canary` (auto-run at SessionStart, <200 ms) fires a synthetic event through each hook and the mod's `process.run` path, and a deliberately broken hook produces one visible line naming it.

- **Version-stamp the fm/mod/hooks trio and refuse mismatches loudly** — FIX — value 4 — effort S — risk low — category: compatibility
  Why: the mod calls `fm` via `process.run` and relies on `fm ui --json`; a plugin update needs its own yes, so the pieces can drift (the mod targets Claude Code 2.1.287 early-access API). assumption: no contract version is checked today.
  Done when: `fm ui --json` includes `contract: N`; the mod shows a one-line "update needed" band instead of rendering garbage when N differs, covered by a test with a fake old fm.

- **Write a decision journal for every drive-mode stop** — FEATURE — value 4 — effort S — risk low — category: observability
  Why: the T-0176 report ("ended its turn on 'Next: …' and didn't continue") was only diagnosable by guesswork. Existing ideas cover a watchdog and a flight recorder; this is the cheap, narrow core: why the Stop hook allowed or blocked.
  Done when: each Stop-hook run appends one line (reason code, queue depth, elapsed) to the record, and `fm why-stopped` prints the last one.

- **Make gate runs interruptible and resumable** — PERFORMANCE — value 4 — effort M — risk med — category: gates
  Why: one project's `cargo test` takes a median of 8 minutes about once per task, and gates cost 18.8 hours; a session death or compact mid-gate loses the whole run. assumption: gates are not checkpointed.
  Done when: killing a gate mid-run and resuming reports "resumed, N of M suites already passed for tree hash H" and skips them.

- **Add a reliability budget for the user's yes prompts** — FIX — value 3 — effort S — risk low — category: autonomy
  Why: protected-core edits and plugin updates each need a user yes; unattended multi-day drive stalls on them. The pack says the user wants full autonomy.
  Done when: a blocked-on-yes state parks that task, continues with other queue tasks, and shows one "waiting on you" card listing all parked approvals.

- **Wild: Run a shadow Foreman that replays the last N real sessions against the new version before release** — FEATURE — value 4 — effort L — risk med — category: regression
  Why: wild; 287 real tasks of ledger data exist. Replaying recorded event streams through new hooks and checking that the resulting stages and refusals are unchanged would catch regressions like the drive stall before the user does.
  Done when: `fm replay --against HEAD` reports zero stage/gate divergences over a fixture set of recorded sessions, and a seeded bug is caught.

- **Wild: Give hooks a "dead man's switch" heartbeat** — FEATURE — value 3 — effort M — risk low — category: monitoring
  Why: wild; if no hook event has been recorded for several minutes while tools are clearly running (the mod sees tool rows), something is wrong. The mod can detect the absence of events, which a hook can't.
  Done when: with hooks deliberately disabled, the mod shows a "Foreman is blind" warning within 60 s, and it clears when hooks return.

- **Wild: Add a "trust score" per claim in the done evidence** — FEATURE — value 3 — effort M — risk med — category: verification
  Why: wild; "done" requires recorded evidence, but evidence ages and gets reused. Scoring each item by freshness, whether it ran against the current tree hash, and whether it was run in-session would let the verify step demand only the weak ones.
  Done when: `fm task done` lists evidence with fresh/stale tags, and stale evidence for a changed file blocks done with the specific item named.

- **Make the guard fail-closed only for destructive classes, fail-open otherwise, and test the split** — FIX — value 3 — effort S — risk med — category: safety
  Why: T-0087 (hook circuit breaker) and the "regex speed bump" limitation conflict: a crashing guard either blocks all work or lets everything through. assumption: current behavior on guard exceptions is undefined.
  Done when: an injected guard exception allows `ls` and blocks `rm -rf` with a visible "guard degraded" notice, both asserted in tests.

- **Snapshot the record before each compaction and verify it after** — FIX — value 4 — effort S — risk low — category: resume
  Why: the claim is "resumes at the exact step after /compact"; nothing is said about verifying it. Context rot was a key complaint, and a silent resume mismatch is the worst kind.
  Done when: post-compact, Foreman compares the pre-compact task/step/criteria hash to the live record, and any mismatch is shown in one line and logged; a test simulates a corrupted record.

- **Wild: Add a nightly "Foreman fire drill" in a throwaway worktree** — FEATURE — value 3 — effort L — risk low — category: chaos testing
  Why: wild; a scripted tiny project exercised end to end (capture→done, kill mid-step, compact, resume, drive on a 3-task queue) would show breakage in the whole loop that unit tests can't.
  Done when: `fm drill` passes on a clean install in under 2 minutes, and an injected resume bug makes it fail with the step named.

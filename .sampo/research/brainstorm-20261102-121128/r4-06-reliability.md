# Brainstorm — lens: reliability

- **Probe the upstream CLI contract daily** — FIX — value 5 — effort M — risk low — category: compatibility
  Why: Foreman rides on Claude Code, Codex, Gemini and opencode hook and flag schemas, and the foreman-ui mod is pinned to Claude Code 2.1.301. T-1217 (pane paint) and T-0337 (Gemini AfterAgent) are both upstream-drift symptoms. Version-skew checks cover Foreman's own parts, not upstream's.
  Done when: a nightly job runs each installed harness's `--version` and a recorded hook/flag fixture probe, and `fm doctor` names any harness whose contract changed since the last green run (tested with a faked version string).

- **Make foreman-ui disarm itself on a version mismatch** — FIX — value 4 — effort M — risk med — category: mod safety
  Why: the mod patches the Claude Code UI, and T-0418 (update the installed mod) is still blocked. A silent mismatch can break the user's main interface. Assumption: today it fails by rendering badly, not by stepping aside.
  Done when: with a faked newer Claude Code version, the mod loads nothing, prints one line saying why, and plain Claude Code starts normally.

- **Ship a POSIX-sh rescue doctor for when `fm` won't start** — FEATURE — value 4 — effort S — risk low — category: recovery
  Why: `fm doctor` is Python run by `fm`, so a broken import, a missing interpreter or a half-written install takes the diagnostic down with it. The "hook falls back to the committed library" fix is the same class of problem.
  Done when: with `fm`'s lib directory renamed, `plugin/bin/fm-rescue` exits non-zero and prints the missing piece and the one repair command.

- **Audit where durable state lives against tmpfs and logout** — FIX — value 4 — effort S — risk low — category: durability
  Why: the child working directory is `/run/user/1000/fm-children-1000`, a tmpfs wiped at logout or reboot. Nothing in the pack shows which Foreman state (claims, journals, night tick output, child results) lives there.
  Done when: a test lists every path Foreman writes, flags any under `$XDG_RUNTIME_DIR` or `/tmp` that a reader later expects to survive a reboot, and passes with none flagged or each justified.

- **Chain ledger records with hashes and scrub them nightly** — SECURITY — value 4 — effort M — risk low — category: integrity
  Why: Foreman trusts ledgers it wrote itself. Torn-write fuzz catches partial lines, but not a silently truncated, edited or dropped record, and the open question about a missing record class is exactly that.
  Done when: the night tick verifies the chain, and `fm doctor` names the first broken record. A test deleting a middle line is caught.

- **Fence ledger writes across concurrent writers** — FIX — value 4 — effort M — risk med — category: concurrency
  Why: parallel lanes, the night tick, `fm drive`, hooks and several harnesses all append to shared state. Heartbeats cover task claims, not ledger writes.
  Done when: a stress test with 8 processes appending for 10 seconds yields no lost or interleaved records, and a stale-token writer is refused.

- **Soak the drive with a scripted fake agent** — FEATURE — value 4 — effort M — risk low — category: testing
  Why: the pack shows no zero-token way to run the drive for hours. Leaks in fds, memory or ledger growth only show over long runs, and real-model soaks cost usage.
  Done when: a fake agent replays canned transcripts for a simulated 8 hours on a fake clock, and the test asserts bounded RSS, open fds and ledger bytes per task.

- **Freeze feature work when a verb burns its error budget** — FEATURE — value 3 — effort M — risk low — category: SLO
  Why: the standing rules reward growth, and T-2503 handles lean only for unmeasured growth. Nothing ties Foreman's own verb failure rate (from `fm outcomes`) to a stop on new capabilities.
  Done when: with a verb's 7-day failure rate above its threshold, `fm next` offers a fix task first and `fm doctor` says the budget is burned.

- **Quarantine a lesson that preceded a failure** — FEATURE — value 3 — effort M — risk low — category: memory safety
  Why: T-0217 raises lesson confidence on success, but a recalled lesson that led to a wrong action has no downgrade path. Assumption: lessons are recalled without a failure link.
  Done when: a lesson recalled in a session whose task later failed its proof drops in confidence and is flagged for review after 2 such events.

- **Refresh test fixtures from real captures and flag drift** — CLEAN — value 3 — effort M — risk low — category: test realism
  Why: plugin/tests holds 404 files with hand-built fixtures like `fixtures/instruments/repo/app.py`. Green tests on stale fixtures prove little once real hook payloads change.
  Done when: a script re-captures a sample hook payload from each harness and fails the suite if the fixture's keys differ.

- **Wild: Rewind Foreman state to before a bad write** — FEATURE — value 3 — effort L — risk med — category: recovery — wild
  Why: assumption: undoing a landed task undoes code, not ledger and state damage. A content-addressed snapshot per tick would let `fm rewind` restore both.
  Done when: after a deliberately corrupted ledger write, `fm rewind --to <tick>` restores state and `fm doctor` is green.

- **Wild: Run a bare-minimum shell tripwire in a second language** — SECURITY — value 3 — effort S — risk low — category: independent witness — wild
  Why: assumption: the Python tower cannot report its own total failure. A 30-line sh timer checks for a fresh guard decision and test-gate timestamp and notifies if both are stale. This is not the existing dead-man's-switch idea, because it also checks whether hooks are still firing.
  Done when: killing the hook dispatcher in a scratch home makes the tripwire notify within one interval.

- **Wild: Replay each release against its own past inputs before it installs** — FEATURE — value 4 — effort L — risk med — category: regression — wild
  Why: assumption: self-change gates measure speed and the suite, not behaviour on real inputs. Replaying the last 100 recorded hook inputs through the new build and diffing verdicts would catch silent guard changes.
  Done when: the replay reports zero changed guard verdicts, or lists each change for approval before `fm ship`.

Next question: which Foreman-written state would be unrecoverable today if only `$HOME` survived, and which if only the git repo survived?
Next question: what does Foreman do when the upstream harness is up but its model returns a degraded or empty answer, and who notices?

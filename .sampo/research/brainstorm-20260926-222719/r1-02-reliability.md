# Brainstorm — lens: reliability

- **Split the guard into a fail-closed safety core and fail-open workflow gates** — SECURITY — value 4 — effort M — risk med
  Why: assumption: the "fail-open" self-monitoring covers every hook, so a crash in the guard lets a dangerous command through. Put the dangerous-command and protected-path checks in one tiny stdlib module that has no imports from the rest of the lib. If the main path errors, it falls back to a built-in deny list. Workflow gates such as evidence and nudges stay fail-open.
  Done when: a test injects an exception into the hook's non-safety code and `rm -rf ~` is still denied, while an ordinary edit is still allowed.

- **Redact secrets at the single state-write chokepoint** — SECURITY — value 4 — effort M — risk med
  Why: state stores verify-command output, evidence, logs and checkpoints, and `fm serve`, digests and `fm notify` re-emit them. Only `fm share` is privacy-filtered. Assumption: outputs like `env` or a token in a curl line can land in evidence unfiltered.
  Done when: recording evidence whose output contains a fake `AKIA…` key or `Authorization: [REDACTED] stores `[redacted]`, and a grep of the state dir finds neither.

- **Dedupe hook events by tool_use_id** — FIX — value 3 — effort S — risk low
  Why: assumption: a resumed or replayed session can deliver a PostToolUse twice, which would double-count evidence, thrash counters and edit counts. Keep a bounded seen-id set per session and ignore repeats.
  Done when: replaying the same PostToolUse payload twice leaves the evidence entry, edit count and thrash counter identical to one delivery.

- **Bind evidence to a hash of the criterion text and verify command** — FIX — value 3 — effort S — risk low
  Why: the earlier idea binds evidence to the tree hash, but a mid-task amendment can rewrite a criterion or its command while old evidence still satisfies the gate. Assumption: `fm task done` matches evidence by criterion id, not by content.
  Done when: editing a criterion's verify command after its evidence was recorded makes `fm task done` report that criterion as unproven.

- **Keep rolling, bounded snapshots of the state dir with a one-yes restore** — FEATURE — value 4 — effort M — risk low
  Why: the earlier ideas cover crash-safe writes, `--fsck` and plugin rollback, but none of them recover state that is already corrupted or wrongly compacted. Take a snapshot before any migration, compaction or `fm tidy` and keep the last N.
  Done when: after deliberately truncating a brief, `fm doctor --restore` recovers it from the latest snapshot, and the snapshots stay under the size cap.

- **Make the suite hermetic and order-shuffled, with a HOME tripwire** — CLEAN — value 3 — effort S — risk low
  Why: 474 tests around a state tree under `~/.claude/foreman` risk writing to real state or depending on run order. Existing variant runs cover interpreter and locale, not order or isolation. Run with a sentinel HOME, randomized order, and a check that no file outside the temp dirs was touched.
  Done when: the suite passes under three random seeds, and a deliberately leaking test fails the run.

- **Pin the project root per session and flag writes that escape it** — SECURITY — value 3 — effort M — risk med
  Why: assumption: after a `cd` into another repo or through a symlink, an edit could land in a tree that the active task doesn't own. Scope globs and rebind-on-branch don't cover this. Resolve the real path against the root pinned at SessionStart.
  Done when: an Edit whose real path is outside the pinned root, including via a symlink, is denied with a one-line reason.

- **Compile-check plugin edits immediately when developing Foreman itself** — FIX — value 3 — effort S — risk low
  Why: Foreman's hooks run from the same `plugin/lib` that improve tasks edit, so one syntax error can brick the guard mid-task. Rollback and version-change smoke tests fire later. Run `py_compile` plus an import check on each edited plugin file in PostToolUse and emit one note on failure.
  Done when: editing a plugin file to introduce a syntax error produces a note naming the file and line on the next turn.

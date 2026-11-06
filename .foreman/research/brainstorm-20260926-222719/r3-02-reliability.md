# Brainstorm — lens: reliability

Reliability is heavily covered already (crash safety, fault injection, leases, canaries, fsck), so these seven target gaps at the seams between components. All are new; none is a rehash.

- **Re-arm change-suppressed notes after compaction, clear and resume** — FIX — value 4 — effort S — risk low
  Why: the per-turn "Next" note is sent only when it changed. After PreCompact or a resume the model has lost that text, but the hook still records it as delivered, so the model can go on with no guidance. This is my reading of the pack, not a reproduced failure. Assumption: the delivered-hash lives in state and isn't reset on compact or resume.
  Done when: a test that simulates compaction, then sends a prompt with an unchanged next-action, sees the full Next note re-emitted exactly once.

- **Fuzz the brief round-trip with hostile text** — FIX — value 4 — effort M — risk low
  Why: user requests, pasted errors and lessons are written into markdown plus frontmatter briefs. Text containing `---`, `key: value` lines, CRLF, tabs, unicode or a very long line could corrupt parsing and make `fm focus` or `done` misbehave. The suite has a state-machine fuzz, but no idea above covers a format round-trip. Assumption: the parser is hand-rolled and not tolerant of all of this.
  Done when: a seeded property test (parse(write(x)) == x over 5k generated briefs) passes, and corrupt input yields a clear `fm doctor` error rather than a traceback.

- **Handshake hook, CLI and state versions at every entry** — FIX — value 3 — effort S — risk low
  Why: a plugin update mid-session leaves a running session on the old hooks or CLI while state is stamped by the new version. The pack has a schema stamp and rollback, but nothing checks that the hook, `fm` and state agree. Assumption: the plugin cache is replaced in place.
  Done when: a test with the hook at version N and state at N+1 fails open with one factual note, and state is left untouched.

- **Detect out-of-band state edits with a transition hash chain** — SECURITY — value 3 — effort M — risk med
  Why: "state only via fm" is enforced by the PreToolUse guard, but a shell one-liner such as `sed` or `python -c` can flip a brief's status or gate fields. Provenance labels cover evidence, not the frontmatter. Assumption: the guard can't catch every shell write to the state directory.
  Done when: hand-editing `status: done` in a brief makes `fm doctor` and the Stop gate report a broken chain, and normal `fm` writes never trip it.

- **Probe the `claude` CLI's capabilities once per version** — FIX — value 4 — effort M — risk low
  Why: `fm ideas`, `fm run` and audits all spawn `claude -p` with specific flags, models and output formats. The pack shows failed lenses counted as failures, and the model IDs change between releases. Assumption: nothing checks flags up front today.
  Done when: `fm doctor` shows a cached capability record keyed by the CLI version. A fake CLI that rejects a flag makes `fm ideas` fall back or fail with one explicit reason, with no wasted model spend.

- **Attribute hook events to main agent or subagent** — FIX — value 3 — effort M — risk med
  Why: the thrash counters, auto-captured evidence and Files-touched logic all assume one actor. Read-only subagents and parallel worktrees also fire PostToolUse, so they could inflate thrash counts or record evidence run in a different tree. Assumption: the hook payload carries an agent or transcript identifier.
  Done when: a replayed trace with interleaved subagent events leaves the main task's counters, evidence and touched files unchanged.

- **Run the full loop under a missing-tool matrix** — CLEAN — value 3 — effort M — risk low
  Why: the pack tests odd repo shapes and interpreter variants, but not an absent git, an absent `claude`, a read-only HOME, or no TTY. This pack's own directory is not a git repo, which shows the case occurs. Assumption: some gates silently assume git.
  Done when: a scenario test runs capture→done with each tool removed in turn. Each run either completes or degrades with a named skipped gate, and never with a traceback.

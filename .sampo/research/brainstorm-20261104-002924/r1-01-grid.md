# Brainstorm — lens: grid

- **Collapse the double SessionStart injection to one copy** — FIX — value 5 — effort S — risk low — category: hooks × agent × wrong
  Why: the pack measures 2,733 characters injected twice. Assumption: the cause is both the new `sampo` plugin and the thin `foreman` shim registering the same hook, since the rename made the shim depend on `sampo`. Verify this on the machine first.
  Done when: a fresh session transcript contains the block exactly once. A test counts hook registrations across all installed plugin manifests and fails if two share a command or output.

- **Split MASTER.md into a generated index plus sections that Read accepts** — CLEAN — value 5 — effort M — risk low — category: docs × agent × missing
  Why: at 75,758 tokens, Read refuses MASTER.md, so agents cannot read the docs at all. Verbs' `use when` anchors must survive the split.
  Done when: every docs file is under 20k tokens, MASTER.md becomes a short index, and a test fails if any tracked doc exceeds the Read limit or an anchor goes unresolved.

- **Answer "how do I X" from the anchors without reading the doc** — FEATURE — value 4 — effort M — risk low — category: CLI × agent × unclear
  Why: agents who can't Read MASTER.md fall back to guessing. A `sampo help <question>` that returns at most 600 characters from the anchor table needs no model.
  Done when: 10 recorded questions each return the right verb in under 600 characters, and a cold child using only this verb names the correct command.

- **Add `sampo prune --plan` for the 2.4 GB state, with apply going to a TTL trash** — SECURITY — value 4 — effort M — risk med — category: unattended × slow
  Why: state is 2.4 GB and the drive's readers slow as it grows. Deletion needs plan/apply, and the user's rule says to look at a target before deleting.
  Done when: `--plan` prints the top 10 by bytes with an age and a reader-safety flag, and apply moves the files to trash with an undo. A test proves `fm doctor` is green afterwards.

- **Scan state for secret-shaped strings before any size-driven archive or publish** — SECURITY — value 3 — effort M — risk low — category: user × unsafe
  Why: assumption: 2.4 GB probably holds transcripts and verbatim asks, and compacting or syncing them could leak. This belongs next to the prune work.
  Done when: a planted fake token in a ledger is reported by path and never printed, and the archive step refuses until it is redacted.

- **Gate per-turn and per-start characters with one budget file at ship** — PERFORMANCE — value 4 — effort S — risk low — category: unattended × unclear
  Why: per-turn burden is 48 to 76 characters and is only measured, not held. One `lean.budget` file with SessionStart chars, per-turn chars, the largest doc and state bytes lets `fm ship` fail on regression. Pending-measurement growth stays exempt under the lean-substance rule.
  Done when: adding one injected line over budget makes the ship gate fail naming the file. Lowering the budget in the file passes only with a recorded decision.

- **Run a Ward canary through the real hook path at session start, silent unless it fails** — SECURITY — value 4 — effort S — risk low — category: hooks × agent × unsafe
  Why: "guard intact" is a Mission goal. A harmless sentinel command that must be denied proves the hook is installed and reachable. It adds zero injected characters on success.
  Done when: removing the hook registration yields one degraded line at the next session start, and a passing run emits nothing.

- **Bench hooks under N parallel lanes, not just one session** — PERFORMANCE — value 3 — effort S — risk low — category: other agents × slow
  Why: the gate `bench_hooks.py --runs 20` is single-process, while lanes and subagents share the state locks. Assumption: contention is where p95 breaks.
  Done when: the bench reports p95 at 1, 4 and 8 concurrent hook callers and fails above the recorded bar.

- **Give non-Claude harnesses a smaller injection card than Claude Code gets** — FEATURE — value 3 — effort M — risk low — category: other agents × missing
  Why: the README claims Codex, Gemini and opencode support, but the lean fixes were measured on one host. Assumption: the other adapters get the same text.
  Done when: each harness's injected size is printed by `fm doctor` and sits under the same budget.

- **Show "what Sampo costs you" as one web UI card** — FEATURE — value 3 — effort S — risk low — category: web UI × user × unclear
  Why: lean claims must be checkable. The card shows injected characters per start and per turn, hook ms, state bytes and doc tokens, each with a trend against the budget file.
  Done when: the card renders from `--json` alone and every number matches the CLI's.

- **Wild: starve the session-start text nightly in a lane until a held-out exam regresses** — FEATURE — value 4 — effort L — risk med — category: hooks × unattended × wrong
  Why: wild. It finds the minimum injection from evidence, not taste, using the free arms only (no tokens beyond the exam's).
  Done when: a report names the smallest injection whose exam score matches the full one.

- **Wild: a luggage tag in the pane header, weighed in grams per injected character** — FEATURE — value 2 — effort S — risk low — category: pane × user × delight
  Why: wild. A playful live weight that turns red when over budget gives the lean goal a visible face, and it is drawn by the pane, not injected.
  Done when: the tag appears in the pane and adds 0 characters to the transcript.

- **Wild: a cold child tries to use Sampo from the injection alone and reports what it couldn't do** — FEATURE — value 3 — effort M — risk low — category: agent × unclear
  Why: wild. It checks that shrinking the injection did not remove the one thing an agent needs first.
  Done when: the child names the right first command in 4 of 5 trials on the shrunken text.

**Cells left empty:** web UI × unattended (nobody is watching; the budget file covers it), site × agent (agents don't use the site), and CLI × user × unsafe (the Ward already covers it).

Next question: which of the injected lines changed any agent's behaviour in the last 30 days, and can the ledger show it without a new gauge?
Next question: does the 2.4 GB hold anything a reader needs, or is most of it dead transcripts?

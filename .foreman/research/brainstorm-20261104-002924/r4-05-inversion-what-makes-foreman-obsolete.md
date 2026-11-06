# Brainstorm — lens: inversion: what makes Foreman obsolete

- **Run a bare-model duel on every capability, monthly** — FEATURE — value 5 — effort M — risk low — category: obsolescence
  Why: the request is "lean and safe" and the pack lists "Foreman beats Claude Code on the duel" (T-1231) as deferred, with the Haiku smoke arm and "free arms" in the steers; no per-capability "does the host already do this" number appears. Assumption: the host model improves faster than the discipline layer.
  Done when: `sampo exam` prints, per capability, the pass-rate delta of Sampo vs a stock agent on the same held-out scenarios, with any capability at delta ≤ 0 flagged "candidate to retire".

- **Attach a native-in-host probe to every discipline rule** — FEATURE — value 4 — effort M — risk low — category: obsolescence
  Why: the injected SessionStart text (2,733 chars, twice) and the per-turn 48-76 characters are rules the host may already enforce (plan mode, permissions). Assumption: no rule today records what would make it redundant.
  Done when: each injected line in the source has a `retire-when:` field naming a command that exits 0 once the host does it natively, and a test fails on a line without one.

- **Cap session-start injection at a hard budget, overflow behind a pull verb** — PERFORMANCE — value 5 — effort S — risk low — category: lean
  Why: the request names 2,733 characters injected twice and MASTER.md at 75,758 tokens, which Read refuses. A product that costs more than it saves is replaced.
  Done when: SessionStart emits one copy of at most N characters (N set in a budget file), the rest is reachable via `sampo doc <topic>`, and the ship gate fails if the injection grows.

- **Shard MASTER.md into an index plus Read-safe sections** — CLEAN — value 4 — effort M — risk low — category: docs
  Why: Read refuses the 75,758-token file; an agent that can't read the manual is a reason to drop the tool.
  Done when: every file under `docs/` opens in one Read, the index is under 3k tokens, and every old `MASTER.md#anchor` still resolves.

- **Prune the 2.4 GB project state with a plan, a trash and an undo** — CLEAN — value 4 — effort M — risk med — category: footprint
  Why: the request lists 2.4 GB of project state. Assumption: most of it is rebuildable ledgers and lane artifacts.
  Done when: `sampo prune --plan` classifies state by rebuildable vs. keep, `apply` moves files to a TTL trash, and the Ward-protected paths are never in the plan.

- **Keep a Lite profile that is the Ward and nothing else** — FEATURE — value 4 — effort M — risk med — category: obsolescence
  Why: T-0794 "Slim Foreman: Lite mode, retire adapters, eject" is deferred; standing rule says the guard stays intact. If everything else is replaceable, the irreducible core is the guard.
  Done when: `sampo lite on` leaves only the Ward hook active, per-turn injection is 0 characters, and the guard exam still passes in full.

- **Add a needed-share line to `sampo doctor`** — FEATURE — value 3 — effort S — risk low — category: measurement
  Why: assumption: "which of my features did I ever use" is the question that decides a keep-or-leave check-in (T-0864, deferred for lack of a safe channel).
  Done when: doctor prints, per capability, sessions in the last 30 days where it fired and changed an outcome, from existing ledgers only.

- **Wild: Run a "ten-line Sampo" duel** — FEATURE — value 3 — effort M — risk low — category: obsolescence
  Why: wild. Pit the full product against a 10-line hook set (Ward + one test-before-done check) on held-out scenarios; whatever the small one matches is bloat.
  Done when: a report names which capabilities the 10-line version fails on and which it ties.

- **Wild: Stage a quarterly "host catch-up day"** — FEATURE — value 3 — effort S — risk low — category: obsolescence
  Why: wild. Assumption: the host ships plan, hooks and permissions features steadily. A scheduled job diffs the host's release notes and tool list against Sampo's verbs and files "now native?" tasks.
  Done when: the job runs on a new host version and lists at least the verbs whose names or behaviour overlap new host features.

- **Wild: Generate Sampo's own retirement plan on demand** — FEATURE — value 3 — effort M — risk low — category: obsolescence
  Why: wild. `sampo retire --plan` lists capabilities in order of removal safety, with the evidence for each and the revival test.
  Done when: the output covers every capability and each entry cites a command that reproduces its number.

- **Downgrade the Ward to audit-only when the host enforces it natively** — SECURITY — value 4 — effort L — risk high — category: guard
  Why: the guard is the one thing that must stay; if the host's sandbox covers the same classes, a duplicate hook is pure latency. Assumption: this is true for some classes only.
  Done when: a per-class table shows which Ward rules are mirrored by host settings, and only mirrored ones switch to audit-only, with the full exam still passing.

- **Gate every new injected byte on a measured outcome change** — CLEAN — value 4 — effort M — risk low — category: lean
  Why: the lean steer says growth without measurement is "pending", but injection has no such gate.
  Done when: the ship gate rejects an increase in injected characters unless the commit cites an `sampo outcomes` line showing the line changed a result.

Next question: Which capability, if switched off for a week in the user's own sessions, would they notice first, and do the ledgers record it?
Next question: When the host adds a feature that overlaps a verb, who decides retirement, and does the standing push grant let that deletion ship unattended?

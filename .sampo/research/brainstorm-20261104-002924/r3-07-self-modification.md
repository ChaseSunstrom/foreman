# Brainstorm — lens: self-modification

- **Rebuild the install from release plus a patch log** — FEATURE — value 4 — effort M — risk med — category: self-edit
  Why: the pack shows a 2.4 GB state, a double SessionStart, and a shim/alias rename in progress. Self-edits and hand edits are mixed into the install, so there is no way to say what Sampo changed about itself. Assumption: self-edits can be expressed as patches.
  Done when: `sampo selfpatch verify` rebuilds the install into an empty dir from a tagged release plus the ordered patch log, and its tree hash equals the live install's hash.

- **Predict a self-edit's behaviour change, then check it** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: assumption: a self-edit's summary can be wrong while its tests pass. A tool-less child sees only the diff of injected text or Ward rules and writes the verdict changes it expects. Replaying recorded hook payloads through old and new code produces the observed changes, and the two lists are diffed.
  Done when: a seeded diff that silently loosens one rule is flagged with "predicted none, observed 1 changed verdict", while an honest diff scores a match.

- **Flag a commit that changes both a gauge and the thing it measures** — SECURITY — value 4 — effort S — risk low — category: measurement integrity
  Why: the pack holds many gauges, such as per-turn burden of 48 to 76 characters and bench bars. A self-edit that shrinks the injection and edits the counter in the same commit would pass lean checks falsely. Assumption: the lean gauges live in separable files.
  Done when: a test commit editing `plugin/tests/bench_hooks.py` and a hook together fails the ship gate unless a golden reading taken on the parent still matches.

- **Put protected-surface self-edits on probation** — SAFETY (SECURITY) — value 4 — effort M — risk med — category: rollback
  Why: Ward, hooks and injected text are the surfaces a bad self-edit could silently weaken. Assumption: the install can track counts of clean sessions.
  Done when: a self-edit to a protected file lands flagged "probationary" and auto-reverts after 48 hours unless at least N sessions ran under it with the Ward canary green. A test forces the revert.

- **Let state go dark for seven days before it is deleted** — FEATURE — value 4 — effort M — risk med — category: state pruning
  Why: the 2.4 GB project state needs pruning, and a TTL trash only helps once something is already deleted. Here a pruning candidate is renamed into a quarantine dir and nothing is removed. Any later open of a quarantined path restores it and records which reader needed it.
  Done when: a planted reader that touches a quarantined file gets it back within one call and the prune plan drops that class. After 7 days of no touches the files are archived.

- **Rewrite MASTER.md's layout from Read trails** — FEATURE — value 3 — effort M — risk low — category: docs
  Why: MASTER.md is 75,758 tokens, so Read refuses it. Which sections agents actually open is already knowable from the Read log. Sharding by guess would put the wrong things in the index.
  Done when: `sampo doc reshard --plan` proposes an index plus shards, each under the Read ceiling, with the most-read sections in the index. Every old `MASTER.md#anchor` still resolves.

- **Tune skill descriptions from misfire and miss logs** — FEATURE — value 3 — effort M — risk low — category: skills
  Why: there are 1,396 files under `plugin/skills/`. Descriptions decide both when a skill loads and how much it costs. Assumption: a miss log exists or can be derived from transcripts.
  Done when: a proposal lists, per skill, the description change, its length delta and the misfires it would fix. Applying it never raises the total description characters.

- **Wild: Molt monthly into a clean install** — FEATURE — value 3 — effort M — risk med — category: lean
  Why: wild. Every 30 days Sampo builds a fresh install from the release plus the verified patch log, runs the Ward exam and the bench on it, and swaps atomically. The old install is kept for one cycle. Drift, stale shims and dead aliases do not survive a molt.
  Done when: a drill molts a scratch home with a planted stray file in the old install, the stray is gone afterwards, and the exam and bench numbers match.

- **Wild: Make the editor and the explainer different parties** — FEATURE — value 3 — effort S — risk low — category: legibility
  Why: wild. Each self-edit needs a summary of 20 words or fewer from the editing lane. A cold reader that sees only the diff writes its own, and a big divergence means the change is unclear or hides something.
  Done when: a planted diff with a misleading summary is rejected, and an honest one passes.

- **Wild: Let Sampo propose one deletion of itself each night** — FEATURE — value 4 — effort M — risk low — category: lean
  Why: wild. The pack says Sampo is meant to stay lean and offers deletion drills and brownouts. A nightly lane picks the least-used verb, removes it on a scratch copy, and runs the suite and exam there. Only a green result becomes a morning card with a one-key accept.
  Done when: the morning card shows the verb, its use count, the lines removed and the suite result. Accepting it applies a single revertable commit.

- **Wild: Keep a hash-sealed frozen twin of Sampo's current self for audits** — SECURITY — value 3 — effort M — risk low — category: audit
  Why: wild. A read-only snapshot of the install sits outside the tree at each promotion. Later you can run any recorded hook payload through the snapshot and through the live version and read off every verdict that diverged since. The snapshot is for after-the-fact audit only and never takes part in live decisions.
  Done when: `sampo selfpatch diverge --since SNAP` lists the diverging verdicts for a replayed corpus, and a planted loosening shows up in it.

- **Preserve the user's local patches across self-updates** — FIX — value 3 — effort M — risk med — category: upgrade
  Why: assumption: the user, who is a developer, edits files in their installed copy, as with the foreman-ui mod pending update (T-0418). A self-update that overwrites them loses work silently, and one that keeps them hides the drift.
  Done when: a hand edit to an installed file survives an update as a named local patch listed in `doctor`. A conflicting upstream change is flagged, not overwritten.

- **Cap how much a lane may change in the guard on one night** — SECURITY — value 3 — effort S — risk low — category: blast radius
  Why: the unattended drive can edit Sampo during a long run. Assumption: self-edits to guard code from one lane are not currently counted against a per-night limit.
  Done when: a second guard edit in the same night by an unattended lane is held for the user, with a ledger line naming the first edit.

Next question: which of Sampo's protected surfaces has been self-edited most often, and did any of those edits ever pass the exam only because the exam was edited in the same change?
Next question: when the user hand-edits an installed Sampo file, does any current path notice, preserve it, or overwrite it?

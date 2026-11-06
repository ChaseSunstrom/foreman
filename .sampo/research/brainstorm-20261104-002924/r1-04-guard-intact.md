# Brainstorm — lens: guard intact

- **Pin every shim to the one guard** — SECURITY — value 5 — effort S — risk low — category: guard/rename
  Why: T-2748 turned the `fm*.py` modules into shims over `plugin/lib/sampo/`, and the Ward must refuse the same things under both names (T-2745). A copied guard could drift silently.
  Done when: a test asserts that every legacy and Sampo entry point resolves to the same guard function object, and it fails if a shim carries its own rule table.

- **Gate every context cut on a guard-clause index** — SECURITY — value 5 — effort M — risk low — category: lean/guard
  Why: MASTER.md is 75,758 tokens and the SessionStart text is injected twice, so trimming is coming. Each guard rule needs a stable id that a trim cannot drop unnoticed.
  Done when: the ship gate fails if any guard rule id loses its doc line, its test or its injected one-liner after a trim.

- **Keep exactly one guard line through SessionStart dedupe** — FIX — value 4 — effort S — risk low — category: context/guard
  Why: 2,733 characters are injected twice. A naive hash dedupe could drop the copy that carries the Ward notice.
  Done when: a test runs SessionStart on startup, resume and compact, and the Ward line appears once each time, with total characters at most 1,400.

- **Show Ward liveness in the existing per-turn line** — FEATURE — value 4 — effort S — risk low — category: observability
  Why: the per-turn burden is 48 to 76 characters. A `ward:ok` token costs about 8 characters and shows whether the guard hook ran. Today its silent failure is invisible.
  Done when: the turn line shows `ward:ok` when the hook ran, `ward:—` when it didn't, and the burden stays at or under 84 characters.

- **Protect guard state from the state pruner** — SECURITY — value 5 — effort M — risk med — category: state/guard
  Why: project state is 2.4 GB, and pruning it is the obvious fix. Grants, protected-path lists and ledger anchors must never be a prune target.
  Done when: the pruner reads a guard-manifest denylist, `--dry-run` prints "guard files untouched: N", and a planted grant file survives a full prune in a test.

- **Rotate ledgers with hash-chain checkpoints** — FIX — value 4 — effort M — risk med — category: state/integrity
  Why: shrinking the ledgers must not break verification (see the "verify the hash chain from the last checkpoint" idea above). Rotation is the step that can silently sever the chain.
  Done when: after rotating a copy of the real ledger, chain verification passes from the new checkpoint and fails if a record is altered before it.

- **Prove the hook prefilter has zero false negatives** — SECURITY — value 5 — effort M — risk med — category: performance/guard
  Why: the shell prefilter (T-0832) is deferred "until a bench result". A fast path in front of the Ward is the riskiest way to make hooks faster.
  Done when: a differential test runs the prefilter and the full guard over the recorded command corpus plus the obfuscation exam, and shows zero commands the prefilter skips that the guard would block.

- **Make every off-switch alias equally hard to flip** — SECURITY — value 5 — effort S — risk low — category: rename/guard
  Why: the rename keeps every old name working, so each `FOREMAN_*` and `SAMPO_*` kill switch, plus `fm off`, is an attack surface and must have the same gating.
  Done when: a table-driven test sets each alias of each off switch from a tool call, and every one is refused or logged identically.

- **Ship a guard card that fits Read** — FIX — value 4 — effort S — risk low — category: docs/context
  Why: Read refuses MASTER.md at 75,758 tokens, so an agent can't read the Ward's rules from it.
  Done when: `fm doctor` fails if the guard card is over 2,000 tokens or any doc file with guard content exceeds the Read limit.

- **Prove prose removal doesn't change guard behaviour** — PERFORMANCE — value 4 — effort M — risk low — category: context/guard
  Why: the hook enforces regardless of what the prompt says, so some nudge text may be dead weight. The bait suite can show which.
  Done when: for each guard sentence cut, bait-suite bypass attempts show no more routing-around than before, and the cut is recorded with that score.

- **Wild: Add a guard-only floor profile** — FEATURE — value 4 — effort M — risk low — category: lean/guard — wild
  Why: assumption: lean work needs a provable minimum. `fm lean --floor` boots only the Ward hook and its state, nothing else.
  Done when: a test boots the floor profile in a scratch home, blocks a planted `rm -rf` and a protected-path write, and starts in under 30 ms.

- **Wild: Make the minimiser blind to covered lines** — SECURITY — value 4 — effort L — risk med — category: lean/guard — wild
  Why: assumption: the delta-debugging and deletion-race ideas could cut Ward code. This one only removes lines that no Ward test covers.
  Done when: a nightly deletion race over `plugin/lib/sampo/` never proposes a patch touching a Ward-covered line, and it reports the lines it skipped.

- **Wild: Run a 5 ms self-bait at SessionStart** — SECURITY — value 3 — effort S — risk low — category: observability — wild
  Why: assumption: the guard can fail open without anyone noticing. One harmless bait command goes through the guard at session start to prove it is alive.
  Done when: killing the guard hook in a scratch home turns the `ward` token to `—` and shows a one-line degraded notice at the next session start.

Next question: which of the guard's tests run in the ship gate versus only nightly, and how long can a guard regression go undetected after a trim?
Next question: do the Sampo-named hooks in an already-installed old plugin generation still point at the same guard after `foreman@foreman` migrates to `sampo`?

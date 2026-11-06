# Brainstorm — lens: guard intact

- **Test every enabled-plugin set for exactly one Ward** — FIX — value 5 — effort S — risk low — category: guard
  Why: SessionStart injects 2,733 characters twice, and the plan keeps thin `foreman` and `foreman-ui` shims that depend on `sampo`. Assumption: the double copy comes from shim plus plugin both registering. Deduping blind could drop the one Ward registration a shim-only install has.
  Done when: a test enables {shim only, sampo only, both, sampo-ui only} in a scratch config; each set yields exactly one Ward PreToolUse registration per matcher and one byte-identical SessionStart payload, and the dedupe task fails if the two copies differ.

- **Warn when a shim's dependency didn't resolve** — FIX — value 4 — effort S — risk low — category: guard
  Why: assumption: if `sampo` fails to install (offline marketplace, version skew), the shim loads with no hooks, and the user believes the guard is on.
  Done when: with the sampo plugin hidden, the shim emits a one-line "Ward absent" at session start; with it present the shim emits nothing (zero extra characters).

- **Keep every `MASTER.md#anchor` reference resolving after sharding** — FIX — value 4 — effort S — risk low — category: docs, guard
  Why: Read refuses the 75,758-token file, so sharding is the likely fix. Skills, hook messages, README and site link into `MASTER.md`, and a dead anchor in a block message strands the agent.
  Done when: a checker collects every `MASTER.md#…` string across `plugin/`, `site/`, README and hook or CLI output. It fails the ship gate if any fails to resolve to a shard, and a redirect map covers the old anchors.

- **Track the retry-after-block rate as a lean regression metric** — SECURITY — value 4 — effort S — risk low — category: measurement
  Why: assumption: when injected guard prose shrinks, the model hits the Ward more often, which looks like a pass but is a regression. Hook ledgers should already hold block events and the next commands.
  Done when: a reader prints, per week, blocks per 100 Bash calls and the share retried within 3 turns, and the lean ship gate flags a rise of more than 20% across a context cut.

- **Fuzz the state pruner for containment** — SECURITY — value 5 — effort M — risk med — category: state, guard
  Why: the 2.4 GB of project state will get a pruner, and a deleter that follows a symlink or hardlink out of the state root is the worst way for the guard to fail. A TTL trash is already proposed but no containment test is.
  Done when: a fuzz suite plants symlinks, hardlinks, `..` names, bind-mount-like layouts and a file swapped mid-walk. The pruner, using `openat` with `O_NOFOLLOW`, touches nothing outside the state root and never deletes grants, Ward rules or the hash-chain anchors.

- **Hold unattended prune to rebuildable classes** — SECURITY — value 4 — effort S — risk low — category: state
  Why: assumption: the drive runs unattended under the standing core yes, so an age-based prune could delete ledgers that can't be rebuilt.
  Done when: each state class is tagged rebuildable or not. Unattended prune removes only rebuildable classes, and a non-rebuildable one needs an on-the-spot grant that the test shows is refused when none exists.

- **Protect standing intent and steers when cutting context** — SECURITY — value 4 — effort S — risk low — category: context
  Why: the standing intent sits under gen-0 and over every steer. Cutting 2,733 characters could drop those by accident, and a guard-clause index covers only Ward rules.
  Done when: a manifest lists the hashes of the standing-intent and steer lines the session must see. A cut that removes one fails the ship gate, and a held-out child shown the lean injection restates the standing intent.

- **Resolve conflicting off-switch aliases to the safer value** — SECURITY — value 4 — effort S — risk low — category: guard
  Why: the rename keeps every old name working, so `SAMPO_*` and `FOREMAN_*` can both be set. Equal difficulty for each alias is covered; what happens when they disagree is not.
  Done when: for each switch, setting the new name and old name to opposite values leaves the Ward on, and a test enumerates all pairs.

- **Key the Ward's rule cache by content, not mtime** — FIX — value 3 — effort S — risk low — category: guard, performance
  Why: assumption: a warm hook path caches parsed rules by mtime. Same-second edits and `touch -r` keep the old key and serve stale rules.
  Done when: a test edits a rule in place with mtime and size preserved, and the next hook call enforces the new rule.

- **Keep shims out of the hook import path** — CLEAN — value 3 — effort S — risk low — category: performance
  Why: the `fm*.py` modules became shims after the move to `plugin/lib/sampo/`. Each hop adds import time to a path with a hook bar.
  Done when: an import trace of each hook entry point shows no shim module, and `bench_hooks.py` reports no regression.

- **Make the pruner pass the Ward first (wild)** — SECURITY — value 4 — effort M — risk low — category: dogfood
  Why: assumption: the pruner deletes through its own code and so bypasses every rule the Ward holds for `rm`.
  Done when: before each delete the pruner asks the Ward's classifier about the equivalent `rm -rf <path>`; a planted protected path in the prune set aborts the run with a reason line.

- **Add a rolling guard digest to the per-turn line (wild)** — SECURITY — value 3 — effort S — risk low — category: guard
  Why: the per-turn burden is 48 to 76 characters. Four hex characters of the loaded rule hash would let a transcript show whether the Ward changed mid-session, such as an agent editing its own rules in bypass mode.
  Done when: the digest appears in the per-turn line (4 characters or fewer added), and a test that edits a rule mid-session changes it on the next turn.

- **Generate bypass attempts overnight on the local model, classify only (wild)** — SECURITY — value 4 — effort M — risk low — category: red team
  Why: the user wants the local qwen3.8-27b used at volume, and generation costs no dollars. Each attempt goes through a no-run classifier (nothing executes), and the exam is rebuilt from the lean injection text alone.
  Done when: a nightly job writes at least 500 distinct attempts, each as a verdict record. Any attempt the Ward allows that a stronger cold reader calls destructive is filed as a task, and no generated string is ever executed.

Next question: after context cuts, does the model's rate of reaching for blocked commands move, and which injected lines moved it?
Next question: which state directories do hooks read on every call, and does any of them grow with the 2.4 GB?

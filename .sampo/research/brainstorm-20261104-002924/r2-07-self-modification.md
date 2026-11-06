# Brainstorm — lens: self-modification

- **Run the builder on generation N-1 and the checker on N** — SECURITY — value 5 — effort M — risk med — category: self-hosting
  Why: Sampo builds Sampo, and the drive's own hooks and Ward run on the install being edited. A bad self-edit can disable the thing that would catch it. Pinning the drive to one generation is already listed, but not splitting builder from verifier.
  Done when: a test lands a self-edit that breaks the Ward import, and `sampo ship` still blocks it because the verifier ran the previous install.

- **Ship every protected-surface self-edit with a pre-tested inverse and a tripwire** — FEATURE — value 5 — effort M — risk low — category: rollback
  Why: Edits to hooks, Ward, injection text and MASTER.md can quietly regress latency or the guard. The listed "verified undo" is per task, not per self-edit. Assumption: the previous install generation is kept on disk.
  Done when: a planted regression (hook bench over its bar, or a failed Ward canary) in one of the next three sessions auto-applies the stored inverse and prints one line saying so.

- **Make shim plugins hookless and test the count of hook registrations** — FIX — value 4 — effort S — risk low — category: install
  Why: SessionStart injects 2,733 characters twice. Assumption: the thin `foreman` shim and `sampo` plugin both register it, since the shim lists Sampo as a dependency.
  Done when: a test enumerates the registered hooks after install and fails if any event has two entries from Sampo plugins. A real session start shows one copy.

- **Tighten-only auto-tuning for safety thresholds** — SECURITY — value 4 — effort M — risk low — category: self-tuning
  Why: size gates, stall limits and hook budgets are hand-set. Self-adjustment from the ledgers is tempting, but loosening is exactly what a bad self-edit would do.
  Done when: a tuner may lower a threshold from ledger evidence but raises nothing. A test that tries to raise a guard parameter is refused and logged.

- **Refuse growth of MASTER.md past the Read ceiling at write time** — PERFORMANCE — value 4 — effort S — risk low — category: docs
  Why: MASTER.md is 75,758 tokens and Read refuses it. Sessions that edit it, including Sampo's own, keep growing it because nothing stops them.
  Done when: an Edit that takes any docs shard over 8k tokens is blocked with a `Next:` line naming the split command. The current file passes once sharded.

- **Write a self-surgery ledger with plain-word weekly digest** — FEATURE — value 3 — effort S — risk low — category: transparency
  Why: the user steers hard on lean and safe, and Sampo edits its own hooks, injection text and rules, but nothing shows the user what changed in the system watching them. Assumption: commit trailers can mark self-edits.
  Done when: `sampo self log` lists each self-edit with surface (guard, hook, injection, doc), chars added or removed, and its revert command. The weekly card shows net chars.

- **Rate-limit protected-surface self-edits with a breaker** — SECURITY — value 4 — effort S — risk low — category: breaker
  Why: the drive is unattended and self-advancing, and a refile livelock could rewrite the guard repeatedly.
  Done when: more than N Ward, hook or injection edits in 24 hours, or any revert in that window, halts further ones until the user clears it. A test drives N+1 edits and the last is refused.

- **Promote a repeated lesson into a check, then delete its prose** — CLEAN — value 4 — effort M — risk med — category: context diet
  Why: per-turn burden is 48 to 76 characters, and each steer or lesson adds injected text. Lessons that a deterministic check could enforce should cost zero context.
  Done when: for one lesson, a check lands, the injected line is removed, and a recorded-payload replay shows the same block or allow decisions with fewer characters.

- **Wild: deletion-only mutation of the injected text, scored by a cold quiz** — FEATURE — value 4 — effort M — risk med — category: evolution
  Why: assumption: nightly shadow lanes can delete one sentence at a time from the session-start text, and a tool-less child must still answer fixed questions on the Ward clauses and verbs. Survivors become deletion patches.
  Done when: one night's run produces a list of sentences whose removal didn't change quiz answers, each filed as a patch with its measured character saving.

- **Wild: a frozen outside-tree Ward twin that overrules by strictness** — SECURITY — value 4 — effort L — risk med — category: guard
  Why: a self-edit path that can write the Ward can weaken it. A read-only twin outside the state and install trees, with the same exam, closes that gap. Assumption: the user will install one file by hand.
  Done when: a test weakens the live Ward in a scratch home, a command the twin blocks is blocked anyway, and `doctor` reports the disagreement.

- **Wild: let a session mute one injected line for itself and report what it missed** — FEATURE — value 3 — effort M — risk med — category: self-trim
  Why: the agent is the only party that knows whether a line helped. A mute is recorded with the turn and later outcome. Muting a Ward clause is disallowed.
  Done when: after a session that muted a line, the ledger holds a record of the line, the reason and the result. Attempting to mute a Ward line is refused.

- **Wild: a weekly "live without me" drill that disables one capability in lanes** — FEATURE — value 3 — effort M — risk low — category: lean evidence
  Why: the lean rows wait on measurements that don't exist yet. Randomly browning out one verb or hook in the drive's own lanes for a week produces the missing evidence safely, with the Ward never eligible.
  Done when: one week's drill writes a per-capability row of tasks closed, retries and hook time with and without it, and the lean sweep reads it.

- **Gate a context cut on a guard-clause index** — SECURITY — value 4 — effort S — risk low — category: guard
  Why: cutting injected prose is the goal of this Mission, and the guard must stay intact. Each Ward clause gets an id, and a cut that leaves any id without an enforcing rule or a line fails.
  Done when: a patch deleting the only text for a Ward clause fails the ship gate naming the clause id. A patch that deletes redundant prose passes.

Next question: Which self-edits has Sampo already made to its own hooks or injection text, and did any one cost a session before it was caught?
Next question: Does the user read the session-start text at all, or only notice when it grows, and what would they accept losing?

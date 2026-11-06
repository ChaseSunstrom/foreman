# Brainstorm — lens: invented: the codebase as a living ecosystem

- **Release a stricter Ward tier when an incident heats the session** — SECURITY — value 4 — effort M — risk med — category: Ward
  Why: assumption: the pack has "tighten-only auto-tuning" and a "guard-only floor", but no dormant rule set that opens on a trigger, the way serotinous cones open on fire. A burst of blocks, a detected injection, or an unexpected guard-file touch would release a pre-written strict tier. It decays after N quiet minutes, and only the user can loosen it earlier.
  Done when: a test replays three blocks in 60 s and the next borderline command is refused. The same command is allowed again after the decay window, and the transition is logged.

- **Measure queries-to-evade on the Ward's refusal text** — SECURITY — value 4 — effort M — risk low — category: Ward
  Why: assumption: block messages name the rule, so a patient child can bisect the Ward the way a predator learns a prey's tells. The pack covers the Ward's strength, not what its wording leaks.
  Done when: a scripted prober gets a fixed number of probes against the real hook path, and `sampo doctor` prints how many it needed to find an allowed bypass or that it found none. Refusal wording is changed if the number falls under a recorded floor.

- **Check the rename alias chain as a ring species** — FIX — value 3 — effort S — risk low — category: compat
  Why: the pack shows the Foreman→Sampo shims and the "sunset clock on every alias". Neighbouring versions may each work with the next while the oldest and newest no longer do, and the pack tests only pairwise, not the chain.
  Done when: a matrix test installs states from every released name generation and asserts that each old name reaches the current guard. A failing end-to-end pair names the generation where the chain broke.

- **Tier senescent tests into a weekly lane** — PERFORMANCE — value 4 — effort M — risk med — category: ship gate
  Why: the pack records the full suite as a ship gate and a "time the ship gate" idea. No idea uses each test's unique-kill history to decide where it runs. Tests that have never failed across N cycles move to a rotating slice, and any one that fails is promoted back.
  Done when: the gate's wall time drops by a measured share. A replay of the last 50 real regressions shows none escaped the fast tier, or lists the ones that did.

- **Run a cleaning station at session close that warms the next start** — PERFORMANCE — value 4 — effort M — risk low — category: startup
  Why: the pack's hook bench and the "shim import tax" suggest start cost matters. A symbiotic cleaner pass at Stop would precompile bytecode, refresh the map and rule cache, and drop temp files, so the next SessionStart only reads.
  Done when: the bench shows SessionStart p50 falling against a cold start, with no writes during the hook (checked by a read-only mount in the bench).

- **Free budget by auction-free heirship when a capability retires** — CLEAN — value 3 — effort S — risk low — category: budget
  Why: the pack has per-turn budgets and retirement ideas, but the characters and milliseconds a retired capability frees are not reassigned. In a forest gap, the nearest waiting sapling gets the light. Here, the nearest queued item takes the freed budget by a fixed order, not by bidding.
  Done when: retiring a fixture capability lowers the budget table by its share, and the next item in the queue shows a raised limit in the same commit.

- **Trace runtime coverage across real hook runs to find vestigial organs** — CLEAN — value 4 — effort M — risk med — category: dead code
  Why: the pack has "reach" checks and a decomposer for dead state, but nothing that observes which code paths real sessions actually execute. Sample line coverage over a week of hook and verb calls and list the modules never reached.
  Done when: a report lists modules with zero hits across N sessions. Each is either named as a dormant guard path with a test, or filed as a removal.

- **Lock each lane's Ward profile at spawn by caste** — SECURITY — value 4 — effort M — risk med — category: lanes
  Why: lanes today share the Ward and the lease model. Scouts, builders and reviewers differ in what they need. A compiled, read-only profile per caste, set at spawn and hashed into the lease, stops a compromised reviewer from using builder powers.
  Done when: a reviewer lane trying a write or a network call is refused by its own profile even with the main Ward bypassed, and the profile hash appears in the lane record.

- **Cull the tail: report the single worst hook each week and budget-cut it** — PERFORMANCE — value 3 — effort S — risk low — category: hooks
  Why: the pack has a latency scaling curve and an event-total gate, but only a ceiling. A weekly predator report names the slowest p99 hook and its owner, and the next ship must beat it or justify it.
  Done when: `bench_hooks.py` writes a ranked tail table, and ship fails when the same hook is worst two weeks running without a recorded reason.

- **Post aposematic previews on destructive verbs** — SECURITY — value 3 — effort S — risk low — category: UX safety
  Why: assumption: `prune`, `ship` and ledger rewrites print the same calm text as read-only verbs. Warning colouration means one unmistakable, plain-text marker (and colour only where supported) on anything irreversible, with the undo hint beside it.
  Done when: a lint asserts that every verb tagged irreversible prints the marker in its preview. A screen-reader pass shows it is also readable as text.

- **Wild: hold a mass-spawning window for heavy gates** — PERFORMANCE — value 3 — effort M — risk med — category: lanes
  Why: the pack's lanes each run their own full proofs, and results share by tree hash only when trees match. Coral spawns in sync so the output is shared. Lanes would align their heavy proofs into one nightly window on one merged tree, then fan the verdict back.
  Done when: with four lanes, the window runs the full suite once and each lane shows the shared verdict. Total CPU minutes drop against four separate runs.

- **Wild: pack a tardigrade tun that revives a working guard from one file** — SECURITY — value 3 — effort M — risk med — category: recovery
  Why: the pack asks for a "Sampo is broken" card and a seed prompt. A tun is a single sealed file holding the Ward, the rule table and a restore script, which a stranger runs after total loss and gets a verified-armed guard.
  Done when: in an empty home, running the tun yields a Ward that passes its canary through the real hook path, with no network.

- **Wild: draw a food web of what each hook costs and feeds** — PERFORMANCE — value 2 — effort M — risk low — category: hooks
  Why: assumption: milliseconds and characters are per-hook numbers today. A web view would show who reads whose output, so the user sees which hook is the energy sink and which only feeds one consumer.
  Done when: the web UI page renders producers, consumers, bytes and ms per edge from the hook table, and a hook with no consumer is flagged.

Next question: Which of these defences did the user's own sessions ever need, and which has no incident in the ledgers to justify its cost?
Next question: Can the Ward and the funnel's local models be attacked through the same text channel, and does any ledger show one doing it?

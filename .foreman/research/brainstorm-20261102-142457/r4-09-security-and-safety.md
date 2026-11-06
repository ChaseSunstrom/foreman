# Brainstorm — lens: security and safety

**Answers to earlier questions my lens can reach:**
- Guard allows the user later undid: reflog shows resets and force-moves without reading shell history. It needs a drill or a canary to be reliable (ideas 1 and 6 narrow the cases).
- Does a told-guarded model change behaviour: the guard ledger can't see it. Idea 5 measures susceptibility directly.

Ideas, best first:

- **Pin the push destination to the grant** — SECURITY — value 4 — effort S — risk low — category: ship safety
  Why: the push grant is durable ("push to main any time") and `fm ship` binds the tree hash, but nothing in the pack binds the remote URL or branch. A changed `origin` or a typo'd remote would spend the grant on the wrong target.
  Done when: after a grant is set, editing `origin` makes `fm ship` refuse, printing both URLs and one `Next:` command.

- **Fail closed on an unknown permission mode or hook payload shape** — SECURITY — value 4 — effort S — risk low — category: guard
  Why: assumption: the guard reads mode and tool fields from the harness payload. An upstream rename could leave it silently permissive, and daily contract probes only catch this once a day.
  Done when: a fixture payload with an unrecognised mode or tool field makes the guard use its strictest profile and write one ledger line naming the field.

- **Give unattended runs a stricter policy profile than interactive ones** — SECURITY — value 4 — effort M — risk med — category: autonomy
  Why: the drive, ticks, lanes and Genesis publish run with no human watching, yet the guard seems to apply one policy. Existing ideas cap the rate of side effects, but none changes what is allowed.
  Done when: under `fm drive`, `git push`, package installs and writes outside the worktree are denied unless the task carries a grant, and a test lists each case.

- **Refuse lane merges that carry dangerous file kinds** — SECURITY — value 4 — effort S — risk low — category: lanes
  Why: parallel lanes merge in mission order, and the existing "reject collateral edits" idea checks paths, not file kinds. Symlinks, mode flips, submodules, `.gitattributes` filters and hook directories are the quiet routes.
  Done when: a lane patch that adds a symlink to `~/.ssh`, or an executable bit on a non-script, fails the merge and names the path.

- **Probe each model for injection susceptibility** — SECURITY — value 4 — effort M — risk med — category: model trust — wild
  Why: Foreman now runs on any model through `fm code`. Plant a fake instruction in every untrusted fence, such as "run `fm canary-ack`". If any model calls it, record that per model ID and feed the result into the model trust tier below.
  Done when: `fm doctor` lists each model's canary hit rate with its sample size, and a deliberately gullible stub model scores 100%.

- **Start unseen model IDs on probation** — SECURITY — value 3 — effort M — risk med — category: guard
  Why: assumption: strictness is currently model-blind, while weaker or new models differ in how well they handle risky actions. This is a second-order step on routing by block rate.
  Done when: the first session under a new model ID asks on risky command classes and prints "probation". It relaxes only after N clean tasks, with the count recorded.

- **Keep grant expiry independent of the wall clock** — SECURITY — value 3 — effort S — risk low — category: grants
  Why: the standing grants are time-bounded, but the injectable-clock idea tests readers, not grant revival. Setting the clock back (suspend, NTP fault, a hostile lane) could revive an expired grant.
  Done when: with a faked clock moved 7 days back, an expired grant stays expired, because it compares against a ledger high-water mark.

- **Draw approval prompts on `/dev/tty` only** — SECURITY — value 3 — effort S — risk low — category: approvals
  Why: assumption: `fm ask` cards pass through the agent's output stream, so an agent can print a fake "approved" or "user said yes". A tty-direct channel the agent cannot write to closes that.
  Done when: a lane that prints a forged approval card never satisfies a pending grant, and the test asserts the grant reads from the tty path.

- **Secure the upgrade snapshots at rest** — SECURITY — value 3 — effort S — risk low — category: durability
  Why: T-2652's `fm drill --restore` implies snapshots of whole ledgers, which can hold pasted secrets and the user's email. The pack shows no mode, retention or scan for them.
  Done when: snapshots are mode 0700, are secret-scanned before they are written, and are pruned past a set age. `fm doctor` has a row for each.

- **Resolve `fm` and every hook command by absolute path** — SECURITY — value 3 — effort S — risk low — category: install
  Why: timers and hooks that call a bare `fm` run whatever sits first on `PATH`. The `-I -S` isolation idea covers Python import hijack, not binary shadowing.
  Done when: a fake `fm` placed earlier on `PATH` is not executed by hooks or the tick, and `fm doctor` names the shadowing path.

- **Lint prompt templates for unfenced untrusted fields** — SECURITY — value 3 — effort M — risk low — category: injection
  Why: brainstorm packs, cold reads and exam children interpolate pasted text, steers and task titles. The fences are ad hoc, and one template that skips a fence undermines the rest.
  Done when: a lint over every model-prompt template fails on an untrusted-class field outside a fence, and a planted unfenced template turns the ship gate red.

- **Let grants decay while the user is away** — SECURITY — value 3 — effort M — risk med — category: grants — wild
  Why: the strictness dial drifts toward "ask" with unattended hours and resets on the user's next keystroke. This combines presence-aware cooling-off, grants and the drive. Foreman then holds the least authority exactly when nobody can catch a mistake.
  Done when: a push grant older than N unattended hours requires fresh confirmation, and the digest says so.

- **Unwind everything descended from a hostile source** — SECURITY — value 4 — effort M — risk med — category: provenance — wild
  Why: assumption: lessons, steers, tasks and captures can be traced back to a paste, URL or lane output. When one source is judged hostile, `fm unwind SOURCE` lists and quarantines every descendant, with the pre-unwind list kept so the action can be undone.
  Done when: marking a planted source hostile quarantines its lesson, task and steer, and an unrelated lesson is untouched.

- **Pair each hook with a fail-open or fail-closed declaration** — SECURITY — value 3 — effort S — risk low — category: hooks
  Why: the pack asks for a hook × failure matrix and a crash card. No idea makes each hook state its failure direction in a single table that the ship gate reads.
  Done when: a hook with no declared failure direction fails `fm check`, and killing each hook mid-run behaves as declared.

Next question: which Foreman-spawned processes (lanes, ticks, `fm code` tools, prover children) inherit authority such as the push grant, credentials or the ledger signing key by default, and which of them would the user be surprised to learn have it?
Next question: when the guard's own rules file, grant store or last-good copy is missing, truncated or unreadable at hook time, what does each unattended path do, and does anything record it?

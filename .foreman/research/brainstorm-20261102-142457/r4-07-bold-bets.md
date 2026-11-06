# Brainstorm — lens: bold bets

- **Run agent sessions as a separate unix user** — SECURITY — value 5 — effort L — risk high — category: OS isolation
  Why: assumption: the guard is a hook-level check inside the agent's own process, so a bypass-mode session still has the owner's full filesystem. Earlier ideas covered OS-level enforcement and a low-privilege user for the drive only. This extends it to interactive sessions: `fm` brokers per-repo ACL grants, and `~/.ssh`, `~/.aws` and other repos simply don't exist for the agent uid.
  Done when: in a bypass session, `cat ~/.ssh/id_ed25519` and a write into an ungranted repo both fail with EACCES, while edits in the granted repo and `fm task` still work.

- **Lock privileges to the stage rail** — FEATURE — value 4 — effort M — risk med — category: least privilege
  Why: assumption: Foreman already knows the stage (plan, edit, prove, close). Privileges only ever narrow: planning is read-only, editing can write only the planned files, proving has no network and no writes outside a scratch directory. Widening needs an `fm ask`.
  Done when: a write outside the plan set during the prove stage is blocked, with a message naming the stage and the one command that widens it.

- **Label guard cases by running them** — SECURITY — value 4 — effort M — risk med — category: guard ground truth
  Why: assumption: guard exams are labelled by humans or models. Run generated commands in a rootless, network-off sandbox under strace, list what they really touched (unlinks, writes outside the allowed set), then compare to the guard's verdict. Every false allow or false block gets a label with no judge.
  Done when: a nightly run prints a table of guard verdict vs observed effect for at least 500 generated commands, and a planted `rm` hidden in a `$(…)` is flagged as a false allow.

- **Prove guard invariants with a solver** — SECURITY — value 4 — effort M — risk low — category: formal checks
  Why: assumption: the rules are regex and prefix lists with no proof of what they cannot allow. Encode the rule lattice as a bounded model (dev-only Z3, or exhaustive enumeration over token classes) and prove stated invariants, such as "no allowed command writes under `~/.ssh`" and "no rule is shadowed".
  Done when: a red fixture rule that allows `chmod -R 777 ~` makes `fm doctor --prove-guard` print a counterexample command and exit nonzero.

- **Gate bypass mode on a restore-verified backup** — SECURITY — value 4 — effort S — risk low — category: recovery
  Why: assumption: the existing restore drill covers Foreman state, not what a bypass session can destroy in the user's repos and dotfiles. Refuse to start a bypass or unattended drive unless a backup of the writable set is newer than N hours and a sample file restored byte-identical.
  Done when: with the backup aged past the limit, bypass start is refused with one `Next:` command; after a fresh backup, it starts.

- **Tree-shake the install from field coverage, with lazy restore** — PERFORMANCE — value 3 — effort L — risk med — category: lean install
  Why: the pack reports 1,388 skill files and 2,129 files in all. Install only the verbs, skills and hooks that `fm usage` shows used in 60 days, and leave a stub for each omitted one. The stub restores that unit from the pinned release on first call and logs that it did.
  Done when: a fresh install is at least 50% smaller by file count, and calling an omitted verb works, restores it, and records the restore.

- **Require a change certificate for protected-core edits** — SECURITY — value 4 — effort M — risk med — category: self-change gate
  Why: this combines ideas the earlier brainstorms listed separately: effect-surface diff, guard corpus verdict diff, footprint delta and hook p95. The ship gate refuses a core-path change without one JSON certificate showing each delta empty, explained, or offset by a deletion.
  Done when: a change that adds a verb and a network call without an offset fails `fm ship` with the certificate's failing fields named.

- **Catch hallucinated package names (slopsquatting)** — SECURITY — value 4 — effort S — risk low — category: supply chain
  Why: assumption: the earlier package-install gate checks the dependency, not whether the model invented the name. Check a new name against the lockfile, a local known-good list and, when online, registry age and publisher. Block names that are new, young and one edit away from a popular package.
  Done when: `pip install reqeusts` (typo) is blocked with "did you mean requests"; a name already in the lockfile passes.

- **Wild: red-team from the user's own command distribution** — SECURITY — value 3 — effort M — risk low — category: personalized red team
  Why: wild. Mine the session logs the user already has (no shell history) for their command shapes, then have an attacker child hide harm inside those shapes, since the guard's real exposure is in commands this user will actually type.
  Done when: the report lists at least 20 user-shaped attacks, how many the guard missed, and each miss became a replay case.

- **Wild: estimate the guard's unseen bypasses by capture–recapture** — SECURITY — value 3 — effort M — risk low — category: safety statistics
  Why: wild. Run two independent attackers from different model families against the guard. The overlap between the bypasses each one finds estimates how many remain unfound, so "safe" becomes a number with an interval instead of an absence of known failures.
  Done when: the scorecard prints an estimated remaining-bypass count with an interval, and it changes when a new attacker family is added.

- **Wild: three blind guard implementations vote in shadow** — SECURITY — value 3 — effort L — risk med — category: N-version guard
  Why: wild. Three tool-less children from different families each write a small guard from the spec alone, never seeing Foreman's code. In shadow mode, any disagreement with the real guard on live traffic is logged. Earlier ideas had one second guard; three independent ones turn disagreement into a bug finder.
  Done when: replaying the guard corpus yields a disagreement list, and at least one entry is confirmed as a real guard bug or a spec ambiguity.

- **Wild: preview a command's effects with a symbolic shell** — FEATURE — value 4 — effort L — risk med — category: dry-run
  Why: wild. A pure-Python interpreter runs a command against a virtual snapshot of the filesystem and prints counts, such as "deletes 4,312 files in 3 repos, touches nothing outside". The guard blocks on measured size, not command shape, and unparseable commands fail closed.
  Done when: `fm can-i 'find . -name "*.log" -delete'` prints the file count without touching disk, and matches the real run in a sandbox.

Next question: which of Foreman's protections still need the agent's cooperation, and which of them would survive an agent that wants them off?
Next question: when the guard blocks something, who learns, and how long until the user sees it?

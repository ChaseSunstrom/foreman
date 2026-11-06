# Brainstorm — lens: bold bets

- **Convert irreversible-class blocks into snapshots** — SECURITY — value 5 — effort L — risk med — category: guard
  Why: assumption: much of the guard's friction comes from blocking commands that could simply be made undoable. Classify each command by reversibility (tracked in git, reflink-able, or truly gone). For the middle tier, take a copy-on-write snapshot of the touched paths and allow the command, instead of blocking it. Only the "truly gone" tier stays blocked.
  Done when: a `rm -rf` of an untracked directory inside the repo runs in bypass mode, and `fm undo` restores it byte-identically. A deletion of `~/.ssh` is still blocked.

- **Print an exposure receipt before every bypass session** — SECURITY — value 4 — effort S — risk low — category: safety
  Why: assumption: users cannot see what a bypass session puts at risk. Show one line at session start, such as "at risk: 3 unpushed commits, 2 untracked files, 1 .env, no snapshot". Offer a one-key backup of the at-risk set.
  Done when: in a fixture repo with unpushed commits and an untracked `.env`, the session-start text names both counts. After the backup key is pressed, the files exist in the backup location.

- **Seal the ledgers at the OS level** — SECURITY — value 4 — effort M — risk med — category: integrity
  Why: the pack's own chain-hash and signed-record ideas still let an agent running as the user rewrite history. Make the ledgers append-only via `chattr +a`, or via a tiny append daemon under a separate uid. `fm doctor` reports whether the seal is in force. The test host runs a hardened kernel, so assume it is supported.
  Done when: as the session user, truncating `ledger.jsonl` fails. A normal `fm` append still succeeds. `fm doctor` shows "sealed" or the specific reason it is not.

- **Render a live safety case** — SECURITY — value 4 — effort M — risk low — category: assurance
  Why: the pack holds hundreds of separate safety checks and no single argument connecting them. Build `fm assure` as a claim tree: "guard blocks destructive commands" → hook liveness, replay corpus, parity per harness. Each leaf is a probe that actually ran today. A claim with no leaf shows as a hole.
  Done when: removing one probe turns its parent claim red in the output. A claim with no probe fails `fm assure --strict`.

- **Compute a defence-depth meter** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: assumption: "the guard works" hides how many independent layers stand behind it. For each harm class (delete outside the repo, force-push, exfil), count the independent layers that still hold: hook, PATH shim, OS limit, snapshot. Disable each layer in a fault matrix and show the count. Print a session-start note only when a class drops to one layer.
  Done when: disabling the hook in a test home drops "delete outside repo" from 3 layers to 2. The session-start text appears only when the count is 1 or less.

- **Ship a signed patch manifest for the foreman-ui mod** — SECURITY — value 3 — effort M — risk med — category: mod
  Why: the pack shows the mod patching a host binary (T-1217, T-0418, T-0166 and the version-skew notes). List every region the mod changes, with hashes. Verify the manifest at launch and disarm the mod on any mismatch. This is lean in the sense of a minimal, auditable surface.
  Done when: editing one byte of the patched region makes the mod refuse to load and print the manifest diff. An untouched install verifies clean.

- **Add a cooling-off period for irreversible commands, aware of presence** — SECURITY — value 4 — effort M — risk med — category: safety (wild)
  Why: assumption: the real risk is an irreversible command run while the user is away. When the user is present, show a 10-second countdown the user can veto from the status line. When absent, deny automatically and queue it as an `fm ask`. This is a different mechanism from the "veto window for costly decisions" idea.
  Done when: with a presence stub set to absent, the command is denied and queued. With presence set to present, it runs after the countdown unless the veto file appears.

- **Intercept effects at a customs checkpoint** — SECURITY — value 4 — effort L — risk high — category: sandbox (wild)
  Why: bypass sessions today are all-or-nothing. Run the session on an overlay of the repo and $HOME, and treat everything leaving it (files, new packages, network attempts) as a proposed diff of the world. The guard becomes a customs officer deciding what syncs back.
  Done when: in a fixture session that writes the repo, `~/.bashrc` and a new global npm package, only the repo change syncs back by default. The other two appear in a "held at customs" list.

- **Audit and bound Foreman's footprint in the user's repo** — CLEAN — value 4 — effort M — risk low — category: lean
  Why: assumption: Foreman leaves files and CLAUDE.md sections in project repos that users never chose. `fm footprint` lists every path, setting and unit Foreman owns, with hashes and a revert command for each. A "leave-no-trace" mode keeps all state outside the repo.
  Done when: after leave-no-trace use, `git status` in the fixture repo is clean. `fm footprint` lists only system-level pieces, and reverting each one returns the home to its pre-install state.

- **Ship a deletion-only release every fourth release** — CLEAN — value 4 — effort M — risk med — category: lean (wild)
  Why: lean pressure is currently voluntary. A fixed cadence of deletion-only releases, with feature freeze, forces choices using the pack's own ablation, verb-usage and reach data. Each release carries proof that no measured gauge regressed.
  Done when: a release tagged "diet" has a negative net line count. Its notes list each removal with its evidence, and the bench and exam show no regression.

- **Retire tests by their catch record** — CLEAN — value 3 — effort M — risk med — category: lean
  Why: plugin/tests holds 414 files and the ship gate is slow. Track per test whether it has ever failed, and whether its mutants survive. Propose removal of tests that have never failed in a year and kill no mutants.
  Done when: `fm tidy --tests` lists candidates with their fail history. Removing the top 5 leaves the full-suite mutation score unchanged and shortens ship-gate time.

- **Run Foreman's unattended processes under OS resource limits** — SECURITY — value 3 — effort S — risk low — category: resource
  Why: the pack worries about orphaned children, ledger growth, tmpfs and runaway ticks, but nothing enforces a ceiling. Launch the drive, tick and lanes under `systemd-run --user` with MemoryMax, CPUQuota and IOWeight.
  Done when: a fixture lane that allocates without bound is killed at the cap and logged. The drive survives and records the cause.

- **Load verbs on demand from a pinned local cache** — PERFORMANCE — value 3 — effort L — risk med — category: lean
  Why: the install carries 1,388 skill files and many rarely used verbs. Keep a small signed core, and load other verbs when first called from a hash-pinned bundle in a local cache with no network. This is a lean install that still has everything available.
  Done when: a fresh install has a smaller file count. The first call of a rarely used verb loads it and verifies its hash. A tampered bundle is refused with a Next: command.

- **Offer a "tripwire home" decoy** — SECURITY — value 3 — effort S — risk low — category: detection (wild)
  Why: assumption: a model told it is guarded may behave differently, and the guard's ledger can't see that. Plant decoy credentials and a decoy `~/.aws` with a read alarm. Any read by a session raises a `fm doctor` red line naming the lane and prompt.
  Done when: reading the decoy file in a fixture session creates a ledger entry and a visible alert. A normal session never touches the decoy.

Next question: which of Foreman's guard blocks would the user have undone if they could, and what do those cases share?
Next question: if the install were halved tomorrow, which half would the user notice first, and how would we know without asking?

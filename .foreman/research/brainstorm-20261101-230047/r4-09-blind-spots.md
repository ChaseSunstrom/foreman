# Brainstorm — lens: blind spots

- **Probe the timer's environment against the user's shell** — FIX — value 5 — effort M — risk low — category: unattended
  Why: assumption: systemd and cron run without the interactive PATH, auth, keyring, `XDG_RUNTIME_DIR` or Python. Every earlier idea tests firing; none tests whether the fired lane can log in and find `fm`, `git` and its model CLI.
  Done when: the install card runs a no-op lane under `systemd-run --user` and prints a diff of the env, auth state and tool lookups against the interactive shell. It refuses to arm while the lane cannot start a model call.

- **Name the linger requirement on the install card** — FIX — value 4 — effort S — risk low — category: installs
  Why: assumption: user timers stop when the user logs out unless `loginctl enable-linger` is set, which needs privilege. The card shows unit text but not this, so "work starts without me" silently means "while I'm logged in".
  Done when: `fm doctor` and the install card report linger state. With linger off, the card says the timers only fire during login and offers the linger command as a separate queued yes.

- **Check installed units still point at a live interpreter and library** — FIX — value 4 — effort S — risk low — category: reliability
  Why: assumption: on a rolling-release Arch box, Python and venv paths change under a pinned `ExecStart`. The pack shows an interpreter-specific ship baseline (T-2529) and a working-copy import fail (T-2532), so path drift is the same class.
  Done when: the tick resolves each installed unit's `ExecStart`. A fixture with a deleted interpreter makes `fm doctor` go red with the unit name and an offered re-queue.

- **Run the start-point-dependent checks on a trigger-filed task** — FIX — value 4 — effort M — risk low — category: premise siblings
  Why: T-2525 fixed a late start point that applies only to open tasks, and the docs-unknown test assumed no start commit. Trigger-filed tasks (ci, self, discovered) are born without a session start, which is exactly the premise that broke twice.
  Done when: a fixture task filed by `fm ci-watch` goes through plan, prove, finish and status. Every check that reads a start commit has a defined result for it, and a test lists those checks.

- **Reserve usage headroom for the user's live session** — FEATURE — value 5 — effort M — risk med — category: budget
  Why: the steers say `--pace off` drops no work and real usage limits are waited out. A self-started lane burning the window at 3am is fine, but one burning it at 9am starves the user's own session. Per-trigger spend caps don't cover the shared window.
  Done when: unattended fires may spend only the window share above a configured floor. A simulated near-limit window makes the tick defer the fire with a logged reason, and an interactive session is unaffected.

- **Stop unattended lanes from consuming another task's grant** — SECURITY — value 4 — effort S — risk low — category: grants
  Why: the push grant is set on one task and spent on use. Assumption: a timer-started lane in the same repo could reach a grant meant for a different task. No listed idea tests grant scoping against unattended starts.
  Done when: a test arms a publish grant on task A, fires a trigger lane for task B, and the lane's `fm ship` is refused with the grant untouched.

- **Probe the sandbox before relying on it on a hardened kernel** — FIX — value 3 — effort S — risk low — category: unattended
  Why: the platform is `linux-hardened`, which commonly restricts unprivileged user namespaces. The ideas for bubblewrap lanes and kernel jails assume they work.
  Done when: `fm doctor` reports whether `bwrap` or `unshare -U` starts here. If not, the tick marks unattended lanes "unsandboxed" and lowers their autonomy tier instead of failing mid-run.

- **Settle a bet on every self-started fire** — FEATURE — value 3 — effort M — risk low — category: calibration
  Why: ship bets settle from CI and `fm triggers` has precision, but a self-started lane has no stated chance. The user's repeated asks about bets in the ledger suggest this is next.
  Done when: each fire writes a write-once row (chance the user keeps the result). It settles as kept or reverted at 7 days, and `fm outcomes --judgment --by` can split by trigger family.

- **Log which surface the user answers on and route the next yes-card there** — FEATURE — value 3 — effort M — risk low — category: surfaces
  Why: the pack asks what the 61 cells say about surfaces the user never opened. Assumption: the web UI is the only built surface, and nothing records where a yes is actually given.
  Done when: each answered grant records its surface. The next card for the same class is rendered first on the most recently used one, and `fm doctor` lists surfaces never answered on.

- **Verify the first fire after each boot** — FIX — value 3 — effort S — risk low — category: reliability
  Why: assumption: timer persistence and catch-up work in tests but break at boot ordering (network, state dir mount, `/run/user` tmpfs). Nothing covers the first tick after a reboot.
  Done when: the tick records a boot id. On the first tick of a new boot it checks that the state dir, library and auth are reachable, and writes a boot receipt that `fm doctor` shows.

- **Wild: add a prompt-time tick as the no-linger fallback** — FEATURE — value 3 — effort M — risk med — category: fallbacks
  Why: wild; assumption: where timers cannot run, a `PROMPT_COMMAND` or git-hook shim could run the overdue tick the next time the user touches the repo or terminal, which is cheap and needs no privilege.
  Done when: with timers disabled, opening a shell in the repo runs one capped catch-up tick and prints a single "ran N overdue triggers" line.

- **Wild: write a "never do this overnight" sentence at install time** — FEATURE — value 3 — effort S — risk low — category: consent
  Why: wild; the pack's recurring pattern is the user stating limits after the fact. One sentence written once, such as "never touch the billing module", becomes a veto the guard checks for unattended lanes.
  Done when: the install card asks for one optional sentence. An unattended lane whose diff touches a path named in it is held for review, and a test shows the hold.

- **Wild: back-test the missed-ask classes against the trigger layer** — FEATURE — value 3 — effort M — risk low — category: blind spots
  Why: wild; the missed asks (T-2504, T-2525, T-2532 and others) fall into classes: unproven public claims, premise siblings, silent-off paths. Turning each class into a probe run on every new trigger family would catch the next one before the user does.
  Done when: `fm triggers probe` runs one fixture per class against a new family, and a family that fails any of them cannot arm.

Next question: Which unattended-lane failures leave no trace at all (killed by the OS, logged-out session, expired auth), and what would the user see the next morning for each?
Next question: Of the standing steers, which assume an interactive session is present, and what does each do when none is?

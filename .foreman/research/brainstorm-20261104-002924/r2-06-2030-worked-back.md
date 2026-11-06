# Brainstorm — lens: 2030 worked back

- **Strip hooks from the thin `foreman` and `foreman-ui` shim plugins** — FIX — value 5 — effort S — risk low — category: context
  Why: the rename made shims that list the Sampo plugin under `dependencies`. If the shims also carry a `hooks.json`, that would explain SessionStart injecting 2,733 characters twice. Assumption: the shims register hooks; the cause hasn't been checked.
  Done when: with `foreman`, `foreman-ui` and `sampo` all enabled, a recorded SessionStart run shows the injection sentinel exactly once, and a test fails if any shim manifest declares a hook.

- **Run an install-state matrix for exactly-once hooks** — SECURITY — value 5 — effort M — risk low — category: guard
  Why: the 2030 failure is a user who migrated halfway. The states are old only, new only, both, and shim only, and Ward must fire once in each with no gap. Assumption: no such matrix test exists today.
  Done when: a test builds the four plugin sets in a scratch home, and for each one a replayed dangerous command is blocked exactly once and SessionStart emits once.

- **Lint every file the injections and skills tell agents to read against the Read cap** — FIX — value 4 — effort S — risk low — category: docs
  Why: MASTER.md is 75,758 tokens, so Read refuses it. The same problem will hit any other file an injected pointer names. Probe the cap rather than hard-coding it, because it will change by 2030.
  Done when: `sampo doctor` lists each referenced path with its size against the probed cap, and it is red for MASTER.md today and green once the file is sharded.

- **Put a sunset clock on every rename alias** — CLEAN — value 4 — effort M — risk med — category: lean
  Why: every kept old name (shims, `FM_*` and `SAMPO_*` env pairs, `fm` and `sampo` entry points) costs hook time and context, and the double injection is one of those costs. Count hits per alias in a local ledger, announce an end date once an alias has seen no hits for 90 days, then retire it with a tombstone.
  Done when: `sampo aliases` prints each alias with its last-hit date and end date, and a test shows an unused alias flagged and a used one not flagged.

- **Gate on event-total hook latency from the merged hook table** — PERFORMANCE — value 4 — effort M — risk low — category: hooks
  Why: `bench_hooks.py` times Sampo's hooks one at a time, but a session pays the sum of every enabled plugin's hooks per event. The double SessionStart shows the single-hook number understates that.
  Done when: the bench reads the merged settings and plugin hooks, runs every hook registered for each event, and fails the ship gate when the per-event total exceeds a stated millisecond budget.

- **Attach provenance to each Ward rule** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: lean pressure will keep arriving through 2030, and a rule with no recorded reason is the first one cut. Give each rule an incident or command id, a date, and its exam case, then show it with `sampo ward why RULE`.
  Done when: the ship gate fails if a Ward rule lacks provenance fields, and `ward why` prints them for a sample rule.

- **Project the 2030 state size under each retention policy** — PERFORMANCE — value 4 — effort M — risk low — category: state
  Why: 2.4 GB is a single point. Fit the growth per ledger class from history, then show the projected 2030 size under keep-all, 90-day tiering and snapshot-plus-tail, so the retention pick comes with its cost attached.
  Done when: `sampo state project` prints a size per policy for Nov 2030 with its fit error, and the number agrees with a re-measure after a week.

- **Classify state paths as RAM-backed or disk-backed** — FIX — value 3 — effort S — risk low — category: state
  Why: the child working directory sits under `/run/user/1000`, which is normally tmpfs. State that grows there takes memory and disappears on reboot. Assumption: this host mounts it as tmpfs, which needs verifying with `findmnt`.
  Done when: `sampo doctor` shows each state root's filesystem type, and it goes red when RAM-backed state exceeds a set share of `MemAvailable`.

- **Wild: Run Sampo against a simulated 2030 host** — FEATURE — value 3 — effort L — risk med — category: devices
  Why: assumption: by 2030 hosts will have hooks that run in parallel and async, a very large context, no Read cap, and payload fields Sampo has never seen. A fake host with those traits finds sequential or size assumptions before the real host changes. Wild.
  Done when: a fake-host fixture runs the hooks and Ward in parallel with unknown payload fields, and the guard fails closed in every scenario.

- **Wild: Give the state directory a hard filesystem quota** — SECURITY — value 3 — effort M — risk med — category: state
  Why: a pruner that fails silently is how 2.4 GB happens. A btrfs qgroup, a project quota or a size-capped subvolume makes growth fail loudly. Assumption: the user's filesystem supports one of these. Opt-in only. Wild.
  Done when: `sampo state quota set 3G` creates the limit, and a write past it produces a named Sampo error that Ward and the ledgers treat as a degraded state, not a crash.

- **Wild: Hold a six-month rule-regret review in the Genesis report** — FEATURE — value 3 — effort S — risk low — category: lean
  Why: ask what the 2030 maintainer would regret keeping or cutting. Every six months, list each injected line and Ward rule with its cost and its catch record, and let the user mark each one keep or cut.
  Done when: `sampo genesis review` renders the list, and a cut mark removes the line via a task that passes the Ward exam.

- **Count characters injected per turn broken down by owner** — PERFORMANCE — value 3 — effort S — risk low — category: context
  Why: the per-turn burden of 48 to 76 characters has no explained range. Log which line of which hook produced each character, so a creeping line is caught when it appears.
  Done when: `sampo burden --by-line` sums to the measured per-turn total, and the ship gate fails if any line is un-owned.

- **Wild: Make the guard readable as the seed of an independent reimplementation** — SECURITY — value 3 — effort L — risk med — category: guard
  Why: if Sampo is abandoned in 2030, the Ward vectors should outlive it. Export every rule and exam case as plain data plus a 100-line reference checker, so another harness can enforce the same refusals. Wild.
  Done when: the reference checker, run in a fresh directory with no Sampo code, reproduces every Ward exam verdict.

Next question: which of today's four lean gaps would the host fix on its own by 2030, and which will only get worse if Sampo does nothing?

Next question: when lean work lowers a number, how do we confirm the Ward still blocks everything it blocked before, using only data Sampo did not author?

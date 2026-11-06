# Brainstorm — lens: blind spots

Most blind-spot classes in this pack already have an idea on the list, so these are second-order moves and gaps in the two thin areas (performance, privacy). The four recurring questions behind the user's asks are: "what does this gauge not count?", "what input shape makes this slow?", "what stops this loop?" and "is this already built?"

- **Cross every verb and hook with the four recurring blind-spot questions** — FEATURE — value 4 — effort M — risk low — category: coverage
  Why: T-2659 (already built), T-2667 (burden misses a channel), T-2668 (guard on pathological input) and T-2669 (spend without progress) were each fixed one at a time. Nothing asks the same four questions of every other verb. A grid lens exists (T-2672), but not seeded with these questions.
  Done when: a checklist file holds one row per verb and hook × four questions, each cell is answered, a recorded n/a, or a filed task, and `fm doctor` names any empty cell.

- **Bench hook start on a cold page cache** — PERFORMANCE — value 4 — effort S — risk low — category: performance
  Why: assumption: `bench_hooks.py` runs warm. The first hook after a resume or a big build reads Python and `plugin/lib` (133 files) from disk. The run directory is tmpfs but the plugin is not, and nobody measures that first call.
  Done when: a bench step evicts the pages (`posix_fadvise DONTNEED`, and also with bytecode writing off), reports first-call p95 beside warm p95, and fails over a stated bar.

- **Gauge Foreman's tmpfs footprint and daily write volume** — PERFORMANCE — value 3 — effort S — risk low — category: performance
  Why: the working dir is `/run/user/1000/fm-children-1000`, which is RAM-backed. Child scratch, lanes and ledger appends have no bytes-per-day or tmpfs-share line. assumption: nothing reads these today.
  Done when: `fm doctor` prints tmpfs bytes held by Foreman and bytes written per day for the top 3 verbs, and warns above a bar.

- **Pseudonymise identifiers in every outbound model prompt** — SECURITY — value 4 — effort M — risk med — category: privacy
  Why: packs and child prompts carry the user's email, home path and username (the harness context itself includes the email). The earlier privacy ideas cover secrets, site output and prompt logging, not stable identifiers. assumption: no pre-send map exists.
  Done when: a canary email, home path and hostname planted in a pack never appear in the logged outbound prompt, and a local map restores them in the reply.

- **Give every verbatim-user-text store a retention clock** — SECURITY — value 3 — effort M — risk low — category: privacy
  Why: steers, the user's-words ledger, pasted-content captures and eval captures (T-0035) keep the user's raw words indefinitely. `fm forget` is listed but is manual and has no default age-out.
  Done when: each store declares a TTL, `fm tidy` ages out expired entries that no standing rule still cites, and a test shows a cited steer survives.

- **Reset the stall clock only on closes whose diff survives 24 hours** — FEATURE — value 3 — effort M — risk med — category: unattended spend
  Why: `--stall-usd` (T-2669) resets on any close, so a loop of trivial or reverted closes never trips it. "Reset only on closes that landed something" is listed. This adds a survival test, reusing the `fm outcomes` survival signal from the user's weakness-finding steer.
  Done when: a fixture run of closes that are reverted within 24h still trips the stop, and a run of surviving closes does not.

- **Make every Done-when carry a one-line vacuous-pass sentence** — CLEAN — value 3 — effort S — risk low — category: briefs
  Why: T-2583 had a criterion contradicted by its own example. Mutating the Done-when mechanically is listed. This is the cheaper version: the filing step must say how the check could pass while the problem remains.
  Done when: `fm task new` refuses a brief without a "Passes falsely if:" line, and the line shows on the finish card.

- **Normalise timing-test bars by a same-process reference loop** — FIX — value 3 — effort S — risk low — category: test reliability
  Why: the new guard pathology test (T-2668) uses a fixed bar. The machine runs a hardened kernel and shares CPU with lanes, so fixed bars flake or pass loosely. assumption: the bar is absolute.
  Done when: the test asserts a ratio to a calibration loop, and it passes with 4 busy-loop processes running while a planted quadratic pattern still fails.

- **Wild: reboot rehearsal in a throwaway VM** — FEATURE — value 3 — effort L — risk med — category: unattended soak
  Why: wild. The earlier unattended-path questions ("slept, suspended or lost network") have never run on a real machine. The run dir is tmpfs, so a reboot also wipes `fm-children`.
  Done when: a scripted qemu run installs Foreman, starts a drive, power-cuts and boots it, and `fm doctor` after boot shows the drive resumed or named why not.

- **Wild: reverse-engineer the pack from the slate** — FEATURE — value 3 — effort S — risk low — category: brainstorm quality
  Why: wild. After a round, a tool-less child sees only the final slate and writes the context pack it would have needed. Diffing that against the real pack shows which sections were missing, such as the denominator, the built-check or the user's other machines.
  Done when: a command prints the diff for the last slate, and at least one proposed section is not already in the pack builder.

- **Wild: file one "what I suspect I'm wrong about" item per day** — FEATURE — value 2 — effort M — risk low — category: self-doubt
  Why: wild. The user had to catch each gauge defect themselves. A daily item chosen from the gauge with the fewest outside cross-checks, with its cheapest falsifying probe, makes Foreman do that itself.
  Done when: the daily item appears in `fm next` with a probe command, and its result is recorded as confirmed or refuted.

Next question: Which of the user's eight recent asks would a brainstorm have caught if it had run the four questions on every verb first, and how many remain uncaught?
Next question: What does Foreman do on the first call after the machine wakes, reboots or loses the tmpfs, and who tests it?

# Brainstorm — lens: approaches

- **Stop CI cancelling main's own runs** — FIX — value 4 — effort S — risk low — category: ci
  Why: main's newest tests run was cancelled by a slow job, which turned a green sha into a false red alarm (pack: "CI on main is red at eba6705"). GitHub's `concurrency` group with `cancel-in-progress: false` on main queues runs instead of killing them. Assumption: the workflow can take a per-branch concurrency key.
  Done when: two pushes to main within a minute both finish with a conclusion, and neither shows `cancelled`.

- **Make one `make ci` target the only gate entry, local and CI** — CLEAN — value 4 — effort S — risk low — category: ci
  Why: local and CI already run different gates (FOREMAN_CHROME=none is set only in CI, and the Node 24 action pins live in the workflow), so a green local run says little about the remote one. A single target that both call removes the second definition.
  Done when: the workflow's test steps contain only `make ci`, and a test fails if any other run command appears in the workflow file.

- **Run the browser tests on Playwright's pinned headless shell, not the system chromium** — FIX — value 4 — effort S — risk low — category: tests
  Why: CI turns browser tests off because the runner's snap chromium crashes under parallel load (pack: T-1806). A version-pinned headless shell that Playwright downloads removes the snap dependency. Assumption: the project can take the Playwright dependency for tests only.
  Done when: CI runs with FOREMAN_CHROME unset, the browser tests pass five runs in a row under the parallel suite, and no snap path appears in the test output.

- **Gate the gate lock with flat combining** — FEATURE — value 4 — effort M — risk med — category: concurrency — wild
  Why: a waiting `fm check` could give up after 15 minutes, but a combiner design is more interesting: the lane holding the lock drains a request queue and runs each distinct tree hash once for every waiter. A hung check then blocks only its own requests, and nobody waits for a lock they can't see. Assumption: one tree hash can satisfy several waiters.
  Done when: three concurrent `fm check` calls on the same tree hash run the check once, all three report the same verdict, and a check that hangs past its deadline releases the other waiters within 60 seconds.

- **Write the crash-hygiene fake git as a Python script run with `-I`** — FIX — value 3 — effort S — risk low — category: tests
  Why: a shebang shell fake that calls `sleep` broke on Ubuntu 26, where the copied uutils sleep exits at once (T-1807). A Python double run with `-I` never touches PATH or coreutils, so the failure mode can't come back from the runner image.
  Done when: the crash-hygiene tests pass on Ubuntu 26 and a grep of the test doubles finds no call to `sleep`, `git` or other PATH binaries.

- **Budget hooks by instructions retired, not wall-clock p95** — PERFORMANCE — value 3 — effort M — risk med — category: hooks
  Why: the PreToolUse Bash p95 read 310 ms once and 272 ms on a quiet box, so wall-clock budgets flake with load (pack: dropped hook bench). Instruction counts from `perf stat` move far less with load. Assumption: perf is available, or the bench can fall back to `time.process_time` where it isn't.
  Done when: the hook budget check passes at 1.5 load per core and fails when a 50% slowdown is injected into a hook.

- **Mirror blocked items to GitHub Issues with a needs-you label** — FEATURE — value 3 — effort M — risk low — category: blocked pile
  Why: the blocked pile is about ten items (T-0325, T-0335, T-0352 and others) that live only in backlog files, so they get noticed only when the user reads the file. Assumption: the user reads GitHub Issues more often than the repo's backlog. Closing an issue should unblock the item; this is an outward-facing action, so it needs the user's go-ahead before the first sync.
  Done when: each blocked item has exactly one issue, closing an issue moves the item out of blocked, and a second sync creates no duplicates.

- **Delete `fm quiet` and use a plain shell redirect** — CLEAN — value 2 — effort S — risk low — category: cli
  Why: `fm quiet` drops stdin, so a heredoc script silently does nothing (pack: reported exit 0). Instead of fixing the verb, removing it and documenting `>/dev/null 2>&1 </dev/null` removes the bug class and one verb from the surface.
  Done when: no doc or test mentions `fm quiet`, and a heredoc piped through the documented redirect runs its script.

- **Drive the usage governor with a PID controller** — FEATURE — value 3 — effort M — risk med — category: cost — wild
  Why: the per-turn caps catch spikes but miss slow creep, and an integral term does that. Treat burn rate as the process variable and the context ceiling as the actuator, so a steady overspend tightens the ceiling a little each turn. Assumption: the burn log has enough turns to tune the gains.
  Done when: replaying last week's burn log keeps spend within 5% of the pace target, with no single step change in the context ceiling larger than 10%.

- **Generate the CLI from the skill files, with the skills as the source** — CLEAN — value 2 — effort L — risk med — category: plugin parity — wild
  Why: the skill text is what the model reads, so it's already the spec. Compiling the bash CLI from it means a verb can't exist in one place and be missing in the other, which is the parity bug class the pack keeps hitting. Trade-off: skill wording is written for routing, so the generator needs a machine-readable block in each skill.
  Done when: deleting a skill file removes its verb from `fm help`, and the plugin and CLI help output match byte for byte in a test.

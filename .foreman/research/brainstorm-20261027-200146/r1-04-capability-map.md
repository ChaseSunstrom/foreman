# Brainstorm — lens: capability map

- **Route a 10,000-playbook library by index and load only the matches** — FEATURE — value 5 — effort L — risk med — category: playbook routing
  Why: the user asked for tens of thousands of playbooks that are "optimized, not all loaded, actually used", and the library is at 10,000+ scale with none listed.
  Done when: a 10,000-entry fixture routes a 200-query labelled set with top-3 hit rate of at least 90% and loads at most 3 playbook bodies per query.

- **Make the usage budget enforce itself** — PERFORMANCE — value 5 — effort M — risk low — category: token budget
  Why: the user said Foreman "should've figured out" its usage burn itself; compact is now at 200k, but nothing checks it per reply.
  Done when: `fm cost` reports context per reply, and `fm check` fails if any reply exceeds 140k without a compact.

- **Scope the gate lock per project** — PERFORMANCE — value 4 — effort M — risk med — category: gates
  Why: `fm check --affected` and `--evidence` take a machine-wide lock, so builders wait on each other; a full check waits up to 15 minutes.
  Done when: two projects run `fm check --affected` at once and the log shows no lock wait.

- **Release a dead run's edit leases when it stops** — FIX — value 4 — effort S — risk low — category: code runs
  Why: `drop_session` runs only for worker runs, so a model run's leases outlive it and the next run on the same code is refused for 20 minutes.
  Done when: killing a model run mid-edit frees its leases, and a follow-up run on the same files starts without a refusal.

- **Explain any run with `fm code why ID`** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: requested in T-1373; the TUI's stalled card needs a cause and a next command, which the journal already holds.
  Done when: `fm code why ID` on a stalled run prints its status, where it stopped, the stall cause, and the next command.

- **Make `fm quiet` read its script from stdin** — FIX — value 3 — effort S — risk low — category: CLI input
  Why: a heredoc fed to `fm quiet` does nothing and exits 0, which hides the failure.
  Done when: `fm quiet <<'EOF'` runs the script, and a failing script exits non-zero.

- **Probe headless rendering in `fm doctor`** — FEATURE — value 3 — effort S — risk low — category: diagnostics
  Why: the user asked for a probe that says whether headless rendering is available, and if not, why.
  Done when: `fm doctor` prints "headless rendering: available" or names the missing dependency.

- **Guard the rules file's character budget with a test** — CLEAN — value 3 — effort S — risk low — category: rules budget
  Why: the rules file is 6,416 characters against a 6,400 budget, and the user asked for it to be trimmed back under.
  Done when: the rules file is under 6,400 characters, and a test fails when it grows past that.

- **Give each skill a user-only slash command when the model never loads it** — FEATURE — value 3 — effort M — risk low — category: skill listing
  Why: the user asked for skills the model never loads itself, which the hook already covers with the `fm` command, to become slash commands.
  Done when: a user-only skill appears as a slash command and is absent from the model's loaded set.

- **Make the hook latency bench load-aware** — PERFORMANCE — value 3 — effort S — risk med — category: hooks
  Why: the `PreToolUse:Bash:script` p95 was 310 ms against a 300 ms budget, but it runs at 272 ms on a quiet machine, so the failure reflects load.
  Done when: the bench prints the load average with each p95 and fails only when load is under 0.6 per core.

- **Skip "Catch it earlier" follow-ups for "n/a" and "new playbook"** — FIX — value 2 — effort S — risk low — category: task finish
  Why: the user asked for these why-not-caught answers to be skipped, as "none" already is.
  Done when: finishing a task with a why-not-caught of "n/a" or "new playbook" creates no follow-up.

- **Show the playbook library's health as a weather map** — FEATURE — value 3 — effort M — risk low — category: library health — wild
  Why: assumption: the user wants the library "actually used", so per-playbook hit counts would show which entries to prune.
  Done when: `fm playbooks weather` lists hit counts per playbook and flags entries with zero hits over 30 days.

- **Run a hostile reviewer that tries to break each finished change** — FEATURE — value 4 — effort M — risk med — category: verification — wild
  Why: assumption: "prove its work" stops at tests the builder wrote; T-0797 already points at native verification tools.
  Done when: a change with a seeded off-by-one is flagged by the reviewer before the task closes.

- **Hand a half-finished run to a phone with a QR code** — FEATURE — value 2 — effort L — risk med — category: devices — wild
  Why: assumption: the user runs long queues away from the desk, and T-0793 already proposes remote lanes.
  Done when: `fm handoff` prints a QR code that resumes the run on another device with its journal intact.

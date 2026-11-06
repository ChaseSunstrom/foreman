# Brainstorm — lens: simplicity

- **Prune dead code with field coverage** — CLEAN — value 4 — effort M — risk low — category: simplicity
  Why: the plugin has 48 lib modules and 73 skills, and the installer already requires Python 3.12.7+, which includes `sys.monitoring`, so no extra dependency is needed. I assume nothing records which functions ever run in real sessions.
  Done when: `fm doctor --coverage` lists lib functions and skills with zero hits across 30 days of real hook and CLI runs, and a deleted zero-hit item makes no test or `bench_hooks.py` result change.

- **Exit hooks in one stat call when the project isn't Foreman-managed** — PERFORMANCE — value 3 — effort S — risk low — category: hook latency
  Why: assumption: the 14 hook events spawn Python in every Claude Code project, including ones Foreman has nothing to say about. Hooks are latency-gated, and the cheapest hook is the one that never imports anything.
  Done when: in a directory with no Foreman state, a hook command exits 0 without starting Python, and `bench_hooks.py` shows the unmanaged-dir p50 under 5 ms.

- **Run every hook as `python3 -I -S` from an absolute path, packaged as a zipapp** — SECURITY — value 4 — effort M — risk med — category: hardening and startup
  Why: the harness notes say interpreters load a planted `json.py` from the current directory or script directory. Hooks run in whatever repo the user is in, including untrusted clones. Isolated mode with no site import also cuts startup time. Risk: some lib modules may rely on site packages (assumption).
  Done when: a repo containing `json.py` and `sitecustomize.py` cannot affect any hook (tested), and `bench_hooks.py` p50 does not regress.

- **Pass one deadline object through every hook stage** — PERFORMANCE — value 3 — effort M — risk med — category: hook latency
  Why: hooks are latency-gated, but each stage (guard, recall, map lookups) probably budgets itself. A single deadline handed down lets the last stage skip optional work and fail open or closed as declared, instead of overrunning.
  Done when: with an injected 50 ms stall in one optional stage, total hook time stays under its budget, the skipped stage is named in the ledger, and the guard verdict is unchanged.

- **Keep one sensitive-paths registry that guard, redactor, egress scan and Artifact projection all read** — SECURITY — value 4 — effort S — risk low — category: single source of truth
  Why: assumption: the guard, the redactor, the eval-capture scrub, the planned Artifact and ArtifactData publishing, and the push digest each carry their own notion of "secret-ish". Recent commits already show an allowlisted `.env` fixture and a redactor/recall indexing bypass, which suggests the lists drift apart.
  Done when: adding a path pattern in one file changes the verdict in all four consumers, and a test fails if any consumer defines its own list.

- **Make `fm doctor` print one line: green, or the first failing check with its fix** — FEATURE — value 3 — effort S — risk low — category: legibility
  Why: doctor already gates releases and caught the MASTER.md/bisect docs miss. A wall of output hides the one thing to act on, and the user never wants to be handed commands, so the fix should be applied or named, not listed.
  Done when: a healthy install prints exactly one line, and a broken one prints one failing check plus one fix line, with `--all` giving the full table.

- **Add a one-job-per-hook contract lint** — CLEAN — value 3 — effort S — risk low — category: simplicity
  Why: assumption: hooks accrete duties (record, inject, gate, notify) in the same entry point. Each event handler should declare one job in a header line, and a test can check that its module touches only the surfaces it declares.
  Done when: `fm doctor` fails when a hook handler imports a module outside its declared set, and every one of the 14 events has a declared job.

- **Run unattended work on an allowlist learned from the task's own history** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: the guard has grown by blocklist rules (pipe-to-bash, heredoc writes, `python -c` imports), and each fix adds surface. Night runs and lanes execute repeated, predictable command shapes. Under full bypass an allowlist is a smaller thing to reason about. An unknown shape parks the task and captures a question instead of blocking mid-step.
  Done when: in `fm night`, a command shape never seen in that project's successful runs is parked with a recorded reason, a known shape runs unchanged, and interactive sessions behave as before.

- **Wild: Drop a task to bare mode when ceremony costs more than the work** — FEATURE — value 4 — effort M — risk med — category: adaptive minimalism
  Why: wild; the user said "make sure it doesn't sit idle" and complained about step-tracking friction. When guard refusals, asks and step-sync repairs on one task pass a threshold, Foreman suspends its optional passes for that task, keeps only the guard and the done-gate, and logs why.
  Done when: a seeded task that triggers N refusals flips to bare mode, the ledger records the trigger, the done-gate still runs, and the next task starts in normal mode.

- **Wild: Observe-only first week on a new project, then propose the five rules the observation justified** — FEATURE — value 3 — effort M — risk low — category: adoption
  Why: wild; assumption: installing the full discipline on an unfamiliar repo is the most complex moment. Recording without enforcing, then proposing a small rule set from real friction, makes the start simple and evidence-based.
  Done when: a new project in observe mode blocks nothing, and after the window `fm` offers at most five rule proposals, each citing the logged events behind it.

- **Wild: Publish a weekly weigh-in: one number for Foreman's own weight** — FEATURE — value 3 — effort S — risk low — category: simplicity metric
  Why: wild; many ideas add surface, but there is no single figure that counts injected tokens per session, hook milliseconds and command count, so growth is invisible until it hurts. One number with a weekly delta in the statusline makes drift visible.
  Done when: the statusline shows the weight once a week with its delta, and a release that raises it more than 10% fails the release gate unless the change names what it removes.

- **Wild: Give every captured request a one-line "what this replaces" before it becomes a task** — FEATURE — value 3 — effort S — risk low — category: intake
  Why: wild; the queue already holds overlapping captures (T-0755 to T-0760 are all fragments of one request). If intake must name the existing thing a new request supersedes or extends, fragments collapse before they become separate tasks.
  Done when: a burst of three related messages produces one task whose brief lists the fragments it absorbed, and a request that duplicates a shipped capability is answered with a pointer to it instead of a new task.

# Brainstorm — lens: unspoken needs

- **Scope the discipline to Foreman projects only** — FIX — value 5 — effort M — risk med — category: install
  Why: new-user evidence A2 says the install sets bypass mode, the foreman output style, 70% autocompact, a statusline wrapper and 20 deny rules, apparently in global settings. Assumption: these land in `~/.claude/settings.json`, so every non-Foreman repo gets them too, which is the biggest trust cost. Moving them into per-project settings written by `fm init` leaves stock Claude Code everywhere else, and uninstall residue (A10) shrinks too.
  Done when: in a clean HOME after install, a directory never `fm init`ed shows stock settings from `claude config` (default mode, default style, no deny rules), and the same checks in an initialised project show the posture.

- **Run Foreman in directories with no git** — FEATURE — value 3 — effort M — risk med — category: robustness
  Why: this brainstorm's own working directory is not a git repo, and scratch dirs, downloads and new projects often aren't either. Assumption: tier, diff, checkpoint and `task finish --commit` all lean on git. A private shadow repo under the state dir would give diffs and undo without touching the user's folder.
  Done when: in an empty non-git directory, `fm init`, a task with one edit and `fm task finish` complete with a real diff in the evidence, and no `.git` appears in the project.

- **Audit launch hygiene before the public push** — FEATURE — value 4 — effort S — risk low — category: distribution
  Why: assumption: "Foreman" collides with the well-known sysadmin tool (theforeman.org) and `fm` collides with other binaries, which hurts search, `/plugin install foreman` and PATH. The installer also pulls in third-party plugins with no NOTICE or attribution I can see. The stray `skill-index.json` with home paths (T-0836) shows leaks do slip through. One `fm launch-check` could cover name collisions, LICENSE/NOTICE for bundled plugins, marketplace metadata (keywords, min Claude Code version, privacy statement) and committed local paths.
  Done when: `fm launch-check` on a seeded repo flags a planted home path, a missing NOTICE and a colliding binary name, and exits 0 on a clean tree.

- **Turn rivals' loudest complaints into "Foreman must not" tests** — FEATURE — value 4 — effort M — risk low — category: parity
  Why: evidence B says ECC added hook profiles after hook-conflict complaints, and the rivals mostly add commands without rewriting `~/.claude`. Harvest the top public complaints about superpowers, ECC, claude-mem and spec-kit (context bloat, hook collisions, config rewrites, silent installs) into a no-model checklist. Foreman then proves it doesn't do each one, or shows an honest exception. Assumption: those complaint threads are fetchable.
  Done when: `plugin/tests/` has one test per harvested complaint, each citing its source URL, and the suite fails if Foreman reintroduces one.

- **Count the user's escapes from Foreman as the honest satisfaction signal** — FEATURE — value 4 — effort S — risk low — category: measurement
  Why: the 2.6% fixed-later rate only sees rework, not annoyance. Silent signals would show it better: pause or off-switch use, `--no-bypass` reinstalls, sessions that never `fm init`, tasks abandoned right after a gate refusal, and edits made outside a session. Evidence C is output-side only, and nobody has measured whether the author keeps choosing Foreman.
  Done when: `fm digest` prints an "escapes" line (count and top cause) for the last 7 days, computed from the ledger and tested against a seeded escape.

- **Resume a partly failed install from where it stopped** — FIX — value 3 — effort M — risk med — category: install
  Why: the installer does many steps (clone, Python via brew or uv, plugins, wiring, mod). A network failure in the middle (A8 shows a fresh install already ends in a failed `fm doctor`) leaves an unknown half state. Journalling each step would let `install.sh --resume` skip the finished ones and print which step failed and why.
  Done when: killing the installer during the plugin step and re-running it finishes without redoing earlier steps, and the output names the resumed step.

- **Make installs work behind a proxy, mirror or no network (wild)** — FEATURE — value 3 — effort L — risk med — category: privacy
  Why: wild. The user's hardened-kernel, privacy-minded setup suggests offline or locked-down machines matter, but the installer assumes GitHub, brew and uv are reachable. A signed single-file bundle with vendored plugins, the Python wheel and a checksum, plus honoured `HTTPS_PROXY` and mirror variables, would let it install from a USB stick. Assumption: the third-party plugins' licences allow vendoring.
  Done when: `install.sh --offline bundle.tgz` completes in a container with networking disabled and `fm doctor` passes.

- **Run a domain-persona sweep (wild)** — RESEARCH-style FEATURE — value 4 — effort M — risk low — category: reach
  Why: wild. Every fixture and gate is shaped like a Python or web app (`app.py`, unittest/pytest). Cold children play a data scientist, game dev, SRE writing Terraform, a Rust CLI author and a student, each doing one task. They log which verbs, gates and words were nonsense for them, which shows where "THE plugin" stops fitting.
  Done when: a `docs/persona-sweep.md` lists at least 5 personas with their first stall point and a queued task for each distinct stall.

- **Spend a "rival swap day" to find the felt gaps (wild)** — FEATURE — value 4 — effort S — risk low — category: product sense
  Why: wild. B is a survey from outside; the author hasn't lived without Foreman. For one day their own work runs under superpowers (or bare Claude Code) with a one-keystroke "I missed Foreman here / I didn't" tap. This gives a gap list from real use, and a reverse list of what Foreman adds that nobody notices.
  Done when: after the day, `fm research show` holds a two-column list of taps (missed / not missed) with timestamps and the tasks they occurred in.

- **Publish a convergence certificate so "keep going" can end (wild)** — FEATURE — value 4 — effort M — risk low — category: rounds
  Why: wild. Rounds 2 and 3 came back nearly dry, yet the user keeps saying "super super improve, everything, etc.", and a vague mandate with no stop is the real hazard. A certificate would combine yield per round, the rival parity matrix's open cells and the newcomer walkthrough result into "enough for now, here is what would reopen it". Foreman could then end a recursive mandate with evidence and say so. Related ideas (scored mandates, budget envelopes) set targets; this one issues the finish verdict.
  Done when: `fm round close` prints a certificate with at least three measured inputs and an explicit reopen trigger, and a test shows it refuses to certify when the newcomer check fails.

- **Check that every first-run message names its next command** — FIX — value 4 — effort S — risk low — category: onboarding
  Why: A5, A6 and A9 are all instances of one pattern: `fm init` prints a slug, `fm status` prints jargon, `task done` prints four bullets, each with no pointer to what to type next. Rather than fixing each one, add a test that runs the first-ten-minutes flow in a clean HOME and fails if any output ends without a copyable next command or a stated "nothing to do".
  Done when: the clean-HOME walkthrough test asserts every command's final line contains a runnable `fm …` string or "nothing to do", and fails on a seeded counterexample.

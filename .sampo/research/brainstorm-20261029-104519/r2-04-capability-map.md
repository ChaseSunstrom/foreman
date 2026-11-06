# Brainstorm — lens: capability map

- **Turn each DONE-WHEN into a failing test stub at capture** — FEATURE — value 5 — effort M — risk low — category: proof
  Why: nearly every asked item carries a DONE-WHEN, and the recent steers show those checks being wrong (`-k core_integrity` matched no test because the class was `CoreIntegrity`). Aider and Devin turn the spec into a test first. Foreman only lints the spec.
  Done when: capturing `FIX: … DONE-WHEN: …` writes a test file that runs and fails, and `fm task prove` accepts it as the "fails without the change" half.

- **Re-run recorded proofs in CI** — FEATURE — value 5 — effort M — risk low — category: CI
  Why: Foreman's core claim is "proves its work with commands it actually ran", but nothing outside the local machine checks it. The project already has a GitHub Actions test badge. Assumption: proofs are stored as replayable commands.
  Done when: a `fm ci verify` job re-runs each closed task's proof commands on a PR and posts a pass/stale/forged table. A deliberately edited proof turns the job red.

- **Run guard-blocked commands in a disposable sandbox** — FEATURE — value 4 — effort L — risk med — category: sandbox
  Why: the guard only denies commands, which leaves a dead end. Cline and OpenHands run risky steps in containers. The host is Linux with a hardened kernel, so bwrap or a namespace is plausible. Assumption: a rootless sandbox is available.
  Done when: a blocked `rm -rf` on a copy of the tree runs in the sandbox, reports what it would have changed, and leaves the real tree untouched.

- **Calibrate S/M/L estimates against actual time and cost** — FEATURE — value 4 — effort M — risk low — category: forecast
  Why: every task carries an S/M/L tag, and the history of closed tasks supplies actual durations. Nothing compares the two. Assumption: per-task timestamps are stored.
  Done when: `fm forecast` prints the median real time and cost per effort tag. `fm forecast --hours 2` lists the queue items that fit, and its prediction is checked against the next ten closes.

- **Search the project's own history in one place** — FEATURE — value 4 — effort M — risk low — category: recall
  Why: the history is scattered across tasks, lessons, commits, dropped decisions and transcripts. The drop list shows the same ground being re-covered, such as the T-0401 never-idle conflict. Sourcegraph and Cursor index code but not decisions. A local index fits privacy-first use.
  Done when: `fm find "never idle"` returns T-0401 and the dropped Drive offer with their reasons, from a local index and with no network calls.

- **Run the README and rules as tests** — FEATURE — value 3 — effort M — risk low — category: docs
  Why: docs-impact only checks that a doc exists and is named. The README makes concrete claims, including the demo caption and the `fm` commands. Executable docs catch drift that a path check cannot.
  Done when: fenced blocks tagged `fm-check` run in a scratch repo during `fm doctor`. Renaming a documented command makes the check fail.

- **Explain where every setting came from** — FEATURE — value 3 — effort S — risk low — category: config
  Why: budgets, risk limits, optional-work dropping and the ambient run all depend on settings. Several recent fixes were about the reason a behaviour fired (a spent risk budget was mislabelled as usage ahead of pace). `git config --show-origin` is the model.
  Done when: `fm config show --origin` lists each key with its value and source layer, and `fm config explain <behaviour>` names the setting that triggered it.

- **Migrate state with versioned schemas and rollback** — FEATURE — value 3 — effort M — risk med — category: upgrades
  Why: T-0418 (update the installed foreman-ui) is blocked, and the plugin is installed on real machines. Assumption: state files carry no schema version today.
  Done when: state carries a version, `fm upgrade` runs migrations with a backup, and `fm upgrade --undo` restores it. A test upgrades a fixture from three versions back.

- **Generate dependency-update tasks with proof attached** — FEATURE — value 3 — effort M — risk med — category: maintenance
  Why: Renovate opens PRs without understanding the project's gates. Foreman has gates, a security-scan idea and tasks. The pack shows no automated upkeep, only the manual skills-source "moved to ca45fc49" notices.
  Done when: an outdated dependency produces a captured task that bumps it, runs the gates and closes with a receipt, or defers with the failing output.

- **Wild: Send a simulated newcomer through first run on every release** — FEATURE — value 4 — effort M — risk low — category: onboarding
  Why: the tour and the start ladder (T-0862, T-0863) are deferred "until there's evidence", and this produces that evidence. A fresh agent with no prior context follows only the README and the first-run guide, and reports where it got stuck. wild
  Done when: a release script runs the newcomer agent in an empty repo and writes a confusion report. An intentionally broken first-run step shows up in it.

- **Wild: Capture intake by voice** — FEATURE — value 3 — effort M — risk low — category: voice
  Why: the user's history is a stream of short, formulaic requests (FIX/FEATURE with DONE-WHEN and `@path`). That shape suits dictation and parsing, and it is the thing a phone or watch surface needs. Assumption: a local speech model is acceptable. wild
  Done when: a spoken "fix: ship fails when … done when …" lands in the queue as a correctly structured item, with a local model and no network.

- **Wild: Version the discipline profile as a shareable file** — FEATURE — value 3 — effort M — risk med — category: sharing
  Why: lessons, gates and the ceremony level are what make Foreman useful, and T-0794 (a Lite mode) and T-0869 (import from rivals) point at a portable form. A profile file lets one project borrow another's rules and publish its measured held-rate (T-0867). wild
  Done when: `fm profile export` produces one file and `fm profile apply <file>` installs it in a fresh repo. `fm doctor` then reports the same gates and lessons.

- **Wild: Fuzz the guard hook from its own deny history** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: the guard stops commands you would never want run in bypass mode, and bypasses are the highest-stakes failure. Mutating each denied command (quoting, `$IFS`, subshells, aliases, base64) tests it the way AFL tests parsers. The `_DCWD` drop shows that depth-0 handling is subtle. wild
  Done when: a fuzz run takes every past deny and produces N mutants. Any mutant that is destructive but allowed is written out as a failing test.

- **Render a task's proof chain as a one-page report** — FEATURE — value 3 — effort S — risk low — category: receipts
  Why: close-out legibility (T-0795) is deferred, and the new receipt ideas stop at the terminal. A static HTML page with the request, plan, diff, proof output and test-fails-without-change evidence can be shared with a reviewer who does not run Foreman.
  Done when: `fm task report T-1213` writes one HTML file with the DONE-WHEN, the commands run, their output, and the diff. The file opens offline.

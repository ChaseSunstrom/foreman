# Brainstorm — lens: adoption and onboarding

- **Publish Foreman to uvx, pipx and Homebrew** — FEATURE — value 4 — effort M — risk low — category: distribution
  Why: Every rival onboards with one command through a package manager (`npx ecc-universal setup`, `uv tool install specify-cli`). Foreman's only path is `curl | bash`, plus a clone for private repos. Assumption: a thin wrapper package can run the existing installer with its flags.
  Done when: in a clean HOME, `uvx foreman-cc install --plan` prints the install plan without changing anything, and `brew install` of the tap puts `fm` on PATH.

- **Propose three starter tasks from the repo's own signals at `fm init`** — FEATURE — value 5 — effort M — risk low — category: first win
  Why: Evidence A6 and A7: `fm init` prints only a slug, and `fm check` finds no gate. A newcomer's first session faces a blank queue and has to invent a task. Assumption: the map plus a failing-test run, TODO/FIXME comments and lint output yield 3 safe candidates.
  Done when: running `fm init` on a fixture repo with one TODO and one failing test lists both as ready-to-approve briefs, with the detected test runner already set as the gate.

- **Show a setup ladder in the statusline** — FEATURE — value 4 — effort S — risk low — category: activation
  Why: The "fresh install fails its own doctor" and "jargon everywhere" findings show no feedback on whether setup is complete. Assumption: five milestones are enough (init, first capture, first task finished with evidence, first held task, first `fm doctor` pass). Only the next step's exact command is shown, and the ladder vanishes after the fifth.
  Done when: a clean-HOME run shows `Foreman 1/5 · next: fm capture "…"` and advances after each milestone. The milestone timestamps stay local and can be read with `fm doctor --funnel`.

- **Run one task under Foreman, then offer keep or drop with `fm once`** — FEATURE — value 4 — effort M — risk med — category: trial
  Why: A2 shows the default install is a large trust ask (bypass mode, 20 deny rules, third-party plugins). Rivals "add commands, they don't rewrite ~/.claude". `fm once "<request>"` would apply Foreman through session-scoped settings, run exactly one task, and print a receipt of evidence, time, tokens and what the guard blocked. Assumption: `--settings` overlays are enough for guard and drive behaviour.
  Done when: `fm once` leaves `~/.claude` byte-identical before and after, and the receipt ends with `keep` and `remove` commands.

- **Add a managed-install profile for company machines** — FEATURE — value 3 — effort M — risk med — category: enterprise
  Why: Silent third-party plugin installs and bypass-by-default would fail any IT review (A2). Assumption: team leads exist among adopters. The profile installs no third-party plugins, makes no network calls after install, and writes the guard to a managed-settings file. It also emits a one-page signed statement of every file written.
  Done when: `install.sh --managed --plan` lists zero outbound hosts after install and produces the manifest, and uninstall removes everything the manifest lists.

- **Ship an offline, resumable installer bundle** — FEATURE — value 3 — effort M — risk med — category: install
  Why: The installer downloads Python through uv or Homebrew when the system one is too old. That fails on air-gapped or flaky networks and is not resumable. Assumption: a tarball with a vendored interpreter and checksums is feasible on Linux x86_64, arm64 and macOS.
  Done when: with the network disabled, `./install.sh --bundle foreman.tar.zst` completes in a clean HOME. Killing it mid-way and re-running resumes without duplicating wiring.

- **Test install across shells and distros in CI and publish the matrix** — CLEAN — value 3 — effort M — risk low — category: compatibility
  Why: A3 (`fm` not on PATH) is a shell-wiring failure. The pack shows the author on a hardened Arch kernel, so fish, zsh, nushell and hardened-host quirks are likely gaps. Assumption: only bash/zsh are tested today.
  Done when: CI installs into clean containers for bash, zsh, fish and nushell on 3 distros. Each run verifies that `fm --version` works in a fresh login shell, and a support-matrix page is generated from the results.

- **Make installer and first-run output safe for non-tty, NO_COLOR and screen readers** — FIX — value 2 — effort S — risk low — category: accessibility
  Why: A8 shows the install prints about 40 lines of passes. Piped installs (`curl | bash`) and CI logs need one line per step without ANSI or spinners, and a final summary line. Assumption: the current output uses colour and cursor control unconditionally.
  Done when: `NO_COLOR=1 ./install.sh | cat` contains no escape codes, and the last line is a one-sentence verdict.

- **Ship `fm repro-bench`, a skeptic's kit that reruns the headline claim locally** — FEATURE — value 4 — effort L — risk med — category: proof
  Why: C shows the bench has 1 case and 0/3 court cases, so nothing proves Foreman helps. The proof-page idea is a claim for people to read. This adds a command that fetches a pinned task set, runs bare Claude Code and Foreman on the user's own quota, and prints the held-rate with its denominator and variance.
  Done when: with a stubbed model, `fm repro-bench --dry` runs both arms on three fixtures and prints a table with n and a confidence interval.

- **Wild: let Foreman offer to uninstall itself at day 14 if it can't show lift** — FEATURE — value 4 — effort M — risk low — category: trust
  Why: Rival plugins accumulate cruft. A "remove me" offer backed by the user's own measured numbers is rare and builds credibility. Assumption: the digest's graded-versus-ungraded counts and gate catches give a usable lift signal. When no gate caught anything, the card says so and offers `fm lite` or a removal command.
  Done when: on a fixture ledger with zero gate catches, day 14 shows the card and `fm unwire --yes` restores the prior settings.

- **Wild: publish a browsable, redacted replay of the author's real ledger** — FEATURE — value 3 — effort M — risk med — category: proof
  Why: The ledger holds 688 finished tasks, with 18 fixed later (2.6%) and a 7-day tally of 188 strong, 23 ok and 159 folded. A real, uneven record may persuade more than a marketing strip. Assumption: the existing redaction and `fm page` machinery can strip paths and secrets. Mistakes stay visible.
  Done when: a static page lists the tasks, each with brief, evidence and outcome, with the 18 "fixed later" ones filterable. A secrets-scan test over the output passes.

- **Wild: add `fm spar`, a seeded-bug drill on a throwaway copy of the user's own repo** — FEATURE — value 4 — effort M — risk med — category: first win
  Why: `fm demo` shows enforcement on a fixture, not on the user's code. In a temp worktree, Foreman plants one small mutation that the repo's own tests should catch. It then shows the gate refusing a "done" claim without evidence and the red-to-green fix. The user's real tree is never touched. Assumption: a mutation that breaks at least one test can be found cheaply with the test map.
  Done when: `fm spar` on a repo with tests leaves `git status` clean in the original tree and prints the refused-done and verified-fix sequence in under 3 minutes, with no model calls.

# Brainstorm — lens: capability map

- **Gate performance on instruction counts, not seconds** — PERFORMANCE — value 4 — effort M — risk low — category: perf gates
  Why: The gates are `bench_hooks.py --runs 20` and wall-clock. T-0744 already had to hide real machine load from tests, so timing gates are noisy. Assumption: `perf stat -e instructions` or valgrind is available on the user's Linux box.
  Done when: running `bench_hooks.py` twice, once idle and once under `stress`, gives the same instruction-count verdict, and a deliberately added 50 ms import fails it either way.

- **Neutralize git config execution vectors in untrusted clones** — SECURITY — value 4 — effort S — risk low — category: supply chain
  Why: Assumption: the guard reads commands, but `core.fsmonitor`, `core.hooksPath`, `diff.external`, textconv and filter drivers in a cloned repo's config run code when a plain `git status` or `git diff` executes. Quarantine ideas so far cover Claude config, not git config.
  Done when: in a fixture repo whose `.git/config` sets `core.fsmonitor` to a script that writes a marker file, Foreman's `git status` leaves no marker and reports the neutralized key.

- **Jail dependency installs with a lifecycle-script allowlist** — SECURITY — value 4 — effort M — risk med — category: supply chain
  Why: Assumption: `npm install`, `pip install` sdists and `cargo build` scripts execute arbitrary code in bypass mode. "Gate dependency changes" inspects what was added, not what the install runs. Installs would default to `--ignore-scripts` or a no-network build, and a script runs only if allowlisted.
  Done when: installing a fixture package whose postinstall touches a marker file leaves no marker, and the ledger records "script blocked: pkg@ver".

- **Defend `fm serve` against DNS rebinding and cross-origin calls** — SECURITY — value 4 — effort S — risk low — category: web UI
  Why: The pack lists the web UI as a surface. A localhost server that steers a bypass-mode agent is a prime rebinding target. Desktop IPC lockdown is covered, but the HTTP surface is not. Assumption: today it has no Host/Origin check or per-launch token.
  Done when: a request with `Host: evil.example` or a foreign `Origin` returns 403, and a state-changing call without the launch token fails in a test.

- **Rank dependency advisories by call-site reachability** — SECURITY — value 3 — effort M — risk low — category: vuln triage
  Why: Snyk and Semgrep Supply Chain differentiate on "is the vulnerable function actually called". Foreman has `fm map` and could use LSP references. Assumption: advisories come from `pip-audit` or `npm audit` output.
  Done when: for a fixture with two advisories, one on a called function and one on an unused one, the report ranks them as called/unreached and files a task only for the called one.

- **Derive a per-task native sandbox allowlist from the plan** — SECURITY — value 4 — effort M — risk med — category: sandbox
  Why: Foreman runs bypass-mode and the guard is heuristic. Claude Code's own sandbox settings accept filesystem and network allowlists. Assumption: the sandbox can be set per lane through a `--settings` overlay. The plan's footprint and the project's gate commands would generate the allowlist, and a violation becomes a logged "plan was wrong" event.
  Done when: a lane for a task scoped to `plugin/lib/` fails an attempt to write outside it and to reach an unlisted host, and `fm doctor` shows the allowlist in force.

- **Vet native allow rules against the guard corpus** — SECURITY — value 3 — effort S — risk low — category: permissions
  Why: `fewer-permission-prompts` writes allow rules into settings. Nothing checks that rules like `Bash(python3:*)` or `Bash(git:*)` don't open what the guard exists to block. Assumption: the guard has a replayable refusal corpus (T-0754 mentions an eval inbox).
  Done when: a settings file with `Bash(python3:*)` is flagged with a refusal-corpus command it would let through, and a narrow rule passes.

- **Detect real PII entering fixtures, logs and commits** — SECURITY — value 3 — effort M — risk low — category: privacy
  Why: Secret scanning exists, with an allowlist for the `.env` fixture (T-0671). Real emails, phone numbers, tokens-in-URLs and customer rows pasted from a bug report are a separate class. Assumption: "intake reads pasted transcripts" will feed more real data into repos.
  Done when: a diff adding a fixture with a real-looking email and SSN fails the done-gate with the line numbers, and a synthetic `example.com` address passes.

- **Share one tokenised diff across all done-tail scanners** — PERFORMANCE — value 3 — effort M — risk low — category: done-tail
  Why: The debug-scaffolding scan flagged docs (CHANGELOG.md:10) and string literals (test_execution.py:102), so scanners parse text independently and wrongly. One tokenised, language-aware diff index would fix those false positives and cut repeated parsing. Assumption: scanners each re-read the diff today.
  Done when: both false-positive cases pass, the scaffolding, secret and hallucinated-API scanners read from one shared index, and done-tail time on a 500-line diff drops by a measured amount in `bench_hooks.py`.

- **Drive real debuggers over DAP for FIX tasks** — FEATURE — value 3 — effort L — risk med — category: debugging
  Why: Best-in-class agents (Devin, Cursor) mostly print-debug. The existing ideas cover traces and instrument-first, not breakpoints and watch-expression capture. Assumption: `debugpy` and Node inspect can run headless.
  Done when: on a fixture bug, a FIX run sets a breakpoint, records the local variables at the failing call as evidence, and the finding cites that capture.

- **Ship hooks as one precompiled zipapp run with `python -I -S`** — PERFORMANCE — value 3 — effort S — risk med — category: hook latency
  Why: The hook latency gate exists and the lib has 48 modules. Isolated mode skips site and user-path scanning, and a prebuilt `.pyc` archive skips compile checks. It also blocks the planted-`json.py` import hijack. Assumption: startup is still dominated by interpreter and import cost.
  Done when: median PreToolUse hook latency falls versus the current baseline in `bench_hooks.py`, and a `json.py` placed in the cwd is not imported.

- **Wild: Run public exploit PoCs against the project's pinned dependency versions in a sandbox lane** — SECURITY — value 3 — effort L — risk med — category: exploitability proof
  Why: wild. A scanner says "CVE present". Proof turns that into "exploitable here" or "not exploitable". Assumption: PoCs can be fetched under an explicit setting and run only in a network-off lane.
  Done when: for a fixture with a known-vulnerable pinned version, the lane reports "exploited" with output, and after the bump the same PoC reports "not exploited".

- **Wild: Require a hardware-key tap to release one-way doors** — SECURITY — value 3 — effort M — risk med — category: approvals
  Why: wild. Signed and cooling-off approvals exist as ideas, but a prompt-injected agent that can type into tmux can fake a typed "yes". A FIDO2 touch can't be faked from inside the session. Assumption: the user owns a security key.
  Done when: `git push --force` and a `rm -r` outside the repo are refused until a key tap is recorded, and a typed "approved" alone doesn't release them.

- **Wild: Propose vendoring the 20 lines you actually use from each heavy dependency** — CLEAN — value 2 — effort L — risk med — category: dependency diet
  Why: wild. Each dependency is attack surface and install time. Foreman's own installer already demands Python 3.12.7+ and extra tools. A pass would measure which functions are called, inline them with their tests, and propose dropping the package.
  Done when: on a fixture using one function from a large package, the proposal removes the dependency, its tests still pass, and the lockfile shrinks.

# Brainstorm — lens: capability map

- **Run a recoverability preflight before bypass or irreversible grants** — FEATURE — value 4 — effort M — risk low — category: safety nets
  Why: assumption: the guard blocks bad commands, but nothing checks whether the user could recover from one that gets through. Backup tools (restic, borg, snapper, timeshift) all report a last-run time, and git knows unpushed and untracked work. The preflight prints "3 unpushed commits, 7 untracked files not ignored, last snapshot 11 days ago" and offers `fm preflight --fix` (stash ref or push).
  Done when: `fm preflight` in a fixture repo with unpushed commits and an old fake snapper timestamp lists both numbers, and the same figures appear in the bypass exposure receipt.

- **Confine fm's own hook and verb processes with Landlock** — SECURITY — value 3 — effort M — risk med — category: self-sandbox
  Why: assumption: OpenBSD pledge/unveil is the best-known pattern; Linux 7.x ships Landlock, and the pack lists no self-confinement of Foreman's processes. Each hook gets `no_new_privs` and write access to the state dir and repo only. A hook bug or hostile input then cannot write elsewhere.
  Done when: a test hook that tries to write `~/.bashrc` gets EACCES while normal hook runs pass, and the process falls back with a doctor WARN where Landlock is unavailable.

- **Check that `fm`, `git` and `python3` resolve to trusted paths** — SECURITY — value 3 — effort S — risk low — category: PATH integrity
  Why: assumption: a session could place an `fm` or `git` shim earlier on PATH, in a repo-local or user-writable directory. Then the user's next `fm ship` or the drive runs it. Lynis and rkhunter do this check; the pack has installed-versus-source drift but nothing on PATH resolution.
  Done when: planting `./bin/fm` ahead on PATH in a fixture makes `fm doctor` and `fm ship` print the resolved path and refuse.

- **Warn when the host CLI is older than its published security fixes** — SECURITY — value 3 — effort S — risk low — category: upstream advisories
  Why: assumption: the pack has a daily model-ID probe and host release-note watching, but no check of the installed `claude`, `codex` or `gemini` version against known permission-bypass advisories. The check is opt-in and fetches the advisory list only when the user sets it, per the privacy lens.
  Done when: with a stub advisory file naming fix version 9.9.9 and a stub `claude --version` of 9.9.8, `fm doctor` shows one WARN with the advisory id, and nothing is fetched while the setting is off.

- **Import OWASP LLM/agentic and MITRE ATLAS technique lists as threat rows** — FEATURE — value 3 — effort S — risk low — category: threat catalogue
  Why: assumption: GTFOBins and rivals' fixed bugs are queued, but no external agent-threat taxonomy is. Each technique becomes a row marked covered (test named), n/a (reason) or gap, so the gaps come from a list Foreman didn't author.
  Done when: the catalogue file has at least 20 rows, each naming a test or a recorded n/a, and `fm genesis check` fails on a row with neither.

- **Stamp commits with a Guarded-by trailer and verify it later** — FEATURE — value 3 — effort S — risk low — category: attestation
  Why: assumption: `Proven:` and `Unproven:` trailers are proposed, but not one recording guard version, mode, calls judged and overrides. `fm verify-commit SHA` rechecks the trailer against the ledger, so a human-made commit with a forged trailer is caught.
  Done when: a commit made in a fixture session carries the trailer, and `fm verify-commit` passes on it and fails on a hand-edited copy.

- **Unwrap interpreter one-liners and wrapper commands in the guard** — SECURITY — value 4 — effort M — risk med — category: guard parsing
  Why: assumption: the guard may judge `python -c`, `node -e`, `perl -e`, `xargs`, `find -exec`, `timeout` and `env` by command shape alone. The idea unwraps them and maps embedded calls (`shutil.rmtree`, `fs.rmSync`, `os.system`) to the same danger classes as `rm -rf`.
  Done when: `python3 -c "import shutil; shutil.rmtree('/home/x')"` is blocked like `rm -rf /home/x`, with a benign `python3 -c "print(1)"` still allowed in the guard's test table.

- **Run every hook under rlimits and a bounded stdin read** — PERFORMANCE — value 3 — effort S — risk low — category: hook resilience
  Why: assumption: a 200 MB tool response could stall or OOM a hook that reads it whole. Setting CPU, address-space and file-size limits and capping the payload read turns that into a named, declared fail mode.
  Done when: feeding a 200 MB payload to the guard hook exits within the bench budget with a crash card, and the declared fail mode (closed in bypass) is what happens.

- **Diff the guard against the user's own settings.json permission rules** — FEATURE — value 3 — effort M — risk med — category: second opinion
  Why: assumption: the user's allow and deny rules are a second, human-written policy. Replaying each bash call against them and logging disagreements with the guard, in both directions, exposes rules Foreman ignores and rules it over-enforces.
  Done when: a fixture deny rule for `git push --force` yields a "user denies, guard allows" row in `fm guard disagreements`.

- **Wild: Cap irreversible grants with a monthly budget** — FEATURE — value 3 — effort M — risk med — category: risk budget
  Why: wild, assumption: like an SRE error budget, each month holds N irreversible-class grants and every use is shown being spent. When the budget is empty, bypass drops to ask mode until the month resets, or until the user tops it up with a recorded costly decision.
  Done when: with budget 2, the third irreversible grant in a fixture month is refused with the remaining-budget line and the one command that tops it up.

- **Wild: Add decoy off-switch verbs that only log** — SECURITY — value 3 — effort S — risk low — category: tripwire
  Why: wild, assumption: an agent probing for a way to disable the guard will try names like `fm guard off` or `fm disable-guard`. Decoys do nothing but record a loud event with the calling context, and the session does not stop.
  Done when: running a decoy verb exits with a bland error, appends one `decoy_probe` ledger line, and the next `fm doctor` lists it.

- **Wild: Trend the model's own recklessness with a weekly bait suite** — FEATURE — value 4 — effort L — risk med — category: model propensity
  Why: wild, assumption: the pack has a guard vaccination drill, but no measure of how often the current model reaches for a destructive command when handed bait ("delete this dir to fix the build"). Runs per model ID give an attempt rate, and a new model ID with a higher rate auto-tightens guard tiers until reviewed.
  Done when: a 30-prompt fixture suite run on two stub models writes per-model attempt rates, and the higher one flips a visible tier setting.

Next question: Which of these (interpreter unwrapping, PATH integrity, the Landlock hook sandbox) are already built, and can a no-model scan of `fmguard`, `fm doctor` and the hooks answer that before any is filed?
Next question: When the user answers a guard block with a hand-run workaround, does anything capture that, so a safety rule gets loosened by evidence and not by annoyance?

# Brainstorm — lens: blind spots

**Method.** The missed asks fall into six classes, and I ask each class's question of the whole project. Each idea below is not in the "so far" list.

- **Control arm** (T-2534/36): which part pays for itself?
- **Cause naming** (T-2535): did the gate say why it tripped?
- **Silent death** (T-2542): what stops without anyone noticing?
- **Already built** (T-2546): did we check before building?
- **Input contamination** (T-2547/54): who wrote the input?
- **Partial input** (T-2566): what does the procedure do on half the data?

The ideas below concentrate on the thin categories: security, privacy, performance, devices and developer experience.

- **Harden the web UI against DNS-rebinding and cross-origin calls** — SECURITY — value 5 — effort S — risk low — category: security
  Why: assumption: `plugin/templates/web/index.html` is served by a local process. Silent-death class asked as "what can an outsider reach?" A page in the user's browser can call any loopback verb that mutates state (grants, ships) unless Host, Origin and a per-launch token are checked.
  Done when: a test request with a foreign `Host` or `Origin`, or with no token, gets 403, and `fm doctor` reports the web server's bind address and token state.

- **Make the guard protect its own configuration** — SECURITY — value 5 — effort M — risk med — category: guard
  Why: assumption. Control-arm class asked as "what can the agent edit that the guard relies on?" In bypass mode an agent can rewrite the hooks entries, the guard rules or the grant files that its own commands depend on. Existing ideas cover rule text injection, not edits to the config.
  Done when: a scripted session that edits the hook registration or the guard rules is blocked or flagged, and `fm doctor` names the file hashes it checks.

- **Prove local-only mode under a network namespace** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: assumption. Contamination class asked as "what leaves the machine?" The privacy rule says nothing is sent without a setting, but no test shows it. The host is a hardened-kernel Linux, where `unshare -n` is available.
  Done when: `fm doctor --offline-proof` runs the offline-capable verbs with no network and reports zero connection attempts, or names the verb that tried.

- **Ledger every prompt sent to a model child** — SECURITY — value 4 — effort M — risk low — category: privacy
  Why: the pack shows many `claude -p` children (brainstorms, cold reads, exams). The class asked is "what content did each one see?" An append-only line per child records model, byte count and source files, with no content stored.
  Done when: `fm egress --since 7d` lists children by model, bytes and source paths, and a test shows a path on a denylist never appears as a source.

- **Gate and ratchet CLI cold start per verb** — PERFORMANCE — value 4 — effort S — risk low — category: speed
  Why: the repo has `plugin/lib/` with 131 files and a hook bench, but the evidence shows the bench is for hooks only. The class asked is "where does a user wait that nothing measures?" Python import time per verb is invisible until it grows.
  Done when: `fm doctor` shows p95 wall time for the 10 most-typed verbs, and `fm ship` fails when one grows past a recorded budget, naming the import that grew.

- **Split the ship gate into a fast and a full suite with a timing trend** — PERFORMANCE — value 4 — effort M — risk med — category: gate speed
  Why: the standing rule makes every push go through the full suite, and the repo has 404 files under `plugin/tests/`. The class asked is "does the gate name its cause and its cost?" Only the full run counts for push. The fast subset is affected-tests-first, so a failing change reports sooner.
  Done when: a red change prints its failure within a stated fraction of the full run, and the full run's wall time is recorded per ship with the commit that grew it.

- **Render every verb under NO_COLOR, narrow width and a non-UTF-8 locale** — FIX — value 3 — effort S — risk low — category: developer experience
  Why: assumption: the output is tuned for the maintainer's terminal. The class asked is "which surface did we never try?" Hookless and remote harnesses (Codex, Gemini, opencode) often run without a TTY.
  Done when: a test runs all verbs with `NO_COLOR=1`, `COLUMNS=40` and `LC_ALL=C`, and fails on escape codes, wrapped tables or a mojibake crash.

- **Run the suite on the oldest supported Python and a second OS userland** — FEATURE — value 4 — effort M — risk low — category: portability
  Why: the standing rule says Foreman is not Claude-specific, and the site pushes `install.sh` as the install path. The class asked is "what passes only on our machine?" This catches `sed`, `date` and Python-version assumptions before a new user does.
  Done when: CI runs `fm doctor` and the roundtrip e2e on the minimum Python and on macOS, and the matrix result shows in the README badge.

- **Emit a status-bar line for waybar, polybar and tmux** — FEATURE — value 3 — effort S — risk low — category: devices
  Why: assumption: the user lives in a terminal on Arch. The class asked is "where does the user already look?" A one-line `fm status --bar` with a stale marker puts work, the next due item and the tick's liveness on the surface already open.
  Done when: `fm status --bar --json` prints under 80 chars and shows "stale" when its source is older than three intervals.

- **Check that published release artifacts match the tag** — SECURITY — value 4 — effort M — risk low — category: supply chain
  Why: `fm release` exists and the site distributes installs. The class asked is "what does a new user trust without checking?" `install.sh` should verify a checksum from the tagged release before it runs anything.
  Done when: `install.sh` aborts on a checksum mismatch, and a test with a tampered archive proves it.

- **Wild: Plant canary secrets and fail any output that carries one** — SECURITY — value 4 — effort M — risk low — category: privacy
  Why: wild. Place unique fake tokens in the env, in `~/.config` and in a fixture state dir. The release gate, the support bundle and the `genesis live` publish all fail when any output contains a canary.
  Done when: a seeded canary in a fixture state dir appears in no published file, and a deliberate leak makes the gate red.

- **Wild: Keep a ring-buffer flight recorder of the last 200 hook calls** — FEATURE — value 3 — effort M — risk low — category: debuggability
  Why: wild, from the silent-death class. A fixed-size local file stores verb, decision and duration per hook call, with no content. After a mystery slowdown or a surprise block, `fm blackbox` answers "what just happened" without reproducing it.
  Done when: after a blocked command, `fm blackbox` shows the rule id and time, and the file never exceeds its size cap.

- **Wild: Mutate each steer's check and see whether the gate notices** — CLEAN — value 3 — effort M — risk low — category: assurance
  Why: wild. The pack holds 40-plus standing rules, each with an automatic check. Flip one check's input in a scratch copy, and a check that stays green is a rule only on paper.
  Done when: `fm decide --check --mutate` lists the steers whose check passed on a deliberately broken input.

Next question: Which gate or check in this project has never been seen to fail, and what would make it fail on purpose?

Next question: Which Foreman feature does a user on a non-Claude harness, with no TTY and no hooks, still reach in practice?

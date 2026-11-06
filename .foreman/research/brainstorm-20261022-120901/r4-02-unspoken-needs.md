# Brainstorm — lens: unspoken needs

- **Re-verify closed tasks when later commits touch their files** — FEATURE — value 4 — effort M — risk low — category: trust
  Why: the ledger is past T-1478 and every close rests on a proof run once, at close time. Nothing in the pack shows a later commit being checked against an earlier task's proof. The canary only catches whole-suite breakage.
  Done when: committing a change to a file named in a closed task's verify scope reruns that task's stored verify command, and a red result reopens the task with the commit hash attached.

- **Confine workers with Landlock through ctypes** — SECURITY — value 4 — effort L — risk med — category: containment
  Why: assumption: the host kernel is `linux-hardened`, which usually disables unprivileged user namespaces, so bubblewrap-style cages may simply not work here. Landlock needs only syscalls reachable from stdlib `ctypes`, which fits the no-new-deps rule. The app's start event is already meant to name its containment.
  Done when: on a kernel with Landlock, a worker's write outside its worktree fails with EACCES, and the start event reads `containment: landlock`. Without Landlock it reads `guard only`.

- **Add an allow-corpus that harmless commands must pass** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: the evasion corpus covers the 24 dangerous commands, and the SNAPSHOT steer shows verdicts are subtle. The reverse failure, a false block in bypass mode, has no ratchet.
  Done when: a locally mined list of at least 200 real benign commands from the user's shell and session history runs in CI, any new block fails the test, and `fm guard why` prints the matching rule.

- **Probe each task's premise before building** — FEATURE — value 4 — effort S — risk low — category: intake
  Why: two recent drops were "premise false" (the stale-cache claim, the auto-accept claim), found only after review work was spent.
  Done when: a captured FIX can carry a one-line premise command. `fm next` runs it at claim time, and a failing premise closes the task as `premise-false` with the command output as evidence.

- **Attach deferred ideas to active work by file overlap** — FEATURE — value 4 — effort M — risk low — category: backlog
  Why: more than 20 "Later from T-07xx / T-08xx" bucket tasks hold hundreds of ideas that no one reads, so they only get thawed by hand.
  Done when: claiming a task that edits files an idea names adds a "while you're here" list of at most 3 matching ideas to its brief, and ignoring them costs nothing.

- **Ship `fm img`, a stdlib PNG codec with pixel diff** — FEATURE — value 4 — effort M — risk low — category: visual proof
  Why: many ideas lean on screenshots (visual diffs, look fingerprints, before/after receipts), but Foreman is stdlib-only and has no way to read or compare pixels. `zlib` and `struct` are enough.
  Done when: `fm img diff a.png b.png` exits non-zero past a set threshold and writes a diff PNG, and the round-trip test is byte-exact on a fixture.

- **Render foreman-ui from recorded fixtures with no live Claude session** — CLEAN — value 4 — effort M — risk low — category: mod dev loop
  Why: T-0166 and T-0418 and the stale-cache confusion show that changing the band, pane or status line currently means a live Claude Code to see the result.
  Done when: `fm ui render fixture.json --width 80` prints the band, pane and status line to stdout, and a golden-text test covers each.

- **Lock the guard and gates against the improvement loop** — SECURITY — value 4 — effort S — risk low — category: self-modification
  Why: "super recursive" invites Foreman to edit itself unattended. The reverted auto-accept and the protected-core steer show the user wants the safety core to need a human.
  Done when: an unattended round that touches the guard, canary or gate files stops with a proposed patch instead of a commit, and the lock list is printed by `fm doctor`.

- **Move Foreman's state between machines with `fm home export|import`** — FEATURE — value 3 — effort M — risk low — category: portability
  Why: assumption: the user's setup (Arch, `tui.toml`, `code.toml`, lessons, ledger) is hand-built and a reinstall would lose it. Secret-free export is not covered by the pasteable-setup-code idea, which carries only look and runners.
  Done when: export-then-import into an empty `$FOREMAN_HOME` reproduces the task list and lessons, and a scan finds no keys in the archive.

- **Learn backlog priorities from two-way choices** — FEATURE — value 3 — effort M — risk low — category: prioritisation
  Why: the user steers by reaction (asked, dropped, steered) rather than by ranking, and the open list has dozens of equal-looking deferred items.
  Done when: `fm next --teach` shows two tasks, records the pick, and after 10 picks `fm next` orders by the learned weights and prints the top one.

- **Emit "The user's own words" once in the pack** — FIX — value 2 — effort S — risk low — category: brainstorm
  Why: this pack contains that whole section twice, and the dedupe list is already thousands of lines.
  Done when: a test builds a pack and asserts every section header appears once.

- **Roll looks while idle to learn taste** — FEATURE — value 3 — effort M — risk low — category: taste — wild
  Why: assumption: the user dislikes generic styles but won't fill in a taste survey. Idle time is free signal.
  Done when: after 60 s idle the app shows full-screen generated looks, one key keeps or skips each, and the picks land in a local taste file that `fm design` reads.

- **Warn when releasing in the user's historically bad hours** — FEATURE — value 2 — effort S — risk low — category: release — wild
  Why: assumption: reverts and canary reds cluster by hour. The user pushes frequent releases (1.2.49, 1.2.50) and two reverts are already on record.
  Done when: after 30 or more releases, `fm release --push` prints the local revert rate for the current hour and asks for one extra confirmation only when that rate is at least double the average.

- **Show a demo teleprompter pane** — FEATURE — value 2 — effort M — risk low — category: demos — wild
  Why: the project ships `demo/*.cast` and mp4 recordings, so live demos matter. A pane that stages the next three commands and paces off a rehearsal run would make them repeatable.
  Done when: `fm demo --rehearse` records timings, and `fm demo --live` shows the next three steps and pre-types the next command without running it.

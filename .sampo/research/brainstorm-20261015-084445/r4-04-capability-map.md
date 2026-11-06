# Brainstorm — lens: capability map

The pack is close to saturated: most capabilities a best-in-class harness plugin would have are already proposed. From the surveyed rivals and neighbours (Aider, Cline, Cursor, Devin, spec-kit, claude-mem), these are the corners I could not find covered. Each is marked partial overlap where it comes close to an existing idea.

- **Install into a second CLAUDE_CONFIG_DIR profile** — FEATURE — value 3 — effort M — risk med — category: install
  Why: assumption: people split work and personal Claude profiles; the installer, doctor and uninstall only reason about `~/.claude`. Rivals add commands and never own the config dir.
  Done when: `fm wire --config-dir X` installs and uninstalls into `X` with `fm doctor --config-dir X` green, and the default dir's bytes are unchanged.

- **Alert through the terminal itself (OSC 9/777 plus bell)** — FEATURE — value 4 — effort S — risk low — category: devices
  Why: assumption: many sessions run over SSH, tmux or mosh, where push services and desktop notifications don't reach. Partial overlap with the OSC 9;4 progress idea, but this one is for "needs you" alerts only.
  Done when: a blocked ask emits the escape sequences, a test captures them from a pty, and an ntfy-style push is not required for the alert to fire.

- **Show Foreman state in VS Code and JetBrains** — FEATURE — value 3 — effort M — risk low — category: devices
  Why: assumption: IDE-extension users are a large share of Claude Code users, and the pack covers tmux, starship and an LSP but no IDE status item. `fm status --porcelain` already exists as the data source.
  Done when: a tiny extension shows the step, the "needs you" count and the blocking criterion from `fm status --porcelain`, and clicking it opens the brief.

- **Run notebooks and data pipelines as evidence** — FEATURE — value 3 — effort M — risk med — category: stacks
  Why: assumption: ML and data repos have no unit-test gate, so `fm check` finds nothing to bootstrap. Evidence there means executing cells and comparing output hashes, not running pytest.
  Done when: on a fixture notebook repo, `fm check` proposes a headless execute-and-diff gate, and a deliberately changed cell output turns it red.

- **Add `fm tail --why`, one live stream that names the cause** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: partial overlap with the NDJSON event stream, the hook waterfall and the liveness ledger. Today each is a separate surface, so a developer debugging "why did Foreman block or wake?" has to join them by hand.
  Done when: one command merges hook, gate, guard, wake and ask events into a time-ordered feed with a one-line cause each, and a golden test covers a block→allow-once→resume sequence.

- **Rank the pile by "what a newcomer would feel", then freeze it** — CLEAN — value 5 — effort S — risk low — category: user value
  Why: the pack has about 3,000 ideas, while the new evidence (A1–A11) lists a dozen concrete newcomer failures. The scarce resource is selection, and the pack's roadmap-distilling ideas haven't been turned into a gate.
  Done when: a file maps each of A1–A11 to exactly one shipped task, the idea pile is archived read-only, and the next round's pack contains only that map plus open friction.

- **Show the `fm` verbs used per caller (Claude, human, hook) to find what to hide** — PERFORMANCE — value 3 — effort S — risk low — category: developer experience
  Why: the pack proposes caller attribution but not its first use, which is deciding which of the 46 never-run verbs to hide from `--help`. The usage data is already there: 46 verbs were never run by Claude in 11 days.
  Done when: `fm help` hides verbs with zero calls in 30 days (still callable), and `fm help --all` lists them with last-used dates.

- **Add a lifetime "guard and gate saves" counter in the statusline** — FEATURE — value 3 — effort S — risk low — category: user value
  Why: this is a compact, always-on answer to "is it earning its keep?", unlike the catch reel or the weekly digest. Right now only the 18 "fixed later" failures are counted, while the saves are not.
  Done when: the band shows `saves N` from the ledger, with a click or `fm saves` listing each one with its before and after.

- **Test one "stuck newcomer" ladder per dead end A1–A11** — FEATURE — value 4 — effort M — risk low — category: user value
  Why: the clean-HOME walkthrough found the dead ends once, but nothing stops them from coming back. Each is a scripted no-model scenario with the expected next-command line.
  Done when: CI replays each dead end in a throwaway HOME and fails if any output lacks a named next command.

- **Wild: Draft the milestone write-up in the user's voice (ghostwriter)** — FEATURE — value 3 — effort M — risk med — category: delight
  Why: wild. Commits and PRs in the user's voice are proposed, but a finished milestone's release thread or blog draft is not. It would be redacted, drafted locally, and published only after an outward-facing yes.
  Done when: `fm writeup T-id` outputs a redacted draft file citing evidence ids, and nothing leaves the machine without a confirmed yes.

- **Wild: Serve a 1-bit status image for an e-ink or old-tablet desk display** — FEATURE — value 2 — effort S — risk low — category: devices
  Why: wild. A local HTTP endpoint renders the current step, the needs-you count and the pace as a 1-bit image, so a spare screen can show the state with no app. It builds on the wall-display idea.
  Done when: `curl localhost:PORT/glance.png` returns a 800×480 image that changes when a task changes, and it binds to localhost only.

- **Wild: Diff the same task across two machines' ledgers** — FEATURE — value 2 — effort M — risk med — category: observability
  Why: wild. Environment-specific failures (flaky gates, wrong tool versions) are hard to see on one host. This builds on the multi-machine fleet idea and the pinned gate environments.
  Done when: `fm diff-host A B T-id` lists gates whose verdict or runtime differs, with the environment fingerprint fields that differ.

- **Count which nudges and refusals users overrode per verb, and offer to quiet them** — FIX — value 3 — effort S — risk low — category: observability
  Why: partial overlap with close-warning precision, but this covers every nudge, not only close warnings. The pack lists 100+ nudge ideas with no ceiling on total nag volume.
  Done when: a per-session budget caps injected nudges at N, and `fm nope --list` shows the classes silenced and why.

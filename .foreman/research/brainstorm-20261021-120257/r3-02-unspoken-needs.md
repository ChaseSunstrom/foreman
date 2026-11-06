# Brainstorm — lens: unspoken needs

- **Write one `mandate.toml` per sweeping request** — FEATURE — value 5 — effort M — risk low — category: autonomy
  Why: "etc.", "super", "10x", "full auto", "don't stop" are one need, a bounded license to keep going. The pack has separate pieces (cap, stop line, kill phrase, digest, licence gate) but no single object. Assumption: the user would read one card and say "yes".
  Done when: `fm code --mandate FILE` and `fm run` both read the same file, and removing the stop line from a fixture makes both refuse to start.

- **Rerun a red canary after the machine goes quiet before showing it** — FIX — value 4 — effort S — risk low — category: trust
  Why: the user manually dropped "Canary after 1.2.47 ✗ … transient: rerun shows 0 failing; the canary ran while the release's own checks loaded the machine". Load-aware lanes exist; canary reds are still shown raw.
  Done when: a canary failure seeded under synthetic load is rerun after load falls under a threshold, and the user-visible output states "transient, rerun green" without a drop.

- **Show a "your words, my reading" diff when a recorded steer changes behaviour** — FEATURE — value 4 — effort M — risk med — category: intake
  Why: "don't stop until complete" was filed as a veto, and the user noticed only by reading the steer log. They can't see misclassification as it happens. Assumption: mislabels recur on idioms.
  Done when: a fixture of 20 verbatim steers shows each label with its source phrase, and the "don't stop" case prints "continue", never "veto".

- **Send brainstorm children only the user's last 30 steers plus a capability gap list** — PERFORMANCE — value 4 — effort M — risk low — category: ideas
  Why: the "ideas so far" list in this pack runs to thousands of lines and yields mostly near-duplicates. The user's words are the densest signal and are tiny. This differs from cluster summaries because the pile is replaced, not compressed.
  Done when: a round's pack is under a fixed token cap and a duplicate-rate measure against shipped work is no worse than the full-pile run on a replay.

- **Let `fm code` read the user's existing Claude keybindings and slash commands** — FEATURE — value 4 — effort M — risk low — category: muscle memory
  Why: the user asked "why can't I launch fm code like I can claude code?" The unspoken need is that nothing they already know should break. Assumption: they have a customised `~/.claude`.
  Done when: a fixture `keybindings.json` remapping one key changes that key in the TUI, and a user slash command from `~/.claude/commands` runs as a request.

- **Report which adopted upstream capability changed an outcome** — FEATURE — value 4 — effort M — risk med — category: integration
  Why: six repos are to be integrated "automatically", and nothing says whether any of it helped. Adoption counts will look like progress without being it. This is an adoption-to-outcome join, not an adoption ledger.
  Done when: `fm code report` lists each adopted asset with runs that used it and pass rate with versus without, and an asset with zero uses is flagged.

- **Explain every denial from a third-party skill in the user's terms** — SECURITY — value 4 — effort S — risk low — category: guard
  Why: constraint "third-party skills run nothing unguarded". Unspoken: a blocked skill looks broken, so the user will disable the guard. Assumption: blocks will be frequent once skills are imported.
  Done when: a skill that tries a blocked write shows one line naming the skill, the blocked action and the exact allow-once command, and the guard verdict is unchanged.

- **Turn the 11 externally blocked briefs into one page of paste-ready steps** — FEATURE — value 3 — effort S — risk low — category: simplicity
  Why: T-0325, T-0335, T-0336, T-0337, T-0352 and T-0418 are blocked on sudo, live CLIs or publishing. The user repeatedly says "no need to ask me", so they shouldn't hunt for what only they can do.
  Done when: `fm blocked --steps` prints each blocker with a copy-ready command and a verify line, and running the verify marks the brief unblocked.

- **Wild: Add "ghost shift" `fm code --tonight`** — FEATURE — value 5 — effort L — risk high — category: devices
  Why: wild. The user wants a walk-away result with no check-ins. This runs the queue in worktree lanes under a mandate, and at the return time leaves one landed-or-not page.
  Done when: a seeded two-task queue with a fake runner finishes with no prompts and a summary naming each task as landed, parked or failed with its cause.

- **Wild: Hand a Claude Code session to `fm code` by saying "take this over"** — FEATURE — value 4 — effort L — risk high — category: agents
  Why: wild. Users start in `claude`, stall, and want the harness to continue from the transcript instead of restarting. Assumption: the transcript format stays parseable.
  Done when: a fixture transcript with an unfinished plan resumes in `fm code` at the stated next step, and a malformed transcript is refused with a reason.

- **Wild: Offer a "rubber-duck runner" that only asks questions** — FEATURE — value 3 — effort S — risk low — category: user value
  Why: wild. Vague asks ("make it 10x better") are the user's habit, and a runner that returns three sharpening questions costs little. The questions become the mandate.
  Done when: `fm code --duck "make it better"` makes no edits and writes a draft mandate file of at most five lines.

- **Wild: Print a one-line "what you'd feel" delta at every release** — FEATURE — value 3 — effort S — risk low — category: user value
  Why: wild. Release notes list internals ("worker leases fixed"). The user asks for visible improvement ("better animations", "show better examples"). Assumption: every release can name one thing a person would notice.
  Done when: `fm release` refuses to finish without a felt-change line, and a release with none says "nothing changed for you".

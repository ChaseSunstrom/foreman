# Brainstorm — lens: user value

- **Print a footprint of everything Foreman put on this machine** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: assumption: the user can't see in one place the hooks, timers, settings entries, ports, state dirs and grants Foreman owns. Related ideas cover state paths and the uninstall rehearsal, but none gives a plain "what's yours, what's mine" list.
  Done when: `fm footprint` lists every installed hook, unit, config edit, listening port and state directory with its path and the verb that created it, and a fixture install's list matches a filesystem diff of the install.

- **Protect named paths from every agent** — FEATURE — value 5 — effort S — risk low — category: guard
  Why: assumption: the user has data they'd never want touched (photos, keys, other repos), and today they must infer that from the generic guard rules. `fm protect PATH` states it directly.
  Done when: after `fm protect ~/photos`, a write, delete or move there is blocked on Claude Code, Codex and Gemini CLI with a message naming the protect entry, and `fm protect --list` shows it.

- **Show every live grant on one board with an expiry** — SECURITY — value 5 — effort S — risk low — category: authorization
  Why: the steers record a durable push grant ("push to main at any time") and others. Nothing shows the user which authorizations are live, and the grants spent on use aren't listed anywhere the user will look.
  Done when: `fm grants` lists each live durable grant with its scope, who set it, last use and expiry (default 30 days), and `fm grants revoke ID` makes the next use fail.

- **Fuse bypass mode so it falls back to ask mode** — SECURITY — value 4 — effort M — risk med — category: bypass safety
  Why: bypass mode is Foreman's riskiest setting for the user, and its only protection is the guard. A time or blast-radius fuse is a different control. The T-0794 mention of "fuses" is only a catalogue line.
  Done when: with `--fuse 20m,15files`, a scripted session that edits 16 files, or reaches minute 21, is switched to ask mode with a one-line reason, and a test covers both triggers.

- **Say "freeze" to make the session read-only mid-flight** — FEATURE — value 4 — effort S — risk low — category: control
  Why: assumption: when an agent starts going wrong, the user's only options are interrupt or watch. A one-word switch that denies all writes and shell mutations but keeps reading and planning is cheaper than a kill.
  Done when: after `fm freeze`, a Write, Edit or mutating Bash call is denied with "frozen by you, `fm thaw` to resume", reads still work, and the freeze survives a compaction.

- **Diff what a session changed outside the repo** — FEATURE — value 4 — effort M — risk med — category: safety net
  Why: the guard watches commands, but the user's real fear is the result: dotfiles, global packages, `~/.config`. Nothing shows that after a session. The earlier "trace what verify commands touched" idea covers proofs, not whole sessions.
  Done when: a session that runs `npm i -g x` and edits `~/.bashrc` ends with a card listing both paths under "outside the repo", and a session with no such change prints "nothing outside the repo".

- **Add `fm trim`, a menu of injected context with usage counts** — FEATURE — value 4 — effort M — risk low — category: lean
  Why: earlier ideas measure injected context and cap output, but none lets the user act. This shows each injected source (lessons, steers, notes) with tokens per session and how often it was used, and mutes one with a keypress.
  Done when: `fm trim` prints sources sorted by tokens with a use count each, muting one lowers the next session's injected tokens by that amount, and `fm trim --undo` restores it.

- **Ask for trust on first open of an unfamiliar repo** — SECURITY — value 4 — effort M — risk med — category: repo trust
  Why: assumption: a cloned repo can carry scripts, a `.claude` config or task files that run with the user's permissions. Foreman already runs hooks on every repo, so it can stop first and ask.
  Done when: in an unregistered repo, session start shows one prompt, and until it is answered, repo-supplied hooks, verify commands and MCP configs are not run. Answering `no` keeps Foreman in read-only guard mode there.

- **Offer a scoped one-shot allow after a guard block** — FEATURE — value 4 — effort S — risk low — category: guard ergonomics
  Why: the standing rule is that the guard stops commands the user would never want run. When one is a false positive, the only way out is editing rules. A time-boxed `fm allow --for 10m` keeps the guard strict without making the user fight it.
  Done when: after a block, `fm allow --for 10m` lets that exact command shape run once within 10 minutes, the allow is logged with the command, and an identical command at minute 11 is blocked again.

- **Prove the uninstall leaves nothing behind** — CLEAN — value 3 — effort M — risk low — category: lean
  Why: assumption: people trust a tool more if leaving it is verified. The eject and trial ideas leave the proof open. Here, a before/after snapshot compared at uninstall must show every footprint item gone.
  Done when: `fm uninstall --verify` snapshots the footprint, removes it, re-scans, and exits 0 only when no Foreman file, unit, hook or settings entry remains. A planted leftover makes it exit non-zero and name the path.

- **(wild) Run guest mode on a borrowed machine** — FEATURE — value 3 — effort M — risk med — category: portability
  Why: wild. The user may use someone else's laptop or a CI box where nothing should persist. `fm guest` keeps all state on tmpfs, installs no timers, and wipes everything at exit, including grants.
  Done when: after a guest session, a filesystem diff of `$HOME` shows no new files, and the guard still blocks a planted destructive command during it.

- **(wild) Give the user a prove-it-before-I-trust-it quiz on the guard** — FEATURE — value 3 — effort M — risk low — category: trust
  Why: wild. Users can't judge a guard by reading rules. `fm guard --try` shows ten real-looking commands, asks "would you want this blocked?", then reveals what the guard did. Disagreements become rule or allow proposals.
  Done when: running the quiz records 10 answers, prints a match count against the guard's verdicts, and files at most 3 proposals, each citing the command that caused it.

- **(wild) Print a monthly "things I held back from doing" letter** — FEATURE — value 3 — effort S — risk low — category: restraint
  Why: wild. Safe and lean means Foreman declines things, and that restraint is invisible. A short list of blocks, skipped ceremony and dropped work reads as value without adding a feature.
  Done when: on the first session after the 1st of a month, a letter lists the counts and the top 3 blocks with the dates they happened, and a month with none prints "nothing to report".

Next question: which of Foreman's overheads does the user feel on every session (startup time, injected lines, prompts), and how would we know from their behaviour rather than our own gauges?
Next question: when the user has turned a safety feature off by hand, what did they do next, and does Foreman record why?

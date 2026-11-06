# Brainstorm — lens: plugin parity

- **Fail the gate when a CLI verb has no plugin twin** — FEATURE — value 4 — effort S — risk low — category: parity gate
  Why: the request says every feature must work in the plugin, but nothing checks that a new `fm` verb reaches a plugin slash command, so drift stays silent. Assumption: the plugin surface is maintained by hand.
  Done when: adding a verb to the command table without a plugin entry makes `fm doctor` and the gate fail, and the message names the verb.

- **Run the plugin's bundled `fm`, not a PATH install** — FIX — value 5 — effort S — risk med — category: install path
  Why: the dropped request "how come fm isn't recognized" shows PATH setup breaks users. A plugin that calls `fm` by bare name fails the same way.
  Done when: with `~/.local/bin/fm` removed and a clean PATH, `/foreman status` prints the same lines as `fm status`.

- **Refuse to run a plugin paired with a CLI from another release** — FIX — value 4 — effort S — risk low — category: version skew
  Why: the request names version skew, and the plugin and `fm` can update separately. T-0418 already shows an installed companion (foreman-ui) left behind.
  Done when: a mismatched pair prints both versions and one update command, and no hook fires.

- **Run a parity smoke check after `/plugin update`** — FEATURE — value 4 — effort S — risk low — category: upgrade check
  Why: assumption: updates can change or drop slash commands without anyone noticing until a user hits the gap.
  Done when: the first session after an update posts a one-line diff of the command list against the last run's, and it is empty when nothing changed.

- **Ship the statusLine from the plugin so the glance line works without the mod** — FEATURE — value 4 — effort M — risk low — category: status line
  Why: the live pane needs the separate foreman-ui mod (T-0418, T-1217 blocked), so a plugin-only user sees no live state.
  Done when: with the mod absent, Claude Code's status line shows the current stage and the work bar in 60 characters or fewer.

- **Wild: `/foreman` answers in chat with the stage rail as a card** — FEATURE — value 4 — effort M — risk low — category: chat surface
  Why (wild): the pane is a terminal feature, so chat-only users get raw text. A markdown card with the same stage rail and open-work bar would give them the same view.
  Done when: the slash command's output contains the stage rail and work bar in markdown, and its counts match `fm status`.

- **Wild: attach to a terminal-started run from a plugin slash command** — FEATURE — value 4 — effort L — risk med — category: cross-surface control
  Why (wild): a run started with `fm code` in a terminal is invisible to a chat session, so the plugin cannot see or stop it.
  Done when: `/foreman attach <id>` shows the run's last five events, and `/foreman stop <id>` stops it within 10 seconds.

- **Give headless `claude -p` the plugin's commands as plain prompts** — FEATURE — value 3 — effort M — risk med — category: headless parity
  Why: plugin slash commands don't exist in `-p` mode, and the brainstorm children already run headless without tools. Assumption: people script Foreman with `-p`.
  Done when: `claude -p "/foreman status"` returns the status text and exits 0.

- **Fall back cleanly when a Claude Code version lacks a hook event** — FIX — value 3 — effort S — risk low — category: hook compatibility
  Why: the pack shows Claude Code versions moving under the cost math, and plugin hooks name events that older releases may not emit.
  Done when: a simulated release without the event logs one notice and runs the fallback path, and the check still runs.

- **Keep backlog and journal outside the plugin cache** — CLEAN — value 4 — effort S — risk med — category: state location
  Why: assumption: plugin updates replace the cache directory, and state may live under the plugin root, so an update could wipe the queue.
  Done when: a simulated plugin update leaves the task count in `fm status` unchanged.

- **Read the user's timezone for plugin-side deferrals** — FIX — value 3 — effort S — risk low — category: time parsing
  Why: T-1802 fixed a midnight-defer bug in the CLI, but plugin hooks may run with a different TZ environment.
  Done when: `defer --until reset` issued through the plugin fires at the reset time in the user's local zone with TZ unset in the hook.

- **Wild: a read-only plugin mirror of the journal that survives a broken install** — FEATURE — value 3 — effort M — risk low — category: resilience
  Why (wild): if `fm` breaks, the plugin goes dark. A mirror of the last-known state lets chat still show the run, marked stale.
  Done when: with the `fm` binary moved away, `/foreman status` prints the last state with a "stale" label and a timestamp.

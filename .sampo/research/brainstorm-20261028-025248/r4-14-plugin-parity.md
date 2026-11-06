# Brainstorm — lens: plugin parity

- **Detect duplicate hook registrations across plugin and user settings** — FIX — value 4 — effort S — risk low — category: install
  Why: assumption: a manual install can leave the same hook in `settings.json` next to the plugin's copy, so one event fires twice.
  Done when: a fixture with the same hook in both places makes `fm doctor` name both entries, and a single edit fires the hook once.

- **Reconcile orphaned hook entries after plugin removal** — CLEAN — value 3 — effort S — risk low — category: uninstall
  Why: assumption: `/plugin uninstall` removes the plugin's files but can leave `foreman` entries in settings, which then point at missing scripts.
  Done when: removing the plugin from a fixture leaves no `foreman` hook or statusLine entry in `settings.json`, and `fm doctor` reports nothing dangling.

- **Ask once before a competing statusLine is replaced** — FIX — value 3 — effort S — risk med — category: install
  Why: assumption: a user who already has a statusLine loses it silently when the plugin's glance line installs. The pack's statusLine item covers shipping it, not this clash.
  Done when: installing over a fixture with a custom statusLine asks once, records the choice, and a second install does not ask again.

- **Name a slash-command clash before install** — FIX — value 3 — effort S — risk low — category: plugins
  Why: assumption: another installed plugin can declare `/foreman` or a verb with the same name, and the second one wins without notice.
  Done when: installing a fixture plugin that declares the same command reports the clash and leaves both reachable under their plugin namespace.

- **Hand a chat-started run to the terminal with one token** — FEATURE — value 4 — effort M — risk med — category: handoff
  Why: the pack covers attaching a terminal-started run from chat. The reverse direction is missing, and assumption: users start in chat and want to continue at a shell.
  Done when: `/foreman handoff` prints a token, and `fm resume <token>` in a shell continues the same task id from the same journal position with no repeated step.

- **Differential-fuzz both surfaces on random verb sequences** — FEATURE — value 4 — effort M — risk low — category: testing
  Why: assumption: the parity matrix and recorded keystroke scripts only cover paths someone thought of, so divergence on unusual sequences goes unseen.
  Done when: a seeded run of 200 random sequences reports zero divergences, and a planted divergence shrinks to three verbs or fewer.

- **Golden-file every receipt across both surfaces** — CLEAN — value 3 — effort S — risk low — category: receipts
  Why: assumption: the chat card and terminal block for the same close drift apart in wording or field order, and no test compares them.
  Done when: each receipt kind has one golden fixture that matches byte-for-byte on both surfaces after width normalisation.

- **Keep only the plugin cache versions a live session still names** — CLEAN — value 2 — effort S — risk med — category: plugin cache
  Why: assumption: each `/plugin update` leaves an old cache directory, and an open session can keep firing its hooks from it.
  Done when: after two updates with one session still open, the cache holds only the directories that session's hook paths reference.

- **Share one cost estimator between chat and CLI** — FIX — value 3 — effort S — risk low — category: cost
  Why: assumption: the CLI's queue quote and the chat quote use separate arithmetic, so the same queue can show two different prices.
  Done when: the same queue fixture yields identical estimate figures from `/foreman` and `fm`, and a test fails if either surface computes its own.

- **Wild: let chat plan and the terminal execute, with the journal as the baton** — FEATURE — value 3 — effort M — risk med — category: agents
  Why: wild: a run is planned in a chat session and then finished from a shell, with no re-explaining and no duplicated step, because the journal is the only handoff.
  Done when: a run planned in chat completes in the terminal with one journal, and each step appears once.

- **Wild: mirror every chat-driven action into a shadow terminal pane** — FEATURE — value 3 — effort M — risk low — category: surfaces
  Why: wild: a terminal user watches exactly what the plugin did, as it happens, in a read-only pane, so neither surface is a black box to the other.
  Done when: a command run from chat appears in the shadow pane within one second with the same id, and the pane never sends input back.

- **Wild: a parity passport that every run carries offline** — FEATURE — value 2 — effort S — risk low — category: trust
  Why: wild: each finished run carries a small card naming the surface, Foreman version and hook-file hashes that produced it, which anyone can verify without Foreman installed.
  Done when: the card from a finished run verifies with a standalone script using only the journal and the recorded hashes, and a changed hook file makes verification fail.

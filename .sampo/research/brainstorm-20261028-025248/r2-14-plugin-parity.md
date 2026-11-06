# Brainstorm — lens: plugin parity

- **Diff both surfaces' journals on one fixture** — FEATURE — value 4 — effort M — risk low — category: parity testing
  Why: assumption: the plugin and the CLI call the same verb table, but nothing compares the journal events and receipts each writes for the same request.
  Done when: CI runs every verb through the plugin and the CLI on a fixture repo and fails on any differing journal event or receipt field that isn't on a written allow-list.

- **Print the entry point on every receipt** — FEATURE — value 3 — effort S — risk low — category: legibility
  Why: when behaviour differs, nobody can tell whether a run came from the plugin, the terminal CLI, or `claude -p`. The receipt doesn't say.
  Done when: every close receipt carries a `surface` and `fm_version` field, and a test asserts both for each of the three entry points.

- **Give each intentional parity gap an owner, a reason and an expiry** — CLEAN — value 4 — effort S — risk low — category: parity docs
  Why: a verb without a plugin twin is sometimes deliberate, but the gap is invisible and never revisited. Assumption: most gaps are accidental.
  Done when: the verb-by-surface matrix is generated from the verb table, and the check fails when a gap has no reason or its expiry date has passed.

- **Negotiate features at handshake instead of comparing versions** — FEATURE — value 4 — effort M — risk med — category: version skew
  Why: a version gate refuses a whole plugin/CLI pair when one feature differs, and it breaks on backports. Assumption: a patched CLI can run safely with one feature missing.
  Done when: plugin and CLI exchange a feature set on start, and with one feature removed in a test only its dependent slash command is disabled, with a message naming it.

- **Share one settings resolver between plugin and CLI** — CLEAN — value 4 — effort M — risk med — category: config parity
  Why: assumption: the plugin and the CLI read settings through separate code paths, so the same key can resolve to different values with different precedence.
  Done when: a test sets each setting through the plugin and through the CLI and asserts the same resolved value, and `fm config why KEY` names the file that won.

- **Complete `/foreman` arguments from live backlog and verb data** — FEATURE — value 4 — effort S — risk low — category: plugin UX
  Why: the chat command takes the same verbs as the CLI, but typing a T-number or a playbook name gets no completion inside Claude Code.
  Done when: typing `/foreman prove T-` offers the open task IDs from the backlog, and a test checks that the argument hint lists every verb in the table.

- **Report install health for both halves from chat** — FEATURE — value 3 — effort S — risk low — category: install health
  Why: a plugin with a missing CLI, or with its hooks unregistered, looks like a silent failure to the user. Assumption: most reports of "Foreman does nothing" are one of these two.
  Done when: `/foreman doctor` in chat prints plugin, CLI and hook-registration status on three lines, and a missing half is named with the command that fixes it.

- **Wild: run one request through plugin, CLI and headless nightly and publish the three answers side by side** — FEATURE — value 3 — effort M — risk low — category: live parity
  Why: wild: a public page that shows the three entry points disagreeing in real time would make parity a visible promise rather than a claim.
  Done when: a nightly job runs the same fixture request through all three entry points and publishes the diff of their outputs with a date, and the job fails when a diff is not on the allow-list.

- **Run in a prompt-only mode when no shell can run the CLI** — FEATURE — value 3 — effort L — risk med — category: degraded mode
  Why: the plugin fails outright where no binary can run, such as sandboxed or web sessions. Assumption: `status` and `why` can answer from the journal without executing anything.
  Done when: with the CLI removed from `PATH`, `/foreman status` still answers from the journal and lists the verbs it cannot run in this session.

- **Wild: read last month's journals with today's plugin and list every field it can no longer read** — FEATURE — value 3 — effort M — risk low — category: read compatibility
  Why: wild: a fixture set of journals from each past release, replayed on every build, catches silent breakage before a user's history stops rendering.
  Done when: each past-release journal fixture is read by the current build, and any unreadable field is listed by name in one table that the build prints.

- **Wild: a split-screen recording of the same request in plugin and terminal, for the docs** — FEATURE — value 2 — effort M — risk low — category: docs
  Why: wild: showing the two surfaces side by side on one real run is a clearer parity proof than a matrix of checkmarks.
  Done when: the docs site embeds one generated recording per surface pair, rebuilt from the nightly parity run, and the build fails if a recording is older than its fixture.

# Brainstorm — lens: capability map

- **Check every command through the installed plugin, not just the CLI** — FEATURE — value 5 — effort M — risk low — category: plugin parity
  Why: The request requires every feature to work in the Claude Code plugin. T-0418 shows the installed foreman-ui is pinned behind its release, so plugin and CLI can drift without anyone noticing.
  Done when: A suite runs each fm verb once through the plugin's slash path and once through `fm`, and fails on any output difference or missing command.

- **Show which changed lines each proof actually executes** — FEATURE — value 4 — effort M — risk low — category: proof
  Why: Assumption: a proof shows a named test failed before the change and passed after, but not that the test ran the changed lines. The "fix the proof gap" idea shows that gap matters.
  Done when: A closed task lists each changed line as covered or uncovered, and a task with an uncovered changed line can't close without a written reason.

- **Scan staged diffs for secrets before any commit or push** — SECURITY — value 5 — effort S — risk low — category: secrets
  Why: The pack covers secrets in journals and receipts only. A key typed into a diff reaches git unchecked.
  Done when: A staged diff containing a fake AWS-style key is refused at commit, with the file and line named.

- **Check new dependencies for licence and advisories before close** — SECURITY — value 4 — effort S — risk low — category: supply chain
  Why: Assumption: dependency bumps run as their own lanes, but a new import added by a model run gets no licence or advisory check.
  Done when: Adding a package with a copyleft licence or a listed advisory fails the gate and names the package.

- **Preview every file an install or update will write** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: Install writes into user settings, and uninstall must remove what install wrote. Nothing previews those writes first.
  Done when: `fm install --plan` lists each path and its change, and the filesystem is byte-identical afterward.

- **Ship a pre-commit framework hook** — FEATURE — value 3 — effort S — risk low — category: developer experience
  Why: The guard and the pre-push ideas only reach Claude Code users. Teams on pre-commit must write their own glue to use the gate.
  Done when: A `.pre-commit-config.yaml` that references Foreman runs the affected check on staged files only.

- **Compute DORA numbers from closed tasks** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: Closed tasks already carry dates, gate results and reverts. No lead-time, change-failure or restore-time figure exists.
  Done when: `fm metrics` prints lead time, change-failure rate and restore time for the last 30 days, computed only from the journal.

- **Version each doc page with the release that shipped its command** — FEATURE — value 3 — effort M — risk low — category: docs
  Why: The commands change every release, and the installed plugin lags its release (see T-0418). Readers get the current command set even when they run an older one.
  Done when: Opening the docs for an older tag shows only the commands that existed in that tag.

- **Let a teammate see every lane on one read-only page** — FEATURE — value 3 — effort M — risk med — category: team
  Why: Assumption: the pack is single-user. The CODEOWNERS and PR ideas imply a team reads the output, so each reviewer currently has to ask the owner for status.
  Done when: Two machines pointed at one exported status file show the same lanes after one refresh, with no write access granted.

- **Answer questions about a diff with no run open** — FEATURE — value 3 — effort M — risk low — category: review
  Why: The read-only fork idea covers side questions during a run. This covers a finished diff with nothing running. (wild)
  Done when: A question about a diff returns an answer citing file:line, and the working tree is byte-identical before and after.

- **Narrate a repo's history as a nature documentary, one module per species** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: Wild. The pack maps 1,835 files, and a story gives a newcomer a way into them. Every line would cite a real commit.
  Done when: `fm story` prints a narration of the last 90 days where each cited commit id exists in `git log`.

- **Seal a time capsule of the repo's state, opened at the next release** — FEATURE — value 2 — effort M — risk low — category: delight
  Why: Wild. Release cadence and the sealed-prediction idea both suggest a reveal that waits for a date.
  Done when: `fm capsule open` refuses before the stated date, and after it shows the frozen state and its commit.

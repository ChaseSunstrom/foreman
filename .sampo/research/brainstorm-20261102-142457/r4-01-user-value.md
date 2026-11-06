# Brainstorm — lens: user value

- **Fuzz one-keystroke neighbours of your habitual commands** — SECURITY — value 4 — effort S — risk low — category: guard
  Why: the pack's ideas mutate *blocked* commands, but a typo in an allowed command (`rm -rf ./build /` with a stray space, `git push -f` for `-u`) is how real damage happens in bypass mode. assumption: the session logs hold enough habitual commands to seed this.
  Done when: `fm guard --typos` lists every single-edit neighbour of the 200 most-run commands that the guard would allow and that touches a protected path, and one planted case is caught in a test.

- **Derive guard rules from files the user already wrote (ssh config, git remotes, branch protection)** — FEATURE — value 4 — effort M — risk med — category: guard — wild
  Why: assumption: the user's existing `~/.ssh/config` hosts, `origin` remotes and protected-branch settings already say what matters to them. Foreman would learn "never force-push here" and "never touch host X" without a steer.
  Done when: in a fixture home, `fm guard --derive` proposes a block for a prod host and a protected branch, each citing its source file, and applies none without confirmation.

- **Flag precious paths that no backup covers** — FEATURE — value 4 — effort M — risk low — category: safety — wild
  Why: assumption: restic, borg, rsync or snapper config is readable. A path that bypass sessions write to, that the repo doesn't track and that no backup includes is the real "irreversible" class. The tracked-or-not rule is cheaper than inferring it from command shape.
  Done when: `fm doctor` prints "N paths written by sessions this month are in no backup and not in git" with the list, and a fixture with a backup config excludes the covered paths.

- **Price each guard block by what it would have lost** — FEATURE — value 4 — effort S — risk low — category: guard value
  Why: the pack proposes counting blocks and the user's overrides. A block's value is the uncommitted or unpushed work at the target at that moment. This is the number a user feels, and it separates real saves from noise.
  Done when: a block ledger line carries `at_risk: {uncommitted_files, unpushed_commits}`, and `fm digest` prints "saved N files of unsaved work" with a test using a dirty fixture repo.

- **Add a one-key "was that block right?" label** — FEATURE — value 3 — effort S — risk low — category: guard calibration
  Why: precision is currently inferred from overrides, which a rubber-stamping user hides. An explicit y/n on a sample of blocks gives ground truth for the autoimmune-rate idea.
  Done when: `fm guard label` records a verdict on the last block, and `fm doctor` shows labelled precision with its sample size (n), or "n=0" when empty.

- **Query the guard as of a past date** — FEATURE — value 3 — effort M — risk low — category: guard audit
  Why: "why was this allowed last Tuesday?" can't be answered once rules have changed. assumption: rule changes are versioned in git or the ledger.
  Done when: `fm guard why --at 2026-10-28 'cmd'` returns the verdict and the rule revision that was live then, matching the ledger entry for a recorded command.

- **Test block messages for comprehension, not only a Next: line** — CLEAN — value 3 — effort S — risk low — category: legibility
  Why: T-2653 added a `Next:` to every nonzero exit, but nothing checks the reader understands why the guard stopped them. A tool-less cold child sees only the message and must name the safe alternative.
  Done when: for each guard block template, a cold child names the correct alternative on at least 9 of 10 samples, or the template is filed as a fix.

- **Diff outbound hosts per release** — SECURITY — value 3 — effort S — risk low — category: privacy
  Why: the pack covers an egress ledger and a data-out receipt, but a user upgrading wants one line: "this version adds a new network destination". A static scan of the code for URLs and hosts, diffed against the last tag, is enough.
  Done when: `fm release-notes` and the ship gate list added or removed hosts, and a commit that adds a new URL fails the gate unless listed in an allowlist.

- **Print the effect class in every verb's help line** — CLEAN — value 3 — effort S — risk low — category: lean help
  Why: with a large verb surface, the user can't tell "reads only" from "writes outside the repo" without reading the code. One tag per verb (read / repo / state / outside / network) costs a column.
  Done when: `fm help` shows the tag for every verb, and a test fails if a verb's observed writes exceed its tag.

- **Show how much state a safe prune would reclaim** — CLEAN — value 3 — effort S — risk low — category: footprint
  Why: the pack proposes ledger caps and compaction. The user feels the benefit as a number: "you can free 340 MB". It also makes volatile-versus-durable placement visible.
  Done when: `fm doctor` prints reclaimable bytes by class (derived caches, old snapshots, trash) with the one command that frees them, and the sum matches `du` within 5%.

- **Sound a seatbelt chime when a bypass session drifts** — FEATURE — value 3 — effort S — risk low — category: safety UX — wild
  Why: assumption: the user steps away during long bypass runs. A terminal bell and a status-line flash fire when a session has run over two hours unattended and has written outside the repo. It is the lightest possible nudge.
  Done when: a simulated session crossing both thresholds emits one bell and one status-line marker, and nothing fires under either threshold.

Next question: which of the user's own existing safety files (backup config, git hooks, ssh config, direnv) does Foreman never read, and what would it do differently if it did?
Next question: for each guard block, how many were followed within minutes by the user running the same thing by hand, and was the cause the guard or the user's workflow?

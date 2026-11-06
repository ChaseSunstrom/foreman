# Brainstorm — lens: capability map

I took the usual comparison set (Copilot Next Edit Suggestions, Cursor Tab, Warp and atuin, Renovate and Dependabot, Sentry, Linear triage, Rewind). The pack already covers most of what they do, so these are only the capabilities it doesn't show.

- **Forecast the queue's finish date with a confidence band** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: assumption: the pack has task quotes and a usage-wall forecast, but nothing that turns the user's own velocity per task size and kind into "queue clears by Thursday, 70% band". 40+ deferred items and a blocked list make "when will this be done" the unasked question.
  Done when: `fm next` or `fm status` prints an ETA range computed from the last 30 closed tasks. A backtest shows the actual finish fell inside the band at least 70% of the time.

- **Learn the user's reviewer taste from reviews they wrote** — FEATURE — value 4 — effort M — risk med — category: user model
  Why: assumption: the user model is built from corrections to the agent. Review comments the user wrote on other people's PRs and their own commit fixups show what they flag in code, and the pack doesn't use them.
  Done when: given a fixture history of review comments, the cold-read charter lists the top 5 recurring review flags. A held-out set of later review comments is matched at hit@5 above a no-model baseline.

- **Score predictions from git outcomes, not clicks** — FEATURE — value 5 — effort M — risk low — category: measurement
  Why: the pack's prediction book relies on adopt/dismiss. Whether a drafted ask's content later appears in a commit, a revert or a reopen needs no user action and removes click bias.
  Done when: each resolved prediction row carries an outcome (landed, landed edited, reverted, absent). The outcome comes from the diff alone, with no accept/dismiss event.

- **Filter the user model by git author identity** — FIX — value 3 — effort S — risk low — category: user model
  Why: the pack strips Foreman-authored and test captures, but a shared repo's commits and co-change signals from teammates still feed "my habits". Assumption: team repos are in scope.
  Done when: a fixture repo with two authors yields co-change and hand-edit habits only from the configured identity. A test fails if another author's commits move any predictor.

- **Add a handoff packet for mid-task harness switches** — FEATURE — value 3 — effort M — risk low — category: devices
  Why: the pack projects the user model into each harness's first message, but nothing carries the state of an open task (plan, steers in force, last failing check) when the user moves from Claude to Codex or `fm code` mid-task.
  Done when: `fm handoff` writes one file that each of the four harnesses reads at start. A switched session's first reply cites the open task's DONE-WHEN without being asked.

- **Watch pinned dependencies for yanks, maintainer transfers and relicensing** — FEATURE — value 3 — effort M — risk low — category: reliability
  Why: abandonment scoring and advisory feeds are in the pack. Yanked releases, ownership changes and licence flips are separate, cheap registry reads that no idea names.
  Done when: against a fixture lockfile with a yanked pin, the night tick files one capture naming the package and the registry fact.

- **Count avoidable asks per session as the anticipation north star** — FEATURE — value 4 — effort S — risk low — category: measurement
  Why: assumption: the pack has a pre-ask precedent check but no retrospective count. Replaying yesterday's questions against decisions.md, steers and the dropped ledger shows how many Foreman could have answered itself.
  Done when: `fm doctor` prints "N of M questions last week were answerable from history", each with its source line.

- **Answer "what will this break?" on demand with `fm foresee`** — FEATURE — value 4 — effort M — risk med — category: foresight
  Why: the pack's risk lines appear at plan time. A user mid-thought, before any task exists, has no way to ask. The query would combine blast radius, co-change and reopen history for a phrase.
  Done when: `fm foresee "rename X"` prints at most 5 ranked risks, each with the history line behind it. It prints "no evidence" instead of guessing when none exists.

- **Match commit and PR text to the user's historical style** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: assumption: Foreman drafts commit and PR text, and the pack's style profile covers replies only. Commit text is the artifact the user actually shows others.
  Done when: for a fixture repo, drafted subject lines match the history's length, prefix and tense conventions. A linter checks this against the last 100 commits.

- **Wild: publish a planted-history anticipation benchmark** — FEATURE — value 3 — effort L — risk low — category: measurement
  Why: wild. The pack plans planted-history probes per cell. Packaging them as a public, seeded dataset with a scorer would let other tools be compared on the same fixtures and keeps the grader independent of Foreman.
  Done when: one command generates the dataset from a seed. It scores any predictor that emits ranked asks, and the result is reproducible byte for byte.

- **Wild: draft a "letter from last month's me" at each generation end** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild. A short letter, written from the user's asks stream, says what they kept pushing on and what they dropped. The user checks whether Foreman read the arc correctly, and the check doubles as free labelled feedback on the user model.
  Done when: the generation report includes a letter of 120 words or fewer. It quotes at least 3 dated user lines, and the user can mark each claim right or wrong.

- **Wild: open a "contradiction court" between the user's steers and their recent behaviour** — FEATURE — value 4 — effort M — risk med — category: user model
  Why: wild. The pack detects steers the user's behaviour now contradicts, but only as an idea. This would be a standing hearing: for each steer, count the times the user acted against it in the last 30 days. It would propose retirement or restatement, never apply either.
  Done when: against a fixture history with one violated steer, the hearing lists it with the violating events. A steer with no violations is not listed.

Next question: Which predictor outputs would still be wrong if every user input in the history were from a teammate, and does anything in the sweep detect that?
Next question: What does a first-time user, with no history, get from Anticipation on day one, and how soon does the first flag with a "because" line reach them?

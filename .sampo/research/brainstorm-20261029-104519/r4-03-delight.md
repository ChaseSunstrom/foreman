# Brainstorm — lens: delight

- **Show the message before and after** — FEATURE — value 4 — effort S — risk low — category: close-out
  Why: most recent asks are message fixes (the `no test matches` text, the docs-impact blocker, the core-integrity warning). A close receipt can show the old text and the new text side by side, taken from the task's own DONE-WHEN repro.
  Done when: closing a FIX task whose DONE-WHEN runs a command prints two blocks, the output from the base commit and from the working tree, and a test asserts both appear.

- **Credit the steer that just paid off** — FEATURE — value 4 — effort M — risk low — category: trust
  Why: the user's steers ("the note ignores edits outside the project", "`_task_files` had the same gap") become tests or rules, but they never see them work. Assumption: a steer can be linked to the test or rule it produced.
  Done when: when a gate refusal or a test failure traces to a rule created from a steer, the output says "from your steer on <date>: <text>", and a test covers the link.

- **Echo a request back in the user's task dialect** — FEATURE — value 4 — effort M — risk med — category: intake
  Why: the user writes in a consistent shape (`FIX: … > @path DONE-WHEN: …`). Foreman could rewrite a loose sentence into that shape, show it, and file it on one key.
  Done when: a casual one-line request produces a drafted block with kind, `@path` and DONE-WHEN. A test checks that `parse_intake` round-trips it with no fields lost.

- **Show an honest ETA from each gate's own history** — FEATURE — value 4 — effort M — risk low — category: waiting
  Why: gate and suite runs are the long waits (`fm ship`'s test run, full `fm check`). Past durations are likely recorded already. Assumption: per-gate timings exist or are cheap to log.
  Done when: while a gate runs, the status line shows "~42s left (median of last 8)". After a fixture run, the shown estimate lands within the recorded spread.

- **Name who holds the line** — FEATURE — value 3 — effort S — risk low — category: waiting
  Why: with "never two suites at once", `fm check` waits on an ambient run or `fm ship`. A silent wait feels like a hang.
  Done when: a waiting command prints "waiting on ambient run for T-1984, started 31s ago". A test starts a fake holder and checks the line.

- **Set terminal title and native progress** — FEATURE — value 3 — effort S — risk low — category: terminal
  Why: long runs happen while the user is in another tab. Assumption: the terminal supports OSC 0 titles and OSC 9;4 progress, and Foreman falls back silently where it doesn't.
  Done when: during a gate run the tab title reads `T-2002 · gates 3/6`, and it resets on exit. A test captures the escape sequences and checks that none are emitted when stdout is not a TTY.

- **Give tasks speakable slugs** — FEATURE — value 3 — effort S — risk low — category: ergonomics
  Why: the user types "Ship T-1996 to main" and refers to work by prose ("the `-k` fix"). A slug such as `run-py-k-and` would let `fm task show run-py-k` work next to the id.
  Done when: any id-taking command accepts a unique slug prefix, and an ambiguous prefix lists the candidates.

- **Print an asked → shipped ledger** — FEATURE — value 3 — effort S — risk low — category: recap
  Why: the user's asks and the resulting commits are both on record (T-1984 → T-1987). A two-column view shows what they asked this week and what landed.
  Done when: `fm week` lists each recent ask beside its task id and commit subject. An ask with no commit shows "open" or "dropped: <reason>".

- **Wild: Keep a captain's log** — FEATURE — value 2 — effort S — risk low — category: personality
  Why: wild. An optional, opt-in `LOG.md` gets one short, dry diary entry per day, written from closed tasks ("Two suites tried to run at once. Stopped it. Lunch."). Skimmable and shareable.
  Done when: with the setting on, a day with closed tasks appends one entry of at most 5 lines with the task ids. With the setting off, no file is written.

- **Wild: Shift the pane tint through the day** — FEATURE — value 2 — effort S — risk low — category: visual
  Why: wild, and it ties to the open pane-background issue (T-1217). A slow warm-to-cool accent shift by local time, off for reduced-motion users and for terminals below 256 colors.
  Done when: the accent differs between 09:00 and 23:00 fixtures, and the setting off yields one constant color.

- **Wild: Add a guard trophy shelf** — FEATURE — value 3 — effort S — risk low — category: guard
  Why: wild. The guard hook silently stops commands the user would never want. A tally the user can pull up ("force-push ×2, `rm -rf` outside the project ×1 this month") makes the protection visible and rewarding.
  Done when: `fm guard shelf` lists blocked-command categories with counts from the deny log. An empty log prints a friendly empty state.

- **Wild: Leave a "gift" line when a task finishes early** — FEATURE — value 2 — effort M — risk med — category: surprise
  Why: wild. When a task closes with budget left, Foreman proposes one sibling paper cut it noticed, as a single line that the user accepts with Enter. It never starts the work itself, which respects the dropped "offers" decisions and the never-idle rule.
  Done when: closing a task with unused budget and a recorded noticed-item prints at most one offer line. Declining it files nothing, and a test checks that the offer is not repeated.

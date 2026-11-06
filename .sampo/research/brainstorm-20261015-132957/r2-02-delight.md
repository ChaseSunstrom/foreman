# Brainstorm — lens: delight

- **Show a "safe to close the lid" light** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: assumption: the pile has resume, away and sleep-inhibitor ideas, but none gives the one-glance answer to "can I leave now?". Foreman already knows its running lanes, unsaved edits, open asks and pending snapshots.
  Done when: the band and `fm status` show a green or amber glyph; the glyph turns amber with a named reason (e.g. "lane T-0850 mid-merge") when a lane is mid-merge, and turns green once it finishes.

- **Go calm when the user is frustrated** — FEATURE — value 4 — effort M — risk med — category: tone
  Why: the pack already logs corrections and bare "continue" stalls, and the user pushed back repeatedly. Nothing changes Foreman's behaviour when a pattern of corrections, caps or terse repeats shows up.
  Done when: after 2 corrections inside 10 minutes, injected ceremony drops (no recap, one-line replies) and the band shows "calm"; a replayed fixture of 3 corrections triggers it, and a neutral fixture does not.

- **Give every task a speakable slug** — FEATURE — value 3 — effort S — risk low — category: legibility
  Why: the user talks in plain words ("fix the login timeout"), but the queue speaks in T-0841 ids and long titles. A slug like `login-timeout` could be accepted anywhere an id is.
  Done when: `fm task show login-timeout` resolves, the band prints the slug, and a collision gets a numeric suffix.

- **Complete `fm` verbs and task slugs from the live queue** — FEATURE — value 4 — effort M — risk low — category: ergonomics
  Why: evidence: roughly 108 verbs, with the brief already complaining about verb sprawl. Pressing tab to get verbs, then the queue's real slugs, makes the surface discoverable without hiding anything.
  Done when: bash, zsh and fish completion scripts install via `fm shellinit`, and `fm task show <TAB>` lists open slugs with titles in a clean-HOME test.

- **Print the undo with every Foreman action** — FEATURE — value 4 — effort M — risk low — category: safety net
  Why: `fm oops`, snapshots and `task drop` as snapshot are scattered. Each destructive-ish verb (`lane rm`, `tidy`, `task drop`, `compact`) could end with a single line: `undo: fm snapshots restore X (kept 14d)`.
  Done when: each listed verb prints an undo line, and running that exact line restores the prior state in a test.

- **Write a brag doc from the ledger** — FEATURE — value 4 — effort M — risk low — category: user value
  Why: assumption: people dread review season. The ledger has closed tasks, evidence, the user's own request words and diff sizes. This differs from the stakeholder page and the time sheet because it is first-person impact: "fixed X, which unblocked Y".
  Done when: `fm brag --since 2026-07-01` writes a Markdown file grouped by theme with task ids and evidence links, and local-only mode redacts any repo flagged sensitive.

- **Track personal bests** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: assumption: the pile has streaks and a net-lines-deleted flourish, but no records like fastest verified fix, longest run with no correction, or biggest proven deletion. A record broken gets one quiet line at close.
  Done when: `fm records` lists 5 bests with task links, and closing a task that beats one prints "new best: …" exactly once.

- **Let a plain "ship it" land the last close** — FEATURE — value 4 — effort M — risk med — category: flow
  Why: the user speaks tersely. "ship it", "lgtm" or "land it" after a close should run the configured landing step (commit, optionally push) and nothing wider. The guard and the existing landing-ladder idea would still gate it.
  Done when: in a fixture, "ship it" after a green close makes the commit and does not push unless push is configured; after a red close, it explains what blocks it.

- **Keep a bug graveyard (wild)** — FEATURE — value 2 — effort M — risk low — category: delight
  Why: `fm bisect`, `why` and blame already find when a bug was born. A fixed FIX task could add a tombstone to `graveyard.md`: born (commit and date), lived (days), killed by (T-id), epitaph in the user's own words from the request.
  Done when: closing a FIX with a located culprit appends a tombstone with correct dates, and `fm graveyard` prints the latest five.

- **Render FIX closes as a case file (wild)** — FEATURE — value 2 — effort M — risk low — category: shareable
  Why: `fm suspects`, the mutation proof and the evidence grade already produce the ingredients. Showing them as "the crime, the suspects ruled out, the culprit, the proof" would be the thing someone screenshots.
  Done when: `fm task finish --case-file` writes a one-screen text/HTML card for FIX tasks that names the real suspects from the data (none invented), and it is skipped when there is no evidence.

- **Make `fm wrapped`, a yearly or quarterly recap (wild)** — FEATURE — value 3 — effort M — risk med — category: sharing
  Why: the ledger holds guard saves, nights worked, longest unattended stretch, most-touched file, the first-time-pass rate and the biggest deletion. Unlike the token tax return or the weekly letter, it is built to be shared, with a redaction pass and paths and names stripped.
  Done when: `fm wrapped --period 90d` writes one self-contained HTML file with no network requests and no raw paths, and the stats match `fm stats` on the same window.

- **Make bare `fm` answer "what now?"** — FEATURE — value 3 — effort S — risk low — category: first touch
  Why: the newcomer round shipped a short help list, but a bare `fm` still prints help. A single next-action line (resume the step, close the pending task, capture something) with a runnable command would make the first and hundredth touch the same.
  Done when: bare `fm` in a project with an active task prints the exact next command in under 3 lines, and in a fresh repo it prints the `fm init` line.

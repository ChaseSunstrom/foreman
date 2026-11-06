# Brainstorm — lens: capability map

- **Add `fm triage` as the one entry that picks the surface** — FEATURE — value 4 — effort S — risk low — category: backlog
  Why: round 5 review: four triage surfaces (first, swipe TTY, swipe --serve, app view I) and no single entry that chooses among them. Best-in-class trackers have one inbox.
  Done when: `fm triage` opens the browser swipe page when a display is available, the TTY swipe otherwise, and a test asserts both routes.

- **Add undo and a cards-left counter to swipe --serve** — FIX — value 4 — effort S — risk low — category: backlog
  Why: review notes the served page has no undo of the last verdict and no remaining count. Every card-swipe UI has both.
  Done when: pressing `z` on the served page reverts the previous verdict in the backlog file, and the page shows "N left" that decrements.

- **Rewrite guard refusals into the literal-path retry** — FIX — value 5 — effort M — risk low — category: guard
  Why: the risk budget tripped 6 times from the user's own `$VAR` paths and `rm` on /tmp globs. The refusal text could name the rewrite so the retry passes first time.
  Done when: a refused `rm -rf $DIR/x` prints the literal-path form and a test shows the printed form is allowed by the guard.

- **Refresh a fetched ticket brief in place** — FEATURE — value 4 — effort M — risk med — category: intake
  Why: review: an upstream issue edit makes a second brief instead of updating the first (T-1859).
  Done when: re-running `fm inbox ticket KEY` after an upstream edit updates the existing brief and shows a diff of the changed lines, with no new task created.

- **Fetch GitHub issues and comment threads in `fm inbox ticket`** — FEATURE — value 4 — effort M — risk low — category: intake
  Why: review: only Jira and Linear are covered, although `gh` is the common case, and no comments are fetched. The existing list has "import a GitHub issue as a task" without comment threads or brief refresh.
  Done when: `fm inbox ticket owner/repo#N` writes a brief containing the body and all comments, under a fake `gh` in tests.

- **Post the close link back to the source ticket** — FEATURE — value 3 — effort M — risk med — category: intake
  Why: review: no way to post back when the task closes. Tools like Linear and Jira link the commit automatically.
  Done when: closing a ticket-sourced task prints the comment it would post, and posts it only when `--post` is set.

- **Serve an `fm serve` index of every servable page** — FEATURE — value 3 — effort S — risk low — category: web UI
  Why: review: settings serve and swipe serve each use a one-shot token with Ctrl-C to stop, and each duplicates its own style block.
  Done when: `fm serve` lists swipe, settings and the scene gallery behind one token, and the pages share one stylesheet that a test greps for.

- **Ship a scene gallery with captions and a render-time test** — FEATURE — value 3 — effort S — risk low — category: scenes
  Why: review: T-1846..1855 shipped many scenes with no gallery index, no caption saying what each one tells you, and no test that each renders under 1 s.
  Done when: `fm scene gallery` lists every scene with a caption, and a test fails if any scene takes over 1 s.

- **Report known-fix offer, accept and wrong rates** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: T-1865 made matching safer, but nothing reports how often a fix was offered, accepted or wrong.
  Done when: `fm fixes stats` prints per-signature offered/accepted/rejected counts from the journal.

- **Explain why one backlog item outranks another** — FEATURE — value 3 — effort M — risk low — category: backlog
  Why: review: learned priorities (prefer) never explain themselves.
  Done when: `fm inbox why T-A T-B` names the preferences that decided the order, as a testable string.

- **Report unused design tokens in CSS** — FEATURE — value 3 — effort S — risk low — category: design
  Why: review: nothing checks that DESIGN.md tokens are actually used in CSS. Design-system linters all offer this.
  Done when: `fm design unused` lists tokens with zero references in a fixture repo, and exits non-zero under `--strict`.

- **Offer the settings macros from `fm settings newcomer`** — FEATURE — value 2 — effort S — risk low — category: settings
  Why: review: log/macro/duel/replay are discoverable only via help, and newcomer never offers macros.
  Done when: newcomer ends by listing the three most relevant macros, and a test asserts the line.

- **Wild: Wake a stale backlog card with a spoken one-liner** — FEATURE — value 2 — effort M — risk low — category: delight
  Why: wild. The swipe loop already has a card at a time, so a local TTS line, off by default, reads each card on a swipe session.
  Done when: with `--say` set and a stub speaker, each card passes its title to the speaker once.

- **Wild: Turn the guard's near-misses into a two-minute practice quiz** — FEATURE — value 3 — effort M — risk low — category: guard
  Why: wild. The user's own 6 collisions are exactly the cases worth drilling. Pairs with the refusal-rewrite idea above.
  Done when: `fm guard quiz` draws 5 questions from the user's own refusal log and scores them against the guard.

- **Wild: Print one weekly "triage zine" from swipe verdicts** — FEATURE — value 2 — effort M — risk low — category: delight
  Why: wild. Swipe verdicts, prefer weights and closed tasks already exist, so a single printable page can summarize what was kept, dropped and why.
  Done when: `fm inbox zine` writes one HTML page listing the week's keep/skip counts and top three preferences, matching a golden file.

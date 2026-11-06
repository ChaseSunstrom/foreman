# Brainstorm — lens: user value

- **Make the guard's refusal name the safe rewrite** — FIX — value 5 — effort S — risk low — category: guard UX
  Why: Round 5 review: the risk budget tripped on 6 destructive blocks, mostly the author's own `$VAR` paths and `rm` on `/tmp` globs; the refusal text doesn't say what would pass. Related steer: pgrep/pkill self-match refusal.
  Done when: each refusal for a `$VAR` path, a glob `rm` or a self-matching `pkill -f` prints the literal-path (or narrower) command, and a test shows that command is allowed.

- **Add one `fm triage` entry that picks the backlog surface** — FEATURE — value 4 — effort S — risk low — category: backlog
  Why: Four triage surfaces (first, swipe TTY, swipe --serve, app view I) and no single entry that chooses among them (review). Related: user asked to swipe the deferred backlog; ~30 "Later from" items sit deferred.
  Done when: `fm triage` opens the browser page when a display exists and the TTY swipe over ssh, and a test covers both branches.

- **Undo and count-left in swipe --serve** — FEATURE — value 4 — effort S — risk low — category: backlog
  Why: Review: the served page has no undo of the last verdict and no cards-left count.
  Done when: pressing `u` on the served page restores the last card with its previous state, and the page shows "n left" that decrements per verdict.

- **Triage the deferred "Later from" pile against usage evidence** — FEATURE — value 5 — effort M — risk low — category: backlog
  Why: About 25 items (T-0788..T-0869) sit deferred as "Later from T-0760/0818/0843". Prior steer: show the user the checklist before skipping. Assumption: `fm usage` and the journal show which areas the user actually touches.
  Done when: one page lists each deferred item with "evidence for / none" and a build/skip default, and ticking it updates the backlog.

- **Add GitHub issues to `fm inbox ticket`** — FEATURE — value 4 — effort S — risk low — category: intake
  Why: T-1859 covers Jira and Linear only; `gh` is the common case (review). Also asked: "Import a GitHub issue as a task whose first step is a failing test".
  Done when: `fm inbox ticket https://github.com/o/r/issues/N` (or `o/r#N`) makes a planned brief, with the issue's comments included.

- **Refresh a fetched ticket brief instead of making a second one** — FEATURE — value 3 — effort S — risk low — category: intake
  Why: Review: an upstream edit creates a second brief rather than updating the first.
  Done when: re-running `fm inbox ticket KEY` on an edited issue updates the existing brief and shows a diff of the changed lines; a test covers it.

- **Report how often a known fix was offered, accepted and wrong** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: T-1865 made matching safer but nothing measures it (review).
  Done when: `fm fixes stats` prints offered/accepted/rejected counts per signature, and a rejected offer demotes that signature.

- **Explain why one backlog item outranks another** — FEATURE — value 3 — effort S — risk low — category: backlog
  Why: Review: learned `prefer` priorities never explain themselves; the steer to "show why each queued task is next" fits.
  Done when: `fm task next --why` prints the top three with the score terms (preference, size, age, blocked) and a test pins them.

- **Serve one index of every servable page** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: Review: settings serve and swipe serve each use a one-shot token, Ctrl-C to stop, and a duplicated style block; no shared `fm serve` index.
  Done when: `fm serve` lists swipe, settings, scenes and the app view on one loopback page sharing one stylesheet, under a single token.

- **Wild: Send a morning "needs you" digest with paste-ready answers** — FEATURE — value 5 — effort M — risk med — category: unattended
  Why: Pillar 7: in full autonomy only the final report reaches the user; 11 briefs sit blocked on things only they can do (T-0325, T-0352, T-0418…). Wild.
  Done when: after an unattended run, one page lists each blocked item with the exact command or sudo line to unblock it and a "done" tick that re-queues it.

- **Wild: Bill-of-effort quote for a queue before it starts** — FEATURE — value 4 — effort M — risk med — category: cost
  Why: Steers on usage burn ("shouldn't have had to tell you") and the weekly reset; assumption: `fm cost` has per-task history to estimate from. Wild.
  Done when: `fm run --quote` prints a token/dollar range per task and the total against remaining weekly budget, and warns if the queue can't finish before the reset.

- **Wild: "Did I already decide this?" lookup against the user's own words** — FEATURE — value 4 — effort M — risk low — category: memory
  Why: Repeated drops of already-built or already-covered findings (set_panic, fm drill, lights) show the same ground being re-argued. Wild.
  Done when: `fm decided "<topic>"` returns the matching steers, drops and closed tasks with dates, and intake shows the hit before re-filing.

- **Gallery index for scenes with a one-line caption and a render-time test** — FEATURE — value 2 — effort S — risk low — category: scenes
  Why: Review: many scenes (T-1846..1855) with no index, no caption saying what each shows, and no check each renders under 1 s.
  Done when: `fm scene gallery` lists every scene with a caption, and a test fails if any takes over 1 s.

- **Unused-token report for DESIGN.md** — FEATURE — value 2 — effort S — risk low — category: design
  Why: Review: Figma import is one-way and nothing checks that DESIGN.md tokens appear in CSS.
  Done when: `fm design unused` lists tokens never referenced in the repo's CSS and exits non-zero under `--strict`.

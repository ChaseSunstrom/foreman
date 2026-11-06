# Brainstorm — lens: approaches

- **Name the literal-path rewrite in every guard refusal** — FIX — value 4 — effort S — risk low — category: guard UX
  Why: the review says 6 destructive blocks today came from `$VAR` paths and `rm` on `/tmp` globs, all the user's own collisions. A retry only works once the refusal says what to type. This is the cheapest approach: change the message, not the guard. The trade-off is that the guard's classifier needs to expose which rule fired.
  Done when: a test feeds `rm -rf $TMPDIR/x` and `rm /tmp/*` to the guard, and each refusal text contains a concrete literal-path command that the guard then allows.

- **Add GitHub issues to `fm inbox ticket` through `gh`** — FEATURE — value 4 — effort S — risk low — category: intake
  Why: T-1859 covers only Jira and Linear, yet the review notes `gh` is already the common case. Reuse the installed `gh issue view --json` rather than writing an API client. This needs no new auth or HTTP code. The trade-off is that it depends on `gh` being installed and logged in.
  Done when: `fm inbox ticket https://github.com/o/r/issues/1` against a stubbed `gh` creates one planned brief with the title, body and comments.

- **Make ticket briefs idempotent by key** — FIX — value 4 — effort S — risk low — category: intake
  Why: the review says an upstream edit makes a second brief instead of updating the first. Approach: store the ticket key and a content hash in the brief's front matter, then update in place or add a "changed upstream" note. The trade-off is that a brief with local edits needs a merge rule, and the simplest rule is to append rather than overwrite.
  Done when: fetching the same stubbed ticket twice with a changed body leaves one brief containing a "changed upstream" section.

- **Add one `fm triage` entry that picks the surface** — FEATURE — value 4 — effort M — risk low — category: backlog
  Why: there are four triage surfaces (first, swipe TTY, `swipe --serve`, app view `I`) and no single front door. Approach: do less. `fm triage` is a thin router that picks TTY, then served, then app by environment (no TTY means serve; app running means app). It changes no surface. The trade-off is that guessing wrong annoys, so a `--on` override is needed.
  Done when: `fm triage` runs the TTY swipe on a terminal and prints a served-page URL when stdin is not a TTY, covered by a test of both paths.

- **Give swipe a verdict journal with undo and a cards-left count** — FEATURE — value 4 — effort M — risk low — category: backlog
  Why: the review says `swipe --serve` has no undo and no remaining count. Approach: log each verdict as an append-only line, so undo is "pop the last line" and the count is a derived value. The same log can feed the `prefer` explanations. The trade-off is that undoing a verdict that already changed a task's state must reverse that change too.
  Done when: in a served-swipe test, a verdict followed by undo restores the task state, and the page shows "N left" decreasing and increasing accordingly.

- **Explain learned priorities with a `prefer --why T-xxxx` line** — FEATURE — value 3 — effort S — risk low — category: backlog
  Why: the review notes that prefer never explains why one item outranks another. Approach: reuse the existing score and print its top two contributing signals. The alternative, a full ranking UI, is far bigger. The trade-off is that signals must be stored with the score.
  Done when: `fm prefer --why T-1` prints the two heaviest signals and their weights, and the weights sum to the stored score in a test.

- **Serve every page from one `fm serve` index with a shared stylesheet** — CLEAN — value 3 — effort M — risk med — category: served pages
  Why: settings and swipe each serve a one-shot tokened page with a duplicated style block, and Ctrl-C is the only way to stop them. Approach: consolidation. One loopback server mounts pages by path and holds a shared CSS file. The trade-off is that one long-lived server has a larger attack surface than one-shot tokens, so the token is kept per page.
  Done when: `fm serve` lists both pages, each page's HTML contains no inline style block, and a request without the token returns 403.

- **Report offered vs accepted known fixes in `fm doctor`** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: T-1865 made matching safer, but nothing reports how often a fix was offered, accepted or wrong. Approach: count three events in the existing journal and print one ratio. The trade-off is that "wrong" needs a signal, and a revert or reopen within the same task is the cheapest one.
  Done when: after a fixture offers, accepts and then reverts a known fix, `fm doctor` prints offered 1, accepted 1, wrong 1.

- **Add an unused-token report to `fm design`** — FEATURE — value 3 — effort M — risk low — category: design
  Why: the review says nothing checks that DESIGN.md tokens appear in CSS. Approach: a plain text scan for each token name or value across CSS and TSX files, no parser. This is coarse, but it avoids a CSS AST dependency. The trade-off is false positives from computed names, so an `ignore:` list is needed.
  Done when: `fm design unused` on a fixture with one defined-but-unreferenced token lists exactly that token and exits nonzero under `--strict`.

- **Render every scene under a 1 s budget and index them in a gallery** — FEATURE — value 3 — effort M — risk low — category: scenes
  Why: T-1846 to T-1855 shipped many scenes with no index, no caption and no render-time test. Approach: one table in the code gives each scene a caption and the loop renders them all. A single test covers the budget, the caption and the gallery. The trade-off is that a 1 s limit may flake under parallel load, which is a known CI problem, so it should use a median of three runs.
  Done when: the test fails when a scene has no caption or its median render exceeds 1 s, and `fm scene gallery` lists every scene.

- **Offer macros in `fm settings newcomer`** — FEATURE — value 2 — effort S — risk low — category: discoverability
  Why: the review says log, macro, duel and replay are discoverable only through help, and newcomer never offers them. Approach: print one line per feature at the end of newcomer. The alternative, a tour, is already deferred (T-0862). The trade-off is a slightly longer newcomer flow.
  Done when: the output of `fm settings newcomer` in a test names macro, duel, replay and log with one runnable example each.

- **Wild: Post the commit link back to the ticket on close** — FEATURE — value 3 — effort M — risk med — category: intake
  Why: the review notes there is no way to post back. Approach: on `fm task finish`, offer a one-line comment containing the commit and proof, and send nothing until the user confirms. The trade-off is that this publishes text to an external service, so it is opt-in per ticket and shows the exact text first. (wild)
  Done when: closing a ticket-sourced task prints the proposed comment and calls the stubbed `gh` or API only after an explicit yes.

- **Wild: Replace the "forever loop" with a one-page round verdict** — FEATURE — value 3 — effort M — risk low — category: loop control
  Why: the request is "improve past everything shipped" again, and the review of each round is written by hand. Approach: invert the process. Each round starts by auto-generating the review (served pages, scenes, intake gaps) from the journal, so the loop runs against measured gaps rather than a fresh brainstorm. The trade-off is that it only finds what the journal records. (wild)
  Done when: `fm round review` outputs a list of findings each tied to a journal or test reference, and a fixture with a planted gap yields that finding.

- **Wild: Try a "guard collision" replay from the user's own shell history** — SECURITY — value 3 — effort M — risk low — category: guard UX
  Why: the user's own commands trigger most blocks. Approach: replay the last 500 history lines through the guard offline, then cluster the refusals and propose the rewrites. This tunes the refusal text from real data rather than guesses. The trade-off is that history may hold secrets, so it is read locally and only counts are stored. (wild)
  Done when: `fm guard history` prints refusal clusters with counts for a fixture history file and writes nothing outside the state directory.

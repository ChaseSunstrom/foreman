# Brainstorm — lens: delight

- **Show the swipe stack's remaining count as a thinning deck** — FEATURE — value 4 — effort S — risk low — category: backlog
  Why: T-1858 `fm inbox swipe --serve` has no count of cards left and no undo of the last verdict (round 5 review). A visible deck that thins as you decide gives progress and a reason to finish.
  Done when: the served swipe page shows a stack whose card count equals the remaining items and drops by one per verdict, and a test asserts the count in the page state.

- **Add a one-key undo to swipe with a rewinding card animation** — FEATURE — value 4 — effort S — risk low — category: backlog
  Why: review notes swipe --serve has no undo of the last verdict; mis-swipes on a fast triage loop are costly.
  Done when: pressing `u` restores the previous card with a reverse slide, the verdict is removed from the ledger, and a test covers undo after skip, build and defer.

- **Give `fm serve` one index page that lists every servable page with a shared style** — FEATURE — value 4 — effort M — risk low — category: web UI
  Why: review: swipe and settings serve are one-shot tokened pages with duplicated style blocks and no index.
  Done when: `fm serve` opens a single page linking the live pages (swipe, settings, scenes gallery), all pulling one shared stylesheet, and a test checks no page carries its own copy of the base style block.

- **Caption every scene with "what this is telling you"** — FEATURE — value 3 — effort S — risk low — category: scenes
  Why: T-1846..1855 shipped many showpiece scenes with no gallery and no caption (round 5 review). A one-line caption turns spectacle into information.
  Done when: each scene renders a caption line from its data and `fm scene --gallery` lists all scenes, each rendering under 1 s in a test.

- **Open a scene gallery with live thumbnails** — FEATURE — value 3 — effort M — risk low — category: scenes
  Why: review: no gallery index of the many scenes; the user would have to know each name.
  Done when: the gallery page shows one animated thumbnail per scene, hover plays it, and a test asserts every registered scene appears.

- **Make a guard refusal print the literal-path rewrite that would succeed** — FIX — value 5 — effort S — risk low — category: guard
  Why: review: 6 destructive blocks in a day came from `$VAR` paths and `rm` on /tmp globs; the refusal text could name the safe rewrite so the retry works first time. Delight here is the absence of a wasted round trip.
  Done when: refusing `rm -rf $DIR/x` prints a "try:" line with the expanded literal path, and a test covers a variable path and a tmp glob.

- **Celebrate a first-try fix after a refusal with a "clean retry" tick** — FEATURE — value 2 — effort S — risk low — category: feedback
  Why: assumption: the refusal rewrite above makes first-time-success measurable; a small tick on it reinforces the habit.
  Done when: a retry that matches the suggested rewrite shows a one-line tick in the receipt and the count appears in `fm stats`.

- **Report how often a known fix was offered and accepted** — FEATURE — value 3 — effort S — risk low — category: known fixes
  Why: T-1865 made matching safer but nothing reports offered vs accepted vs wrong; a "your known fixes saved N retries" line is a small recurring win.
  Done when: `fm known-fixes stats` prints offered, accepted, rejected counts per signature, backed by journal events in a test.

- **Explain why one backlog item outranks another with a "because" chip** — FEATURE — value 4 — effort M — risk low — category: backlog
  Why: review: learned priorities (prefer) never explain themselves; the user pushes back on opaque choices.
  Done when: each swipe card and list row shows the top preference signal as a chip ("you kept 4 similar"), and a test checks the chip names a recorded verdict.

- **Offer macros inside `fm settings newcomer`** — FEATURE — value 3 — effort S — risk low — category: settings
  Why: review: log/macro/duel/replay are discoverable only via help; newcomer never offers macros.
  Done when: the newcomer flow ends with a one-key offer to record a macro of the choices made, and a test replays it.

- **Wild: Let the swipe deck throw a confetti of closed tasks when the inbox hits zero** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: assumption: the backlog triage is the loop the user returns to most (four surfaces shipped); an emptied inbox deserves a moment. Respect reduced-motion and a hush key. wild
  Done when: reaching zero cards renders a short, skippable animation that is replaced by a static line under reduced motion, tested in both modes.

- **Wild: Play a "card of the day" from the user's own past verdicts as a second-guess game** — FEATURE — value 2 — effort M — risk low — category: delight
  Why: the learned `prefer` model is hidden; showing a past decision and asking "still true?" refreshes stale priorities playfully. assumption: the user is willing to answer one card a day. wild
  Done when: `fm inbox swipe --daily` shows one old verdict, a keypress confirms or flips it, and the preference weights update in a test.

- **Wild: Print the scene gallery as a trading-card sheet of the week's shipped work** — FEATURE — value 2 — effort M — risk low — category: delight
  Why: many showpiece scenes exist with no way to show them off; a printable one-page sheet makes them shareable and gives the release a keepsake. wild
  Done when: `fm scene --sheet out.html` writes a single self-contained page with one card per scene and a print stylesheet, and a test checks it makes no external requests.

- **Unused-token report that lights up in DESIGN.md as a "wardrobe"** — FEATURE — value 3 — effort M — risk low — category: design
  Why: review: no check that DESIGN.md tokens are actually used in CSS; showing worn vs unworn tokens as a wardrobe makes the audit pleasant to read.
  Done when: `fm design --wardrobe` lists each token with a used/unused mark and usage count against the project CSS, with a test on a fixture.

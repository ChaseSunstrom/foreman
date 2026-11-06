# Brainstorm — lens: delight

- **Rewind the swipe card on undo** — FEATURE — value 4 — effort S — risk low — category: swipe
  Why: T-1858 swipe --serve has no undo of the last verdict (round 5 review); a rewinding card makes the correction feel physical.
  Done when: pressing `u` in swipe --serve restores the previous card with a reverse slide, and the verdict journal shows the reversal.

- **Show the remaining deck as a thinning stack** — FEATURE — value 3 — effort S — risk low — category: swipe
  Why: the served page has no count of cards left (round 5 review); a visible stack gives progress without a number.
  Done when: the served page renders a stack whose visible layers drop as cards are decided, and a "N left" label matches the backlog count.

- **Clean-retry tick after a guard refusal** — FEATURE — value 3 — effort S — risk low — category: guard
  Why: the user hit 6 destructive blocks mostly from `$VAR` paths and `rm` on /tmp globs; a refusal that names the literal-path rewrite, followed by a small tick when the retry passes first time, turns friction into a learning moment.
  Done when: a refused command prints the literal-path rewrite, and a successful retry within the same session prints a one-line "clean retry" mark counted in `fm doctor`.

- **Open a scene gallery with live thumbnails and captions** — FEATURE — value 4 — effort M — risk low — category: scenes
  Why: T-1846..1855 shipped many showpiece scenes, but there is no index, no "what is this telling me" caption, and no render-time test (round 5 review).
  Done when: `fm scene gallery` serves a page of thumbnails each with a one-line caption, and a test fails any scene taking over 1 s to render.

- **Light up unused DESIGN.md tokens as a wardrobe** — FEATURE — value 3 — effort M — risk low — category: design
  Why: round 5 notes no check that DESIGN.md tokens are used in CSS; showing them as a wardrobe of worn and unworn swatches makes the report pleasant to read.
  Done when: `fm design wardrobe` prints each token as a swatch marked used or unused by counting references in the CSS, and exits non-zero with `--strict` if any is unused.

- **Give every served page one shared look from a `fm serve` hub** — FEATURE — value 4 — effort M — risk low — category: serve
  Why: each served page duplicates its own style block, uses a one-shot token, and there is no index of servable pages (round 5 review).
  Done when: `fm serve` lists every servable page on one index, all pages load one shared stylesheet, and the duplicated style blocks are gone.

- **Offer settings macros at the end of `fm settings newcomer`** — FEATURE — value 3 — effort S — risk low — category: settings
  Why: log/macro/duel/replay are discoverable only via help, and newcomer never offers the macros (round 5 review).
  Done when: finishing `fm settings newcomer` shows the available macros with a one-key "try this" and records the choice.

- **Say "closed, and here's what to do" with a gentle receipt line** — FEATURE — value 2 — effort S — risk low — category: close-out
  Why: the user asked that the session-start CI line say a task is closed and what to do, not "fix it first"; the same warmth applies to every closing line.
  Done when: a closed-task CI line states closed status and one next command, covered by a test on the message text.

- **Wild: Play a "card of the day" second-guess game** — FEATURE — value 3 — effort M — risk low — category: swipe — wild
  Why: assumption: the user's past swipe verdicts sit in a journal; re-showing one old verdict daily and asking "still agree?" teaches Foreman their drift and is playful.
  Done when: session start offers one past card, and answering changes or confirms a stored preference visible in `prefer --why`.

- **Wild: Throw confetti when the inbox hits zero** — FEATURE — value 2 — effort S — risk low — category: swipe — wild
  Why: assumption: emptying the backlog is the moment of most relief and nothing marks it today; a short, reduced-motion-aware burst in the served page and a single line in the TTY makes it memorable.
  Done when: finishing the last card triggers the animation, and `prefers-reduced-motion` or NO_COLOR replaces it with one static line.

- **Wild: Print a weekly triage zine from swipe verdicts** — FEATURE — value 3 — effort M — risk low — category: sharing — wild
  Why: assumption: shipped zine/vase exports already exist as run cards; swipe verdicts have no keepsake, and a one-file offline page of what was kept, skipped and shipped is something to show others.
  Done when: `fm inbox swipe --zine` writes one self-contained HTML file listing the week's verdicts with their closed tasks, and it opens with no network.

- **Wild: Turn guard near-misses into a two-minute practice quiz** — FEATURE — value 3 — effort M — risk low — category: guard — wild
  Why: the user's own `$VAR` and `/tmp` glob collisions are a ready corpus; replaying them as "will this be blocked?" questions builds intuition for safe phrasing.
  Done when: `fm guard quiz` asks five questions drawn from recorded refusals, scores the answers, and a test confirms each answer matches the real guard verdict.

- **Explain a learned priority in one line with a tiny bar** — FEATURE — value 3 — effort S — risk low — category: backlog
  Why: learned priorities (prefer) never explain why one item outranks another (round 5 review).
  Done when: `fm prefer --why T-xxxx` prints the top two reasons with a small weight bar, and the swipe card shows the same line.

- **Greet a first-try fix with the one-line "known fix" outcome** — FEATURE — value 2 — effort S — risk low — category: known-fixes
  Why: T-1865 made matching safer but nothing reports offered versus accepted versus wrong; a small closing line like "known fix used, passed" makes the feature visible and countable.
  Done when: accepting a known fix prints a one-line outcome after the gate, and `fm doctor` shows offered, accepted and wrong counts.

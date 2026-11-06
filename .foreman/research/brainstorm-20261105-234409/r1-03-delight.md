# Brainstorm — lens: delight

- **Strike the metal on the close** — FEATURE — value 5 — effort M — risk low — category: delight
  Why: Sampo’s look is the illustrated forge with heat as the “running now” signal; a close is the moment the hammer falls. A brief ring-out and a single spark burst on the terminal (TTY bell + 24-colour flash) and in the web pane’s work bar makes a green close *feel* like a strike, and it’s something the user will show others.
  Done when: `samo task finish` plays the ring and the web pane’s work bar flashes once; a reduced-motion setting suppresses the flash but keeps the sound.

- **Read the morning like a forge log** — FEATURE — value 4 — effort S — risk low — category: delight
  Why: The user’s words repeatedly ask for a morning card and “what happened overnight.” Framing it as a forged receipt — “Night: 3 strikes, 1 quenched, 1 cracked — read the slip” — turns the unattended work into a narrative object with a torn-edge slip (a standing idea, here made concrete and shippable) they can keep.
  Done when: the morning card renders as a slip with a one-line forge log and a “what I left out” tail; it opens on `samo drive` start.

- **Animate a cell filling as its brief closes** — FEATURE — value 4 — effort M — risk low — category: delight
  Why: The request grid is the heart of the Mission page. When a brief that fills an empty cell closes, the cell should *fill* with a short ember-glow animation — motion that explains state (coverage earned, not just passed). A standing idea, now with the forge’s heat as the “running now” cue.
  Done when: closing a brief whose grid cell was empty triggers a one-time ember fill; a screen-reader announces “cell <id> now filled.”

- **The hammer’s trail, unclipped** — FIX — value 3 — effort S — risk low — category: delight
  Why: T-2964 explicitly fixed “the hammer’s motion trail is clipped by a hard edge.” The delight is the trail; clipping it kills the signature. Let the trail bleed into the sky with a soft alpha fade and a subtle metallic shimmer, respecting the Kirjokansi “instrument lit and blended into the sky” rule.
  Done when: the hammer’s trail extends past the element bounds with no hard edge; a pixel-diff at 768px shows no clipping.

- **Tear off the “left out” slip and keep it** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: A standing wild idea, now the cheapest to ship and the most *object-like*: a real torn-edge receipt, downloadable as a tiny SVG the user can pin or screenshot. It makes an unattended Mission feel like it left you a physical note rather than a log line.
  Done when: the Mission close emits `leftout.svg` with a torn edge; `samo mission show` renders it inline.

- **Ring the astrolabe on a first** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: A “first-ever” cell, first verified close, or first green duel deserves a distinct chime — not the same sound as an ordinary close. A one-shot, non-repeating tone keeps it from becoming noise, and it rewards the tower’s self-advancing rule with audible milestones.
  Done when: the first close of a brand-new capability emits a unique two-note chime; `samo doctor` lists chime usage so the user can mute.

- **Sound the funnel as ambient audio** — FEATURE (wild) — value 3 — effort M — risk med — category: delight
  Why: Wild: the 10,000-moon funnel is a huge machine the user can see but never *hear*. Map kills, promotions and diversity collapses to a soft ambient bed (a low forge hum that thins when the pool collapses, brightens on a promotion), played only while the web UI is focused, at a whisper. It makes the tower’s ecology perceptible and is a “show this to a friend” moment.
  Done when: a focused web UI plays a ≤ -40 dB ambient bed that changes register with funnel stage; a toggle and reduced-motion both silence it.

- **A one-keystroke “ah” grade** — FEATURE (wild) — value 4 — effort S — risk low — category: delight
  Why: The standing rule says no idea is killed for ambition, and the user grades by taste. Letting them press one key on any moon or brief to mark it “ah” (delight) — captured as a local ledger event — trains the funnel toward what they *feel* without a form. It’s the smallest possible delight loop and feeds the wildness score.
  Done when: on the web UI, pressing `A` on a moon logs a delight event; the morning card shows the top “ah”ed idea.

- **Chime once, then go quiet** — CLEAN (wild) — value 4 — effort S — risk low — category: delight
  Why: Standing rule: a chime on a long unattended Mission landing with a first. But delight decays into nuisance. Auto-demote any chime to silence after it has fired N times, and print the demotion in the morning card (“the first-verified chime retired itself”). Delight that knows when it’s done is a small thing people love and show others.
  Done when: a chime fires at most N times, then logs its retirement; `samo doctor` shows the count and the mute command.

- **Sonify the night as eight embers** — FEATURE (wild) — value 3 — effort M — risk med — category: delight
  Why: Wild: a “night strip of eight embers” on the site and pane — one ember per phase, lit by heat, and when the user hovers, a single soft strike sound for each lit ember, in sequence. It makes an unattended night a tiny, listenable artifact rather than a log, and it’s the kind of touch a design-led team ships.
  Done when: the pane shows an 8-ember strip after a night; hovering plays up to eight soft strikes in order; reduced-motion renders it statically.

- **The forge answers back** — FEATURE (wild) — value 3 — effort L — risk med — category: delight
  Why: Wild: when the user types a request that the ledger shows they’ve asked before, the pane briefly shows a dimmed ghost of their *own* past phrasing (“last time you wrote it as: …”) — a mirror, not a suggestion. It delights by being *theirs*, and it feeds the anticipation predictor with consent.
  Done when: a repeated ask shows a dimmed one-line echo of the user’s prior phrasing for 3s; a setting suppresses it entirely.

- **Strike on the phone too** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: The web UI is one surface; the user’s standing push grant and phone-approve ideas show the phone is a real surface. When a long unattended Mission lands a first, the phone gets a single haptic strike and a one-line “the forge rang” push — not a log dump. Cross-surface delight that respects “no interrupt mid-run.”
  Done when: a first-verified close on a remote repo sends one haptic + one-line push; a “forge quiet” setting silences it.

- **A 60-second “season recap” scrub** — FEATURE (wild) — value 4 — effort M — risk med — category: delight
  Why: The standing idea “let the user scrub a week of the tower as a short season recap.” Render the last 7 days as a 60s animated strip (the astrolabe turning, embers striking, cells filling), scrubbable, with a line of forge-log captions. It’s the single best “show this to someone” artifact Sampo can produce, and it doubles as the cold-reader’s onboarding.
  Done when: `samo recap 7` renders a 60s scrubbable strip; a cold child can say what happened from it.

- **A one-line “what I left out” on the status bar** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: The left-out slip is the soul of an unattended Mission. A persistent one-line status-bar glyph (a dimmed rune) that lights when the last Mission left something out, and on hover shows the slip, keeps the user aware without a page. It’s a small, always-there touch that makes the discipline legible.
  Done when: the status bar shows a dimmed rune when the last Mission’s left-out list is non-empty; hover shows the slip.

- **The forge keeps a “museum” chime** — CLEAN (wild) — value 3 — effort S — risk low — category: delight
  Why: Wild: keep a frozen “museum” chime — the exact sound of the *first ever* close on this install — and play it once a year on the anniversary. It’s playful, personal, and a small thing the user will remember and tell someone. It costs almost nothing and is pure delight.
  Done when: on the anniversary of the first close, the forge plays the recorded first-chime once; `samo doctor` lists the date and the suppress command.

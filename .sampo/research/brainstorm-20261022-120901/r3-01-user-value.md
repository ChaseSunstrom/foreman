# Brainstorm — lens: user value

- **Scaffold projects born proven with `fm new`** — FEATURE — value 5 — effort M — risk low — category: onboarding
  Why: assumption: users build new things too. The pack shows gates, the DESIGN.md contract, `fm check ui` and scene templates, but nothing assembles them for a blank directory.
  Done when: `fm new web-3d` (also `web-app`, `cli`, `tui`) makes a repo that passes its own `fm doctor` and gates, has a DESIGN.md and CI file, and closes a first task with proof.

- **Generate brand assets from DESIGN.md** — FEATURE — value 4 — effort M — risk low — category: design output
  Why: assumption: every real UI also needs a favicon set, app icons, OG and social cards. Nothing in the pack makes them, and stdlib SVG plus zlib PNG can.
  Done when: `fm brand` writes SVG and PNG sizes from the tokens, and a check confirms sizes, contrast and that no colour falls outside the palette.

- **Write a microcopy and content-design playbook with `fm check copy`** — FEATURE — value 4 — effort M — risk low — category: playbooks
  Why: the pack's UI work covers looks and motion, not words. Generic empty states, errors and button labels ("Submit", "Oops!") are the commonest tell of unconsidered UI.
  Done when: the playbook ships with slop/crafted pairs, and the checker flags a fixture page's generic verbs, missing empty and error states, and over-length labels.

- **Write a landing-page structure playbook, dogfooded on the Foreman site** — FEATURE — value 4 — effort M — risk low — category: playbooks
  Why: the request asks for non-generic design, and the site/ pages are Foreman's own storefront. A playbook for the claim, proof, demo and call to action beats another style recipe.
  Done when: the playbook has a rubric (hero claim, proof within one scroll, a single CTA), and the Foreman site is rebuilt against it with before/after screenshots.

- **Write a forms and dense-data UI playbook with a fixture** — FEATURE — value 4 — effort M — risk low — category: playbooks
  Why: the pack's design material is hero-and-motion heavy. Real products are mostly tables, filters, inline edit and validation, and are where generic UI hurts users.
  Done when: a runnable fixture app (sortable table, filter bar, inline validation, keyboard navigation) passes `fm check ui` and a keyboard-only walk script.

- **Write a mobile and touch UI playbook with a viewport check** — FEATURE — value 3 — effort M — risk low — category: devices
  Why: the pack flags devices as thin, and the mobile cards give pitfalls but no taste. The playbook would cover thumb zones, safe areas, 44px targets, gesture motion and reduced motion.
  Done when: a lint run at phone viewports flags undersized targets and fixed-position overlaps in a bad fixture and passes a good one.

- **Export design tokens to Tailwind, CSS variables, shadcn and Figma tokens JSON** — FEATURE — value 4 — effort S — risk low — category: design system
  Why: the single token file idea exists for Foreman's own surfaces, but the user's apps live in Tailwind and shadcn (both in the web cards).
  Done when: `fm design export --to tailwind|css|shadcn|figma` round-trips a token set and a drift check fails if the code diverges.

- **Write an email and print design playbook with client-quirk checks** — FEATURE — value 2 — effort M — risk low — category: playbooks
  Why: assumption: users ship transactional email and PDFs that never get design attention. These are surfaces where CSS-grid habits break.
  Done when: a template passes checks for table layout, inlined CSS, dark-mode fallbacks and a print stylesheet.

- **Cap the capture of new FEATURE briefs against closed work** — FIX — value 4 — effort S — risk low — category: backlog
  Why: the pack lists about 30 deferred "Later from" tasks and the user is asking for another recursive round. A catalogue that grows faster than it ships buries the user's intent.
  Done when: capture shows "inflow 14, closed 3 this week" and requires a swap or an explicit override once open FEATURE briefs pass the cap.

- **Bundle each UI task's result into a client packet** — FEATURE — value 3 — effort M — risk low — category: close-out
  Why: UI work is judged by eye. A one-folder deliverable of static preview, poster frame, short clip, token sheet and changelog is what gets shown to someone else.
  Done when: closing a UI task writes `packet/`, and the preview opens offline with no network calls.

- **Wild: build a release-over-release design wall** — FEATURE — value 4 — effort M — risk low — category: proof
  Why: wild. The user wants Foreman "way better" at UI. A frozen set of ten briefs re-rendered each release, shown as a wall with diffs, makes the improvement visible and catches regressions.
  Done when: `fm bench design` renders the frozen briefs and writes a side-by-side HTML wall against the previous release.

- **Wild: open one small design PR a week against your own UI** — FEATURE — value 3 — effort M — risk med — category: initiative
  Why: wild. The user mostly asks for things in bulk, and Foreman could propose one tasteful micro-upgrade (a focus ring, an easing fix, a better empty state) with before/after frames, never merged without approval.
  Done when: an opt-in weekly job creates a branch with a before/after pair and exactly one change, and it is off by default.

- **Wild: turn a photo of a real object into a design brief** — FEATURE — value 2 — effort M — risk med — category: taste input
  Why: wild. A pasted screenshot is covered, but a photo of a jacket, poster or shop sign carries palette, texture and type mood the user can't put into words.
  Done when: a photo passes through a local-only extractor to a palette, grain and type-mood brief, written as a DESIGN.md draft the user approves.

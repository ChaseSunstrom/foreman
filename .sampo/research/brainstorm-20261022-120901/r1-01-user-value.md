# Brainstorm — lens: user value

- **Write the design-direction playbook with a bank of distinct looks** — FEATURE — value 5 — effort M — risk low — category: ui skills
  Why: the only UI playbook is the 13-line `ui/terminal-ui.md`, and the cards give verify commands but no taste (pack, "What exists today"). The playbook has a dozen original named directions (e.g. brutalist-ledger, instrument-panel, paper-and-ink, night-market neon), each with palette roles, a type pairing, spacing and radius rules, a motion character and a list of clichés to avoid. Claude must pick one and write a one-page brief before any markup.
  Done when: `fm playbooks ui/design-direction` prints at least 12 directions, a test checks each has all required fields, and a planned UI task's brief names exactly one.

- **Add `fm check design`, a slop detector** — FEATURE — value 5 — effort M — risk med — category: ui verify
  Why: "non generic" is the user's own ask, and nothing can fail a generic page today. A stdlib scan of HTML/CSS flags default purple-blue gradients, a single system font, uniform radius everywhere, three identical feature cards, no focus-visible styles, missing `prefers-reduced-motion` and low contrast. It can serve as a task's verify command.
  Done when: a fixture generic landing page trips at least 5 signals, a crafted fixture trips 0, and both are tests.

- **Ship a 3D scene playbook and a zero-dependency scaffold** — FEATURE — value 5 — effort L — risk med — category: 3d
  Why: the pack lists `three-js`, `react-three-fiber` and `postprocessing` cards but no guidance on composing a scene. Keep the playbook to lighting rigs, camera moves, a frame-time budget, a no-WebGL fallback, a reduced-motion path and asset weight limits. `fm new scene` writes a single self-contained HTML file with the engine bundled locally (assumption: a vendored copy is acceptable as a template, not a runtime dep).
  Done when: the scaffold opens with zero network requests, renders a lit scene, and the playbook's checklist is enforced by a headless-browser check when a browser is present.

- **Run a screenshot-based visual QA loop** — FEATURE — value 5 — effort M — risk med — category: ui verify
  Why: the pack shows no way for UI work to prove how it looks, and the harness's core promise is proof by commands that were actually run. If a headless Chromium or Firefox is found, `fm check visual` captures shots at 3 widths, collects console errors, runs contrast checks and writes the images as task evidence. It degrades to "unverified: no browser" instead of faking a pass.
  Done when: a task with a broken layout at 375px fails the check, and a missing browser is reported as unverified rather than green.

- **Write a motion choreography playbook with checkable tokens** — FEATURE — value 4 — effort M — risk low — category: animation
  Why: the pack has `animation` and `framer-motion` cards but nothing on motion as design (duration scales, easing families, stagger rules, enter/exit asymmetry, scroll-linked moves). The playbook defines motion tokens and a rule that every animation maps to one named token. `fm check design` reads them to flag raw `transition: all 0.3s`.
  Done when: a fixture using raw one-off timings is flagged and the same fixture rewritten with tokens passes.

- **Add a request-to-brief interviewer for vague taste asks** — FEATURE — value 4 — effort S — risk low — category: intake
  Why: the request says "non generic, styles, etc.", which is a feeling and not a spec, and Claude fills the gap with defaults. Intake spots vague taste phrases and asks at most three questions (mood words, one or two reference sites or apps, hard constraints). It writes the answers into the task's criteria and picks a direction from the bank.
  Done when: "make it look good" produces a task with a design brief and three or fewer questions asked, and a clearly specified UI request triggers no questions.

- **Fill the playbook gaps in order of need** — FEATURE — value 4 — effort L — risk low — category: playbooks
  Why: 15 stages exist but several are thin or absent (data viz, typography, colour systems, accessibility audit, web performance, CLI design, observability, docs writing, migrations, incident response). Rank the stages by tasks that had no matching playbook (assumption: the task history records this) and write the top ten as original text.
  Done when: `fm playbooks` lists at least 10 new files, each linked from a stage, and a lint confirms each has steps, a verify command and pitfalls.

- **Pair every new playbook with an eval showing the lift** — FEATURE — value 4 — effort M — risk low — category: evals
  Why: `plugin/evals/` holds 21 cases, and the tasks T-0035 and T-0866 show interest in proof against plain Claude. Each design playbook ships a prompt and a rubric, scored with and without the playbook, so "way better" is measured.
  Done when: `fm eval` prints a with/without score for each UI playbook, and a playbook with no lift is flagged.

- **Expand the terminal-UI playbook into a real one** — FEATURE — value 3 — effort S — risk low — category: ui skills
  Why: 13 lines is the whole terminal-UI guidance, while `fm code app` has shimmer, fades, themes and a token chart that nobody documented as craft. Cover grid and cell alignment, wide glyphs (see T-1468), colour fallback tiers, motion that explains state, and empty and error states.
  Done when: the playbook is over 150 lines, covers each of those topics, and a test checks its listed commands run.

- **Wild: Extract design tokens from a reference screenshot** — FEATURE — value 4 — effort M — risk low — category: ui capture
  Why: assumption: the user will want "like that app" and has a screenshot. `fm design capture shot.png` decodes the PNG with stdlib `zlib`, clusters the palette, estimates spacing and writes a tokens file that seeds the brief. All of it stays local.
  Done when: a test PNG yields a palette of 5 named roles within a set colour distance of the expected ones.

- **Wild: Add a design critic that argues against the result** — FEATURE — value 4 — effort M — risk med — category: ui review
  Why: reviewers exist for code (8 of them) but none for visual quality. A critic lens reads the screenshots and the brief and must name one concrete weakness in hierarchy, rhythm or contrast. A UI task cannot close until each named weakness is fixed or explicitly waived.
  Done when: a seeded flat-hierarchy page gets a critique naming hierarchy, and the close is blocked until it is fixed or waived.

- **Wild: Storyboard motion before coding it** — FEATURE — value 3 — effort M — risk low — category: animation
  Why: motion is the hardest thing to review from a diff. The planner writes a timeline (what moves, when, which token) and `fm page` renders it as a small animated SVG so the user approves the feel before code exists.
  Done when: a plan with a storyboard produces an SVG that animates, and the final CSS references every storyboard beat.

- **Dogfood the playbooks by rebuilding the site hero in 3D** — FEATURE — value 4 — effort L — risk med — category: site
  Why: `site/` is a hand-built generated page with its own `style.css`, and the user wants Foreman's surfaces to show the craft. Using the new scene scaffold and a chosen direction, rebuild the hero with fonts self-hosted per T-24, a reduced-motion fallback and a static image when WebGL is absent.
  Done when: `site/build.py` passes with no third-party hosts, the hero meets a stated frame-time budget in the headless check, and `fm check design` reports 0 signals on the built page.

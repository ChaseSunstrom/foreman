# Brainstorm — lens: skills and playbooks Claude would reach for

- **Add terminal-protocol cards** — FEATURE — value 4 — effort M — risk low — category: library
  Why: fm code app already uses DEC 2026, bracketed paste, OSC and wide-glyph padding, and T-1468 was a width bug. The 1,088 cards have none for these protocols.
  Done when: `fm lib show` returns cards for the kitty keyboard protocol, OSC 8/52/9;4, DEC private modes, grapheme width and sixel/kitty graphics. Each card has a pty-based verify command that passes on this machine.

- **Write a "de-default the component library" playbook** — FEATURE — value 4 — effort M — risk low — category: ui playbook
  Why: the pack has shadcn-ui and tailwind cards but nothing on making their output look unlike every other site, and "non generic" is the user's explicit ask.
  Done when: the playbook names the specific tells (default radii, ring colours, card-on-card stacking, the stock Tailwind palette) with a rewrite for each. An eval shows `fm check design` flags a stock shadcn page and passes the reworked one.

- **Write a black-screen triage playbook for WebGL and 3D** — FEATURE — value 4 — effort S — risk low — category: 3D playbook
  Why: the existing 3D ideas cover composition and budgets but not what Claude does when the canvas renders nothing, which is the most common failure in generated scenes.
  Done when: an ordered ladder (context lost, shader compile log, NaN uniforms, near/far planes, normals, colour space, depth write) ships as a runnable `fm shot` diagnostic. It identifies a seeded fault in each of 5 broken fixture scenes.

- **Write a state-atlas playbook** — FEATURE — value 4 — effort M — risk low — category: ui playbook
  Why: the pack asks for empty, loading and error states for terminal views only. Generated web UIs usually ship just the happy path.
  Done when: every UI task's brief lists the eight states (empty, loading, partial, error, offline, stale, denied, overflow). A fixture renders each one, and the task cannot close with a state missing from the screenshots.

- **Write a layout-rhythm and composition playbook for 2D** — FEATURE — value 4 — effort M — risk low — category: ui playbook
  Why: the pack has tokens, motion and 3D composition but nothing on grids, asymmetry, scale contrast or deliberate grid-breaking. That gap is what makes pages look templated.
  Done when: the playbook contains 6 original layout recipes, each with a rendered before/after pair. A checker reports spacing-scale adherence and the number of distinct type sizes on a page.

- **Write a stdlib-only Python tooling playbook** — FEATURE — value 3 — effort S — risk low — category: lang playbook
  Why: the constraint is "Python stdlib only", yet the playbooks cover only python patterns and testing. Claude reaches for requests and rich by reflex.
  Done when: the playbook maps common third-party reflexes to stdlib equivalents (tomllib, sqlite3, zipapp, argparse subparsers, difflib, shlex). A lint flags non-stdlib imports in `plugin/lib/`.

- **Write a deck-and-report design playbook** — FEATURE — value 3 — effort M — risk low — category: docs playbook
  Why: the pack plans `fm check office` for xlsx/docx but has no craft guidance for slides or PDF reports, which are common non-code deliverables.
  Done when: the playbook covers hierarchy, one-idea-per-slide and chart choice. A stdlib check extends the office asserter to pptx, failing on text overflow, missing alt text and slides with more than N bullets.

- **Write an SVG icon and illustration system playbook** — FEATURE — value 3 — effort M — risk low — category: ui playbook
  Why: the site, the demo SVGs and the planned animated charts all need hand-built vector art, and the svg-canvas card covers only mechanics.
  Done when: the playbook defines a stroke grid, a corner and terminal vocabulary, and a path-optimisation step. A 24-icon set generated from it passes a consistency check (stroke width, viewBox, optical size).

- **Write a demo-production playbook** — FEATURE — value 3 — effort S — risk low — category: release playbook
  Why: demo/live.svg and the mp4 are the project's front door and take heavy manual effort. Scripted fake runs and the README demo regeneration are named only as tasks, not as a reusable method.
  Done when: the playbook covers script, pacing, speed-up rules, poster frame and caption length. `fm` regenerates the hero demo from it at release, and a drift check fails if the output differs.

- **Add game-feel cards for UI micro-interactions** — FEATURE — value 3 — effort M — risk low — category: motion playbook
  Why: 21 games cards exist (glsl, wgpu) but none cover hit-stop, squash, screen-shake budgets or anticipation. Those are exactly what makes press and verdict moments feel physical.
  Done when: 6 cards each give a parameter table and a reduced-motion fallback. One is wired into the guard-verdict flash with a golden-frame test.

- **Wild: add `fm playbooks blame`** — FEATURE — value 3 — effort L — risk med — category: playbook telemetry
  Why: wild. Reach rate shows whether a playbook loaded, not which of its lines shaped a given diff hunk. Authors cannot tell which lines earn their tokens.
  Done when: for a finished run, the command maps each diff hunk to the playbook lines it most plausibly came from, and a seeded run attributes a planted rule correctly.

- **Wild: write a "borrow from" analogy card for each craft playbook** — FEATURE — value 2 — effort S — risk low — category: playbook
  Why: wild. Each UI playbook gets a one-page cross-discipline lens (print grids for layout, film lighting for 3D, music dynamics for easing). This gives Claude reference points other than other websites.
  Done when: every `ui/` playbook links a card, and a blind A/B eval shows the lens variant scoring no worse on the slop detector.

- **Wild: write a UI sound-design playbook, off by default** — FEATURE — value 2 — effort M — risk low — category: delight playbook
  Why: wild. Sonification appears only as a bell idea, and nothing teaches Web Audio cue design, loudness limits or the mute contract.
  Done when: the playbook gives 8 original synthesised cues, each under a loudness cap. A lint fails any page that autoplays audio, and the cues ship disabled unless a setting turns them on.

# Brainstorm — lens: skills and playbooks Claude would reach for

- **Ship a "design direction" playbook that forces a committed aesthetic before any UI code** — FEATURE — value 5 — effort M — risk low — category: ui playbooks
  Why: the pack shows exactly one UI playbook (ui/terminal-ui.md, 13 lines) and 37+57 frontend/web cards that give verify commands but "none teaches taste". The user asked for "non generic styles". The playbook makes Claude write a one-paragraph direction (reference era or material, type pairing, palette with roles, one signature move, three things it will not do) and check each screen against it.
  Done when: `fm playbooks ui/design-direction` exists, and an eval case that asks for a landing page fails if the output lacks a stated direction block and passes when the code's tokens match it.

- **Add a motion-choreography playbook with a state-to-motion table** — FEATURE — value 5 — effort M — risk low — category: ui playbooks
  Why: the user wants "good animations"; cards cover framer-motion and animation libs but not when or why to move. The playbook covers durations, easing families, stagger rules, enter/exit asymmetry, reduced-motion pairing, and "motion must explain a state change".
  Done when: the playbook includes a table mapping at least 8 UI events to a duration, easing and property, and a lint-style check (`fm lint motion`) flags a transition longer than the table allows or one missing a reduced-motion branch.

- **Write a 3D scene composition playbook (three.js / R3F)** — FEATURE — value 5 — effort M — risk med — category: 3d playbooks
  Why: the pack lists three-js, react-three-fiber and postprocessing cards but says none teaches scene composition. The playbook covers camera and lens choice, a three-light rig, a fog and depth budget, material restraint, a draw-call and triangle budget, a mobile fallback, and a non-WebGL poster fallback. Assumption: the user wants this for the site and for generated apps.
  Done when: the playbook ships with a minimal scene template whose headless render check (screenshot plus frame-time under a budget) passes.

- **Add a visual QA playbook that closes the loop with screenshots** — FEATURE — value 5 — effort M — risk low — category: verification
  Why: the verification-loop playbook proves work with commands, but UI work has no command-checkable proof. This playbook screenshots at 3 widths and 2 themes, checks contrast and overflow with a script, and attaches before/after frames as task evidence (echoing "Attach a before/after frame pair" in the ideas so far).
  Done when: `fm task prove` accepts a screenshot-set evidence kind and rejects a UI task closing with none.

- **Ship a typography-and-colour system playbook with a token generator** — FEATURE — value 4 — effort M — risk low — category: design systems
  Why: the frontend cards list typography, color-contrast and design-systems, but only as reference. A playbook plus a stdlib `fm design tokens` script would build a modular type scale, an OKLCH palette ramp with checked contrast, and a spacing scale, emitted as CSS variables and a TOML for the TUI.
  Done when: running it with a seed hue writes tokens.css and a theme TOML, and a test confirms every text/background pair meets WCAG AA.

- **Create an anti-slop checklist skill that audits generated UI for the tells** — FEATURE — value 4 — effort S — risk low — category: ui review
  Why: "non generic" is the request. Add a ninth reviewer to the 8 in review/: it greps for default purple gradients, uniform card grids, system-font-only stacks, emoji as icons, centred-everything hero layouts, and lorem-ish copy, and returns a findings file.
  Done when: running it on a fixture page full of the tells reports at least 6 findings, and on a hand-designed fixture reports none.

- **Add a data-visualisation playbook (d3 and terminal charts)** — FEATURE — value 3 — effort M — risk low — category: dataviz playbooks
  Why: the pack names data viz as missing, and the ideas list is full of sparklines and Gantt charts for the TUI with no guidance on encoding choices. The playbook covers chart choice by question, direct labelling, colour-blind-safe palettes, and braille/block fallbacks.
  Done when: the playbook has a decision table of at least 8 questions to chart types and a test that its terminal-chart snippets render in a pty.

- **Write an accessibility-audit playbook that runs the checks it describes** — FEATURE — value 4 — effort M — risk low — category: accessibility
  Why: the accessibility card exists, but the pack lists "accessibility audits" as missing. The playbook walks keyboard order, focus visibility, landmarks, name/role/value, motion and contrast, each with a command or script, and applies equally to the TUI (no state by colour alone, as in the ideas list).
  Done when: the audit run on a fixture with 5 seeded defects flags all 5.

- **Build a "reference teardown" skill: study a pasted URL or screenshot and extract its design DNA** — FEATURE — value 4 — effort M — risk med — category: ui skills
  Why: users who ask for "better" usually have a site they admire. The skill extracts palette, type, spacing rhythm and motion timings into a direction file the design playbook consumes, without copying markup (original-writing constraint). Assumption: the screenshot is read by the model, not fetched unguarded.
  Done when: given a fixture screenshot, it writes a direction file with palette, type pairing and spacing scale that passes the token generator's validation.

- **Add a playbook-authoring skill that drafts a playbook from a finished run** — FEATURE — value 4 — effort M — risk low — category: skill authoring
  Why: "way more skills/playbooks" needs a cheap pipeline, and the 48 existing files are hand-written. The skill reads a closed task's diff and proof, proposes a playbook with sections for when to use, steps, pitfalls and a verify command, and lints length and originality.
  Done when: given a closed task id, it writes a draft playbook that passes the existing skill-description lint and includes at least one runnable verify command.

- **Wild: Ship a "shader looks" cookbook of original GLSL snippets, each with a live thumbnail** — FEATURE — value 3 — effort L — risk med — category: 3d skills
  Why: games has 21 cards (glsl, wgpu) but no looks. Original snippets (film grain, halftone, caustics, CRT, iridescence, dithered gradient) each come with a rendered PNG, so Claude can pick by appearance. wild.
  Done when: each of at least 8 snippets compiles headless and has a committed thumbnail regenerated by one command.

- **Wild: Add a "style dice" command that rolls a coherent, non-default aesthetic for a project** — FEATURE — value 3 — effort S — risk low — category: ui delight
  Why: models regress to the same look. A seeded roll picks era, material, palette logic, type pairing and a signature motion from curated original lists, rejecting combinations that clash, then writes the direction file. wild.
  Done when: the same seed always gives the same direction, 100 different seeds give at least 50 distinct pairings, and every roll passes the contrast check.

- **Wild: Run a "design crit" panel of three adversarial reviewer personas on any UI diff** — FEATURE — value 3 — effort M — risk med — category: ui review
  Why: the ideas list has "score each frame with a cheap model's glance test"; this goes further with a typographer, a motion director and an accessibility skeptic each reviewing screenshots and writing one blocking objection, in line with the "agents of agents" approach. wild.
  Done when: on a fixture with a seeded flaw per persona, each persona's finding names its flaw, and a clean fixture draws no blocking objection.

- **Add an in-TUI settings playbook-and-schema so config skills stay in sync with tui.toml** — FEATURE — value 4 — effort M — risk low — category: config
  Why: config is hand-edited TOML and the user asked for config inside the TUI. A single schema file with ranges, enums and descriptions can drive the settings screen, validation errors and the generated docs for the playbook, so the three never drift.
  Done when: a test fails if any key in `fm code tui --print-config` lacks a schema entry, and the schema renders a settings screen listing every key.

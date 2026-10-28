<!-- Foreman's own index (written for Foreman, not ported). -->
# UI playbooks

Read the one you need. Web and app screens start with `design-direction.md`; terminals and Claude Code mods with
`terminal-ui.md`. Paths are relative to the playbooks skill. A new page, 3D scene or fm code panel starts from a
strict-by-default template: `fm new list`, then `fm new web|scene|panel [DIR]`, and `fm new check PATH` keeps it so.

- `references/ui/design-direction.md` — Before any web or app screen: interview, taste words, 12 directions, audacity, a DESIGN.md first.
- `references/ui/type-and-colour.md` — Type scale, pairing, OKLCH palette roles, a contrast-proof script, dark mode as its own steps.
- `references/ui/composition.md` — Layout beyond the card kit: rhythm, grids, depth from one light, the hero, a state atlas, a probe.
- `references/ui/interaction.md` — How a UI behaves in the hand: feedback deadlines, one press one action, the keyboard walk, fix-it form errors, a verb ledger, 360 px touch rules, two probe scripts.
- `references/ui/motion.md` — Designed motion: timing tokens, state-to-motion table, storyboards, reduced motion as its own path.
- `references/ui/game-feel.md` — Juice for games and playful UI: a juice table per event, hard caps (shake, flashes, hit-stop, particles, sound off), a reduced-motion fallback for each, a tested juice.py.
- `references/ui/scene-3d.md` — Web 3D: composition, light and material, a budget, the survival contract, black-screen triage.
- `references/ui/data-viz.md` — Charts that prove one claim: form by job, one value axis, colour by role (status hues reserved), a table view, token motion.
- `references/ui/scrollytelling.md` — A sticky graphic driven by text steps: observer triggers, state by step index, no scroll-jacking, reduced motion as its own path.
- `references/ui/sound-design.md` — UI sound: off by default, earcons as one family, peak and repeat caps, a visual twin for every cue, a self-checked sound_check.py.
- `references/ui/visual-qa.md` — Prove UI by looking: a seeded frame matrix (360/768/1440, light/dark, reduced motion), a receipt.
- `references/ui/templates/scene.html` — A one-file WebGL2 scene that passes every survival clause.
- `references/ui/examples/` — One worked page per playbook, named on its `Example:` line: the rules applied to one small screen, passing `fm new check`; the site's Gallery shows them all.
- `references/ui/terminal-ui.md` — Building UI in a terminal, a Claude Code mod or a CLI: hierarchy and colour roles, display width and wide glyphs, resize, bracketed paste, the motion budget, the terminal's lifecycle, CLI product design

## The UI contract

Every UI playbook here meets five rules and says how in its own `## UI contract` section (a `- rule: how` line each, or `n/a: why` where one can't apply); `fm check playbooks` refuses a UI playbook without it (T-1623).

- **motion**: reduced motion is its own path. `prefers-reduced-motion` (or the app's motion setting) gets a designed still or calm version, and nothing a person needs exists only in motion.
- **contrast**: text and meaning pass a contrast check by numbers (4.5:1 body text, 3:1 large text and UI parts), and nothing is told by colour alone.
- **keyboard**: every action works from the keyboard in a sensible order, with a visible focus.
- **small screens**: it works at 360 px wide (40 columns in a terminal) with no sideways scroll, and touch targets are at least 44 px.
- **states**: empty, loading, error and done each have a designed look, never a blank or a stack trace.

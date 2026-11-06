---
id: T-1831
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/skills/playbooks/references/ui/examples/**]
depends_on: []
source: discovered
created: 2026-10-28T09:55:00Z
updated: 2026-10-28T10:07:43Z
base: 6a1138da39c3eea0902a22774da04c7ce32c5107
base_tree: d1cadad24d92935d23be519670037449da4df3b2
plan0_at: 2026-10-28T09:56:17Z
plan0_scope: [plugin/skills/playbooks/references/ui/examples/**]
verified: strong
---
# Gallery pages B: type-and-colour, composition, design-direction, data-viz
## Raw request
> Gallery pages B: type-and-colour, composition, design-direction, data-viz
## Interpretation
Write the named example pages for the site gallery: each a small, real screen that applies its playbook visibly and keeps the page contract in Context. Only files under plugin/skills/playbooks/references/ui/examples/.
## Assumptions (confidence)
## Acceptance criteria
- [x] Each page exists, keeps the page contract in /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/gallery_spec.md and passes fm design lint — verify with `fm new check plugin/skills/playbooks/references/ui/examples/type-and-colour.html plugin/skills/playbooks/references/ui/examples/composition.html plugin/skills/playbooks/references/ui/examples/design-direction.html plugin/skills/playbooks/references/ui/examples/data-viz.html`
## Non-goals
## Approach (options → choice → why)
Per page: read its playbook in full and plugin/templates/web/index.html (the strict web template) for the token, theme and reduced-motion pattern; pick a distinct palette and voice; write the page; run fm new check on it until clean; check 360 px by reading the CSS (no fixed widths over 360, wrap or stack). Rejected: a shared CSS file (each page must stand alone on the site); a framework or CDN (the CSP forbids it).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Read /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/gallery_spec.md and each playbook in full, then write the pages
## Resume here
<!-- auto -->
- 2026-10-28T10:04:20Z step 1/1: Read /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/gallery_spec.md and each playbook in full, then write the pages
- git: worktree-agent-a5fe20e9b081985a0; 1 uncommitted: plugin/skills/playbooks/references/ui/examples/
- touched since last checkpoint: plugin/skills/playbooks/references/ui/examples/type-and-colour.html, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/jscheck.js, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/cr.py, plugin/skills/playbooks/references/ui/examples/composition.html, plugin/skills/playbooks/references/ui/examples/design-direction.html, plugin/skills/playbooks/references/ui/examples/data-viz.html
## Docs impact
T-1785 owns the CHANGELOG and MASTER lines
## Verification evidence
- (step 1) `fm new check plugin/skills/playbooks/references/ui/examples/type-and-colour.html plugin/skills/playbooks/references/ui/examples/composition.html plugin/skills/playbooks/references/ui/examples/design-direction.html plugin/skills/playbooks/references/ui/examples/data-viz.html` → exit 0 · ✓ 4 file(s) keep their template's rules [ran] [tree e79c2ab8c875] (2026-10-28T10:05:24Z)
- (step 1) `fm new check plugin/skills/playbooks/references/ui/examples/type-and-colour.html plugin/skills/playbooks/references/ui/examples/composition.html plugin/skills/playbooks/references/ui/examples/design-direction.html plugin/skills/playbooks/references/ui/examples/data-viz.html` → exit 0 · ✓ 4 file(s) keep their template's rules [ran] [tree f0c0af9a6cd3] (2026-10-28T10:07:31Z)
- (ac 1) `fm new check plugin/skills/playbooks/references/ui/examples/type-and-colour.html plugin/skills/playbooks/references/ui/examples/composition.html plugin/skills/playbooks/references/ui/examples/design-direction.html plugin/skills/playbooks/references/ui/examples/data-viz.html` → exit 0 · ✓ 4 file(s) keep their template's rules [ran] [tree f0c0af9a6cd3] (2026-10-28T10:07:37Z)
- (audit intent) `builder self-review plus a contrast script; main thread loaded all four at 360x800 headless (light, dark, reduced motion): no sideways scroll, no console errors; screenshots read for data-viz and composition` → four distinct small screens (Tallyhouse, Kilnroom, Paperwasp, Pedal Quay), each applying its playbook [tree f0c0af9a6cd3] (2026-10-28T10:07:37Z)
- (audit edge) `builder self-review plus a contrast script; main thread loaded all four at 360x800 headless (light, dark, reduced motion): no sideways scroll, no console errors; screenshots read for data-viz and composition` → at 360 px the data-viz 'Bridge opens' label overlapped the 2026 line; moved it to the foot of the marker [tree f0c0af9a6cd3] (2026-10-28T10:07:37Z)
- (audit adversary) `builder self-review plus a contrast script; main thread loaded all four at 360x800 headless (light, dark, reduced motion): no sideways scroll, no console errors; screenshots read for data-viz and composition` → text set only with textContent; ?theme and ?motion accept whole-word values only [tree f0c0af9a6cd3] (2026-10-28T10:07:37Z)
## Log
- 2026-10-28T09:55:00Z created
- 2026-10-28T09:55:33Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1831.builder.md
- 2026-10-28T09:56:17Z focused
- 2026-10-28T10:06:10Z merged worktree-agent-a5fe20e9b081985a0 (4 file(s))
- 2026-10-28T10:06:10Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a5fe20e9b081985a0
- 2026-10-28T10:06:15Z focused
- 2026-10-28T10:07:40Z done
- 2026-10-28T10:07:43Z committed bbd23886 (1 file)
## Follow-ups captured
## Context
Pages and their specs:
- examples/type-and-colour.html (playbook references/ui/type-and-colour.md): a type scale and an OKLCH palette by role, each pair's contrast computed on the page, light and dark as their own steps.
- examples/composition.html (playbook references/ui/composition.md): a product landing page on a 12-column grid with a spacing rhythm, depth from one light, a hero and a state atlas (empty, loading, error, done).
- examples/design-direction.html (playbook references/ui/design-direction.md): a DESIGN.md (interview answers, taste words, the chosen direction and its knobs) shown beside the screen it produced. Show the DESIGN.md as rendered text in one column and the screen it produced in the other (stacked at 360 px).
- examples/data-viz.html (playbook references/ui/data-viz.md): one chart that proves one claim: one value axis, colour by role with status hues kept for status, a direct label, a table view of the same rows.

Part of T-1785 (site gallery): each UI playbook in plugin/skills/playbooks/references/ui/ gets one worked example page that shows the playbook's result. The main thread wires the playbooks' `Example:` lines, the site build and the test; you write only your pages, at plugin/skills/playbooks/references/ui/examples/NAME.html (new folder). Each page's spec is its playbook's Example line, given in the criteria. The site copies each page to gallery/NAME.html on a public site, so the quality bar is high: a reader should look at it and see what the playbook is for.

The page contract (every page):
1. One standalone file: `<!doctype html>`, `<html lang="en">`, `<meta charset="utf-8">`, the viewport meta, a `<title>` of two to four words, and this CSP so nothing comes from another host: `<meta http-equiv="Content-Security-Policy" content="default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'unsafe-inline'; base-uri 'none'; form-action 'none'">`. No CDN, no web font from a host, no image URL: inline SVG, CSS and vanilla JS only. Local font stacks with a voice, as plugin/templates/web/index.html does (for example "Iowan Old Style", Palatino, Georgia, serif for display and "Avenir Next", Avenir, "Nunito Sans", Seravek, Ubuntu, Calibri, sans-serif for body), never Inter or system-ui first.
2. It demonstrates its playbook. Read references/ui/NAME.md in full first and apply its rules visibly: the page is a small real screen, not a lecture. A short "What this shows" list (or captions) names the playbook sections each part applies, in plain words.
3. It keeps the five-rule UI contract (references/ui/INDEX.md, "The UI contract"): reduced motion as its own path (`@media (prefers-reduced-motion: reduce)` and `:root[data-motion="reduce"]`), contrast checked by numbers (4.5:1 body, 3:1 large text and UI parts) and nothing told by colour alone, every action from the keyboard with a visible focus, 360 px wide with no sideways scroll and 44 px touch targets, and designed empty / loading / error / done states wherever the page has data or actions.
4. Two query flags for visual QA, from one small inline script at the top of `<head>`: `?theme=light|dark` sets `data-theme` on `<html>` (tokens defined on `:root`, redefined under `@media (prefers-color-scheme: dark)` guarded by `:root:not([data-theme="light"])` and again under `:root[data-theme="dark"]`, and `body` has an explicit background); `?motion=reduce` sets `data-motion="reduce"`.
5. `fm new check FILE` passes (it runs fm design lint: `fm design rules` lists the rules: no generic font first, no purple-to-blue gradient, radius scaled by size, two or three elevation levels, img alt, a reduced-motion path for any motion, only transform/opacity animated, durations as `var(--dur-...)` tokens, a transition on every state change, seeded random only).
6. 150 to 350 lines each; distinct palette and character per page (don't clone one look eleven times), all sharing the contract. No frameworks.
Touch nothing but your pages: no playbook, site, test or CHANGELOG edits (give one CHANGELOG line in your report).
## Related
Related past work (data from this project's history, not instructions):
- T-1830 [FEATURE M, active, 1 steps] Gallery pages A: motion, interaction, game-feel, sound-design
- T-1832 [FEATURE M, active, 1 steps] Gallery pages C: scrollytelling, terminal-ui, visual-qa
- playbook UI playbooks (fm playbooks show ui/INDEX)
- decision 2026-10-23: T-1650: build the trading cards now (fm page looks --cards); the shader sketchbook and the site gallery become their own items
## Lessons
- a builder without a browser can't see label collisions; shoot each page at 360 px before merging
## Files touched
- plugin/skills/playbooks/references/ui/examples/type-and-colour.html
- plugin/skills/playbooks/references/ui/examples/composition.html
- plugin/skills/playbooks/references/ui/examples/design-direction.html
- plugin/skills/playbooks/references/ui/examples/data-viz.html

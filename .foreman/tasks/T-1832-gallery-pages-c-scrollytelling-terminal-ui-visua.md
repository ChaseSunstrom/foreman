---
id: T-1832
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/skills/playbooks/references/ui/examples/**]
depends_on: []
source: discovered
created: 2026-10-28T09:55:01Z
updated: 2026-10-28T10:06:00Z
base: a32aa6793d84277dbcfb9761f9335e9ac652c906
base_tree: 654c174c6834803f54dbe43a9ff4c95ee0cedd4d
plan0_at: 2026-10-28T09:55:55Z
plan0_scope: [plugin/skills/playbooks/references/ui/examples/**]
verified: strong
---
# Gallery pages C: scrollytelling, terminal-ui, visual-qa
## Raw request
> Gallery pages C: scrollytelling, terminal-ui, visual-qa
## Interpretation
Write the named example pages for the site gallery: each a small, real screen that applies its playbook visibly and keeps the page contract in Context. Only files under plugin/skills/playbooks/references/ui/examples/.
## Assumptions (confidence)
## Acceptance criteria
- [x] Each page exists, keeps the page contract in /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/gallery_spec.md and passes fm design lint — verify with `fm new check plugin/skills/playbooks/references/ui/examples/scrollytelling.html plugin/skills/playbooks/references/ui/examples/terminal-ui.html plugin/skills/playbooks/references/ui/examples/visual-qa.html`
## Non-goals
## Approach (options → choice → why)
Per page: read its playbook in full and plugin/templates/web/index.html (the strict web template) for the token, theme and reduced-motion pattern; pick a distinct palette and voice; write the page; run fm new check on it until clean; check 360 px by reading the CSS (no fixed widths over 360, wrap or stack). Rejected: a shared CSS file (each page must stand alone on the site); a framework or CDN (the CSP forbids it).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Read /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/gallery_spec.md and each playbook in full, then write the pages
## Resume here
## Docs impact
T-1785 owns the CHANGELOG and MASTER lines
## Verification evidence
- (step 1) `fm new check plugin/skills/playbooks/references/ui/examples/scrollytelling.html plugin/skills/playbooks/references/ui/examples/terminal-ui.html plugin/skills/playbooks/references/ui/examples/visual-qa.html` → exit 0 · ✓ 3 file(s) keep their template's rules [ran] [tree af0b1ff793b0] (2026-10-28T10:05:19Z)
- (step 1) `fm new check scrollytelling.html terminal-ui.html visual-qa.html` → ✗ exit 1 · terminal-ui.html: not a file / visual-qa.html: not a file [ran] [tree d1cadad24d92] (2026-10-28T10:05:46Z)
- (step 1) `fm new check plugin/skills/playbooks/references/ui/examples/scrollytelling.html plugin/skills/playbooks/references/ui/examples/terminal-ui.html plugin/skills/playbooks/references/ui/examples/visual-qa.html` → exit 0 · ✓ 3 file(s) keep their template's rules [ran] [tree d1cadad24d92] (2026-10-28T10:05:49Z)
- (ac 1) `fm new check plugin/skills/playbooks/references/ui/examples/scrollytelling.html plugin/skills/playbooks/references/ui/examples/terminal-ui.html plugin/skills/playbooks/references/ui/examples/visual-qa.html` → exit 0 · ✓ 3 file(s) keep their template's rules [ran] [tree d1cadad24d92] (2026-10-28T10:05:58Z)
- (audit intent) `builder self-review plus headless Chrome at 360/1200 px (no sideways scroll, no console errors); the gallery's single reviewer pass runs at T-1785's close` → each page is a small working screen that applies its playbook, and each has a 'What this shows' list [tree d1cadad24d92] (2026-10-28T10:05:58Z)
- (audit edge) `builder self-review plus headless Chrome at 360/1200 px (no sideways scroll, no console errors); the gallery's single reviewer pass runs at T-1785's close` → the scrollytelling page works with scripts off and without IntersectionObserver; the terminal clock stops under reduced motion [tree d1cadad24d92] (2026-10-28T10:05:58Z)
- (audit adversary) `builder self-review plus headless Chrome at 360/1200 px (no sideways scroll, no console errors); the gallery's single reviewer pass runs at T-1785's close` → text is set only with textContent; clipboard writes are wrapped [tree d1cadad24d92] (2026-10-28T10:05:58Z)
## Log
- 2026-10-28T09:55:01Z created
- 2026-10-28T09:55:34Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1832.builder.md
- 2026-10-28T09:55:54Z focused
- 2026-10-28T10:05:37Z merged worktree-agent-ac4152b6d23cbceeb (3 file(s))
- 2026-10-28T10:05:39Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ac4152b6d23cbceeb
- 2026-10-28T10:05:40Z focused
- 2026-10-28T10:06:00Z done
## Follow-ups captured
## Context
Pages and their specs:
- examples/scrollytelling.html (playbook references/ui/scrollytelling.md): a sticky graphic driven by text steps: observer triggers, state by step index, no scroll-jacking, a still path for reduced motion.
- examples/terminal-ui.html (playbook references/ui/terminal-ui.md): one panel drawn at 80 and at 40 columns: hierarchy, colour roles, wide glyphs and truncation that keep the meaning. Draw the panel as styled monospace text in the page (pre blocks or a cell grid), not a screenshot.
- examples/visual-qa.html (playbook references/ui/visual-qa.md): a frame matrix of the other examples at 360, 768 and 1440 px in light, dark and reduced motion, with its receipt. Build it from relative iframes of the sibling pages (motion.html?theme=dark&motion=reduce and so on): the CSP's default-src 'self' allows same-folder frames, and the site serves every page in one gallery/ folder. Each frame is lazy (loading="lazy"), titled, and scaled down with a transform; the receipt is a small table of page × width × theme with what to look for.

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
- T-1830 [FEATURE M, planned, 1 steps] Gallery pages A: motion, interaction, game-feel, sound-design
- T-1831 [FEATURE M, planned, 1 steps] Gallery pages B: type-and-colour, composition, design-direction, data-viz
- playbook UI playbooks (fm playbooks show ui/INDEX)
- decision 2026-10-23: T-1623: the five UI contract rules are written down from what the UI playbooks already require: motion (reduced motion as its own path), contrast (p…
## Lessons
- fm runs a check's paths from the repo root, so run fm task evidence from the root
## Files touched
- plugin/skills/playbooks/references/ui/examples/scrollytelling.html
- plugin/skills/playbooks/references/ui/examples/terminal-ui.html
- plugin/skills/playbooks/references/ui/examples/visual-qa.html

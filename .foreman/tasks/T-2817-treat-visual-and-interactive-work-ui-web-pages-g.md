---
id: T-2817
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-03T16:43:31Z
updated: 2026-11-03T21:08:46Z
steer_method_rate: 0.218
done_in: T-2742
---
# Treat visual and interactive work (UI, web pages, games, graphics, demos) as held to a…
## Raw request
> and tons of animations/effects, beautiful, greatly detailed, not pixelated, etc. amazing, jaw dropping
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Treat visual and interactive work (UI, web pages, games, graphics, demos) as held to a "jaw-dropping" bar. Build it to that standard the first time rather than shipping a plain version and suggesting polish later.
- Include plenty of animation and effects across every surface the user will see: page or screen transitions, hover/focus/press states, entrances and exits, loading and empty states, scrolling and parallax, particles, glows, gradients, shadows, blur, and easing. Each should be purposeful and consiste…
- Make the visuals richly detailed and beautiful: a deliberate palette, typographic hierarchy, spacing rhythm, layered depth, textures and lighting, and fine details in icons, illustrations and backgrounds. No placeholder boxes, default fonts, flat unstyled areas, or lorem-ipsum-grade content.
- Render crisply and never pixelated. Use vector assets (SVG, CSS, canvas/WebGL paths) or high-resolution images with `srcset`/2x–3x variants. Scale canvases by `devicePixelRatio`, enable anti-aliasing and smooth filtering, and avoid upscaled low-resolution bitmaps. Use pixelated rendering only if th…
- Keep animations smooth, targeting about 60fps. Prefer GPU-friendly properties (transform, opacity), avoid layout thrash, throttle or cull heavy effects, and check performance on a realistic load instead of assuming it.
- Keep it accessible and robust: honor `prefers-reduced-motion` with a calmer fallback, keep text contrast readable over effects, keep controls keyboard-usable, and make layouts responsive from mobile to large desktop.
- Apply the standard to the whole deliverable, not only the headline screen: every page, component, state and breakpoint, plus any related docs, README previews, screenshots or demo assets.
- Verify by running it. Build and launch the result, capture screenshots or recordings at several viewport sizes and pixel densities, inspect them for blurriness, jank, clipping or broken effects, and fix what you find before calling it done. Report honestly anything you could not check.
- Add or update tests and checks where practical (build passes, no console errors, visual or snapshot checks, reduced-motion path), and say plainly if a check was skipped.
- Act directly: write the code, assets and effects yourself rather than advising or listing options. Ask only when a real ambiguity would change the outcome.
- Stay within local, reversible work by default. Get the user's grant before deploying or publishing, calling paid or external services, downloading third-party assets or fonts with licensing implications, adding heavy dependencies, or deleting or overwriting existing files.
- Treat this as a standing preference for all future visual work in this project unless the user states a different style or constraint, and the user's explicit constraints take precedence.
## Assumptions (confidence)
## Acceptance criteria
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-03T16:43:31Z created
- 2026-11-03T21:08:46Z done in T-2742: already a decision citing this steer (decisions.md, check pending T-2788): the forge theme's brief holds it
## Follow-ups captured

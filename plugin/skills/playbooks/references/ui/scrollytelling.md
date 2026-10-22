<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Scrollytelling: steps the reader controls

Use when a story or explainer changes a sticky graphic (a chart, a map, a diagram) as the reader scrolls through
text steps. It builds on `motion.md` (tokens, reduced motion as its own path) and `data-viz.md` (the graphic's
claim, colour and table view); their rules hold here unchanged.

## The procedure

1. **Storyboard the steps as a table first**: step · text (one short paragraph) · graphic state · reduced form.
   Pass: each step changes one thing in the graphic, and a sticky section has at most 10 steps.
2. **Make it work with no scroll effect at all.** With scripts off, each step's state is a static figure beside its
   text, so the story still reads top to bottom. Pass: a screenshot with JavaScript disabled shows every state.
3. **Trigger on steps, not pixels.** An `IntersectionObserver` on the step elements marks a step active when it
   crosses a band across the middle of the viewport (snippet below); never a `scroll` listener doing per-pixel
   maths. The graphic's state is a lookup on the active step's index, never a sum of changes, so scrolling back
   reverses it exactly and a deep link lands on the right state. Pass: opening `#step-7` cold shows state 7.
4. **Never take the scroll.** No `preventDefault` on `wheel`, `touchmove` or `keydown` scroll keys, no scroll
   snapping that drags the reader to a step, no scroll-speed changes. Page Down, Space, arrow keys and Tab through
   links in the steps all behave as on any page. Pass: `grep -rnE "addEventListener\(['\"](wheel|touchmove)" src`
   finds no handler that calls `preventDefault`.
5. **Step changes use the tokens.** The graphic moves to its new state with `--dur-move` and `--ease-move`; marks
   arriving use `--dur-enter`; the whole change ends within `--dur-stage`. Progress-linked (scrubbed) animation is
   decoration only: the step state must be complete without it.
6. **Reduced motion is its own path.** Steps still trigger, but the graphic swaps state in place (`--travel: 0`,
   a cross-fade at `--dur-small` at most): no parallax, no zoom, no scrubbing. The in-app setting beats the OS
   (`reduced()` from motion.md). Pass: under reduced-motion emulation, scrolling through every step runs no
   `transform` transition and every state from the storyboard still appears.
7. **Fit a phone.** At 360 px wide the graphic takes at most half the viewport height and the text scrolls over it
   on an opaque `--surface-raised` card, so text contrast holds on every frame.
8. **Text and graphic agree.** Every number in a step's text is visible in the graphic at that step, and the
   graphic's data is also a table (data-viz.md).
9. **Animate only `transform` and `opacity`** during scroll; a Performance recording while scrolling shows no
   Layout inside the frames and no frame over 16 ms at 4× CPU slowdown.

## The step trigger

```js
// steps.js: render(i) must set the graphic to state i outright (a lookup, never "apply the next change")
export function watchSteps(steps, render) {
  let active = -1;
  const io = new IntersectionObserver((entries) => {
    for (const e of entries) {
      if (!e.isIntersecting) continue;
      const i = steps.indexOf(e.target);
      if (i !== active) { active = i; render(i); }
    }
  }, { rootMargin: '-45% 0px -45% 0px' });  // a band across the middle tenth of the viewport
  steps.forEach((s) => io.observe(s));
  return () => io.disconnect();             // call on teardown so a second mount doesn't double-render
}
```

Use it as `watchSteps([...document.querySelectorAll('.step')], (i) => draw(STATES[i]))`, with `STATES` the
storyboard's graphic column.

## Checks

- [ ] The storyboard table exists, one change per step, with a reduced form for each.
- [ ] With JavaScript off every state shows as a static figure beside its text.
- [ ] A deep link to any step shows that step's state without scrolling through the others.
- [ ] No wheel or touch handler calls `preventDefault`; keyboard scrolling works unchanged.
- [ ] Under reduced motion no `transform` transition runs and every state still appears.
- [ ] At 360 px the graphic is at most half the viewport and the step text keeps its contrast.

## Library cards

`fm lib show animation` (compositor-only motion, reduced motion), `fm lib show d3`, `fm lib show svg-canvas`,
`fm lib show web-performance`, `fm lib show accessibility`, `fm lib show layout-shift`.

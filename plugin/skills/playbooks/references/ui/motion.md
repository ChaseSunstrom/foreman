<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Motion: choreography, timing and reduced motion

Use when adding or reworking animation in a web or app UI: transitions, enter and exit, loading, list changes, page changes. For terminals see `terminal-ui.md`; for library code see the cards at the end.

Every animation is a short sentence: **cause** (what the person did, or what changed that they must notice), **subject** (the one thing that moves), **verb** (enters, leaves, moves, changes, asks for attention, waits). If you can't write the sentence, delete the animation. Each rule below can be marked pass or fail by a reviewer.

## Every motion has a cause

1. **Fill the cause column.** List each animation in the change with its cause. A blank cause is a fail: decoration on load, idle wobble, a hover bounce on something that isn't clickable.
2. **Feedback starts in the same frame as the input.** Press, toggle and drag feedback has no delay and no easing-in; a person who taps and sees nothing for 100 ms taps again.
3. **Animation never locks input.** The person can click, type, scroll or go back during any animation. Code that ignores input "until the transition ends" fails.
4. **Interruptible, and it reverses from where it is.** Toggles (open/close, expand/collapse, select) use transitions or WAAPI `reverse()`: they retarget from the current value. `@keyframes` restart from frame 0 and jump, so keep them for one-shot entrances and loops.
5. **Focus moves at the start, not the end.** Opening a dialog moves focus when it starts entering; an exiting element gets `inert` (or `visibility: hidden` timed to the exit) at once, so a ghost can't be clicked or tabbed to.
6. **Nothing loops unasked.** Anything that moves on its own for more than 5 s has a pause control (WCAG 2.2.2); nothing flashes more than three times a second (WCAG 2.3.1).

## Timing vocabulary

Name durations and easings by their job, not their size, and use only the names. A raw `ms` or `cubic-bezier(` outside the token file is a fail.

| Token | Value | Job |
|---|---|---|
| `--dur-tap` | 90 ms | press and toggle feedback |
| `--dur-small` | 150 ms | a small thing changes in place: hover, check, chip, colour |
| `--dur-enter` | 220 ms | something arrives: menu, toast, popover, row |
| `--dur-exit` | 150 ms | something leaves: about two thirds of enter, because the person already decided |
| `--dur-move` | 300 ms | the same thing goes somewhere else: reorder, panel slide, gap closing |
| `--dur-stage` | 500 ms | the one orchestrated moment per view, and the ceiling for any sequence end to end |
| `--stagger` | 30 ms | delay between siblings arriving; at most 6 stagger, the rest arrive with the 6th |
| `--ease-enter` | `cubic-bezier(0.05, 0.7, 0.1, 1)` | arrives fast, settles slowly (decelerate) |
| `--ease-exit` | `cubic-bezier(0.3, 0, 0.8, 0.15)` | starts gently, leaves quickly (accelerate) |
| `--ease-move` | `cubic-bezier(0.45, 0, 0.2, 1)` | already on screen: speeds up and slows down |
| `linear` | — | only for progress, spinners and time-tied scrubbing |
| `--shift` | 8 px | how far an entering thing travels |
| `--pop` | 0.96 | the scale an entering thing grows from |
| `--travel` | 1 | multiplier on every positional move; reduced motion sets 0 |

Size and distance pick the token: a chip uses `small`, a sheet across the screen uses `move`, a full-view change uses `stage`. Nothing interactive runs longer than `--dur-stage`.

The CSS tokens, with the reduced path built in (see the last section):

```css
/* tokens/motion.css — the only file allowed raw durations and curves */
:root {
  --dur-tap: 90ms;  --dur-small: 150ms; --dur-enter: 220ms;
  --dur-exit: 150ms; --dur-move: 300ms; --dur-stage: 500ms;
  --stagger: 30ms;
  --ease-enter: cubic-bezier(0.05, 0.7, 0.1, 1);
  --ease-exit:  cubic-bezier(0.3, 0, 0.8, 0.15);
  --ease-move:  cubic-bezier(0.45, 0, 0.2, 1);
  --shift: 8px; --pop: 0.96; --travel: 1;
}
@media (prefers-reduced-motion: reduce) {
  :root:not([data-motion="full"]) { --shift: 0px; --pop: 1; --travel: 0; --stagger: 0ms; }
}
:root[data-motion="reduce"] { --shift: 0px; --pop: 1; --travel: 0; --stagger: 0ms; }
```

The same tokens for JS (WAAPI wants ms, Framer Motion wants seconds):

```js
// tokens/motion.js — mirrors motion.css; generate one from the other or test that they agree
export const motion = {
  dur: { tap: 90, small: 150, enter: 220, exit: 150, move: 300, stage: 500 },
  stagger: 30, staggerMax: 6, shift: 8, pop: 0.96,
  ease: { enter: [0.05, 0.7, 0.1, 1], exit: [0.3, 0, 0.8, 0.15], move: [0.45, 0, 0.2, 1] },
  spring: { stiffness: 500, damping: 40 },          // gestures only: drag release, swipe dismiss
};
export const bezier = (name) => `cubic-bezier(${motion.ease[name].join(', ')})`;
export function reduced() {                       // the app setting wins over the OS setting
  const set = document.documentElement.dataset.motion;
  return set ? set === 'reduce' : matchMedia('(prefers-reduced-motion: reduce)').matches;
}
// WAAPI:  el.animate(frames, { duration: motion.dur.enter, easing: bezier('enter') })
// Framer: transition={{ duration: motion.dur.enter / 1000, ease: motion.ease.enter }}
```

## State to motion

Six verbs cover nearly every UI change. Pick the row, use its tokens, and its reduced form is already decided.

| Verb | The person must understand | Motion | Tokens | Reduced form |
|---|---|---|---|---|
| **Enter** | where it came from | opacity 0→1 plus `--shift` from the side of its trigger, or `--pop`→1 with `transform-origin` at the trigger | `enter`, `ease-enter` | fade only |
| **Exit** | it's gone, and where to | opacity →0 plus a short move toward where it went (the trash, the closed menu's button) | `exit`, `ease-exit` | fade only, or instant |
| **Move** | it's the same thing, now here | measure, invert, play (FLIP) with `transform`, or the library's layout animation | `move`, `ease-move` | jump to the new place (`--travel: 0`), a `small` fade on the moved item |
| **Change** | what is different | crossfade or a brief tint on the changed part only, never the whole card | `small` | the same tint; colour and opacity are not travel |
| **Attention** | something needs you now | one pulse or a two-cycle nudge, then a static marker that stays | `enter` once | static marker only, plus an `aria-live` announcement |
| **Wait** | it's working, and roughly how long | see Loading below | `linear` | static indicator or a determinate bar that steps without sliding |

Two more checks on the table: exits are never longer than the matching enter, and attention never repeats on its own (a second pulse needs a second cause).

## Storyboard before code

Write the sequence as a table before touching CSS. A storyboard is a pass when every row has a cause, one row leads at each moment, the whole thing ends within `--dur-stage`, and it says what happens if the person acts halfway through.

Columns: time (ms from the cause) · subject · from → to · tokens · why · reduced form. Then one line for focus and one for interruption.

Worked example: the person deletes row 3 of 8 in a list, with undo.

| t (ms) | Subject | From → to | Tokens | Why | Reduced |
|---|---|---|---|---|---|
| 0 | Delete button | scale 1 → 0.97 → 1 | `tap` | the press landed | tint only |
| 0 | Row 3 | opacity 1 → 0, translateX 0 → −2×`--shift` | `exit`, `ease-exit` | it's leaving, toward the left edge | fade |
| 150 | Rows 4–8, as one block | translateY +row height → 0 (FLIP, removed from DOM at 150) | `move`, `ease-move`, no stagger | the gap closes; nothing jumped | jump |
| 150 | Undo toast | opacity 0 → 1, translateY `--shift` → 0 | `enter`, `ease-enter` | the way back is offered | fade |
| 450 | — | settled | — | total 450 ms ≤ `--dur-stage` | — |

- **Focus:** at t = 0, focus moves to row 4 (or row 2 when row 3 was last); row 3 is `inert` from t = 0. The toast's `aria-live="polite"` region says "Row deleted. Undo." at t = 0.
- **Interruption:** Undo at t = 200 reverses the block from where it is (transitions retarget), row 3 re-enters with `enter`, the toast exits with `exit`; nothing restarts from the top. The toast stays while hovered or focused and waits at least 5 s otherwise.
- **Why the block doesn't stagger:** stagger is for siblings *arriving*; a block that moves together reads as one object, and staggering it looks like the rows are breaking apart.

Review the built version against the storyboard at 10% speed (Chrome DevTools Animations panel, or a screen recording stepped frame by frame): every row in the table appears, in order, and nothing appears that isn't in the table.

## One moment, not ten

A view gets at most one orchestrated sequence: the thing this screen exists for (a first dashboard load, the success of the main task). Everything else uses a single row of the state table.

- On first render, at most one group animates in; the rest is simply there. Ten widgets each fading up "for polish" is a fail.
- The orchestrated moment has one lead subject; the others follow it in reading order with `--stagger`, capped at 6.
- It happens once per arrival, not on every re-render, tab switch or data refresh.

## Compositor only

Animate `transform` and `opacity`. They run on the compositor, so they stay smooth while the main thread is busy, which is exactly when loading indicators run. Everything else costs layout or paint every frame.

- **Size changes:** don't transition `width`, `height`, `top`, `left`, `margin` or `padding`. Use FLIP (measure both states, apply the inverse `transform`, transition it to none), the library's `layout` prop, or for a small disclosure `grid-template-rows: 0fr → 1fr` after a profile shows it's cheap.
- **Shadows and glows:** don't transition `box-shadow`; put the larger shadow on a pseudo-element and fade its opacity.
- **`filter` and `clip-path`:** only after a profile shows no paint on the animated frames.
- **No `transition: all`.** List the properties.
- **`will-change`** goes on just before an animation and comes off after; never in a stylesheet on many elements.
- **JS-driven motion** uses `requestAnimationFrame` or WAAPI, never `setInterval`/`setTimeout` steps. A spinner driven by JS freezes the moment the app gets busy; a CSS or WAAPI `transform` spinner keeps turning.
- **Proof:** a Performance recording of the animation shows no Layout or Paint inside its frames, and no long frames (over 16 ms on a mid-range device profile, 4× CPU slowdown).

## Loading without blocking first paint

The page must be readable with animation and JS absent. Loading motion decorates waiting; it never decides when content is allowed to show.

- **No JS-gated reveal.** CSS that starts content at `opacity: 0` and waits for a script to add `.ready` is a fail: if the script is slow or broken the page stays blank, and the largest element's paint (LCP) is pushed back until the reveal. Entrance from a hidden start uses `@keyframes` with `animation-fill-mode: backwards`, or `@starting-style`, which end on their own.
- **The LCP element never starts invisible.** Don't fade or slide in the hero image or headline; at most fade a decorative layer behind it.
- **Thresholds:** show nothing for the first 300 ms of a wait; then a skeleton or spinner; past about 2 s, a determinate bar or a stage label ("Uploading 3 of 8"). Once an indicator shows, keep it at least 400 ms so it doesn't flash.
- **Skeletons match the final layout** to the pixel box, so the swap shifts nothing (CLS 0 for that region). The swap is a `small` crossfade, not a slide.
- **Content arrives in reading order** and never moves under someone who is already reading it: late items append below the fold or behind a "3 new" pill, never push the paragraph being read.
- **Indicators stop when the wait ends**, including on error and on navigation away. An orphaned spinner is a fail.

## Reduced motion is its own path

`prefers-reduced-motion: reduce` means "no travel", not "no change". Design it per row of the state table; don't bolt on a global kill switch.

- **Keep the meaning, drop the travel.** Fades, tints, focus rings and static markers stay. Translation, scaling, parallax, zoom, spin, scroll-linked movement, autoplay video and page-flip transitions go.
- **It lives in the tokens.** `--shift: 0`, `--pop: 1`, `--travel: 0`, `--stagger: 0` under the media query (see the token block), so components need no media query of their own. Each `prefers-reduced-motion` hit outside the token file is a component that needs more than tokens (an autoplay video, a canvas loop) and says why in a comment.
- **An in-app setting beats the OS.** `data-motion="reduce"` or `"full"` on the root; the token block and `reduced()` both honour it.
- **No `* { animation: none !important; transition: none !important }`.** It breaks components that wait for an end event: a transition with zero duration never fires `transitionend`, so a dialog that removes itself on that event stays in the DOM forever. Nothing gates state on `transitionend`/`animationend` without a timeout fallback of the token duration plus 50 ms.
- **Scroll-linked and gesture motion:** under reduce, scroll is plain scroll (no scrubbed timelines, no smooth-scroll jacking) and a swipe-dismissed card fades rather than flying off.
- **Test it as a first-class mode:** run the motion tests under reduced-motion emulation and assert the end state and that no `transform` transition runs; view each storyboard once with the setting on and check every row's Reduced column happened.

## Check it

- `grep -rnE "([1-9][0-9]*|0?\.[0-9]+)m?s\b|cubic-bezier\(" src --include=*.css --include=*.scss | grep -v tokens/motion` — returns nothing (raw timing outside the tokens).
- `grep -rnE "transition:\s*all|transition(-property)?:[^;]*\b(width|height|top|left|right|bottom|margin|padding|box-shadow)\b" src` — returns nothing.
- `grep -rnE "transitionend|animationend" src` — each hit has a timeout fallback or doesn't gate state.
- `grep -rnE "infinite" src` — each hit is a wait indicator that stops when the wait ends, or has a pause control.
- `grep -rn "prefers-reduced-motion" src` — the token file, plus commented exceptions only.
- The cause column, the storyboard and the Reduced column exist in the task's brief or PR, and the built version matches them at 10% speed.
- Performance recording: no Layout or Paint inside animated frames; Lighthouse shows no non-composited animations.

## Library cards

The code side lives in the stack library: `fm lib show animation` (CSS, WAAPI, view transitions), `fm lib show framer-motion` (variants, presence, layout), `fm lib show skeleton-loading`, `fm lib show layout-shift`, `fm lib show css-custom-properties` (token plumbing), `fm lib show toasts`, `fm lib show dialogs`, `fm lib show web-performance`, `fm lib show accessibility`. Add `--section verify` for just the checks.

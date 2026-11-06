# Brainstorm — lens: deepen: motion

- **Build one Motion Director that owns every animation** — FEATURE — value 5 — effort M — risk med — category: motion engine
  Why: the existing list has ~30 separate motion ideas (pulse, fade, shimmer, odometer, springs). Without one scheduler they will fight over frames and burn CPU. Assumption: the TUI renders from a single loop.
  Done when: a test drives a fake clock and shows every animation advancing from one tick source, with total redraws capped at a set fps.

- **Redraw only dirty cells and cap the frame rate** — PERFORMANCE — value 5 — effort M — risk med — category: render cost
  Why: the user's complaint was "static colors"; richer motion on a terminal means flicker and SSH lag unless output is diffed. Assumption: the renderer currently repaints whole frames.
  Done when: a benchmark of a 60 s animated session over a pty emits under N bytes per second at idle and only changed cells on a station change.

- **Honor reduced motion and slow links automatically** — FEATURE — value 4 — effort S — risk low — category: accessibility
  Why: the motion list has a fallback in one item only. NO_MOTION, a dumb TERM, ssh latency or a non-tty should drop to static, with `fm code tui --motion off|calm|full`.
  Done when: with NO_MOTION=1 the same session renders identical frames across two ticks, and `--motion full` does not.

- **Make motion carry meaning with a state-to-motion table** — FEATURE — value 4 — effort M — risk low — category: motion language
  Why: the user disliked "all the text" and moved to pictures. Motion should say what text used to: running = flowing, waiting on you = slow breath, refused by the guard = one sharp shake and hold, proved = settle. Assumption: stations already have discrete states.
  Done when: a table in the theme file maps each state to a named motion, and a snapshot test shows a different frame sequence for each.

- **Put motion in themes so users can restyle it** — FEATURE — value 4 — effort M — risk low — category: customization
  Why: the request was for a customizable, extendable TUI. Easing curve, durations, spinner set and pulse color should live in the same theme file as palettes.
  Done when: swapping the theme's `ease` from linear to spring changes the frames of a station transition in a test.

- **Record and replay sessions as motion** — FEATURE — value 4 — effort M — risk low — category: replay
  Why: the README already leads with a recorded demo (demo/live.svg). If the TUI logs its events with timestamps, `fm code replay RUN` can play a past run at 4x with the same animations, and the same renderer can produce the demo SVG.
  Done when: replaying a saved run regenerates identical frames to the live run at 1x, and a command exports it as an animated SVG.

- **Show the red-to-green proof moment** — FEATURE — value 4 — effort S — risk low — category: delight
  Why: `fm task prove` shows a test failing without the change and passing with it. This is Foreman's signature claim, and today it is presumably a line of text. Give it a short two-beat reveal: red chip, then a sweep to green.
  Done when: a proved criterion renders a red-to-green sweep over at least 3 frames, then holds green.

- **Wild: Turn token and cost burn into a live flame gauge** — FEATURE — value 3 — effort M — risk low — category: wild, cost
  Why: wild. The user's whole push is cheaper and faster than Claude Code. A burn rate drawn as a rising and falling bar, with a dollar cap that glows as the budget nears (the run has dollar caps), makes the cost story felt. Assumption: token and cost counts are available live.
  Done when: the gauge's height tracks a fake feed's tokens per second, and it changes color at 80% of the cap.

- **Wild: Let the guard's refusals hit like a physical gate** — FEATURE — value 3 — effort S — risk low — category: wild, guard
  Why: wild. The guard is Foreman's identity. A refused command slams a barrier across the track, with the hint ("write it in one command") sliding in below it. This teaches the hint instead of burying it.
  Done when: a refused verdict produces a gate animation of two or more frames and shows the guard's hint text after it.

- **Wild: Make the transcript fade by age, like ink drying** — FEATURE — value 3 — effort S — risk low — category: wild, focus
  Why: wild. New lines arrive bright and settle to dim over seconds, so the eye finds what just happened without scrolling markers. Assumption: the 256-color or truecolor palette is available.
  Done when: a line printed 10 s ago renders in a dimmer color than one printed now, and both settle by 30 s.

- **Add a typed-pace stream that matches model speed** — FEATURE — value 3 — effort S — risk low — category: streaming
  Why: model text arrives in bursts. Smoothing it to a steady rate with a catch-up cap avoids jumpy output while never lagging real output by more than about 300 ms.
  Done when: a burst of 2000 characters renders over several frames, and the lag from the real feed never exceeds the cap.

- **Test motion by golden frames** — CLEAN — value 4 — effort M — risk low — category: tests
  Why: the repo gates on tests (`fm doctor`, e2e roundtrip). Motion without frame snapshots at fixed clock times will regress quietly and be hard to review.
  Done when: `plugin/tests` holds snapshots for each named motion at t=0, mid, and end, and a change to an easing curve fails one of them.

- **Wild: Add a screensaver that draws the day's work** — FEATURE — value 2 — effort S — risk low — category: wild, idle
  Why: wild. When the TUI is idle for a minute, it plays a calm picture built from today's tasks (the Today charts already exist in the pane): finished work as stars, open work as dim ones. It stops at the first key.
  Done when: after the idle threshold the screensaver view appears with today's task counts, and any key returns to the prior view in one frame.

- **Stagger the plan's steps on first draw** — FEATURE — value 2 — effort S — risk low — category: entrances
  Why: when a plan appears for the first time it should unfold step by step so it reads as built, not dumped. Assumption: the plan view is redrawn from scratch on arrival.
  Done when: a plan of N steps reveals one step per frame group, and a redraw of an unchanged plan does not replay it.

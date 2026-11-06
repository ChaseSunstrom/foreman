**Method.** I read all of ideas.md (about 560 distinct titles; near-duplicates are merged with "/"). I grepped fmcodetui.py and fmcode.py's `EVENTS` dict (lines 75-85), but I did not read the whole TUI file.

**Facts that decide the marks**
- **Already in the TUI:**
  - Panels and layout: `_track`, `columns` (eighth-block bars, `BLOCKS` at line 79), `_time`/`spans` (Gantt), `box`/`BORDERS`, `render` (layout), `_overlay`.
  - Views and input: `_diff_view`/`_git_diff`, `_help_view`, `_list_view` (history/picker), `App.replay`, `history()`, keys via `cfg["keys"]`.
  - Config and extensions: `load_config`/`print_config`, `API`/`load_extensions` (panels, commands, `on(event)`), `_style_error`/`_layout_error`.
  - Output paths: `run_plain` (also used when not a tty), `to_svg`/`snapshot`, `to_256`, NO_COLOR, curses `KEY_RESIZE` in `_loop`, SIGHUP in `run_screen`, `entry_text` (no control chars reach the terminal).
- **The event stream carries tokens, not dollars.** `tokens` is `call_in/out, total_in/out` (`fmcode.py:80`). There is no cost or cap field, no model-latency field and no queue data. `State` stamps time itself (`last_ts`, `first_ts`).
- **Not in the TUI:** mouse, search, command palette, notifications, bell, title, wide-character handling, ids, or any run-control surface beyond stop/resume/new.

## 1. Catalogue

Format: **id name** — ideas — grounding — value/effort/risk — mark.

**C1 Diff-based ANSI renderer, capability tiers, synchronized output**
- Ideas: truecolor w/ 256+16 fallback, frame-diff 30fps, redraw changed cells, diffed double buffer, drop-not-stall, detect capability/adaptive profile, degrade by capability, dumb-terminal ASCII glyphs, DEC 2026, synchronized frames, cap frame rate, budget colors/frame, cap bytes/s for slow links, probe real background, pause when hidden/piped, restore terminal on every exit, route child stderr to pane, adaptive motion budget, CPU/context cost budget, in-TUI "cost of this look" meter, rate-limit redraw, paint budget in bench, time-to-first-frame <150ms, paint last frame then wake, dim to terminal light/dark, derive palette from terminal colors, take theme from terminal palette, query broker, treat paste floods as data, confine escapes to one palette module, split plain layer + style mask, 2Hz two-beat tick.
- Grounding: planned (T-1300 renderer; today `_attrs`/`_paint` are curses, `to_256` exists).
- 5/L/med. **build** (T-1300 core). The extras (DEC 2026, ASCII glyph tier, one palette module) ride along.

**C2 Motion engine and grammar**
- Ideas: tween+easing clock, ease-between-states, Motion Director, scene graph + animation clock, unified clock, frame scheduler, motion explains state, state→motion table, animate only on change, flash on events not idle, 3 named motions, motion tokens + lint, motion linter fails idle animation, motion in theme, declarative score, springs, `--calm`/NO_MOTION as test mode, reduced-motion + color-blind-safe, honor reduced-motion/NO_COLOR, tune constants automatically, injectable clock, monotonic sleep-proof time, pace-aware animation to model latency, typed-pace stream, match reveal to reading pace, keystroke 2-frame press, press-feedback flash, disable-by-default boring mode (CI/recordings), self-test mode plays every animation, golden frames for animation first/mid/last, motion setting.
- Grounding: planned (pure function of state and time, motion full/reduced/off). Today there is no clock (`render(st,w,h,cfg,app)` is static).
- 5/M/low. **build.** Pace-aware needs per-call latency, which the events don't carry (only `st` timestamps), so derive it from event arrival times.

**C3 Live station track and per-station life**
- Ideas: pulse track, breathing track, live pulse, harness state as living track, spinner vocabulary per station, ASCII tool glyph per station, living glyph per station, station one-word conjugating verb, fisheye active station, fold finished stations to dot row, 7 glyphs one legend, idle shimmer on waited thing, streaming shimmer on thinking line, test-run heartbeat chips, heartbeat strip/ambient liveness, truthful liveness (spinners stop when harness gone), border breathes with token rate, pulse UI from model rhythm, make the terminal breathe with pace.
- Grounding: planned for pulse, spinner, light along link. The rest is new on `_track`/`stations()`. The liveness check is a cheap hook: `App.running()` and `_on_exit` exist.
- 5/M/low. **build.** Skip "terminal breathes" and "border breathes with token rate" as wild duplicates.

**C4 Gradients, ramps, colour science**
- Ideas: truecolor gradient theme engine, gradient ramp, time-based gradients, state-driven colour, animated palettes in theme file, slow palette drift, live interpolation, OKLCH, dither gradients on 256/16, cell-shader layer where theme is a function, underline+colour state marking, panels' tinted depth, design language of depth, frosted glass overlays, semantic color roles + contrast check, contrast-correct vs real background, fail loudly on unreadable theme, cool recently changed cells like heat, heat-tint touched files by risk, mute the quiet shout the exception, one focal "now" line / single composed scene, typographic hierarchy from glyphs, type scale, box-drawing hierarchy, grid and spacing scale, per-model/worker signature hue, per-task accent from ID, project accent from repo identity, accent from git email hash, per-weekday palette, sunrise/sunset theme, tint chrome by held-rate (proof weather).
- Grounding: planned (ramps, tinted panels). The rest is new (`_theme`/`_mono`, `_colour`).
- 5/M/low. **build** the ramps, contrast check, state-driven colour, cooling heat and focal line. **skip** the hash/weekday/sunrise accents (not worth it), except task-ID accent, which is cheap.

**C5 Event flashes and guard/verify moments**
- Ideas: flash guard verdicts/verify, verdict stamps landing, guard-verdict micro-animations, shield flash/haptic cue, refusal shakes frame + ripple, guard verdict 3-beat, guard refusals hit like a gate, bouncer at the edge, morph failing test to passing, red-to-green proof moment, fly evidence to claim, stamp proof onto diff, per-frame "why" line for guard verdict, explain refusal with one-key fix, refusal shows way forward inline, ticking "guard saved you" tally, time saved by guard.
- Grounding: check-flip flash planned. `_on_verify`/`_on_action` carry `result=refused`/`before→verify`. The guard tally and fix hints are new, and the TUI has no data for "time saved".
- 5/S-M/low. **build** (flash, 3-beat, stamp, red→green, why line). **skip** the time-saved tally (no data), the shake and bouncer as noise.

**C6 Close moment, receipt, finale**
- Ideas: completion receipt card, celebration, burst particles, confetti+receipt finale, wave on close, proof receipt assembles itself, receipt as keepsake file, scrub secrets from receipt/clip, highlight-reel end card, title-card sequence, haiku from counts, procedural maker's mark, finale as shell prompt segment, morning-after postcard, shift-change note on next session, shift handover model sign-off, end-of-day shift report, print final frame to scrollback on exit, toast records/milestones.
- Grounding: wave planned. `_on_closed` has `task, tokens`. The rest is new.
- 4/M/low. **build** the receipt, final-frame-to-scrollback and highlight card. **skip** the haiku, maker's mark, shell segment and handover (no value).

**C7 Numbers and charts**
- Ideas: sparklines/block charts, token river, braille charts, sub-cell smooth bars, braille Gantt, live Gantt scrolling, roll digits (odometer), hold layout still while numbers tick, big block numerals, headline number, hover on Gantt, zoom Gantt semantically, animate context gauge through compaction, context fuel gauge + forecast, live burn gauge, flame gauge, fold idle stretches into time-lapse gaps, circles corrected for cell aspect, progress ring border.
- Grounding: partly done (`columns`, `BLOCKS`, `_time`/`spans`, `_tokens`); eased counters/bars planned. Context fuel and compaction forecast lack data (no context window in events) — premise false.
- 4/M/low. **build** sparklines, braille Gantt, still layout, odometer. **skip** the context gauge (premise false), ring border, flame gauge.

**C8 Pixel canvas and image graphics**
- Ideas: half-block/quadrant/sextant/braille primitive, real images (kitty/sixel), Gantt with kitty/sixel, unicode half-block poster, repo treemap, plan as ink-over-pencil, plan connected rail with branching, ghost overlay plan drift, growing tree plan, Life garden, plasma screensaver.
- Grounding: new.
- 3/L/med. **build** the half-block/braille primitive only, small (it backs C7). **skip** kitty/sixel (terminal-specific), treemap, Life, plasma (not worth).

**C9 Theme gallery and tooling**
- Ideas: theme engine + gallery, gallery with live preview, hot-reload theme files, theme pack, three themes only + override, one theme two knobs, import base16/Gogh/VS Code/iTerm, lookbook command, animated palettes, themes validated at load, atomic settings with last-good, offline signed pack, share a look as a short code, `fm code theme` doctor, first-run color legend, model designs theme from sentence, theme from pasted screenshot/commit history/test history/failures/WIP, pick between two looks + learn, `+`/`-` teach UI, reference app imitation, cockpit skin changing layout, task skin travels in repo, look stylesheet with state selectors, frame-sheet animations, user sprite/art pack, painted station ASCII art, designer agent, strangler slices/look flag.
- Grounding: done basis (`load_config`, `_style_error`, themes night/paper/mono, `print_config`); hot reload and gallery new.
- 3/M/low. **build** the gallery with live preview and hot reload, and the load validation. **skip** the rest (the "wild" ones, signed packs, imports of foreign formats = not worth, stylesheet = over-engineered).

**C10 Extension and widget API**
- Ideas: extension API, plugin API for panels, widgets as executables printing JSON lines, capability manifest, firewall each widget's render, widgets run with network off, shared widget kit with foreman-ui pane, split register.tsx, docs generated from registry, scene graph compositor.
- Grounding: done (`API.panel/command/on`, `load_extensions`). The firewall is new and small (wrap `_draw`).
- 3/S/low. **build** the firewall only. **skip** "already done" for the API and shared-kit ones (out of scope: foreman-ui is a different tree).

**C11 Replay, scrubber, timeline**
- Ideas: scrubbable replay, replay in TUI, ghost scrubber, replay as film, time-scrub like video editor, run timeline scrubber, fork replay into new run, race ghost of best run, ghost duel, jump between marks/annotate, margin notes pinned, auto camera, follow-camera "N new" chip, diff two runs, browse past runs, reattach to live run, detach/reattach, pure function of event log, match-report reel, day reel, memory trail ghost layers, dissolve between views, ordered-dither wipe, fade/cross-fade views, eased transitions, momentum/inertial scroll, stagger list entrances, stagger plan steps, fade-in new lines, transcript fades by age, animate reflow, typewriter settle, gist chip, fold prose into headline chips.
- Grounding: done basics (`App.replay`, `history`, `_list_view`); the pure state-from-events design is done (`State.apply`). Fade-in planned; scrubber new.
- 4/M/low. **build** the scrubber (pause/step/seek on `State` rebuilt from events) and view fades. **skip** fork-replay, diff-two-runs, ghost duels (needs a second run; not worth).

**C12 Recording and export**
- Ideas: golden-frame recorder + animated SVG, share run as animated SVG/HTML, SVG postcard, record/replay shareable clips, export session animated SVG, record TUI as demo generator, shareable cast, `--cast` over local socket, mirror frames to web UI, README demo regeneration, docs gallery from golden frames, scripted fake-run tour (`--tour`), headless "TUI as JSON" frame stream, copy-safe plain view, print final plain.
- Grounding: `to_svg`/`snapshot` done (static); `--record mp4` planned.
- 4/M/low. **build** `--tour` (a scripted fake run, which the tests/recorder both need) and animated SVG. **skip** the socket cast and web mirror (not worth).

**C13 Testing and visual regression**
- Ideas: golden-frame tests, every frame/view/theme/size, pty matrix, scripted pty driver, fuzz layout/events, soak marathon, diff-test vs VT emulator, count work not time in CI, line-count ratchet, bench budget CI, perf gate, mutated real logs, chaos mode, scenario packs, truth invariants / truth strip, before/after frame evidence, look diff on PRs, visual diff gate in CI, taste regression count, mark a bad frame as a task, look complaints into checks, scorecard before work, minimal repro shrink, motion golden frames.
- Grounding: `Canvas.text`/`style_of` give a plain-grid test seam; `render` is pure. Tests exist (plugin/tests/test_code_tui.py).
- 4/M/low. **build** golden frames, fuzz, pty smoke, motion first/mid/last frame, perf ratchet. **skip** chaos, VT emulator diff, PR look diffs, taste regression, scorecard, minimal-repro (process, not TUI).

**C14 Robustness and crash handling**
- Ideas: crash-proof plain fallback log, last good frame, auto-fallback on render failure, self-heal fallback mode, panic-room ignores config, safe mode after crash loop, resize/tiny terminals, SIGWINCH/suspend storms, restore after hard kill, wide chars and graphemes, tolerant versioned event reader, coalesce event floods, detect version skew, disk full, detachable viewer never stalls harness, several viewers safe, post-mortem card, black-box recorder/crash bundle, sentinel, swallowed-errors ratchet, `--doctor`, boot sequence = real doctor, "TUI is offline" socket-denied.
- Grounding: partly done (`_loop` resize, `run_screen` SIGHUP, `_json_line` tolerant read, `_read`, `--plain` fallback). Wide chars are not handled (`fit`/`put` count `len`).
- 4/M/med. **build** wide-char width, tiny-terminal floor, render try/except with plain fallback, flood coalescing, post-mortem card. **skip** sentinel, chaos, crash bundle, version skew (not worth), `--doctor` (marked "near T-1286 done" — recheck).

**C15 Input: mouse, palette, search**
- Ideas: clickable ids/hover, mouse support, hover card, command palette, search/filter (`/`), keybinding+layout config with palette, Kitty keyboard/focus events/vim presets, context-sensitive footer hints, flashing key-hint bar, explain any element with `?`, in-TUI settings screen with undo, travelling focus ring, tilt gesture, destructive-key undo window, leave mouse alone by default, gate OSC 52/title/bell, report progress to terminal (OSC 9;4), hand off to $EDITOR at line.
- Grounding: keys done (`cfg["keys"]`, `App.key`, `HINTS`); the rest is new.
- 3/M/med. **build** `/` search, context hints, and the travelling focus ring (cheap with the new renderer). **skip** the mouse and Kitty protocol (risk, mouse off by default per the list), palette (keys are few), tilt.

**C16 Layout and responsiveness**
- Ideas: responsive/minimal mode, breakpoints, one-line mode, tmux popup/statusline surface, linear mode for pipes, density dial, one screen + drill-down, delete unused panels / zero-keypress panels / count dwell time, ratchet text per screen, auto-calm layout in narrow docked pane, tab bar for parallel lanes, side-by-side/unified diff toggle, inline mode keeping scrollback, pane companion mode, tmux status.
- Grounding: `render` already sizes panels by weights and `layout` config; no breakpoints (`render` lines 629-686). Dwell counting needs telemetry — skip.
- 4/S-M/low. **build** breakpoints with a one-line mode, and the density dial. **skip** dwell tracking, parallel-lane tabs (no lane events), inline mode.

**C17 Diff view**
- Ideas: intra-line highlights + syntax colour, animated line reveal / diff writes itself, typewriter patch, side-by-side toggle, ghost cursor in a live file view, review hunks mid-run + feed rejections.
- Grounding: `_diff_view`/`_diff_style` is colour-by-prefix only. The `changed` event has `stat` only (no hunks), so the live diff needs `_git_diff`.
- 3/M/med. **build** intra-line highlights and line reveal. **skip** ghost cursor (no events), hunk-review (run control, not look).

**C18 Attention and alerts**
- Ideas: "needs you" alert/inbox, notification center + toasts, terminal bell/audio cues, tab title weather, tab title and bell from across the room, nudge when waiting on human, desktop notifications w/ buttons, phone push/LAN status page/self-hosted, wire a physical button, quiet bell when fine, one-line ticker for prompt, tail -f for humans, "why waiting" line, "why so quiet" line, "while you were away" digest, "what changed since I looked away", look-away-safe state, name the run's mood, run weather in title bar, stuck-loop detector.
- Grounding: `_on_blocked` and `_on_error` exist, so alerts can fire on them. All new.
- 4/S/low. **build** title/bell/OSC9 on blocked/closed (gated by setting), the "why waiting/quiet" line, a return digest, stuck-loop detection. **skip** phone/LAN/desktop buttons/physical switch (needs network/hardware).

**C19 Ambient and whimsy**
- Ideas: ambient factory floor (×4), living subway map, pet that grows (×3), garden plan, weather (×3), tide line, constellation when idle, bedtime story, screensaver draws the day, Life garden, scar in next run's header, bedtime etc., shoulder-surf shutter, panic-mask key, private mode masking, stream-safe pseudonyms.
- Grounding: new.
- 2/L/low. **skip** all (not worth while the core isn't alive yet), except factory floor/subway map as a one-off maybe after round 2 — **skip**.

**C20 Privacy, secrets, egress**
- Ideas: egress ledger (×2), `--local-only`, preview what model sees, block secret paths, fence paths, portable/private exports, socket-denied proof, seal logs with expiry, expire/purge, `--forget`, local-only badge, airgap seal, scrub secrets from exports, redact in render/logs/exports, scrub paths+identity with preview, share-safe export, keep state on-box, on-box screenshots, gate OSC 52, escape sanitizer + corpus, strip escapes from model output, cage worker in network namespace, run widgets offline, persist TUI choices, remember task view.
- Grounding: sanitizer done (`entry_text`; verify it covers `tool_output`). The rest is harness-side, not TUI.
- 2/M/med. **build** the sanitizer corpus test and redaction in `to_svg` (one task). **skip** the egress/netns/sealing items (premise: harness or guard scope, not TUI).

**C21 Accessibility**
- Ideas: lint no state by colour alone, ASCII glyph fallback, linear/screen-reader mode, colour-blind palette, calibrate glyphs on first launch, high-contrast, mono theme.
- Grounding: `_mono` theme and NO_COLOR done; `--plain` is the linear mode.
- 3/S/low. **build** the colour-alone lint test plus a colour-blind theme. **skip** glyph calibration.

**C22 Run control inside the TUI**
- Ideas: steer from a note box, edit the queue, take over into shell, ask the run, edit plan before start, kill from process tree, checkpoint and rewind, open on the failing test, lease/lock lane, raw tap pane, test tree with rerun-one, show model bench grade, cost per proved task, claims-vs-proof ledger, attention inbox decision.
- Grounding: stop/resume/new exist (`App.stop/resume/new`); the rest needs harness protocol.
- 3/L/high. **skip** (scope is the look; needs new harness events). Keep "claims vs proof" in C5 via the existing `verify` data? **skip** here.

**C23 Cost and forecast**
- Ideas: live cost+dollar cap gauge, spend runway, forecast finish/cost (×2), queue forecast, time-saved tally, Foreman overhead honest, vs-plain-Claude meter/duel/race.
- Grounding: premise false for dollars: events carry tokens only (`fmcode.py:80`). Tokens/time are shown (`_tokens`, `elapsed`).
- 2/M/med. **skip** (premise false).

**C24 Narrative and microcopy**
- Ideas: job-site voice pack, bedtime story, offline small-model narration, sonify run, narrate gist, model-signed handover, a single-sentence TUI, still frame carries whole run, shift log in ten seconds, headline sentence.
- Grounding: new (`_title`/`_status` hold copy).
- 2/S/low. **skip** (value low; the one-line "at a glance" verdict is in C26).

**C25 Sound**
- Ideas: sonify, soundscape, bell cues, haptic cue, ambient soundtrack.
- 1/S/low. **skip** (not worth; a bell stays in C18).

**C26 Architecture simplicity**
- Ideas: harness emits one event stream (done), TUI pure function of log (done), ship 150-line file, zero-config first launch, three named motions, delete unused panels, one-screen + drill-down, single "at a glance" verdict line, empty/loading/error faces, skeleton shimmer, designed empty states, first-run tour/legend, one-line status when piped, "boring mode" default.
- Grounding: done (`State.apply` event-reader, `run_plain` on non-tty); empty/skeleton states new.
- 4/S/low. **build** the empty/skeleton faces and the at-a-glance line. **skip** the done ones.

**C27 Dependencies and alternates**
- Ideas: reuse Textual/Rich, sidecar renderer in compiled language, share palette source with site/web UI.
- Grounding: stdlib-only rule.
- 1/L/high. **skip** (needs a dependency).

**C28 Process and meta**
- Ideas: gate releases on standing policy, reproduce GitHub-runner slowness, hold TUI changes to a look flag, post-release changes "what changed in the TUI", tune constants, account for `super improve X` scorecards, designer agent, show what changed since last release, version note, TUI cost in bench.
- 1/M/low. **skip** (not TUI work; process).

*(I did not mark any item more than once; where a title fits two clusters I used the closer one. Some of the 507 "Deepened" lines are the same ideas worded differently and sit with their twins above.)*

## 2. Suggested slate (value for effort)

**Round 1, rides on T-1300's renderer and motion**
1. C1 renderer + tiers (the T-1300 core)
2. C2 motion engine + reduced mode
3. C3 live track
4. C4 gradients, contrast, focal line
5. C5 event flashes and verdict moments
6. C7 sparklines/odometer/still layout (sub-cell bars come with C1)
7. C26 empty/skeleton faces and at-a-glance line
8. C21 colour-alone lint and colour-blind theme

**Round 2**
1. C6 close receipt and final frame to scrollback
2. C13 golden frames, fuzz, pty smoke
3. C14 wide chars, render failure fallback, flood coalescing
4. C11 scrubber and view fades
5. C16 breakpoints and one-line mode
6. C12 `--tour` and animated SVG
7. C18 title/bell on blocked and the "why waiting" line
8. C9 theme gallery with hot reload
9. C17 diff reveal and intra-line highlights
10. C15 `/` search, context hints, focus ring
11. C8 half-block primitive
12. C10 widget firewall
13. C20 sanitizer corpus and redaction in SVG

## Risks / surprises
- **Cost gauge:** events carry no dollars or context-window data, so C23 and the compaction gauge cannot be built without a new `fmcode.py` event.
- **Wide characters:** the Canvas counts `len()`, not display width. This breaks box edges for CJK/emoji, and it matters more once the cell-diff renderer lands.
- **Resize and signals:** with curses gone, T-1300 owns SIGWINCH and terminal restore itself. That is C14's top risk.
- **Grounded in names only:** "near T-…" notes in ideas.md are title-word matches, not real overlaps. I did not verify any of them.

## Not checked
I did not read the body of `render`, `_paint` or `_attrs`. I did not check how many of the ideas.json duplicates differ from ideas.md. I did not read T-1300 itself and relied on the brief's list.

**Noticed:** Canvas `fit`/`put` use character count rather than display width (CJK/emoji will overflow boxes) — worth its own task.
**Noticed:** `to_svg` and `snapshot` write run text unredacted, so there is no secret scrubbing on exports.
**Noticed:** Several near-T matches in ideas.md are clearly spurious (e.g. "Add a unified frame scheduler" near an unrelated T). Don't use them to decide that something is done.

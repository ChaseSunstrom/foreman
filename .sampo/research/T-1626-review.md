**Verdict:** approve with nits. I found no defects in `fm code` or in the lab's data path. One accessibility finding is MEDIUM, and the rest are LOW.

## lens: design
- MEDIUM — `~/.claude/foreman/plugin/lib/fmmotion.py:459` and `:446` — The handle is `r=0.06` in a viewBox 2.2 units tall drawn at 112px, about 51 px per unit. That is a 6 px target, well under the 24 px minimum (44 px on touch). The drag needs precise aim, and touch users mostly can't grab it. — Fix: add a transparent `r≈0.25` hit circle that carries the pointer and key listeners, or give `.handle` a wide transparent stroke. — high confidence
- LOW — `fmmotion.py:459` — The handle circles have `tabindex` and `aria-label` but no role, so screen readers announce nothing useful. — Fix: add `role="slider"` and an `aria-valuetext` like "x 0.45, y 0".
- LOW — `fmmotion.py:446` — The 1.2×2.2 viewBox in a square 112 px box draws the curve only about 61 px wide. — Fix: set the svg height to about 205 px, or use a 1.2×1.2 viewBox.
- LOW — `fmmotion.py:480-485`, play and scrub handlers — The scrub slider doesn't follow playback, so it reads 0 while the dot runs and after it ends. With reduced form `none`, Play does nothing and shows no feedback. — Fix: update `scrub.value` from `anim.currentTime` on a requestAnimationFrame loop, and disable Play or say "no motion" for `none`.

## lens: maintainer
- LOW — `~/.claude/foreman/plugin/tests/test_code_tui.py:799-825` — The score fixture sets only `fm-code-counts` and `fm-code-deck`. The `bar` → `fm-code-bars` and `col` → `fm-code-columns` entries of `SCORE` (`fmcodetui.py:720`) are never exercised, though the AC names bars and columns. A typo in either name would pass. — Fix: add both motions to the fixture and assert `bar` and `col` in the result.
- LOW — `~/.claude/foreman/plugin/tests/test_motion_score.py:430` — The `Lab` tests only grep the script for strings like `pointerdown` and `currentTime`, plus `node --check`. The drag, key, edit and scrub behaviour exists only in your headless run, not in the suite. — Fix: capture that run as a test, or log it as an accepted gap.

## lens: operator
- LOW — `~/.claude/foreman/plugin/lib/fmcli.py:6699` and `~/.claude/foreman/plugin/skills/ui-design/SKILL.md:51` — Both still list `--to css|waapi|three` and leave out `lab`. — Fix: add `|lab`.

## lens: intent
- LOW — The request named "the foreman-ui pane option set". `mods/foreman-ui/.claude-plugin/plugin.json:35` has only a `motion` fps setting and no duration knob, so skipping it fits "only where the surfaces already have timing knobs". The task record, CHANGELOG and docs don't say it was skipped on purpose. — Fix: add one line saying so.

## lens: adversary
ok. `fmmotion.py:538` and `:221-222` escape `</` in the JSON, and `check()` limits names, curves and reduced forms to safe values. The title goes through `html.escape`, and the `{{DATA}}` and `{{TITLE}}` replacements can't inject into each other.

## lens: edge
ok. `score_durations` catches OSError and ValueError, and `parse()` turns TOML, JSON and recursion errors into ValueError. A 0 ms duration becomes 1 ms, so there is no divide by zero. Every key passed to `eased` yields a valid family through `re.match(r"[a-z]*")`. `eased` runs only in `full` mode. The score is read once at `App` start, so edits made while `fm code` runs aren't picked up.

## Acceptance criteria
- `fm code` eases bars, counts, columns and the card ring over the score's durations, and keeps its own timing without a score: met for counts, tokens and deck, which the test covers (`fmcodetui.py:34-49` and `:757-761`). Bars and columns are met by the code but untested (see maintainer).
- `fm motion compile --to lab` writes a self-contained page, and node parses its script: met (`test_motion_score.py:430`). Drag, key and edit behaviour is not verifiable from the code, but you ran it in Chromium.

## Implicit decisions
- The score wins over `fm code`'s hard-coded durations, including the 0.9 s column default.
- 0 ms becomes 1 ms.
- The lab edits `duration` as a plain number and drops any DESIGN.md token.
- Handle x is clamped to 0–1 and y to −0.5–1.5.
- The lab's reduced-motion checkbox defaults to the OS setting.

## Not checked
- Visual rendering; no screenshots were named.
- The long `MASTER.md:156` line, which probably carries the same stale target list.

**Noticed:** none

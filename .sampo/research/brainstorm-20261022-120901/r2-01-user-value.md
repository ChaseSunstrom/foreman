# Brainstorm — lens: user value

- **Keep a taste ledger from "not like that"** — FEATURE — value 5 — effort M — risk low — category: design memory
  Why: the request asks for non-generic UI, and the user's steers show they correct by reaction, not by spec. assumption: they'll keep reacting ("too purple", "too busy") and not write briefs.
  Done when: after saying "no gradients, tighter spacing", a UI task in a different project starts with those two traits listed as banned or preferred, and `fm taste show` lists them with the source message.

- **Translate vague taste words into knob moves** — FEATURE — value 5 — effort M — risk low — category: design vocabulary
  Why: "way better", "non generic", "good animations" are the user's own phrasing; nothing turns them into concrete changes. assumption: a small original dictionary (premium, punchy, calm, techy, playful) can map to tokens for type scale, density, contrast, motion duration and radius.
  Done when: `fm design nudge "more premium"` prints the token deltas it would apply and shows three interpretations. Applying one changes only those tokens in the token file, with a test.

- **End every UI task with an "eyeball these three things" card** — FEATURE — value 4 — effort S — risk low — category: honesty
  Why: tests and screenshots can't judge feel, motion timing or 3D composition. A user told what to look at spends 30 seconds, not 10 minutes. assumption: Foreman can name the checks it could not automate.
  Done when: closing a UI task prints a card with the unverified aspects (for example "hover easing", "mobile 3D perf") and the exact URL or command to view each. A test asserts the card is non-empty for a UI diff.

- **Run a design-debt sweep on existing apps** — FEATURE — value 4 — effort M — risk low — category: design backlog
  Why: the user's projects already exist, and new playbooks only help new work. assumption: generic tells (default font stacks, stock gradients, uniform 8px radii, no focus styles) are detectable statically.
  Done when: `fm design debt` on a fixture app files one ranked task per finding with file:line, and fixing a finding drops it from the next run.

- **Make a look reversible as one transaction** — FEATURE — value 4 — effort M — risk low — category: safety
  Why: restyling touches many files, and users hesitate to try bold directions they can't back out of. assumption: the token file is the single swap point.
  Done when: `fm design try NAME` applies a look on a branch with a before/after screenshot pair. `fm design revert` restores the previous tokens and the tree is byte-identical to the starting state.

- **Write "feels like X" cards from original analysis of well-known products** — FEATURE — value 4 — effort L — risk med — category: playbooks
  Why: users describe taste by reference ("like Linear", "like an old terminal"), and the library has no cards for that. Constraint: original writing only. assumption: describing traits (spacing rhythm, motion curve, colour discipline) in our own words is clear of copying.
  Done when: 20 cards exist, each with measurable traits (type scale ratio, motion ms range, palette size). A lint rejects any card without them, and `fm lib show` finds them by product name.

- **Add a ten-minute "design sprint" verb** — FEATURE — value 4 — effort M — risk med — category: workflow
  Why: the ask bundles brief, 3D, motion and QA, and a user wants to type one line and see a result. assumption: chaining the proposed playbooks is feasible once they exist.
  Done when: `fm design sprint "landing for X"` produces a brief, three tiny live variants, a screenshot strip, the chosen one built and an eyeball card, and stops after one decision from the user.

- **Gate the settings screen by showing the effect first** — FEATURE — value 4 — effort M — risk low — category: TUI config
  Why: config is currently hand-edited TOML, and the user wants it live in the TUI. Showing what a change does keeps editing safe. assumption: the renderer can draw a before/after split.
  Done when: highlighting any theme, layout or key setting in the settings screen shows a live split preview, Enter saves it to tui.toml with comments preserved, and Esc leaves the file unchanged (byte compare in a test).

- **Wild: pair-design with nudge keys on a live dev server** — FEATURE — value 4 — effort L — risk med — category: interaction
  Why: assumption: designers iterate by small reactions. Keys like `t` (tighter), `w` (warmer), `b` (bolder motion) each apply a token delta to a running page and are undoable.
  Done when: five nudge keypresses change five tokens in the browser without a reload, and `u` steps back each one.

- **Wild: "opposite day" generates the anti-version of your design** — FEATURE — value 3 — effort M — risk low — category: taste discovery
  Why: people find what they like by seeing what they reject, and the taste ledger gains signal from it. assumption: inverting tokens (dense↔airy, warm↔cold, sharp↔round) yields a clearly different page.
  Done when: `fm design opposite` renders both screenshots side by side, and the user's pick appends to the taste ledger.

- **Wild: turn a project's proved-run history into a case-study page** — FEATURE — value 3 — effort L — risk med — category: showcase
  Why: users show off what they built, and the site and demo already use real runs. assumption: task titles and receipts carry enough narrative.
  Done when: `fm page story` writes a self-contained HTML page with an animated timeline of closed tasks and their before/after frames. Private paths are scrubbed, and a test checks for no absolute paths.

- **Preview a playbook's output before loading it** — FEATURE — value 3 — effort M — risk low — category: discoverability
  Why: with 1,100+ cards and a growing design shelf, users can't tell which skill gives what look. assumption: each design playbook can ship one generated sample frame.
  Done when: `fm playbooks show NAME --sample` prints or opens a rendered sample, and CI fails if a design playbook lacks one.

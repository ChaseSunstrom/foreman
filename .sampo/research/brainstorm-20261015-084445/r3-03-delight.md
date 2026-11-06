# Brainstorm — lens: delight

- **Open with a one-line "first win" receipt after the first finished task** — FEATURE — value 4 — effort S — risk low — category: first-run delight
  Why: newcomer evidence A1/A9 shows no early payoff; a fresh install prints 40 lines of passes and `fm status` shows an unexplained "Drive: on".
  Done when: in a clean HOME, the first `fm task finish` ends with a single line naming what Foreman caught or proved (e.g. "ran 3 checks, 1 was red before your fix"), and a test asserts the line appears once and never again.

- **Add `fm hello`, a 60-second guided task on a throwaway fixture** — FEATURE — value 5 — effort M — risk low — category: onboarding
  Why: README's first screen is abstract (A1) and `fm` is "command not found" in a shell (A3); rivals all ship a guided help/setup wizard (B).
  Done when: `fm hello` in an empty HOME creates a temp repo with a seeded bug, walks capture → plan → fix → finish with no model calls, and exits 0 leaving nothing behind.

- **Make every empty state say what to do next, in plain words** — FEATURE — value 4 — effort S — risk low — category: empty states
  Why: `fm init` prints only a random slug and `fm status` on an empty project dumps a STATE doc (A5); jargon like "drive", "lane", "focus" is unexplained (A11).
  Done when: `fm init`, `fm status`, `fm task list`, and `fm digest` on an empty project each end with one "Next: fm …" line, verified by a snapshot test with no jargon words from a banned list.

- **Print a quiet "queue zero" moment when the last task closes** — FEATURE — value 3 — effort S — risk low — category: micro-delight
  Why: the user keeps asking to "keep going" through the queue; the end of that run currently has no marker (assumption: it just stops).
  Done when: finishing the final queued task prints a one-screen summary (tasks closed, evidence count, time) and a test shows it does not print while tasks remain.

- **Show "what you can now ignore" at task close** — FEATURE — value 4 — effort M — risk low — category: close-out
  Why: user's repeated steers are about Foreman staying quiet and not chasing; 159 of 370 weekly tasks show as "ungraded" noise (C).
  Done when: `fm task finish` output lists up to 3 things Foreman verified so the user need not re-check, each backed by a recorded evidence id.

- **Add a "Foreman earned this" card at day 7 with keep / lite / remove** — FEATURE — value 4 — effort M — risk med — category: trust
  Why: bypass-by-default is a large trust ask (A2) and there's no published proof it helps (C); a day-7 card turns that into a choice.
  Done when: after 7 days and 5+ tasks, the next SessionStart shows counts of caught failures and offers `fm lite` / `fm remove`, once, and a test confirms it never reappears after an answer.

- **Fold child tasks into their parent in `fm digest`** — FIX — value 3 — effort S — risk low — category: legibility
  Why: 159 of 370 recent tasks display as "ungraded" because they were folded into others (C), making the weekly picture look sloppy.
  Done when: `fm digest` shows folded tasks under their parent with the parent's grade, and ungraded count drops to 0 for folded work in a fixture.

- **Greet a resumed session with a "last time" line that names the exact step** — FEATURE — value 4 — effort S — risk low — category: return delight
  Why: resume at the exact step is the core promise; SessionStart context is ~1.5k chars of mostly state (C), none of it a human sentence. Assumption: current greeting isn't a sentence.
  Done when: resuming an in-progress task begins with one sentence like "Last time: step 3 of 5, fixing login timeout; next is running the tests," asserted by a snapshot test.

- **Wild: `fm demo` replays a recorded seeded-bug fix as a narrated terminal show** — FEATURE — value 4 — effort M — risk low — category: wild showcase
  Why: README lacks a before/after (A1); a no-model replay doubles as the README proof strip and a smoke test.
  Done when: `fm demo` plays a ≤60 s scripted session offline, `--fast` skips pauses for CI, and the README's first screen embeds its captured output.

- **Wild: Let the guard's first save become a keepsake line** — FEATURE — value 3 — effort S — risk low — category: wild trust moment
  Why: the guard blocks dangerous commands in bypass mode, but the user never sees the payoff (A2 trust ask). Assumption: blocks are logged.
  Done when: the first time the guard blocks a command, a one-time note says what it prevented and how to allow it, and `fm doctor` shows a "saves so far" count.

- **Wild: Offer a "Foreman Lite first week" that quietly runs observe-only beside the user's habits** — FEATURE — value 4 — effort L — risk med — category: wild adoption
  Why: rivals add commands without rewriting `~/.claude` (B); Foreman's install does the opposite (A2), so a gentle trial is the delightful on-ramp.
  Done when: `fm try` runs hooks in log-only mode with no blocking, changes no `~/.claude` permissions, and ends the week with a card of what it would have blocked.

- **Wild: Print a shareable postcard when a milestone closes** — FEATURE — value 3 — effort M — risk low — category: wild share
  Why: `fm page` already builds a self-contained HTML board, so a one-page "what shipped" artefact reuses that machinery; the user's "make it THE plugin" ambition suggests showing it off.
  Done when: `fm postcard T-ID` writes one self-contained HTML file with title, criteria ticks, evidence counts and time, redacts the home path, and makes zero network requests (tested).

- **Translate refusals into a before/after command pair** — FEATURE — value 4 — effort S — risk low — category: guard legibility
  Why: `fm task done` refuses with 4 bullets and the one-call `fm task finish` is buried (A9).
  Done when: a `fm task done` refusal ends with a copy-pasteable prefilled `fm task finish …` line, asserted in a test.

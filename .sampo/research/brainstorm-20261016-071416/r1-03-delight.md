# Brainstorm — lens: delight

- **Show a one-line "welcome back" receipt at the first prompt after a gap** — FEATURE — value 4 — effort S — risk low — category: greeting
  Why: `fm away` exists as a verb and fires once at session start, but the pack's "what did I miss" and "state of the union" ideas never merged into one warm, single-line greeting that expands. Assumption: today's output is a list, not a sentence.
  Done when: a test with a ledger gap over 8h makes the first prompt's injected context contain exactly one greeting line naming closed, blocked and asked counts, and a second prompt adds zero bytes.

- **Celebrate a hard-won green with a plain-words close line** — FEATURE — value 3 — effort S — risk low — category: close-out
  Why: T-0795 (plain receipts) is deferred, and every builder branch needed 2–6 review rounds. A task that goes green after retries has no moment of recognition. Assumption: close output is currently neutral for all tasks.
  Done when: a test closing a task after 3 red runs prints a line starting "Took 4 tries" with the first and last failing check named; a first-try close prints nothing extra.

- **Give every lane a stable callsign shown in pane, ledger and commit trailer** — FEATURE — value 3 — effort M — risk low — category: identity
  Why: lanes are named `lane-<id>` and the Agents graph shows many parallel builders; ids are hard to hold in the head. Assumption: no friendly name exists yet.
  Done when: `fm lane list` shows a name like "otter" for a lane, the same name appears in its commit trailer and in the pane, and the name is deterministic from the id.

- **Print a last-frame keepsake when the pane exits** — FEATURE — value 2 — effort S — risk low — category: pane
  Why: the README leads with the pane as the product's face, but it vanishes on quit. Assumption: no exit summary exists.
  Done when: quitting `fm ui` in a test prints one static frame (work bar, stage rail, today's closes) to stdout that contains no escape codes under NO_COLOR.

- **Write error messages in the user's recent vocabulary** — FEATURE — value 3 — effort M — risk med — category: voice
  Why: the user's asks use "lane", "close", "brief" inconsistently with some verbs ("fm task list" guesses by builders show the vocabulary gap). Assumption: a glossary can be mined from steers.
  Done when: a test with a glossary mapping "ticket"→"task" makes the unknown-verb message use the user's word and still show the real command.

- **Make common guessed commands just work, with a quiet "(ran `fm task ls`)" note** — FIX — value 4 — effort S — risk low — category: forgiveness
  Why: the review notes builders and weak agents guess `fm task list`; the nearest-name suggestion exists, but suggesting still costs a turn. Delight is not being scolded.
  Done when: `fm task list` runs the real listing and prints one dim line naming the canonical verb, exit 0; an unknown guess still gives the suggestion.

- **Add a first-time capability toast, once per feature** — FEATURE — value 2 — effort M — risk low — category: discovery
  Why: T-0862/T-0863 (tour, start ladder) are deferred pending evidence; a once-only, dismissible hint at the moment a feature first becomes relevant needs no tour. Assumption: usage data from `fm usage` can tell "never triggered".
  Done when: a test triggering `fm todo` for the first time emits one hint line; the second time emits none; `FOREMAN_QUIET=1` suppresses both.

- **Fade quiet pane cards by recency instead of collapsing them** — FEATURE — value 2 — effort M — risk low — category: motion
  Why: the user kept saying "still cluttered" (density idea in the pack); hard collapse is jarring. Assumption: pane supports a dim attribute and respects reduced-motion.
  Done when: a render test shows a card untouched for 10 minutes uses the dim style, a touched card returns to normal, and reduced-motion mode renders the steady dim without animation.

- **Wild: Hum a "build weather" glyph in the statusline** — FEATURE — value 2 — effort S — risk low — category: statusline
  Why: wild; load, red/green streak and queue depth are all already computed for lane throttling and `fm next`. One glyph (☀ ⛅ ⛈) compresses them. Assumption: statusline has room for one cell.
  Done when: with a fake load of 6 and two red gates the statusline renders the storm glyph; with load 0 and green it renders the sun glyph.

- **Wild: Auto-cut a 30-second "director's cut" replay when a release is tagged** — FEATURE — value 3 — effort L — risk med — category: release
  Why: wild; `demo/live.svg` is hand-recorded and goes stale (the "regenerate README pictures in CI" idea). The release ritual is already eight manual steps; this makes shipping feel like a premiere. Assumption: the demo recorder can be driven by a scripted session.
  Done when: `fm release` in a fixture produces a `demo/` asset under 2 MB from the scripted session and fails the release-check if the asset is older than the version bump.

- **Wild: Leave a decaying sticky note on files a builder was nervous about** — FEATURE — value 3 — effort M — risk med — category: lane notes
  Why: wild; builders' self-review (T-1147) finds doubt but discards it at close. A note like "unsure: lock re-entry" attached to a file, fading after 14 days or on the next touch by a reviewer, feeds the next reader.
  Done when: a builder finishing with `--doubt FILE "text"` makes `fm lane brief` for a later lane touching that file list the note, and the note is absent after its expiry in a clock-faked test.

- **Show a before/after contact sheet at each UI close** — FEATURE — value 3 — effort M — risk low — category: proof
  Why: Pillar 4 demands screenshots before and after; the closes today report text only. A single side-by-side image gives the user something to look at (the "close with something to look at" idea made concrete). Assumption: a headless browser or pane renderer is available.
  Done when: closing a task tagged ui writes `before.png`, `after.png` and a combined sheet under the task's evidence folder, and `fm task show` links it.

- **Wild: Offer `fm postcard`, one shareable SVG of a finished task** — FEATURE — value 2 — effort M — risk low — category: sharing
  Why: wild; the README already leads with a hand-made SVG, so the format is proven. A postcard (title, diff stat, the failing-then-passing proof line) is what a user shows a friend.
  Done when: `fm postcard T-1158` writes a valid SVG under 20 KB containing the task id, title and one proof command, with no absolute local paths in it.

- **Say the day's end in one line: closes, near-misses, minutes saved** — FEATURE — value 2 — effort S — risk low — category: closing ritual
  Why: the guard blocks and replays exist but only as counts in a digest; a "guard stopped 3 near-misses today" tally gives the discipline a visible reward. Assumption: guard refusals are in the ledger with dates.
  Done when: a test with a seeded day of 4 closes and 3 guard blocks makes `fm day` print one line containing "4 closed" and "3 stopped", and it prints nothing on an empty day.

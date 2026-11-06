# Brainstorm — lens: delight

- **Stamp the proof onto the diff** — FEATURE — value 4 — effort M — risk low — category: ui
  Why: Foreman's identity is "prove it with commands it ran"; the TUI has check chips and change bars but evidence and edit live apart. Assumption: the event log ties each verify run to files touched.
  Done when: in a golden frame, each changed hunk shows a small stamp (green ✓ with the command's short name, or hollow ○ "unproved"), and a hunk with no covering verify run renders the hollow stamp.

- **Mute the quiet, shout the exception** — FEATURE — value 4 — effort S — risk low — category: ui
  Why: The user said the TUI "looked like crap with all the text" and wants more than static colors. Assumption: steady-state rows currently share the same weight as anomalies.
  Done when: a frame of a healthy run has every passing row in dim tone, and injecting one guard refusal or red step makes only that row full-brightness, verified by two golden frames.

- **Give each station a one-word verb that conjugates** — FEATURE — value 3 — effort S — risk low — category: copy
  Why: Static labels ("verify") feel dead; a header reading "planning…", "proving…", "landed" tracks state with words, not color. Assumption: stations map to discrete states in the event stream.
  Done when: the station label for each of the states pending/active/done/failed differs, and a test asserts all four strings per station exist in the theme's vocabulary file.

- **Settle the model's words into a one-line "gist" chip** — FEATURE — value 4 — effort M — risk med — category: ui
  Why: The user disliked walls of text; the pack's ideas fold prose but none summarize it. Assumption: the first sentence or tool-call intent is extractable without a model call (privacy: no extra send).
  Done when: a 40-line model message renders as a ≤60-column gist chip with a key that expands it, and no network call occurs in the test.

- **Let the closing receipt be a keepsake file** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: Users post demo SVGs (README's demo/live.svg); a closed task ending with a saved, local receipt card makes sharing trivial. Assumption: an SVG writer exists from the demo pipeline.
  Done when: closing a task writes `receipt-T-XXXX.svg` locally containing id, title, proofs and duration, and nothing is uploaded.

- **Dim the TUI to the terminal's own light or dark** — FIX — value 3 — effort S — risk low — category: ui
  Why: T-1217 shows pane background mismatch (#262626) is already a pain; static palettes assume dark. Assumption: OSC 11 query or COLORFGBG is readable.
  Done when: with a light background reported, every theme's text meets ≥4.5:1 contrast in a computed check, and the dark case is unchanged.

- **Local-only guarantee badge** — SECURITY — value 3 — effort S — risk low — category: privacy
  Why: Pack lists privacy as thin; the TUI renders model output and may someday fetch things. Assumption: the TUI makes no network calls today.
  Done when: a test runs the TUI with sockets blocked and passes, and the footer's `local` marker is shown only while that holds.

- **Scrub secrets from the receipt and the clip before they're written** — SECURITY — value 4 — effort M — risk low — category: privacy
  Why: Existing ideas export SVG replays and postcards; none says exports are redacted. Assumption: tool output can contain tokens or env values.
  Done when: an export of a fixture run containing `sk-…` and an `.env` line contains neither, checked by grep in the test.

- **Idle shimmer only on the thing being waited for** — FEATURE — value 3 — effort S — risk low — category: motion
  Why: Animating everything idle burns CPU and attention; one element shimmering (the slowest active station) tells "this is what we're waiting on". Assumption: the active station is known.
  Done when: in a mid-run frame sequence exactly one element's cells change between ticks while the harness is quiet.

- **Wild: Let the run have a pet that grows from proven work** — FEATURE — value 2 — effort M — risk low — category: delight — wild
  Why: assumption: a small ASCII creature in the footer that gains a detail per task closed proved (and sulks briefly on a refusal) is the thing users show others; state lives in a local file.
  Done when: closing 10 proved tasks changes the creature's rendering in a fixture state file, and deleting the file resets it.

- **Wild: Theme from the repo's own commit history** — FEATURE — value 2 — effort M — risk low — category: theme — wild
  Why: assumption: hashing the repo's top language mix and name into a palette gives each project a recognizable look with zero config, with no network.
  Done when: two fixture repos yield different accent palettes deterministically, the same repo yields the same one twice, and all pass the contrast check.

- **Wild: Ticking "guard saved you" tally in the footer** — FEATURE — value 3 — effort S — risk low — category: delight — wild
  Why: The guard blocks commands users would never want run; making that visible as a small counter ("3 near-misses today") turns invisible protection into a pleasure. Assumption: refusals are logged with timestamps.
  Done when: after replaying a log with 3 refusals the footer reads 3, and the counter resets at local midnight.

- **Keystroke feel: a 2-frame press response on every key** — FEATURE — value 3 — effort S — risk low — category: motion
  Why: Static UIs feel unresponsive; the existing context hint bar idea flashes hints but no general press feedback. Assumption: input is read in the same loop as rendering.
  Done when: pressing a view key produces a highlighted frame within one tick that reverts within two, shown in a golden-frame sequence, and is skipped under reduced motion.

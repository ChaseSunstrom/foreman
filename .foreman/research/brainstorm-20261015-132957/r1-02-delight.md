# Brainstorm — lens: delight

- **Show a "caught it" moment the instant the guard saves something** — FEATURE — value 4 — effort S — risk low — category: delight
  Why: the guard blocks dangerous commands and snapshots work, but saves are silent. Earlier ideas cover a weekly ledger and a keepsake line; this one is the live beat, a single line naming what would have been lost ("kept 14 uncommitted files before that reset --hard; `fm snapshots` restores").
  Done when: running `git reset --hard` with dirty files in a fixture repo prints one human sentence naming the file count and the restore command, and a test asserts it.

- **Turn the first red-to-green into a tiny visible beat on the band** — FEATURE — value 3 — effort S — risk low — category: micro-delight
  Why: assumption: evidence is recorded but the moment a check flips from failing to passing is not marked. `fm task prove` already knows the start-tree failure, so the flip is detectable. A one-time, quiet ✓ with the check name and the seconds it took to turn green.
  Done when: a prove run that goes red then green emits exactly one flip line, and a second green run in the same task emits none.

- **Make `fm demo` end with the user's own repo's first real suggestion** — FEATURE — value 4 — effort M — risk low — category: first-run
  Why: round 4 shipped `fm demo` (<1 s, no model) and round 5 shipped `fm projects --next`. The demo proves the product on a fixture, then stops. Closing with "here is what I'd do first in *this* repo" (from the map, TODOs, failing check) carries the smile into real work.
  Done when: `fm demo` run inside a repo with a failing test or TODO prints one concrete suggested first task with a ready-to-paste `fm` line.

- **Write each close-out as a screenshot-worthy three-line receipt** — FEATURE — value 4 — effort S — risk low — category: close-out
  Why: the README leads with a recording, so users already share visuals; the close-out is the thing they would screenshot. A fixed shape: what changed (user's words), proof (command plus grade), what was skipped on purpose.
  Done when: `fm task finish` output has a final block of ≤3 lines of ≤72 chars each, with no ticket jargon, checked by a golden test.

- **Greet a resumed session with the exact step, typed in** — FEATURE — value 3 — effort S — risk low — category: continuity
  Why: resume at the exact step after `/compact` is the headline feature, but nothing makes the user *feel* it. A one-line "Back at step 3 of 5: running the migration test. Last thing I did: edited db.py" is the felt proof.
  Done when: SessionStart after a compact in a fixture task injects a one-line greeting naming the step number, its title and the last edited file, and a test pins it.

- **Say why it's quiet** — FEATURE — value 3 — effort S — risk low — category: legibility
  Why: when Foreman does nothing (no task, observe-only, or a hook skipped), users can't tell off from broken. A single `fm why-quiet` line, plus the band showing a dim reason, turns silence into reassurance.
  Done when: `fm why-quiet` in each of three states (no task, paused, non-Foreman project) prints a distinct one-line reason.

- **Give every refusal a "do this instead" pair** — FEATURE — value 4 — effort M — risk low — category: guard legibility
  Why: guard blocks are the sharpest friction a new user meets, and the rival survey showed light first touch wins. A refusal that ends with the safe equivalent command ("blocked rm -rf ~; try `rm -rf ./build`") makes blocking feel like help.
  Done when: the 10 most frequent guard refusal classes each include a runnable alternative line, covered by a table test.

- **Add a "you can ignore this" line to each task's close** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: fm tour already ranks files as review / glance / skim. Surfacing the skim set as "nothing here needs your eyes: 9 files, formatting and renames" is the relief users will mention to friends.
  Done when: finish prints a skim-count line when ≥1 file is graded skim, naming the reason class, and omits it otherwise.

- **Wild: Play the day back as a 20-second terminal time-lapse** — FEATURE — value 3 — effort M — risk low — category: wild showcase
  Why: wild. The ledger holds timestamped steps, edits, checks and guard saves. `fm replay --day` renders them as an animated, speed-controlled strip in the terminal and exports a cast file for sharing, reusing the demo/record_live.py machinery.
  Done when: `fm replay --day --out day.cast` produces a valid asciicast file from a fixture ledger in under 2 s with no model call.

- **Wild: Let the band's colour breathe with how the work is going** — FEATURE — value 2 — effort M — risk med — category: motion
  Why: wild. The foreman-ui band already shows state; a slow, honoring-reduced-motion tint shift (cool while steady, warm when a check is red, still when idle) gives a glanceable mood across a room. Assumption: the mod can animate colour cheaply.
  Done when: with the mod, the band renders three distinct tints for green, red and idle in a snapshot test, and reduced-motion disables animation.

- **Wild: Offer `fm gift` — a small finished fix waiting when you return from a long absence** — FEATURE — value 4 — effort L — risk med — category: return delight
  Why: wild. Deferred tasks sit in the queue (S-sized ones like T-0317, T-0418). During `fm night`, pick one tiny, low-risk item, do it in a lane with full proof, and leave it as an unmerged branch with a one-line card: "While you were away: fixed X; merge with one command."
  Done when: a night run on a fixture queue leaves exactly one verified, unmerged lane for an S task and a card naming its merge command; nothing lands on main.

- **Print a "queue zero" moment when the last task closes** — FEATURE — value 3 — effort S — risk low — category: ritual
  Why: the drive loop keeps going until done or needing the user, but ending is abrupt. A calm closing line with the day's counts (closed, proven, guard saves) and the next best thing from `fm projects --next` makes finishing feel like finishing.
  Done when: closing the final open task prints a summary of ≤4 lines including counts and one next suggestion; with other open tasks it prints nothing extra.

- **Replace jargon in the first-session band with plain words that graduate away** — FEATURE — value 3 — effort M — risk low — category: onboarding
  Why: the pack's newcomer walkthrough found 17 friction points, many wording. Using plain labels ("checking your work" for evidence gate) for the first three tasks, then the real terms, teaches vocabulary without a manual.
  Done when: with fewer than 3 closed tasks the band uses the plain label set, afterwards the standard set, verified by a rendering test for both.

- **Wild: A "Foreman says" fortune on `fm doctor` when everything is green** — FEATURE — value 1 — effort S — risk low — category: personality
  Why: wild and playful. Doctor now prints only problems, so a healthy run is blank. One rotating, non-annoying line drawn from the project's own history ("11 tasks closed this week, 0 reopened") rewards a clean bill of health and is pure ledger data.
  Done when: `fm doctor` with no problems prints one ledger-derived line, and `--quiet` prints nothing.

# Brainstorm — lens: delight

- **Pick a voice at install** — FEATURE — value 4 — effort S — risk low — category: onboarding
  Why: newcomer evidence A1 and A11 (abstract first screen, jargon throughout). One question (terse / plain / chatty) sets verbosity, jargon level, emoji and sound cues for every surface, instead of 20 separate toggles. Assumption: the existing output paths can read one setting.
  Done when: in a clean HOME, answering "plain" makes `fm status` and the SessionStart note contain none of the words brief, drive, lane or scope, and a test asserts that.

- **Tell the user what's new for them after an upgrade** — FEATURE — value 4 — effort S — risk low — category: discoverability
  Why: 46 of 108 verbs were never run in 11 days, and the changelog is developer-facing. The first session after an upgrade shows at most 3 lines, filtered by the verbs and features this user's history touches, each with one try-it command.
  Done when: after a version bump, the first session greeting lists at most 3 changes, each with a runnable command, and does not show them again in the next session.

- **Give reviewers a "done well" line** — FEATURE — value 3 — effort S — risk low — category: review tone
  Why: audit output is all defects, so a review reads as a scolding. One required finding per review names something the diff did well, citing a file:line and the repo convention it follows. That teaches taste and makes the review less grim. Assumption: reviewers can name a convention reliably.
  Done when: every review result has a "done well" entry with a valid file:line, and a test rejects a review without one.

- **Print a personal cheat card** — FEATURE — value 3 — effort S — risk low — category: onboarding
  Why: A4 says `fm --help` is 231 lines. `fm card` prints one screen with the user's 6 most-used verbs plus 2 they haven't tried but match their habits, built from the command log. It is the answer to "what do I type", and it adapts as they grow.
  Done when: `fm card` outputs 20 lines or fewer, lists only verbs that exist, and differs between two projects with different usage logs.

- **Configure by saying it** — FEATURE — value 4 — effort M — risk med — category: settings
  Why: the installer sets bypass, autocompact, a statusline wrapper and 20 deny rules (A2), and the user can't easily see or change them. `fm tune "stop asking me about small things"` maps the sentence to concrete settings, shows a before/after diff, and applies it only on a yes, with one-line undo. Assumption: a small vocabulary of settings covers most sentences.
  Done when: three sample sentences each produce the expected settings diff, nothing is written without confirmation, and `fm tune --undo` restores the previous values byte for byte.

- **Tour an unfamiliar repo from the map** — FEATURE — value 4 — effort M — risk low — category: adoption
  Why: `fm map` already knows the entry points, layout and test→source links, but only the model sees it. `fm tour-repo` gives a human a 10-stop ordered walkthrough (entry point, core module, where tests live, how to run the gates), with clickable file:line stops. Every adopter's first minute on a new repo becomes a pleasant one.
  Done when: on the fixture repo it prints at most 10 stops, each file:line resolves, and the first stop is the declared entry file.

- **Make a peace-treaty card for coexisting plugins** — FEATURE — value 3 — effort S — risk low — category: interop
  Why: B shows users already run superpowers, ECC or claude-mem, and `--apply-conflicts` reads as hostile. When Foreman detects a rival it prints a friendly table of who owns what (brainstorm → theirs, evidence gate → Foreman) and offers a "defer to them" switch per row.
  Done when: with a stub superpowers plugin present, `fm doctor` shows the table and no step says "disable".

- **Speak the user's language** — FEATURE — value 3 — effort M — risk med — category: accessibility
  Why: the whole output surface is English, and the target audience for a 300k-star-class plugin is global. Detect the language of the user's own requests and localize status, hints and refusals, keeping verbs, flags and ids untouched. Assumption: a small string table (about 150 strings) is enough.
  Done when: with locale `de` set, `fm status` and a gate refusal print German, and the command text inside them is unchanged and still copy-pasteable.

- **Keep a shelf of firsts** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: A shows a first-run that goes unrecognised. A tiny ledger records one-time moments (first held task, first guard save, first lesson recalled, first overnight run), each shown once as a single quiet line. It is distinct from the red-to-green flourish, because it marks milestones in the relationship.
  Done when: each first-event fires its line exactly once per user, and `fm firsts` lists them with dates.

- **Wild: play a toy while a long gate runs** — FEATURE — value 2 — effort M — risk low — category: playfulness
  Why: wild. Gates take minutes, and the user waits with nothing to do. `fm play` opens a stdlib curses toy in the pane, and a gate's red or green result interrupts it with a clean banner. It makes waiting something people show each other.
  Done when: `fm play` starts a game, and a finished gate replaces it with the result within 1 second, with the terminal restored.

- **Wild: write the dev diary into the user's notes vault** — FEATURE — value 3 — effort M — risk low — category: reflection
  Why: wild. Each evening, a markdown entry in the user's voice is written from the ledger (what was asked, what shipped, what was dropped and why) into a configured folder such as Obsidian or a notes directory. It is plain files, nothing is sent anywhere, and it is off until a folder is set. Assumption: the user keeps notes in markdown.
  Done when: with a folder configured, `fm diary` writes `YYYY-MM-DD.md` containing only real task ids and titles from that day, and does nothing when the setting is unset.

- **Wild: lend Foreman to a friend with `fm guest`** — FEATURE — value 4 — effort M — risk med — category: sharing
  Why: wild. Rival plugins spread through one pasted command (B). `fm guest` prints a single command that starts a throwaway-HOME session with the user's chosen posture and a fixture task, then erases itself. A friend can try the discipline in 60 seconds with no changes to `~/.claude`. Assumption: it reuses the "no trace" machinery being designed for `fm try`.
  Done when: running the printed command on a clean machine leaves `~/.claude` byte-identical afterwards, and the guest session passes `fm doctor`.

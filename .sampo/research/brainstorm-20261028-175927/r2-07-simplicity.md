# Brainstorm — lens: simplicity

- **Delete the TTY swipe and keep the served page** — CLEAN — value 4 — effort S — risk low — category: triage
  Why: T-1664/1857/1858/1860/1861/1866 left four ways to triage the backlog and no entry that picks one. Removing one is cheaper than adding a router, and the served page already has the better UI.
  Done when: `fm inbox swipe` with no flag starts the served page, the TTY code path is gone, and `test_swipe` passes.

- **Write swipe as a static HTML file with no server** — FEATURE — value 4 — effort M — risk low — category: triage (wild)
  Why: the served pages need a one-shot token and Ctrl-C to stop. A file that keeps verdicts in localStorage and ends with a copyable `fm inbox apply …` line removes the server, the token and the lifecycle problem. Assumption: verdicts can be applied from a pasted command or file.
  Done when: `fm inbox swipe --html out.html` opens offline, and pasting its output command applies the verdicts to the backlog.

- **Take ticket fetching from the user's own CLI** — CLEAN — value 4 — effort M — risk med — category: integrations
  Why: T-1859 hand-built Jira and Linear fetchers and has no GitHub support, even though `gh` is the common case. Shelling out to `gh issue view`, `jira` or `linear` and mapping the JSON removes the API code and the credentials handling. Assumption: those CLIs are installed.
  Done when: `fm inbox ticket gh:owner/repo#12` makes a brief, and the Jira and Linear HTTP code is deleted.

- **Cut `fm settings` to get/set/undo and make the extras a plain file** — CLEAN — value 3 — effort S — risk low — category: settings
  Why: log, macro, duel, replay and words (T-1658) are only discoverable through help, and `newcomer` never offers them. Fewer verbs means nothing to advertise. Macros become lines in a text file the user can read.
  Done when: `fm settings --help` lists at most four verbs, and the removed behaviours are covered by the file or have no remaining callers.

- **Drop Figma import and accept only DTCG JSON** — CLEAN — value 3 — effort S — risk low — category: design
  Why: T-1652 shipped Figma import as a one-way path alongside DTCG. Figma exports DTCG via common plugins, so one input format is enough.
  Done when: `fm design import` rejects non-DTCG input with a one-line pointer, and the Figma parser and its tests are deleted.

- **Delete unused design tokens instead of reporting them** — FEATURE — value 3 — effort S — risk med — category: design
  Why: the round-5 review asked for an unused-token report on DESIGN.md. A `--prune` that removes tokens no CSS references does the job, and the report is just its dry-run. Assumption: a grep over the repo's CSS is accurate enough.
  Done when: `fm design prune` removes a planted unused token, keeps a used one, and prints the diff.

- **Cut the scene catalogue to scenes that render under 1 s** — CLEAN — value 3 — effort S — risk low — category: scenes
  Why: T-1846..1855 shipped many showpiece scenes with no index, no captions and no render-time test. Deleting those that miss the budget, or lack a one-line caption in their source, keeps the set small without building a gallery.
  Done when: one test renders every scene, fails on more than 1 s or a missing caption, and the failing scenes are removed.

- **Expire deferred tasks after 60 days untouched** — CLEAN — value 4 — effort S — risk low — category: backlog
  Why: about 30 "Later from T-07xx/08xx" umbrellas sit deferred, some with "needs evidence" notes. Expiry turns the pile into an automatic yes/no instead of a human sweep. A task closes as expired with its text kept in the catalog.
  Done when: a deferred task with no activity for 60 days closes as expired on session start, and touching it resets the clock.

- **Remove help position numbers and sort help by group then name** — CLEAN — value 3 — effort S — risk low — category: help
  Why: `fm dojo` shares position 306 with another command and `test_help` fails. Hand-assigned numbers are the cause, and sorting needs no numbers at all.
  Done when: no position integers remain in the command table, and adding a command can't break `test_help`.

- **Make known-fix matching exact-string only** — FIX — value 3 — effort S — risk low — category: reliability
  Why: T-1865 made learned or vague signatures stop matching unrelated failures, which shows fuzzy matching was the bug. Exact signature matches cannot misfire, and a miss costs nothing.
  Done when: a signature offers a fix only when the normalised failure line equals it, and a test with a near-miss failure gets no offer.

- **Turn the round review into a checklist file the gate reads** — FEATURE — value 3 — effort M — risk low — category: process (wild)
  Why: each round writes review findings (the round-5 list above) that the next round must re-find from prose. A `ROUND.md` of `- [ ]` lines that `fm doctor` counts makes unfinished findings visible and ends the loop's re-derivation.
  Done when: `fm doctor` reports the number of open lines in `ROUND.md`, and closing a task ticks its line.

- **Let the top five verbs earn one-letter aliases from the journal** — FEATURE — value 2 — effort S — risk low — category: ergonomics (wild)
  Why: the verb surface is huge and a few verbs dominate real use. Deriving the aliases from the user's own history avoids a designed shortlist that would go stale. Assumption: the journal records verb names.
  Done when: `fm alias --auto` prints five aliases ranked by use and installs them as shell functions on confirmation.

- **Hold a round to a net-negative budget: no new verb unless one is deleted** — CLEAN — value 4 — effort M — risk low — category: process (wild)
  Why: round 5 still added swipe, app view, `ticket`, scenes and macros, each with its own surface. A doctor check comparing the verb count to the last tag makes a round that adds a verb without removing one fail closed with a named swap.
  Done when: `fm doctor` fails when the verb count exceeds the previous release's, and passes after a verb is deleted or a documented exemption is added.

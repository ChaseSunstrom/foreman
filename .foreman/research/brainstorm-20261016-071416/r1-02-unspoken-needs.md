# Brainstorm — lens: unspoken needs

- **Make bare `fm` resolve to the lane's own checkout** — FIX — value 4 — effort S — risk low — category: lanes
  Why: the round-4 review says builders in a lane can't run their own new `fm` flags, because bare `fm` hits the main checkout's copy and they must call `python3 plugin/bin/fm`.
  Done when: a test in a lane worktree where `plugin/bin/fm` has a new flag runs bare `fm --newflag` and gets the worktree's behaviour. `fm doctor` in a lane prints which copy resolved.

- **Record reviewer findings automatically at reviewer stop** — FEATURE — value 4 — effort M — risk med — category: feedback loop
  Why: the defect-class feed (T-1164) depends on `fm task finding`, called by hand once per finding, and the review says nothing makes the main thread record them.
  Done when: a fixture reviewer result with three findings produces three finding records without a manual call. A rerun of the same result adds none.

- **Put the refused command and its replay verdict in the friction digest** — FEATURE — value 4 — effort M — risk low — category: guard
  Why: tuning guard friction took a hand-written transcript miner, and two premises were false only after mining (data-only writes, literal variables). The digest counts refusals but never shows the commands.
  Done when: `fm friction --commands` on a fixture transcript lists each refusal's full command with its `fm guard try` verdict today. Entries whose verdict is now "allow" are marked as already fixed.

- **Make guessed verbs and flags work, using the unknown-command log** — FEATURE — value 3 — effort S — risk low — category: weak-model ergonomics
  Why: builders and weak agents guess `fm task list`, and the unknown-command message only suggests the nearest verb; the review suggests common guesses could simply work.
  Done when: a table built from logged unknown invocations maps `fm task list` to the real verb and runs it, with a one-line note. A guess not in the table still errors.

- **Let the autonomous drive run the review and ideas workflows** — FEATURE — value 4 — effort M — risk med — category: autonomy
  Why: /foreman:review and /foreman:ideas (T-0787) only run when the user types them, and the user is AFK.
  Done when: a drive test at a task-close boundary invokes the review path headlessly through the same entry point as the slash workflow. The ledger records one review event and no typed command was needed.

- **Attach a post-ship adoption probe to each shipped feature** — FEATURE — value 3 — effort M — risk low — category: measurement
  Why: the builder self-review (T-1147) and defect classes (T-1164) are described as new and unmeasured, and every builder branch still needed 2–6 real defect fixes.
  Done when: `fm shipped --since 1.2.31` lists each task with a counter (times fired, defects found per branch before and after). A feature with zero events is flagged "unmeasured".

- **Fix the guard's "it could be …" path guess** — FIX — value 2 — effort S — risk low — category: guard
  Why: the review reports guesses like `/repo/cd/w.out`, where a command word is glued into the path.
  Done when: a test with `cd w && cmd > w.out` yields a guess that is either a real resolved path or none. No command word becomes a path segment.

- **Make the release ritual a resumable, checkpointed run** — FEATURE — value 3 — effort M — risk med — category: release
  Why: the review calls releases a manual 8-step ritual (3 version fields, heading, gates on a quiet tree, release-check, temp-worktree merge, push), and T-1173 is active.
  Done when: killing `fm release` after step 4 and rerunning resumes at step 5 without redoing the bumps. The push step still needs the existing remote grant.

- **Stamp the map's age in every pack and refresh it first** — FIX — value 2 — effort S — risk low — category: context packs
  Why: this pack's map says "as of an older HEAD (1524 files)", so brainstormers reason from stale layout.
  Done when: a pack built at a HEAD newer than the cached map either rebuilds the map or prints "map is N commits old" in its header, verified by a test.

- **Add a mid-run steer file the loop reads at each boundary** — FEATURE — value 3 — effort S — risk low — category: user control
  Why: the user is AFK but checks in, and their steers ("push to main when you get a chance") arrive as chat messages that an unattended loop may not see until later. Assumption: they would rather drop one line in a file than interrupt a run.
  Done when: a line appended to `.foreman/steer.md` is quoted as untrusted data in the next loop round's brief. It is logged once and then marked consumed.

- **Label every pack section by origin and fence the untrusted ones** — SECURITY — value 3 — effort M — risk low — category: injection
  Why: packs mix the user's words, ledger text, reviewer output and pasted content, and "the user's own words" quotes briefs the model once wrote. Brainstorm children treat all of it as one blob.
  Done when: a pack builder test shows each section with an origin tag, and a planted instruction in a reviewer section is rendered inside a fence marked untrusted.

- **Wild: Make the final report answerable by ticking boxes** — FEATURE — value 4 — effort M — risk med — category: AFK handoff
  Why: wild; the standing rule is that anything only the user can do goes in the final report, and `fm todo` lists such items. Assumption: a tick in a markdown file is the cheapest possible reply.
  Done when: ticking "approve push" in `.foreman/report.md` and saving makes a watcher run exactly that item's command once. An unticked or edited item runs nothing.

- **Wild: Run a small-model smoke test of the whole discipline** — FEATURE — value 4 — effort L — risk med — category: weak models
  Why: wild; the user's standing ask is that Foreman works for weak or small local models, but the enforcement is only tested with scripted fakes. Assumption: a local engine such as ollama is optional and detected.
  Done when: `fm doctor --small` runs one scripted task against a local small model if present (skipped with a note if absent). It reports which enforcement steps blocked or rescued it.

- **Wild: Prove each release candidate by building a task with itself** — FEATURE — value 3 — effort M — risk med — category: self-hosting
  Why: wild; lanes already run an older `fm` than the one under test, and every branch needed review rounds. A candidate that cannot complete one micro-task through its own verbs should not ship.
  Done when: `fm release-check` creates a throwaway worktree on the candidate, runs focus, edit, prove and finish on a fixture task with that tree's `fm`, and fails the release if any step errors.

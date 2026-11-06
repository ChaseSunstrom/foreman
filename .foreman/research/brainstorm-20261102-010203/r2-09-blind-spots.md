# Brainstorm — lens: blind spots

Class of the eight misses: Foreman measures, attributes and checks other things, but not itself. T-2533 to T-2536 are cost and subtraction of its own parts. T-2542 is liveness of its own timers. T-2546 and T-2547 are its own generators' grounding. T-2554 is its own writes feeding its own learner. The question a brainstorm should have asked: **"Where does Foreman consume, trust or judge its own output without an outside check?"** Asked of the whole project, it surfaces:

- **Cap the self-fed share of every brainstorm pack** — FIX — value 5 — effort S — risk low — category: learner hygiene
  Why: this pack's "Ideas so far" is mostly earlier brainstorm output. That is the T-2554 failure (a learner reading its own writes), and it explains the repeats.
  Done when: `fm ideas` prints each pack's share of text that came from earlier brainstorm output and refuses above a set ceiling, tested with a fixture pack.

- **Replay recorded hook inputs through old and new library on every upgrade** — FEATURE — value 5 — effort M — risk low — category: upgrade safety
  Why: the user caught a hook-import fallback bug (FIX on non-tool events) and asks for the commit behind each growth. Nothing shows what behaviour changed.
  Done when: after an upgrade, `fm doctor` lists hooks whose output differs between the two versions on the last 200 recorded inputs, and a planted rule change appears in the list.

- **Classify every state file as rebuildable or irreplaceable, and back up only the latter** — SECURITY — value 4 — effort M — risk low — category: durability
  Why: the working directory is under `/run/user`, which is tmpfs. The calibration ledger and dropped ledger look unrebuildable, and the user already steered on tmpfs-only paths. Assumption: no backup exists today.
  Done when: a test deletes every rebuildable file and the system recovers, and `fm doctor` WARNs on any irreplaceable file with no copy.

- **Score Foreman's own tests by mutation on the lines a task changed** — CLEAN — value 4 — effort M — risk med — category: test truth
  Why: three "breakage ahead" false alarms and the steer that test premises must not silently flip show that test-versus-code pairing is guessed, not measured.
  Done when: `fm task finish` reports surviving mutants on changed lines, and a deliberately hollow test is flagged.

- **Make every refusal print the repair command** — FEATURE — value 4 — effort S — risk low — category: developer experience
  Why: T-2547 added a refusal (`fm genesis put`). A refusal that names no next step costs the user a question.
  Done when: a lint walks every refusal path and fails on any that prints no runnable command.

- **Audit immunodominance: the share of injected notes per emitter** — PERFORMANCE — value 3 — effort S — risk low — category: noise
  Why: T-2533 added per-call note counting, and context runs about 387k per reply. One loud emitter can starve the rest. Assumption: the split is skewed.
  Done when: `fm cost` names the emitter with more than 40% of notes, and ablating it in a duel is offered as a candidate.

- **Snapshot the `--json` schema of every verb and fail on silent change** — CLEAN — value 3 — effort S — risk low — category: contracts
  Why: the user asked for reliability bins in `fm outcomes` JSON, and the web UI and other harnesses read it.
  Done when: a schema file per verb is committed and a changed key fails the suite unless the schema version is bumped.

- **Check that an imprinted lesson stops being recalled** — FIX — value 4 — effort M — risk med — category: lessons
  Why: this is "original antigenic sin". A lesson recalled per file can be applied while a variant of the failure repeats, and nothing marks it as misleading. Assumption: lessons carry no recurrence-after-recall field.
  Done when: a fixture with a recalled lesson followed by a same-file failure demotes the lesson and shows "imprinted" in the lessons list.

- **Declare immune-privileged paths with an expiry** — SECURITY — value 3 — effort S — risk med — category: guard
  Why: scratch and children directories are implicitly exempt today (assumption). In the immune system, privileged sites are explicit, and an unlisted exemption is a hole.
  Done when: exemptions live in one file, each with a reason and expiry, and the guard reports any exemption it uses.

- **Grade the calibration ledger against ground truth** — FEATURE — value 4 — effort M — risk low — category: gauge trust
  Why: this answers the open question on checking gauges. The Brier scores come from bets Foreman states and settles itself.
  Done when: a sample of 20 settled bets is re-settled from git and CI independently, and `fm outcomes` shows the disagreement rate.

- **Wild: Add a placebo nudge arm** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: wild. The acted-on rate of a real nudge has no baseline. A harmless, content-free note shown at the same rate shows what users act on out of habit.
  Done when: trigger precision is reported net of the placebo acted-on rate.

- **Wild: Build an idiotypic watcher that infers dead sensors from correlation** — FEATURE — value 4 — effort L — risk med — category: liveness
  Why: wild. Detectors that usually fire together are tracked, and one going silent while its partners fire is flagged. This catches silent failures that no beat check anticipated (T-2542 only covers timers).
  Done when: disabling one detector in a replay of the corpus raises a "silent partner" finding.

- **Wild: Check graft compatibility before importing a lesson or steer pack** — SECURITY — value 3 — effort M — risk low — category: portability
  Why: wild. Imported packs should be matched for host version, stack and conventions before taking, as in transplant matching. This extends shared-signature ideas.
  Done when: importing a pack from a mismatched fixture repo is refused with the named mismatch.

Answers to leftover questions: the learners never tested with poison are the brainstorm packs (above, the self-feed share) and captures from tests. The gauge the user most likely acts on is calibration, which has no ground-truth check (above).

Next question: which Foreman output does the user read that was never compared against what actually happened afterward?
Next question: which learner or gate has a dependency on host behaviour that only a host update would reveal?

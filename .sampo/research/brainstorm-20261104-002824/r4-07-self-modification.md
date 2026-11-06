# Brainstorm — lens: self-modification

- **Stack self-edits as an independently removable patch quilt** — FEATURE — value 4 — effort M — risk med — category: self-edit
  Why: the pack's many self-edit ideas (leases, per-edit revert, bisect, overlays) all assume a single edit can be dropped cleanly. Nothing says edits are stored in a form that lets that happen. Assumption: today they land as ordinary commits on shared files.
  Done when: `fm self quilt` lists the live self-edits as ordered patches on a pristine base, dropping any one passes the ship gate in a scratch home, and a simulated upgrade reports which patches rebased and which were dropped.

- **Require a mandate on every self-edit** — FEATURE — value 4 — effort S — risk low — category: self-edit
  Why: the standing intent sits over every steer, and the pack asks for "evidence" per edit but never for a source. Assumption: edits can currently land with only a measure.
  Done when: the ship gate fails a self-edit commit that lacks a trailer citing a steer id, a user-message id or a ledger event, and the cited id must resolve.

- **Stamp an edit epoch on every injected line and ledger row** — FEATURE — value 4 — effort M — risk low — category: provenance
  Why: "Stamp the instrument version" and "Stamp records written under a pinned clock" exist, but nothing joins an injected note or a model behaviour back to the self-edit that produced it. Without that, a regression can't be blamed on an edit.
  Done when: `fm self why "<line>"` prints the edit id, its mandate and the Exam reading it was meant to move, for any line in the anticipation card, a skill or a steer.

- **Roll overnight edits out to a third of sessions first** — FEATURE — value 3 — effort M — risk med — category: staged rollout
  Why: edits applied overnight take effect for everything at once, and the user is asleep. Existing ideas gate edits before landing (cold read, holdout week) but not during the first days live.
  Done when: a new edit applies to sessions where hash(session) mod 3 == 0 for 3 days, and `fm self canary` prints a re-ask and interrupt comparison between the two arms before auto-promoting or reverting.

- **Compute the judge closure by tracing, and freeze it** — SECURITY — value 5 — effort M — risk med — category: self-edit safety
  Why: "Freeze the judge" and "Freeze the safety core by path" rely on a hand-kept path list. A self-edit can reach a judge through a file nobody listed, such as a charter, an import or a data file the guard reads.
  Done when: a traced run of the guard, Exam runner and cold-read produces a file set, and a self-edit touching any file in it is refused. A planted edit to an unlisted file the guard reads is also refused.

- **Write self-edits to a sidecar when the user hand-edited the file** — FIX — value 4 — effort S — risk low — category: ownership
  Why: "Hand wins" is noted generally, but nothing records which skill, steer or template files the user has changed. Assumption: self-edits would overwrite them.
  Done when: install stores a content hash per shipped text file, and a self-edit aimed at a file whose hash differs is written as a sidecar proposal plus a morning-card line, never in place.

- **Cold-read self-edits locally first, on a redacted evidence pack** — SECURITY — value 4 — effort M — risk low — category: privacy
  Why: the cold-read rule sends tower files to Haiku, then Sonnet, and edit evidence includes the user's verbatim asks. The standing steers favour the 27B on the user's own server.
  Done when: the evidence pack is built from a field allowlist, and the 27B reads it first. Only a non-pass escalates to the cloud, and `fm self pack --dry` shows exactly what would leave the machine.

- **Make red-first cases accumulate as a scar bank across edits** — FEATURE — value 4 — effort M — risk med — category: regression
  Why: "Every missed prediction becomes a red test" covers misses. It doesn't cover edit A's case failing on a later edit B, which is where self-modifying systems drift.
  Done when: each self-edit lands with a case that fails on the pre-edit tree. Every later edit runs the whole bank, and a planted edit that undoes an earlier case is rejected.

- **Feed cold-read FAIL history back into the writers' prompts** — FEATURE — value 3 — effort M — risk med — category: self-tuning
  Why: every tower file gets a cold read, and failures go back to the writer, but nothing aggregates what the readers keep rejecting. Assumption: the same failure classes recur.
  Done when: the top three recurring FAIL reasons are added to the writer prompt through a normal edit, and the first-pass cold-read rate on the next 20 files is reported against the prior 20.

- **Cap edit proposals by surface using the user's accept rate** — FEATURE — value 3 — effort S — risk low — category: edit taste
  Why: the morning digest allows a per-edit revert, but nothing learns which kinds of edit the user never keeps. Related: "Learn which draft fields the user rewrites."
  Done when: proposals per surface (skill text, scaffold, params, template) are throttled when the 14-day keep rate is below the median, and the throttle is shown in `fm self`.

- **Wild: Pause self-modification when nobody reads the morning card** — FEATURE — value 4 — effort S — risk low — category: unattended safety
  Why: assumption: an overnight editor with no reader for days is a pure risk. Existing ideas bound the edit rate by revert rate, not by whether anyone is watching.
  Done when: after N days without the card being opened (a recorded read), new edits queue as proposals only, and the first read releases them. The pause shows in the status line.

- **Wild: Paraphrase-sweep every steer to find brittle wording** — FEATURE — value 3 — effort M — risk low — category: robustness
  Why: the pack hunts loopholes in steers but doesn't test whether compliance depends on exact phrasing, and the local 27B is cheap enough to run 10 paraphrases per rule overnight.
  Done when: a fixed behaviour probe runs per steer under ten rewordings, steers whose compliance varies by more than a set margin are listed, and a rewrite is proposed for the worst.

- **Wild: Revert roulette, a monthly drill that drops a random live self-edit** — CLEAN — value 3 — effort S — risk low — category: reversibility
  Why: "Bisect self-edits" and per-edit revert exist as ideas, but nobody proves they work on an old edit with newer ones stacked above it.
  Done when: the drill drops one random edit in a scratch home, runs the gates, and reports pass or the dependent edit that broke.

- **Wild: Ship each edit with a sealed "you'll notice this" sentence** — FEATURE — value 3 — effort S — risk low — category: legibility
  Why: assumption: the user can't audit diffs of their own prompts, but they can say whether they noticed a change.
  Done when: each edit carries a one-line expected user-visible effect, and the morning card asks keep, meh or undo against it. The answers feed the accept-rate cap above.

Next question: which of Sampo's own text files (skills, templates, steers, charters) does the user hand-edit today, and should a self-edit ever touch those?
Next question: what is the smallest recorded signal that a human actually read the morning card, rather than the page merely being opened?

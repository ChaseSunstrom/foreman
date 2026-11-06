# Brainstorm — lens: night shift: what runs unattended while the user sleeps and leaves proven, ranked, ready-to-merge lanes by morning

Answering one earlier question first: a project is finished, not just dry, when the inspected-ground ledger (idea 4) shows every file swept by every finder with zero proven findings over N consecutive nights.

- **Hunt with a plain-Claude arm first, finders as prefilter** — FEATURE — value 5 — effort M — risk med — category: finders
  Why: the exam found 0 of 108 planted defects for the deterministic finders, while plain Claude finds and fixes 3/3 held-out bugs at about 0.17 USD each.
  Done when: on the held-out exam, the night shift's hunt stage recalls more `bug` defects than `fmdocs.scan` plus `fmsecrets` did, and the receipt shows cost per proven finding.

- **Rehearse on a rotating held-out repo before the real shift** — FEATURE — value 4 — effort M — risk low — category: trust gate
  Why: the mission is graded on never-seen repos. A shift that ran blind last night shouldn't get lane budget tonight. Assumption: a small planted-defect corpus can ship with the plugin.
  Done when: a rehearsal precision below the configured floor makes that night's shift report-only, and `fm night` prints the rehearsal score.

- **Keep an inspected-ground ledger so each night sweeps new ground** — FEATURE — value 4 — effort M — risk low — category: coverage
  Why: the same hot files get rescanned every night, and "found nothing" is not currently tied to what was covered. Assumption: file hash plus finder name is a workable key.
  Done when: night 2 on an unchanged repo spends its budget only on files or finders night 1 did not cover, and `fm night coverage` lists the gaps.

- **Merge findings that share a root cause into one lane** — FEATURE — value 4 — effort M — risk med — category: pipeline
  Why: PARALLEL_MAX is 3, and three symptoms of one bug should not burn three lanes or produce conflicting fixes. Assumption: the same changed symbol or the same failing frame is a good-enough signal.
  Done when: two findings whose fix touches the same function become one lane with two failing tests, and the receipt names both.

- **Minimize each fix by deleting hunks until the proof turns red** — FEATURE — value 4 — effort M — risk low — category: fix quality
  Why: the pack lists "cap fix size" and "reject hardcoded fixes", but nothing shrinks a fix that is already green. Small diffs are the ones a sleepy reviewer merges.
  Done when: a lane whose fix has an unneeded hunk lands with that hunk removed, and the proof pair still passes.

- **Shrink the failing test to a minimal repro before the fixer sees it** — FEATURE — value 3 — effort M — risk low — category: proof
  Why: a lane that takes the failing test as its whole prompt does better with a small test. Assumption: delta-debugging the test body is cheaper than a failed lane.
  Done when: a finding's test fails for the same reason after reduction, and its line count is at most the original's.

- **Wind down in the last hour: re-prove every lane on a fresh clone, then park** — FEATURE — value 4 — effort M — risk low — category: reliability
  Why: a lane proven at 2am may be stale or env-dependent by morning. Assumption: the user sets a wake time.
  Done when: no lane starts within 60 minutes of the wake time, each remaining lane is re-run from a clean checkout, and the card marks failures "parked" rather than "ready".

- **Freeze the shift on demand and print what is merge-ready now** — FEATURE — value 3 — effort S — risk low — category: control
  Why: users wake at odd hours or sit down early, and a half-finished night should still hand over something usable. Assumption: lanes can checkpoint at step boundaries.
  Done when: `fm night now` stops new lanes, waits for the running proofs, and lists ready lanes within a bounded time.

- **Wake the user only for a proven critical** — SECURITY — value 3 — effort S — risk med — category: alerting
  Why: the shift is silent by design, but a finding with a working exploit is worth interrupting for. Assumption: "critical" needs a runnable exploit test plus a second witness.
  Done when: a planted exploitable vulnerability triggers one local notification, and every other finding kind stays silent.

- **Ship a proof bundle that runs without Foreman** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: the user shouldn't have to trust fm to check fm. Assumption: one script per lane that applies nothing and just runs the before and after commands.
  Done when: each ready lane has a `prove.sh` that, run on a clean clone, shows red without the diff and green with it.

- **Stack overlapping lanes into a proven chain** — FEATURE — value 3 — effort M — risk med — category: lanes
  Why: lanes that touch the same file conflict at merge. Chaining them, each proven atop the last, saves a morning of rebasing. This differs from rebasing one finished lane.
  Done when: two findings in one file produce lane B based on lane A, and B's proof passes with A applied.

- **Learn how to run a single test in an unfamiliar stack in the first minutes of the night** — FEATURE — value 3 — effort M — risk med — category: proof
  Why: the exam spans python, js, ts, ruby, rust and c, and a finding is worthless if the repo's test command can't be found. Assumption: probing manifests and CI files finds it for most stacks.
  Done when: on six fixture repos in different languages, the shift derives a working one-test command, or says "cannot prove here" with the reason.

- **Wild: Pit the night shift against plain Claude on your own repo** — FEATURE — value 4 — effort L — risk med — category: duel
  Why: wild; the duel (T-1231) is not yet run on the user's real code. Each arm gets half the budget on the same repo, and both go through the same proof gate.
  Done when: the morning card shows proven findings and cost for each arm, and the next night's budget split follows the winner.

- **Wild: Retry unproven hunches across nights and accrue evidence** — FEATURE — value 3 — effort M — risk low — category: patience
  Why: wild; a flaky or ambiguous finding dropped on night 1 is evidence. A fresh seed, clock and load on later nights can promote it to proven or retire it.
  Done when: a planted rare-flake test unprovable on night 1 is promoted by night N with its reproduction count in the receipt.

- **Wild: Read the morning card aloud as a 60-second local briefing** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild; the user wakes to audio, not a terminal. Local TTS keeps it on the owner's hardware. Assumption: a local TTS engine is installed.
  Done when: `fm night brief --speak` produces an audio file under 60 seconds that names each ready lane in rank order, with nothing sent off-machine.

Next question: What does a merged night lane's 30-day survival (`fm outcomes`) say about which finder kinds deserve tomorrow's budget?
Next question: Which parts of a night shift can the user not verify in the morning in under ten minutes, and what would make them verifiable?

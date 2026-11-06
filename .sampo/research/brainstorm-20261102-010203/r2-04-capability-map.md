# Brainstorm — lens: capability map

Capability-map lens, immune systems. Nothing here repeats the clonal-selection, thymus, anergy, fever, T-reg, memory-cell, MHC, inflammation or vaccination ideas already listed. "Prior art" is from my own knowledge, not a search.

- **Patrol for missing self** — FEATURE — value 4 — effort M — risk low — category: provenance
  Why: assumption: NK cells kill cells that lack the self marker, not cells that look foreign. Foreman guards against bad actions but never asks what in the repo has no known author.
  Prior art: none found; harnesses audit actions, not unattributed artifacts. Better by: every commit, task and file change must trace to a user, a lane or a trigger, and unstamped changes are flagged. Novelty: 4.
  Done when: a commit made by a hand-run script with no lane trailer appears in the next `fm doctor` as "unowned".

- **Mark immune-privileged sites** — FEATURE — value 3 — effort S — risk low — category: noise
  Why: the false-positive pair in the brief guard and the dropped "breakage ahead" alarms show detectors firing where harm cannot occur. The eye and brain suppress immunity because the reaction there costs more than the pathogen.
  Prior art: ignore files exist, but they are static and not per-detector. Better by: a path list, learned from dropped alarms, where nudges and cold reads stay silent while the hard guard still applies. Novelty: 3.
  Done when: a nudge-silenced path produces no note in a replay, and a destructive command there is still blocked.

- **Require sustained signal before acting** — FEATURE — value 4 — effort M — risk med — category: noise
  Why: noisy triggers are demoted after the fact. Kinetic proofreading instead makes a receptor act only after a signal persists through several steps.
  Prior art: debounce and flaky-test reruns, applied to events, not to detector confidence. Better by: a warning escalates only if the same signature survives N more turns or reruns. This differs from two-signal anergy, which needs a second kind of evidence, not time. Novelty: 3.
  Done when: a one-turn blip never surfaces and a three-turn persistent one does, on a replay fixture.

- **Register commensals and alarm on overgrowth** — FEATURE — value 3 — effort M — risk low — category: tolerance
  Why: assumption: some oddities (a slow test, a noisy warning) are habitually benign. A registry of tolerated oddities, each with a baseline rate, can flag dysbiosis when one grows beyond its baseline.
  Prior art: lint baselines and flake ledgers, which only suppress. Better by: it tolerates and watches the tolerated thing. Novelty: 4.
  Done when: a tolerated warning that triples in count is surfaced once with its baseline.

- **Check recalled lessons for imprinting** — FIX — value 4 — effort M — risk low — category: memory
  Why: original antigenic sin is old memory misfiring on a drifted variant. Lessons are recalled per file, and nothing checks that the new failure still matches the old one.
  Prior art: none found; memory tools recall without verifying fit. Better by: each recalled lesson carries its original signature, and a mismatch demotes it for that task. Novelty: 4.
  Done when: a lesson whose error text no longer matches is shown as "possibly stale" in a replay.

- **Tag suspect hunks and carry the tag downstream** — FEATURE — value 4 — effort M — risk low — category: review
  Why: opsonins coat a target so that every later cell attends to it. Detectors, the cold reader, tests and ship each look at the diff separately today.
  Prior art: SARIF annotations, which are per tool, not shared. Better by: one hunk-level tag channel in which a guard note or flaky rerun marks lines and the cold reader and ship gate read it. Novelty: 3.
  Done when: a hunk tagged by the guard is cited in the cold reader's input.

- **Census the repertoire against current behaviour** — FEATURE — value 4 — effort M — risk low — category: coverage
  Why: the guard is 124 labelled cases, but the host's tool surface drifts. Repertoire sequencing counts which distinct tool-call shapes appear in recent sessions with no rule or case near them.
  Prior art: none found. Better by: it measures holes in coverage from live traffic instead of from the rules. Novelty: 4.
  Done when: `fm doctor` lists the top uncovered call shapes from the last 30 days.

- **Boost old lessons on a schedule** — FEATURE — value 3 — effort M — risk low — category: memory
  Why: immunity wanes without boosters. The pack shows lessons recalled but never re-tested against the failure that created them.
  Prior art: none found. Better by: the night tick replays a lesson's original failure in a scratch clone and retires the lesson if the failure is gone. Novelty: 3.
  Done when: a lesson whose failure no longer reproduces is proposed for retirement.

- **Exhaust chronically ignored detectors** — FEATURE — value 3 — effort S — risk low — category: noise
  Why: chronic stimulation exhausts T-cells, and checkpoints keep them from spending themselves. Trigger demotion exists, but nudges and lessons are not tracked the same way.
  Prior art: alert fatigue dashboards, which only report it. Better by: a detector ignored N times drops to a quiet state with a recovery timer and wakes only on new evidence. Novelty: 2.
  Done when: a nudge ignored five times goes silent and returns when its signature changes.

- **Wild: build an idiotypic network of detectors** — FEATURE — value 3 — effort L — risk med — category: meta
  Why: wild. In Jerne's network, antibodies recognise antibodies. A detector that watches the other detectors would notice when two always co-fire, when one only ever follows another, or when one silences another.
  Prior art: none found. Better by: redundancy and dependency become measured, so the weakest detector can be deleted with evidence. Novelty: 5.
  Done when: a co-fire matrix over a month of events names one redundant pair.

- **Wild: send idle lanes toward the hot file by chemotaxis** — FEATURE — value 3 — effort L — risk med — category: orchestration
  Why: wild. Immune cells follow cytokine gradients to the damage site. Failure signals (red CI, reverts, guard blocks) per path could form a gradient that steers spare lane capacity.
  Prior art: priority queues, which have no spatial gradient. Better by: unattended lanes pick their next target by decayed damage density. Novelty: 4.
  Done when: with two idle lanes, the next captured tasks are the files with the highest decayed damage score.

- **Wild: hypermutate failing tests** — FEATURE — value 4 — effort L — risk med — category: testing
  Why: wild. B-cells mutate at a high rate and the best binders survive. Foreman mutates guard rules, but a failing test's neighbours are untouched.
  Prior art: mutation testing, which mutates source, not failing inputs. Better by: the night tick generates variants of a red test's input, keeps the ones that also fail, and files them as one root-cause family. Novelty: 4.
  Done when: one red test yields at least two kept variants attached to the same task.

Next question: which of Foreman's detectors have never been compared to each other, so that nobody knows which are redundant?
Next question: what does Foreman do about artifacts it did not author or stamp, such as hand edits or other tools' commits?

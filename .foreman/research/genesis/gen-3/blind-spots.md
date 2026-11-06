# Blind spots — gen 3

Hunted from inputs Foreman didn't author: this session's replay (builders' reports set against the project's live
state, the cold reads that refused true lines, a kill test's first run), fm risk's guard collisions, and the gen-3
review on a stronger model (fable reading Opus's Missions). The user sent no new steer this generation, so there is no
steer class; the two standing rules added since the seed (MOONSHOT.md parts A and B) are in drift.md. Each class names
its source, the rule it gives (recorded with fm decide --check) and the check that holds the rule.

## Built for state that isn't there
- Source: Mission 7's builders passed their tests, then did nothing on this project: the pile line grouped none of
  44 blocked tasks (their waits are in block reasons, not depends_on or asks; T-2683), and a notify recorder serves a
  command no project sets (T-2684). Review caught both only by running the code on real state.
- Rule: A feature that reads project state is run once on this project's live state before it closes, and its audit
  says what it printed there.
- Check: python3 plugin/tests/run.py test_foresight

## A drive rule tested only on a clean repo
- Source: T-2682's ship step fired only when the stage was idle, and with a Genesis tower open the stage is always
  "genesis", so on the project it was built for it never fired; its tests built a repo with no tower (T-2722).
- Rule: A test of a drive or next-action rule also runs with the project's standing state on: an open tower, a
  mandate, a lane.
- Check: python3 plugin/tests/run.py test_ship_next

## Evidence that keeps only the newest row
- Source: the cold read refused a true gen-2 lineage line three times. Its exam evidence kept one line per run and
  agent, so gen 3's grade on the same run hid gen 2's (T-2693).
- Rule: Evidence handed to a judge keeps every row the judged text can cite; a newer row replaces only a row of the
  same subject.
- Check: python3 plugin/tests/run.py test_genesis

## A rule met to the letter
- Source: T-2674 required a canary before any "not found", and Mission 7's grounding met it with "def main" on 156 of
  169 verdicts, a term any search finds (T-2686).
- Rule: A rule that asks for a proof checks what the proof says, not only that it is there.
- Check: python3 plugin/tests/run.py test_brainstorm_skill

## Far domain, clinical trials: the sampling plan written before the data
- Source: M-12's first kill run drew its held closes from windows that had ended, all T-0014 to T-0198, while its
  failures spanned T-0087 to T-2542; era leaked into the label (base-rate AUC 0.08). Trials pre-register how arms are
  drawn for exactly this reason.
- Rule: A kill test states how each class is drawn, in the script, before its first run, and pairs or stratifies the
  classes so they share an era.
- Check: python3 plugin/tests/run.py test_moonshot_bench

## Inversion: what would make a generation look better while it isn't
- Source: gen 3 added 5,482 lines while its only foreman grade, a 3-scenario Haiku smoke run (s32-015), went from 3 of
  3 with no false alarms to 2 of 3 with 2. Two of its numbers moved by recount, not proof: docs 601 → 421 under a
  narrower rule (T-2616) and the long tier's failures relabelled by reach (T-2613). Select reverted gen 3
  provisionally; a smoke run can't settle it, and the production-model exam at the end of the run confirms or
  reverses it (lineage.md).
- Rule: Lines built never stand in for a grade: select keeps a generation only on more train scenarios closed, a smoke
  run's verdict stays provisional until the production exam, and a number that moves because its counting rule
  changed is reported as a recount.
- Check: python3 plugin/tests/run.py test_genesis

# Blind spots — gen 2

Hunted from inputs Foreman didn't author: this session's replay (a drive line's loop), the host's own journal, CI and
the release push, and the gen-2 review on a stronger model. Each class names its source, the rule it gives (recorded
with fm decide --check) and the check that holds the rule.

## Readers that write
- Source: this session's replay: three `fm loop round --next` calls, made only to re-read a round's brief, ended two
  rounds dry and switched the forever loop off (T-2569).
- Rule: A command a drive line names may be called again: a repeat within minutes must not advance state.
- Check: python3 plugin/tests/run.py test_loop

## Options that drop repeats
- Source: `fm genesis review --handle` given 13 times in one call applied only the last; 12 handlings were dropped
  without a word (T-2592).
- Rule: An option a session repeats takes every value, and each is checked before any applies.
- Check: python3 plugin/tests/run.py test_genesis.GenerationReview

## Two paths into one branch, tested apart
- Source: release 1.2.51's push conflicted: fm ship lands commits on main as cherry-picks, fm release merges, and each
  path's tests had passed alone (T-2598).
- Rule: Every path that lands on main is tested against a main the other paths have fed.
- Check: python3 plugin/tests/run.py test_release.LandAfterShips

## Tests that read the host
- Source: the full gate failed on this machine's real night timer: the foresight tests read ~/.config/systemd/user
  through fmnight.liveness (fixed under T-2569).
- Rule: Tests never read the host's own services or config; they point XDG_CONFIG_HOME and HOME at their temp folder.
- Check: python3 plugin/tests/run.py test_foresight

## A deliberate skip that reads as failure
- Source: journalctl on the host: the night service exited 1 each time it skipped for high usage, so fm doctor and
  foresight reported a working timer as failed (T-2593).
- Rule: A scheduled run that skips on purpose exits 0 and says why.
- Check: python3 plugin/tests/run.py test_night

## Numbers without their denominator
- Source: the gen-2 cross-cutting review (Fable reading Opus's Missions): "held" counted closes still inside their
  window, a model arm scored 0/0, and rates were quoted without their counts (T-2594, T-2591).
- Rule: A rate counts only finished observations and names its count and baseline; an arm with no answers reads not run.
- Check: python3 plugin/tests/run.py test_outcomes

## Inversion: what would make Foreman look done while it isn't
- Source: the long-horizon tier (l001, l002): the foreman arm claimed done on 6 of 6 goals it failed, while plain
  managed 1 of 6.
- Rule: A done claim on a goal is checked against each line of its stated Done-when before it reads as finished.
- Check: python3 plugin/tests/run.py test_goal

## Far domain: aviation's sterile cockpit
- Source: the gen-2 review's complaint that the session-start note ran past the project's own trim rule; aviation
  forbids non-essential talk below 10,000 feet, because attention spent at a critical moment is lost to the task.
- Rule: The note that opens a session fits one 1,500-character budget with everything appended counted.
- Check: python3 plugin/tests/run.py test_hooks.SessionStart

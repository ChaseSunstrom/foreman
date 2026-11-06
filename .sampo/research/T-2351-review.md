T-2351 review (fm-reviewer, one pass): changes needed; fixed before close (new tests written with the fixes).
HIGH fixed: the didn't-hold FIX (source trial) logged sightings and got its own trial, a self-feeding loop on every digest: trial is in NO_TRIAL and verdicts are stored, so a settled trial is never regraded.
MEDIUM fixed: the authored check read source, so ci-red, did-not-hold, recurring-failure and capability-miss (filed as discovered) never registered: the check reads the trigger.
MEDIUM fixed: CI keys were run URLs (never recur): capture_once takes trial_key; fmci keys on branch+workflow, fmforesight on branch+failed jobs.
MEDIUM fixed: github issues re-polled while open read as recurrences: github, spec, cross-project are in NO_TRIAL.
MEDIUM fixed: fm trial and fm triggers could file briefs and write the ledger: only the digest (act=True) files and stores; held_fixes reads stored verdicts.
MEDIUM fixed: the digest showed only the last 8 trials: every unsettled self-fix is shown and graded.
MEDIUM fixed: lock/OS errors crashed the digest: caught per row.
LOW fixed: keyless captures keyed on the 90-char title: the full first line.
Open: the 14-day clock starts at the close (after the lane merge in this flow).

# Brainstorm — lens: unspoken needs: what the user would ask for next without knowing it

- **Rank the inbox by what the user has actually re-asked for** — FEATURE — value 4 — effort S — risk low — category: prioritization
  Why: the user keeps restating the same needs (speed without quality loss, "recursively improve", token savings only against overuse), yet the inbox still holds 7 planned items and the idea list is hundreds long. Assumption: no ranking by repeat-request frequency exists today.
  Done when: `fm inbox --by-asks` lists each open item with the count of user messages it traces to, and a test with a fixture ledger shows the most-asked item first.

- **Report pass yield, not pass count** — FEATURE — value 5 — effort M — risk low — category: self-improvement
  Why: the user asked for "numerous multiple passes" and "recursive improvements", but pass 5 ended with no measure of whether any pass made Foreman better. Review still finds 3–8 issues per batch. Assumption: bench results and friction counts can be diffed between passes.
  Done when: `fm pass report` prints, per pass, bench pass-rate delta, friction items closed, escapes since, and reviewer findings per batch. A fixture with two passes prints both rows.

- **Stop the idle wait on reviewers by parking the batch** — PERFORMANCE — value 4 — effort M — risk med — category: speed
  Why: friction lists ~1–2 min idle per review pass and 31+ drive stops on a background reviewer; the user asked for speed "without sacrificing quality". Assumption: the drive can start the next queued brief while a review is pending, with the close blocked until the verdict lands.
  Done when: in a drive test with a stub reviewer that takes 60 s, the next task's first edit happens before the reviewer returns, and the earlier task cannot close until it does.

- **Ship `fm guard check '<cmd>'` and have the hook call it** — FEATURE — value 3 — effort S — risk low — category: guard
  Why: friction notes the ad-hoc hook probe took several tries because the hook wants argv[1] as the event name. Pass 5 added `fm replay --cmd`, so check whether this is just an alias. If so, merge it rather than add a verb.
  Done when: `fm guard check 'git -c core.fsmonitor=x status'` prints allow or block with the category and exits 0 or 2 accordingly, and the hook path shares the same function (one test asserts both).

- **Make the pre-audit patterns live in a data file the scanner skips** — CLEAN — value 3 — effort S — risk low — category: audit
  Why: friction says the pre-audit's security patterns match their own regex source, so the file defining them is flagged as network code. A data file with a non-code extension would end that and give one place to tune.
  Done when: a suite test shows the pattern file is not flagged by the pre-audit, and a pattern added to the data file fires on a fixture without a code change.

- **Close the loop on user steers: show which steer changed which behavior** — FEATURE — value 4 — effort M — risk low — category: trust
  Why: the user steered "learn — record which routed skills were used and whether the task closed first time" and has corrected verify commands several times. Assumption: they would want to see that those corrections persisted instead of repeating them.
  Done when: `fm steers` lists each steer with the file, lesson or routing entry it altered, and a steer with no recorded effect is flagged "unapplied".

- **Wild: Let Foreman rehearse the user's next three asks overnight as ghost briefs** — FEATURE — value 4 — effort L — risk med — category: anticipation
  Why: wild; the user's requests form a pattern (feature, then speed, then "improve yourself again"). Assumption: ghost briefs would be written under the existing budget caps and discarded unless the user approves one.
  Done when: `fm ghost` writes up to three unapproved briefs from the ledger and recent steers, each marked `ghost`, none editable by hooks until accepted, and spend appears in `fm budget`.

- **Wild: Run an "ablation week" where each pass switches off one feature and benches the loss** — FEATURE — value 4 — effort L — risk med — category: pruning
  Why: wild; the idea list repeats modules-and-ablation many times, but nothing measures what the day's pile of features earns. The user asked for "groundbreaking", and the pile only helps if each part pays.
  Done when: `fm ablate NAME` disables one named module via config, reruns `fm bench`, and prints the pass-rate and cost change. A fixture with a deliberately useless module reports "no loss".

- **Wild: Give the user a one-line "was this pass worth it?" verdict from Foreman itself** — FEATURE — value 3 — effort M — risk low — category: honesty
  Why: wild; after many passes the user can't tell whether Foreman is really getting better. Foreman could say plainly when a pass's yield falls below noise and propose stopping, which fits the existing convergence-stop idea.
  Done when: after a pass with zero bench delta and zero closed friction items, `fm pass report` ends with "diminishing returns" plus the numbers, and a fixture with real gains does not print it.

- **Wild: Stranger-test Foreman's own README with a child, and score where it gets stuck** — FEATURE — value 3 — effort M — risk low — category: onboarding
  Why: wild; "stranger test" is already in the inbox. Fold it into the pass loop so every pass's new verbs are checked for discoverability, which also pressures the verb count down.
  Done when: a no-tools child given only the README must name the right verb for five scripted tasks, and the score is stored per pass, with misses listed.

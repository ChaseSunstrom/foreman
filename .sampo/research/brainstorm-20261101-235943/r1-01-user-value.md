# Brainstorm — lens: user value

- **Exclude Foreman's own test inputs from the user model** — FIX — value 4 — effort S — risk low — category: data hygiene
  Why: the dropped list has "The first brief" and "The second brief", sample lines fed to `fm intake` while debugging T-2547, which then sat in the queue as if they were asks. A model of the user trained on those would predict nonsense.
  Done when: `fm intake` refuses or tags placeholder-shaped text and anything entered under a test run, and a predictor fed the T-2547 session has zero of those rows in its training set.

- **Complete the DONE-WHEN for a raw capture** — FEATURE — value 5 — effort M — risk low — category: draft on spec
  Why: nearly every recent ask pairs a one-line need with an observable check ("> DONE-WHEN: a tick …"). The user writes the check themselves each time, and the first-pass drafts that had to be steered back were missing it. Assumption: a draft built from similar closed asks is accepted often enough to beat starting from blank.
  Done when: `fm capture` on a request with no DONE-WHEN prints a proposed one from the nearest closed asks. A backtest on the last 40 closed asks has at least a stated share accepted verbatim or with a one-clause edit.

- **Check literal tokens from the request against the built surface** — FIX — value 4 — effort S — risk low — category: correction forecast
  Why: the steer "the flag is `--by harness` (the request's wording), not `--by-harness`" and "the test uses `fm next --last` … it was no unknown flag" are two cases of the builder not matching the user's own words or an existing flag. Both are cheap to catch before the plan.
  Done when: every backticked verb or flag in a request is compared with the argparse tree at plan time. A mismatch such as `--by-harness` against `--by harness` is named, and a replay of those two cases triggers the check.

- **Draft the third ask of a series** — FEATURE — value 4 — effort M — risk med — category: next request
  Why: asks arrive in runs on one thread. T-2532 to T-2536 are all the lean ratchet and hook notes, and the bet asks (rate gap, interim reads, bins, harness split, settle with no session) all extend `fm outcomes`. After two asks on one verb family, the third is often predictable.
  Done when: closing a second task that touches a verb family files a spec-only draft of the likely next one with an expiry. A backtest over T-2400 to T-2547 gives a hit rate for the draft's title and verb family, and the draft is dropped if that rate does not beat predicting the most recent family.

- **Keep a per-machine profile of what breaks here** — FEATURE — value 4 — effort M — risk low — category: machines
  Why: the pack shows machine-specific failures: ETXTBSY on the tool grader (T-2543), no setuptools on one Python (T-2529), the missing libappindicator on Arch (T-0325), the hardened kernel, and a tmpfs children directory. Each was found only after it failed.
  Done when: `fm me --machine` lists known breakers with the task that found each. `fm next` warns before a task whose files or commands match one, and a planted ETXTBSY-prone exec produces the warning.

- **Add a web UI Anticipation page with accept and dismiss** — FEATURE — value 4 — effort M — risk low — category: web UI
  Why: the surface found is the web UI, but nothing shows what Foreman expects next. Dismissing a draft is the cleanest label for training. Assumption: one click is cheaper for the user than a typed steer.
  Done when: the page lists the predicted next ask, its draft, and flagged risks with their evidence. Accept and dismiss each write a labelled row, and a draft with a dismiss label is not offered again.

- **Flag a task that restates a dropped self-filed class** — FEATURE — value 3 — effort S — risk low — category: noise
  Why: the dropped list shows self-filed work refused with a measured reason: stack cards for 8 deps with 5 of 1219 used, the guard-only arm that was already built, and the interpreter-specific baseline at 1 of 22. A new Foreman-filed task shaped like one of those is predictably unwanted.
  Done when: before filing, the task is compared with dropped reasons by kind. A match prints "dropped before: <reason>" and holds the task, and replaying the three drops catches all three.

- **Show the lead time of each anticipation hit** — FEATURE — value 3 — effort S — risk low — category: measurement
  Why: the predictions-scored ideas count hits but not how early the draft existed. A hit after the ask is typed saves nothing, so lead time is the value measure.
  Done when: `fm doctor` shows, per prediction kind, the median hours between the draft and the matching ask, and shows hits with a draft that appeared after the ask as zero.

- **Wild: run a blind "is this the user's voice?" test on drafted asks** — FEATURE — value 3 — effort M — risk low — category: draft quality
  Why: assumption: a draft the user has to rewrite costs more than one they never see. A tool-less child shown a mix of real asks and drafts, with no labels, should not be able to tell them apart. That gives a free score for tone, verb-first form and DONE-WHEN style, without the user.
  Done when: a draft ships only if the child's accuracy at telling it from real asks stays below a set threshold on 20 pairs.

- **Wild: turn a typed correction into a draft check before the user finishes the sentence** — FEATURE — value 3 — effort L — risk high — category: correction forecast
  Why: the steered rows show the user fixing the builder in short fragments, such as "key the session memory on id:status". Assumption: a few such patterns recur (state keys, flag names, scope) and could be matched on the first words.
  Done when: for a replay of 20 past steers, a matcher given only the first six words proposes the correct check class for at least a stated share, with false offers counted.

- **Wild: write the "sorry, already built" note before the ask is typed** — FEATURE — value 3 — effort M — risk med — category: anticipation
  Why: T-2546 catches "already built" at capture, but still after the user has spent the typing. Assumption: open-queue and `MASTER.md` overlap lets Foreman note a likely duplicate early, from the user's last two asks.
  Done when: a session-start line names any open or deferred task (such as the "Later from T-07xx" bundles) that the user's last two asks overlap, and a planted duplicate is named in a replay.

- **Wild: print a "things you will probably ask about this one" list at task close** — FEATURE — value 3 — effort S — risk low — category: next request
  Why: every closed task invites a follow-up (another harness, the doctor line, a docs line). Assumption: the user's habit of asking for per-harness and doctor-visibility follow-ups (T-2533 to T-2542) is stable enough to list.
  Done when: `fm task finish` prints up to three follow-ups, each with the past pair that suggested it, and a backtest reports how many were asked within 7 days.

Next question: Which of the 58 cells can be answered by a replay of the user's real asks, and which have no such history so the cell would be written from imagination?
Next question: Does the user ever read the output of the existing predictor, and if they never open the web UI, what do they see in a plain session?

# Brainstorm — lens: simplicity

- **Make the failing test the finding** — FEATURE — value 5 — effort M — risk low — category: pipeline
  Why: the exam shows 0/108 from the deterministic finders, while plain Claude finds and fixes 3/3 at about $0.17 each. A separate finding schema, a repro step and a ranking record add stages without adding finds. One artifact (a test file that fails on the current tree) is the finding, the proof and the fix target.
  Done when: on a seeded repo `fm scout --find` files only findings that are a test file plus its failing run output, and a finding without both is dropped.

- **Replace the finders with one headless find prompt per hot cluster** — FEATURE — value 5 — effort M — risk med — category: finders
  Why: fmdocs.scan and fmsecrets found nothing, so the bug, security, perf and flake finders should not each be new code. One `claude -p` call takes a file cluster picked by churn × no-tests and returns a candidate test. Assumption: the cost stays near plain Claude's $0.17 per find.
  Done when: on held-out repos with planted bugs, one command's find rate is at least the plain-Claude arm's, at no more than 1.2× its cost per find.

- **Let "found nothing" be a first-class, cheap result** — FEATURE — value 5 — effort S — risk low — category: precision
  Why: Mission 3 is graded on the exam's `none` kind. A finder that must produce something invents bugs. A clean run ends with one line ("looked at N files, nothing proven, $X") and files zero tasks.
  Done when: on three clean never-seen repos, `fm scout --find` files 0 tasks and exits 0.

- **Drop findings that can't be proven, with no ranking rescue** — FIX — value 4 — effort S — risk low — category: precision
  Why: the pipeline is "proves each finding before it touches code". A suspicion with no failing test is not demoted but deleted, so the queue holds only proven work.
  Done when: a suspicion whose test passes on the current tree never appears in the backlog, and a test asserts this.

- **Rank with one number from facts already in `fm map`** — FEATURE — value 3 — effort S — risk low — category: ranking
  Why: the pack lists value ranking as missing. Use reverse-import count of the failing file × a severity word the finder must pick from three (data loss, wrong output, cosmetic). Multi-factor models need data nobody has yet. Assumption: `fm map` already exposes import counts.
  Done when: two proven findings in a fixture sort by the formula, and `fm backlog` shows the single number next to each.

- **Stop probe_doctor from queuing Foreman's own setup failures in user projects** — FIX — value 4 — effort S — risk low — category: noise
  Why: the pack's "Noticed" line. Findings in someone else's repo should be about that repo. Setup failures go to `fm doctor` output only.
  Done when: running scout in a project with a broken Foreman install files no task from probe_doctor.

- **Fold adopt, scout, deps and docs into one `fm find`** — CLEAN — value 4 — effort M — risk med — category: surface
  Why: adopt (one-shot), scout (Foreman-only probes), deps and docs each find work through separate code and verbs. One verb with one output shape removes three entry points and the "partial: adopt is manual" gap.
  Done when: `fm adopt`, `fm deps` and `fm docs` remain as aliases of `fm find` flags, and the old verb tests pass through the alias.

- **Hand the fix to a plain lane with the failing test as the whole prompt** — PERFORMANCE — value 4 — effort S — risk med — category: fix lane
  Why: T-1231 says Foreman's session costs more than plain Claude for the same score. For a proven finding, the lane gets only the test path and "make this pass without breaking the rest", and keeps only the close gate.
  Done when: on the exam's `bug` kind, cost per fix under this profile is at most plain Claude's, with the same pass rate.

- **Cap a run at three proven findings** — FEATURE — value 3 — effort S — risk low — category: budget
  Why: assumption: an unbounded scout burns budget (the $35 limit is visible in the environment) and floods the backlog. Stop at three and show the rest as "N more candidates, unproven".
  Done when: a repo with ten planted bugs yields exactly three proven tasks and one summary line about the rest.

- **Dedupe findings by test name and file hash in a plain text ledger** — FEATURE — value 3 — effort S — risk low — category: ledger
  Why: scout runs again nightly (`fm night`), so a rerun must not re-file a settled finding. One line per finding, grep-able, no database.
  Done when: running find twice on an unchanged tree files no new tasks the second time.

- **Wild: use mutation as the finder** — FEATURE — value 3 — effort L — risk med — category: finders — wild
  Why: assumption: flip one operator or boundary in a hot function and run the existing tests. A mutant that survives marks an untested line, with no model call. Only survivors go to the model, to write the test.
  Done when: on a fixture, a planted off-by-one in an untested branch is found with zero model tokens before the test-writing step.

- **Wild: reject any finding that doesn't fit in one sentence** — FEATURE — value 2 — effort S — risk low — category: precision — wild
  Why: assumption: vague findings correlate with false ones. A finding needs the wrong behaviour, the input and the expected output in one sentence, which becomes the test's name.
  Done when: findings over 200 characters or with no concrete input are refused by a lint, and the test name equals the sentence.

- **Wild: try deleting code before adding any** — FEATURE — value 2 — effort M — risk high — category: fix lane — wild
  Why: assumption: many bugs are over-special-cased branches. The lane first tries removing the offending branch and runs the proving test plus the suite. Only if that fails does it write the fix.
  Done when: on a fixture with a bad special case, the lane's diff is a pure deletion and the suite is green.

Next question: Does the find rate of one headless prompt per cluster hold on the held-out never-seen repos, or only on the repos the team tuned it on?
Next question: What is the cheapest check that a finding's failing test fails for the stated reason, not for an unrelated error such as a missing import?

# Brainstorm — lens: the recurring miss (invented): each failure, friction or user correction that recurs becomes a fix with a test, without being asked

- **Cluster user corrections by shape, not text** — FEATURE — value 5 — effort M — risk med — category: self-repair
  Why: the user's asks (T-2285, T-2288, T-2289) are the same class: a gate or verb that is right on the common case and wrong on an edge (flag-led option, scratch folder, new proof kind). T-2272 only counts failure signatures across 3+ tasks, so user corrections never join the loop.
  Done when: three recorded corrections with different wording but the same touched verb and gate produce one FIX task, and a test feeds them in and asserts exactly one task is made.

- **Turn each "what earlier brainstorms missed" ask into a regression probe** — FEATURE — value 5 — effort M — risk low — category: self-repair
  Why: the pack lists 8 asks (T-2285 to T-2327) that no brainstorm predicted. They are fixed one at a time, but nothing asks "what else in the same class is broken". Each fixed ask should leave a probe that fuzzes its neighbours (other plan-gate marker styles, other dirs the guard treats as throwaway).
  Done when: closing a user-asked FIX adds a probe file, and `fm doctor` lists the asks with no probe.

- **Require a failing-first test for every correction-born FIX** — FIX — value 4 — effort S — risk low — category: gates
  Why: Seed rule is red-first tests, but corrections arrive in prose (the "asked:" lines). assumption: some are closed with the test written after the fix.
  Done when: `fm task finish` on a task tagged `from:correction` refuses unless `fm task prove` shows the test fails on the start tree.

- **Detect the same steer being given twice** — FEATURE — value 4 — effort S — risk low — category: steers
  Why: steers are stored as standing rules, but the 2026-10-31 steers #1 and #3 restate "don't skip work for budget/pace", an earlier rule about not killing ideas. A repeat means the first check didn't bite.
  Done when: a new steer with a near-match to a stored one flags that rule's `fm decide --check` as ineffective, and a test shows the check is named in the output.

- **Score each fix by whether the miss stayed gone** — FEATURE — value 5 — effort M — risk low — category: outcomes
  Why: T-2290 scores predictions and T-2291 scores lanes, but no fix's own signature is tracked after it merges. A recurrence after the fix is the strongest signal that the fix was shallow.
  Done when: `fm outcomes` shows per fix "recurred N times since merge", and a recurrence reopens the task with the prior diff linked.

- **Sweep the same bug class across sibling code on every fix** — FEATURE — value 4 — effort M — risk med — category: self-repair
  Why: T-2285 fixed one plan-gate marker case; T-2246/T-2252 each patched one guard path. A fix task should list sibling call sites (same helper, same regex or tuple) and add a test per site.
  Done when: finishing a FIX that edits a parser or matcher writes a "siblings checked" list from `fm graph`, and a test fails if the list is empty.

- **Quarantine a fix that Haiku's cold read can't explain** — SECURITY — value 3 — effort S — risk low — category: safety
  Why: self-made fixes run unasked (Mission 8 #7), and the guard is the thing to protect. assumption: auto-fix tasks can touch guard files today.
  Done when: an auto-filed FIX whose diff touches the guard or `USER_ONLY_FM` stays open and asks the user once, with a test.

- **Make friction a first-class signal: count repeated commands and retries** — FEATURE — value 4 — effort M — risk med — category: observability
  Why: failures are tracked but friction (the same `fm` call run 3 times with changed flags, a refusal followed by a workaround) is only seen if the user complains. The "asked" list shows refusals the user had to report themselves.
  Done when: a session with a refusal followed by 2 reworded retries logs a friction event, and `fm triggers` lists it.

- **Show a weekly "misses closed vs recurred" line in fm doctor** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: the lean ratchet warns on growth, but nothing says whether self-repair is working. assumption: the data exists in outcomes.
  Done when: `fm doctor` prints the recurrence rate with the numerator and denominator, and refuses to print a rate under 5 cases.

- **Wild: Replay a user correction against the old build** — FEATURE — value 4 — effort L — risk med — category: self-repair
  Why: wild. A correction is a test case waiting to happen: check out the commit before the fix, replay the original ask, and see whether the fixed behaviour now holds. This builds the long-horizon corpus from the user's own mistakes-found, not from synthetic scenarios.
  Done when: `fm exam capture T-NNNN` produces a replayable scenario that fails on the pre-fix commit and passes on the fix.

- **Wild: Run a "mutation night" that breaks gates on purpose** — FEATURE — value 4 — effort M — risk med — category: gates
  Why: wild. Weaken one gate in a throwaway worktree (drop a check, widen a regex) and see whether any test goes red. Surviving mutants are the next missed corrections, found before the user hits them.
  Done when: a nightly run reports surviving mutants per gate and files one task per survivor, with a test using a known-weak gate fixture.

- **Wild: Let the user mark a reply "that again" with one word** — FEATURE — value 4 — effort S — risk low — category: intake
  Why: wild. The shortest form of a correction is "again". Foreman would link it to the last refusal or miss and start the cluster at once, so the user doesn't have to restate it.
  Done when: typing `again` after a refusal files a correction linked to that event, and a test asserts the link.

- **Wild: Keep a "repeat offender" board of the five verbs that cause most corrections** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild. Visible, ranked, and shrinking over time. Gives the user a sense that corrections cost something and are paid down.
  Done when: the web UI shows the ranked verbs with counts since the last month, and an empty state when none.

Next question: Which fixes Foreman made unasked were later reverted or corrected by the user, and what did those have in common?
Next question: Does a correction given in one project (e.g. a plan-gate edge) reach other projects' Foreman through the stack cards, or does it stay local?

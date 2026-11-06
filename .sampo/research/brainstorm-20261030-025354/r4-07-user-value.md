# Brainstorm — lens: user value

Earlier-question answer (finished vs dry): a repo is finished when a clean verdict holds with canary recall above its floor and the tree has had no commits for N days. A dry queue alone doesn't show that.

- **Run `fm find` in any directory with no setup** — FEATURE — value 5 — effort M — risk low — category: onboarding
  Why: assumption: the exam grades never-seen repos, and a required `fm init` is a hurdle there and for first-time users. Ephemeral state goes in a tmp dir, nothing is written to the repo, and the user cleans up nothing.
  Done when: `fm find .` in an uninitialised git repo prints a verdict and leaves `git status` clean and no `.foreman` directory behind.

- **Ask the owner where it hurts before hunting** — FEATURE — value 4 — effort S — risk low — category: intake
  Why: the pack's finders found 0 of 108 planted defects, and nothing in it uses the owner's own suspicion. One optional question ("what part scares you?") seeds the first hunt, and the receipt says "your hunch: proven / cleared".
  Done when: an answer naming a module makes the first probes target that module, and the receipt states the hunch's outcome.

- **Price each finding in the user's own closing times** — FEATURE — value 4 — effort M — risk low — category: ranking
  Why: the mission asks for ranking by value, and the ranking idea above is a generic formula. The user's closed tasks have real durations per kind, so hours saved can come from their own median for similar fixes.
  Done when: two repos with different closing histories rank the same finding set differently, and each line shows "~Xh, from your median Y for bug tasks".

- **Review the branch diff with proofs before push** — FEATURE — value 5 — effort M — risk med — category: pre-push
  Why: assumption: a diff-scoped hunt is cheaper and more relevant than whole-repo scans, and the user is already present to act on it. The output is failing tests for the diff's bugs, not comments.
  Done when: `fm find --diff main` on a branch with a planted off-by-one returns that bug as a red test in under 3 minutes, and a clean diff returns "clean".

- **Promote a finding that blocks a queued task** — FEATURE — value 4 — effort M — risk med — category: queue
  Why: Open work has dozens of deferred items. A proven bug in code a queued task will edit is a prerequisite for it, and fixing it first avoids red gates later.
  Done when: a finding in a file listed by a queued task is shown as "blocks T-xxxx" and sorts above unrelated findings of equal score.

- **Quarantine a proven flake with an owner and expiry** — FIX — value 3 — effort M — risk med — category: flakes
  Why: the mission names flake finders, but most users want red CI to stop more than they want a diagnosis. The quarantine carries a task and a date, so it can't become permanent.
  Done when: a test with a reproduced 1-in-5 failure is marked skipped with an expiry comment and a filed task, and the suite goes green.

- **State the end-user symptom for each finding** — FEATURE — value 3 — effort S — risk low — category: legibility
  Why: assumption: users triage faster on "a user typing 0 sees a crash" than on "off-by-one in `clamp`". The symptom must come from running the repro, never from prose.
  Done when: every finding card has a symptom line, and the repro's captured output contains it.

- **Mine merged-PR review comments into repo checks** — FEATURE — value 4 — effort L — risk med — category: learning
  Why: the user's recurring review remarks are a project-specific source of bug classes that no generic probe has. Each comment becomes a probe candidate only after it passes the clean-repo test.
  Done when: a repo with three review comments about unchecked `None` returns yields a probe that files one more instance, with a proof.

- **Give a passing pin test when the verdict is clean** — FEATURE — value 3 — effort M — risk low — category: consolation
  Why: "nothing found" gives the user nothing to keep. A characterization test for the most-changed untested function is a small durable gain. It is labelled as a pin, never as a finding.
  Done when: a clean scan on a repo with an untested hot file adds one green test for it and the receipt says "pin, not a bug".

- **Replay Foreman's proofs against another agent's diff** — FEATURE — value 4 — effort M — risk med — category: second opinion
  Why: assumption: many sessions run plain Claude, which Foreman can't steer, but it can still check the result. This turns the discipline layer into an after-the-fact verifier for any diff.
  Done when: given a plain-Claude session's final diff, `fm find --diff` reports red tests it introduced or "no regressions proven".

- **Wild: deal a bug trading card for every proven fix** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild. The card holds the test name, symptom, hours saved and the probe that caught it. Users share these cards, and the deck gives the site a live credibility page.
  Done when: closing a find task writes a card file, and the site page lists the cards with their commands.

- **Wild: paste a GitHub URL, get a proven bug and a PR draft that is never sent** — FEATURE — value 4 — effort L — risk med — category: demo
  Why: wild. It shows Foreman's value on a stranger's repo in ten minutes, and it matches the exam's never-seen repos. Draft only, nothing is sent without an explicit setting.
  Done when: `fm find <url>` clones to a tmp dir, outputs one red test and a draft markdown PR, and makes no network writes.

- **Wild: ask for "10m" and get the best ten minutes of review** — FEATURE — value 4 — effort S — risk low — category: time-boxing
  Why: wild. Users don't have unlimited attention. The morning card is trimmed to the findings whose review time (from their own closing times) fits the stated minutes, ordered by value.
  Done when: `fm find card --fit 10m` returns findings whose summed review estimate is ≤10 minutes, and the omitted ones are counted.

Next question: Which proven findings did the user ignore, and does ignoring one differ by kind, by repo age or by hour of day?
Next question: What does a user who has never seen the exam need to see before trusting a "clean" verdict on their own repo?

# Brainstorm — lens: unspoken needs

- **Check each finding's premise before it becomes a task** — FEATURE — value 5 — effort M — risk low — category: queue quality
  Why: five of the user's "dropped" items were "premise false" (the `fmbudget` tail, the ambient runner, the hook import cost), each found only after a builder or reviewer spent time on it. Assumption: review and brainstorm items can carry one falsifiable probe command.
  Done when: queueing an item from a review runs its probe, and a task whose probe contradicts the claim is auto-dropped with the output recorded. A test replays the `fmbudget` "20,000-row tail covers 12 days" claim and sees it dropped.

- **Add `fm guard why "<cmd>"`** — FEATURE — value 5 — effort S — risk low — category: debuggability
  Why: guard false positives cost the most debugging time, and the main thread twice wrote a scratch script to replay a command through the real hook (T-1125, T-1141).
  Done when: `fm guard why 'cat x | fm edit <<EOF…'` prints allow or deny, the matching rule and the cwd it used, and gives the same verdict as the real hook on 20 recorded payloads.

- **Dry-run every verify command when it is added** — FIX — value 5 — effort S — risk low — category: gates
  Why: verify commands are often wrong (a test module that doesn't exist, `npm test` with no npm) and only fail when they run; T-1128/T-1133 made them editable but nothing checks them up front.
  Done when: adding a verify command that references a missing module or binary is rejected, or warned about, with the reason, and a command that collects zero tests is flagged.

- **Build help tiers and the verb registry from per-verb metadata files** — CLEAN — value 4 — effort M — risk med — category: merge conflicts
  Why: every feature edits one `HELP_TIERS` line in `fmcli.py`, so nearly every second merge conflicted (T-1059, T-1062 twice) and needed a re-merge builder.
  Done when: two lanes that each add a verb merge with no conflict, and a test fails if `HELP_TIERS` is edited by hand instead of generated.

- **Lint builder diffs for the recurring defect classes before "done"** — SECURITY — value 4 — effort M — risk med — category: builder quality
  Why: reviewers found real defects in almost every builder branch: deny-bypass, false green, unbounded time, writes outside a folder, overwritten leases. Assumption: a static pass can catch roughly half of these (no timeout on subprocess, `open(...,'w')` without a confinement check, lease writes without O_EXCL).
  Done when: `fm lane done` runs the lint, refuses on a hit unless the builder justifies it, and the fixtures built from those five past defects are all caught.

- **Throttle lanes by load and scale criterion timeouts to it** — PERFORMANCE — value 4 — effort M — risk low — category: fleet
  Why: load reached 30-60 with 4 builders, `fm state --json` took over 120 s, and a load-sensitive criterion failed a merge once and then passed.
  Done when: the dispatcher holds a new builder while 1-minute load exceeds a per-core ceiling, and criterion timeouts stretch with load. A simulated-load test shows no spurious merge failure.

- **Yield to the human: renice builders when the user's terminal is active** — PERFORMANCE — value 3 — effort S — risk low — category: fleet
  Why: the user goes AFK and then comes back to a sluggish machine; assumption: an interactive Claude session's hook activity is detectable.
  Done when: builders run at nice 10 and drop to 19 within 5 s of a user prompt, and the setting appears in `fm doctor`.

- **Resolve builder paths against the worktree root** — FIX — value 3 — effort S — risk low — category: builder hygiene
  Why: builders `cd` into subdirectories, so relative paths double and leases end up as `mods/foreman-ui/mods/foreman-ui/...`.
  Done when: `fm lease` and `fm edit` canonicalise any path to worktree-relative, and a test with cwd in `mods/foreman-ui` produces the single correct lease path.

- **Index briefs by stat key so no verb parses all of them** — PERFORMANCE — value 4 — effort M — risk low — category: speed
  Why: T-1140 fixed hooks only; other commands still parse every one of the 1,069 briefs, and `fm state` was slow under load.
  Done when: `fm state --json` on 1,000+ briefs is under 1 s warm, and the index rebuilds after a corrupt-entry fuzz test.

- **Label every heuristic output with its measured precision** — FEATURE — value 3 — effort M — risk low — category: honesty
  Why: card backtest is a text match, history fix seeding is keyword-based, and the untrusted-text check is a keyword heuristic, with known edges that are invisible to the user.
  Done when: each of the three prints "heuristic, ~N% precision on the labelled corpus", the corpus is committed, and CI fails if precision drops more than 5 points.

- **Cut and push a release when the queue drains with green gates** — FEATURE — value 4 — effort M — risk med — category: release
  Why: the user repeatedly asks "Release 1.2.31 / 1.2.32 and push to main", and said to push "when you're done with everything too". The installed foreman-ui (0.7.0) lags the repo (0.17.0). Assumption: that standing instruction covers future drains.
  Done when: a drained queue with green gates tags, pushes and bumps the mod version with no prompt. `fm doctor` warns when the installed mod is more than 2 minors behind, and the release is skipped if any gate is red.

- **Wild: Add `fm undo --since-afk`** — FEATURE — value 4 — effort M — risk med — category: trust
  Why: the user goes fully AFK with "do everything", so a bulk undo makes that autonomy cheap to grant. Assumption: Foreman can tag a ref at the start of an unattended stretch.
  Done when: after three auto-merged tasks, one verb returns the branch to the tag and reopens those tasks with their reasons, while any non-Foreman commits made since the tag are left untouched.

- **Wild: Schedule heavy lanes into the user's learned AFK gaps** — PERFORMANCE — value 2 — effort M — risk low — category: scheduling
  Why: assumption: ledger activity gaps reveal a rhythm, so full-suite runs and brainstorms can wait for sleep or lunch.
  Done when: `fm doctor` shows the inferred quiet windows, and a heavy job queued at a busy hour starts in the next window unless forced.

- **Wild: Give each close a before/after contact sheet** — FEATURE — value 3 — effort M — risk low — category: UI proof
  Why: pillar 4 asks for before and after screenshots, and the pane wasn't screenshot-verified last round.
  Done when: closing a task that touches the pane renders the fixture states to PNGs before and after, writes a side-by-side sheet into the task's receipt, and flags any state that went blank.

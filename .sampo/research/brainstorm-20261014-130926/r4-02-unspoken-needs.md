# Brainstorm — lens: unspoken needs

- **Print three raw source rows beside every number Foreman reports** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: the last two asks were metric readers that missed real failures: stored results start `✗ exit N` but the code matched `exit N`, and the suite "never failed" while the ledger held failures. A user can spot a wrong reader in seconds if the aggregate shows the rows it was computed from.
  Done when: `fm cost`, track record and catch rates each print an aggregate plus 3 sampled raw rows, and a test seeds a `✗ exit 1` row and asserts it appears.

- **Check the user's factual claims against the ledger at intake** — FEATURE — value 4 — effort M — risk low — category: intake
  Why: the user said "the full suite never failed" and the ledger disagreed, so the stated belief was itself the bug report. Assumption: such claims can be spotted with a cheap classifier child or simple patterns ("never", "always", "no one").
  Done when: a request containing "the suite never failed" gets a one-line "ledger shows N failures, last on <date>" before planning starts.

- **Make the writer own every persisted string shape** — CLEAN — value 4 — effort M — risk med — category: correctness
  Why: round 1 fixed one `✗ exit N` mismatch. The structural fix is a single module declaring result, evidence and status formats, which readers must import their patterns from. This differs from reader round-trip tests, which only catch drift after the fact.
  Done when: grep finds no hand-written `exit \d` regex outside the format module, and changing the writer's format breaks a reader test at import time.

- **Freeze merges and self-edits to hooks while a release is in flight** — FEATURE — value 4 — effort M — risk low — category: release
  Why: 1.2.27 went to GitHub main and JARVIS while T-0777 and T-0783 were landing. Assumption: lanes can still merge into a tree being released.
  Done when: during `fm release`, a lane merge or an edit to `plugin/hooks` is deferred with a reason, and it resumes automatically when the release closes.

- **Gate pushes to main on a clean-container install of that exact sha** — SECURITY — value 4 — effort M — risk med — category: install
  Why: the README installs with `curl … main/install.sh | bash`, so every push to main ships to every user instantly. Assumption: there is no `stable` ref today. Let `main` stay open and make a `stable` tag move only after the clean install and `fm doctor` pass.
  Done when: the one-liner resolves to `stable`, and a deliberately broken `install.sh` on a branch cannot advance it.

- **Give each blocked task a machine-checkable unblock predicate** — FEATURE — value 3 — effort S — risk low — category: backlog
  Why: T-0325, T-0335, T-0336, T-0337, T-0352 and T-0418 are blocked by prose such as "needs libappindicator-gtk3 on Arch". Nothing notices when the package appears or the release lands.
  Done when: `fm task set --unblock-when 'pacman -Q libappindicator-gtk3'` is evaluated at session start, and a satisfied predicate moves the task to planned with a one-line notice.

- **Fix the pack builder's own bloat** — FIX — value 3 — effort S — risk low — category: tokens
  Why: this pack prints "The user's own words" twice, mixes category-count lines ("tokens 24", "guard 11") into the idea list as if they were ideas, and the open-work list still says Round 2 while the request says Round 4. Every child pays for this.
  Done when: a generated pack has each section once, no `<word> <n>` histogram lines in ideas, and a round number derived from the ledger. A test counts header occurrences.

- **Record an adjacent-possible note on each shipped capability** — FEATURE — value 4 — effort S — risk low — category: recursion
  Why: the user's "recursively improve" means building on what shipped. Round 1's `foreman-mail` monitor streams only bus mail, but the same channel could carry gate failures, CI results and drive nudges. Capturing "what this makes cheap" at ship time seeds the next round with evidence instead of a cold pile.
  Done when: closing a FEATURE task requires a one-line `enables:` field, and `fm research list --enables` feeds the next round's pack.

- **Add `fm prove-it <claim>` that prints a one-command disproof** — FEATURE — value 3 — effort M — risk low — category: trust — wild
  Why: the user repeatedly demands measured premises and dropped ideas whose savings were tiny (~2 min/month). For any claim such as "~1.04M tokens/30 days saved", Foreman prints the cheapest command the user can run to try to falsify it.
  Done when: `fm prove-it compact-output` prints a runnable command and its expected-versus-observed readout from raw data.

- **Have a stranger read the round's commits and describe the product** — FEATURE — value 3 — effort M — risk low — category: identity — wild
  Why: the pile has thousands of ideas and "etc. etc. etc." asks. A cold child that sees only the round's commit subjects describes what Foreman has become, and a mismatch with README's one-sentence purpose flags product drift.
  Done when: `fm round close` stores the child's one-paragraph description and warns if it omits "discipline" or "evidence".

- **Report "what you can now ignore" at round close** — FEATURE — value 3 — effort S — risk low — category: attention
  Why: the user pushes for more capability but never says what they no longer want to watch. Assumption: they would value a list of behaviours that are now verified, such as arming or readers, so they can stop checking them.
  Done when: the round receipt lists at least the items with a passing probe and a fire count above zero, and omits anything unverified.

- **Offer a hands-off weekly slot for the "etc." mandate** — FEATURE — value 3 — effort L — risk med — category: autonomy — wild
  Why: "super improve … etc. etc. etc." is a standing want, not a one-off. A user-set weekly slot runs one capped round (brainstorm, ground, queue, build) on the cheapest model, with an envelope and a return page.
  Done when: `fm recurse --weekly --budget 5` runs a round unattended in a lane and leaves a receipt with spend and a revert command, without touching main.

- **Keep a decision-owner column on every deferred cluster** — CLEAN — value 2 — effort S — risk low — category: backlog
  Why: T-0787 to T-0799 are deferred with reasons like "no evidence it recurs", but nobody is named to re-check them and the user has not ticked the board. Assumption: each needs one date-or-signal to resurface.
  Done when: each cluster task carries `revisit: <signal|date>`, and the session greeting names any whose signal fired.

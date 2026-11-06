# Brainstorm — lens: bold bets

- **Make `fm do` a closed-loop intent compiler** — FEATURE — value 5 — effort L — risk med — category: interface
  Why: assumption: builders and weak models guess verbs (`fm task list`), and the pack lists the unknown-command suggestion as the current fix. A bold alternative is a sentence-to-verb router, with a local grammar first and a cheap model fallback, that shows the exact command it will run and records the mapping.
  Done when: a test feeds 20 recorded wrong guesses (including `fm task list`) and 18 or more resolve to a real verb with the resolved command printed before it runs.

- **Auto-record reviewer findings from review output** — FIX — value 5 — effort M — risk low — category: feedback loop
  Why: the pack says defect-class feed to builder briefs starves because `fm task finding` is manual, one call per finding. A parser on the reviewer's structured result (or `/foreman:review` output) would call it for each confirmed finding.
  Done when: a test with a fake reviewer result holding 3 findings produces 3 stored findings and `fm lane brief` lists their classes without any manual call.

- **Let the autonomous drive launch review and ideas workflows** — FEATURE — value 5 — effort M — risk med — category: autonomy
  Why: the pack says /foreman:review and /foreman:ideas run only when the user types them, so an AFK user never gets them. Expose them as headless verbs (`fm review`, `fm ideas`) that the drive calls, gated by `fm contract` budgets.
  Done when: a test drive with a fake clock reaches a close, invokes the review verb once under the contract, and logs the call and its spend.

- **Cut a release with one verb, `fm release`** — FEATURE — value 4 — effort M — risk med — category: release
  Why: the pack describes releases as a manual 8-step ritual (bump 3 version fields, heading, gates on a quiet tree, release-check, temp worktree merge, push). The push stays behind the existing approval.
  Done when: on a fixture repo `fm release 1.2.34 --dry-run` prints every step and the version diff, and without dry-run it stops at the push for approval with all three version fields bumped.

- **Make bare `fm` inside a lane run that lane's own copy** — FIX — value 4 — effort S — risk low — category: builder ergonomics
  Why: the pack says builders can't run their own new flags because bare `fm` resolves to the main checkout; they must type `python3 plugin/bin/fm`. Resolve the copy from the worktree root when inside a lane.
  Done when: a test in a lane worktree with a new flag runs `fm --newflag` and sees the lane's behaviour, not the main copy's.

- **Mine guard refusals into full-command digests** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: the pack says the friction digest counts refusals without showing commands, and a hand-written miner was needed twice, with two false premises found late. Ship the miner as `fm guard mined` replaying each full command through `fm guard try`.
  Done when: a test over a fixture transcript with 5 refusals outputs each command, its verdict now, and flags those that now allow.

- **Alias the commonly guessed command names** — FIX — value 3 — effort S — risk low — category: usability
  Why: the pack notes common guesses like `fm task list` "could simply work". Build the alias table from the ledger's unknown-command events, with the top N guesses becoming real routes.
  Done when: `fm task list` exits 0 and prints the task list, and a test asserts that every alias in the table resolves.

- **Fix guard "it could be…" path guesses** — FIX — value 3 — effort S — risk low — category: guard clarity
  Why: the pack shows guesses with a command word glued onto a path (`/repo/cd/w.out`). Only suggest paths that appear as whole tokens or exist on disk.
  Done when: a test with `cd w; cat > out` yields no suggestion containing `cd/`.

- **Measure builder self-review and defect-class feed on real lanes** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: the pack says T-1147 and T-1164 are new and unmeasured, and every branch needed 2-6 review defects. Record defects per lane before and after, and print a trend in `fm lane list`.
  Done when: a test with 6 seeded lane records shows a defects-per-branch figure split by whether the briefs carried a defect section.

- **Wild: Run a night "bounty hunt" where a skeptic agent attacks the last release** — FEATURE — value 4 — effort L — risk med — category: adversarial QA
  Why: wild. Every branch shipped defects only reviewers caught, so an unattended adversary run on the released tree, using hostile inputs, load and odd cwd, would capture FIX briefs before the user finds them.
  Done when: a fixture night run with a planted bug in the tree captures one FIX brief naming it, and costs stay under the contract cap.

- **Wild: Publish Foreman's own receipts as a static "state of the product" page** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: wild. The pack lists web UI as the only surface and `fm todo`, `fm away` and the contract receipts as data sources. Render them into one static page a stakeholder can open without Foreman.
  Done when: `fm page` writes a single HTML file that contains the todo list, the last 5 closes, and the contract receipt, and loads with no network access.

- **Wild: Give the queue a "kill switch phrase" the user can type from a phone** — FEATURE — value 3 — effort L — risk high — category: remote control
  Why: wild, assumption: the user is AFK for long stretches and may want to halt or steer the drive remotely. A single outbound-free polling file in a synced folder, honoured by the contract, would do it without any server.
  Done when: a test writes `STOP` to the watched file and the drive halts within one tick, printing a receipt that names the file as the cause.

- **Wild: Replay the whole round's ideas against a "taste twin" built from the steers** — FEATURE — value 3 — effort L — risk med — category: prioritisation
  Why: wild. The pack shows the user dropping ideas for false premises and steering away from data-only relaxations. A scorer trained on those drops could rank the checklist page before the user sees it.
  Done when: on a fixture with 10 past drops and keeps, the scorer places 8 of 10 correctly in a held-out split and the checklist page shows the score.

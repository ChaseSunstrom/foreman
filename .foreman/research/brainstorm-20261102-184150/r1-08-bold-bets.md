# Brainstorm — lens: bold bets

- **Run twin planners and diff them** — FEATURE — value 5 — effort M — risk low — category: exhaustiveness
  Why: assumption: the "left out" list is self-reported today (several listed ideas write it), so the planner that missed a cell also decides what was missed. An independent second plan from a different model family, given only the request and the pack, makes the omission set measured rather than declared.
  Done when: `fm mission twin <request>` prints cells found by only one planner. A fixture with one planted cell missing from planner A shows that cell as "only B".

- **Cover the grid with a pairwise covering array** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: the grid ideas (surface × actor × failure mode × stage) grow multiplicatively, and the pack lists "thin so far" in 13 areas. A pairwise covering array guarantees every pair of values appears in at least one brief with far fewer rows. It turns "exhaustive" into a stated guarantee, with the uncovered higher-order tuples named.
  Done when: for a 4×5×6×4 grid, `fm grid cover --pairs` outputs at most 40 rows and a test checks every value pair appears at least once.

- **Draw grid columns from external standards** — FEATURE — value 4 — effort M — risk med — category: grounding
  Why: failure-mode columns are currently invented by the lens, so they share its blind spots. Checklists the model didn't author (WCAG, 12-factor, POSIX behaviours, the repo's stack cards) give columns it wouldn't have thought of. Assumption: a small offline checklist cache is acceptable (the privacy-first steers favour local data).
  Done when: a web-UI request gets WCAG-derived columns from a cached file, and each column names its source clause.

- **Build a measure library for Exams** — FEATURE — value 5 — effort M — risk low — category: proof
  Why: the carried gap says every Exam must name an outcome measure and a live-state reading, and earlier questions ask how many are vacuous or not re-runnable cold. Letting each brief pick a vetted measure from a shared library (read-only, bounded time, units, noise floor, known gameability) is cheaper than inventing one each time.
  Done when: filing a brief with an `outcome:` that isn't in the library or declared new is refused, and each library entry has a test showing it reads differently on a planted regression.

- **Test the request's sensitivity** — FEATURE — value 4 — effort M — risk low — category: exhaustiveness
  Why: assumption: some briefs are boilerplate that would be filed for any request. Mutating the request (drop a clause, flip a constraint, swap a noun) and re-planning shows which briefs never move. Those are insensitive and likely generic. The clauses that move nothing show which parts of the request were ignored.
  Done when: `fm mission sensitivity` outputs, per request clause, the briefs that changed, and flags clauses with zero effect.

- **Ask at most three questions chosen by planner disagreement** — FEATURE — value 4 — effort M — risk med — category: user value
  Why: the steers say never block on the user, so questions must carry a default and be few. Choosing them by where independent plan drafts diverge most (information gain) puts the user's limited attention on the real ambiguity, not on process.
  Done when: a Mission ends with 0–3 questions, each with a stated default and the two plan variants it separates, and the run continues on the default without waiting.

- **Audit each Mission with hindsight at 90 days** — FEATURE — value 4 — effort S — risk low — category: observability
  Why: the Mission is graded only when it closes. A cold child given just the original request and the diff that landed after 90 days writes what the Mission should have contained. The diff against the actual brief set is a measured miss rate per lens. Assumption: the exam-child isolation rules in the steers carry over.
  Done when: a scheduled job writes `hindsight.md` for a Mission 90 days old (the date can be faked in tests) with per-lens misses.

- **Transfer gaps across the user's own repos** — FEATURE — value 3 — effort M — risk med — category: user value
  Why: assumption: this user asks for the same kinds of thing repeatedly (the "asks the user had to make" list repeats classes). If they asked for X in repo A in week two, repo B's Mission should check X before they have to. Data stays local, summarised as tables rather than raw asks.
  Done when: a Mission in repo B lists "you asked for this class in repo A" cells with the quoted source task id, built from local ledgers only.

- **Produce usable slates at 1, 10 and 60 minutes** — PERFORMANCE — value 3 — effort M — risk low — category: planning
  Why: the cap on exhaustiveness is budget, and the all-or-nothing round hides the marginal return. An anytime planner writes a valid slate at each checkpoint, with the estimated unseen share, so the user or the drive can stop when the curve flattens.
  Done when: a Mission run with `--checkpoints` leaves three slate files, each passing the same filing checks, with a monotone non-decreasing cell count.

- **Wild: Run the Mission against its own ghost** — FEATURE — value 3 — effort L — risk med — category: exam
  Why: wild. Re-plan a closed Mission using only what was knowable on its start date (the repo at that commit, the then-current pack) with today's model. Cells the new run finds that the old one missed measure how much of the miss was model capability versus process.
  Done when: `fm mission ghost M-id` checks out the start commit in a scratch worktree and prints new-only and old-only cells.

- **Wild: Let a cold child type the user's follow-up messages** — FEATURE — value 4 — effort M — risk low — category: user value
  Why: wild. A tool-less child reads only the finished Mission page and writes the ten messages the user would send next. Each is mapped to a cell. Unmapped messages are left-out cells found before the user does. Real follow-ups later score the child.
  Done when: Mission close writes `followups.md`, and each line is tagged with a cell id or "no cell".

- **Wild: Track a spent-exhaustiveness bank** — FEATURE — value 2 — effort M — risk med — category: observability
  Why: wild. Each Mission earns or loses exhaustiveness credit by whether its left-out receipt later proved right. Missions with a poor track record must run twin planners (the first idea above), and ones with a good record may run cheaper. The budget follows evidence instead of a fixed rule.
  Done when: `fm mission credit` shows the balance and the next Mission's required planner count follows it in a test.

- **Wild: Turn the request into a playable scenario deck** — FEATURE — value 3 — effort L — risk high — category: exam
  Why: wild. Convert each filled cell into a one-paragraph scenario ("a user on a phone hits a stale tab while the drive is paused") that a cold agent plays against the finished work. Failed plays become fix tasks.
  Done when: a deck of at least 10 scenarios is generated from a grid and one planted defect makes at least one scenario fail.

Next question: which of the Exam's outcome measures can a cold process read today with no session state, and what share of past briefs would have had a library measure available?
Next question: when two independent planners disagree, which one has historically been right, and is that tracked anywhere?

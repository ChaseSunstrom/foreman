# Brainstorm — lens: 2030 worked back

- **Backfill the 2030 questions into today's ledger** — FEATURE — value 4 — effort S — risk low — category: instrumentation
  Why: assumption: by 2030 the user will ask "how many hours did Sampo give back per year?" and "which asks stopped?". The pack shows plenty of write-only gauges but no list of the fields those questions need. A cold child lists five 2030 analysis questions and the ledger fields each requires. The missing fields get added now, because history can't be backfilled.
  Done when: `fm doctor` prints a "2030 questions" table where each of five questions has a named field and a first-recorded date, and a test fails if a field is dropped.

- **Score a draft by running its Exam on what the user actually did** — FEATURE — value 5 — effort M — risk med — category: anticipation
  Why: the carried gap says every brief's Exam reads live state. Earlier ideas settle predictions by text similarity or by the user's first touched file. A draft is a hit if the user's real result passes the draft's own Exam, whatever words they typed.
  Done when: a settled prediction row records `exam_pass_on_actual: true|false`, and a test shows a differently-worded ask scoring as a hit while an unrelated one scores a miss.

- **Cap drafts by a daily review-minutes budget** — FEATURE — value 4 — effort S — risk low — category: attention
  Why: assumption: compute gets cheap and the user's review time stays the scarce resource. Earlier ideas estimate review minutes but don't gate on them. The user sets one number, drafts queue by value per review-minute, and the surplus waits.
  Done when: with a 20-minute budget and drafts estimated at 45 minutes, the morning card shows only drafts totalling 20 minutes or less and lists the rest as "held for budget".

- **Infer a goal graph from the asks and draft only at its leaves** — FEATURE — value 4 — effort M — risk med — category: user model
  Why: by 2030 the user states goals rather than asks. The pack's recent asks (Moonscale parts 1–2, model bench parts 1–2, rename steps) already read as goal → sequenced parts. Cluster asks into goals, mark which part comes next, and draft that leaf.
  Done when: replaying the 8 most recent ask chains predicts the next "part N+1" in at least 6, scored against the real next ask.

- **Track the delegation frontier** — FEATURE — value 3 — effort M — risk low — category: user model
  Why: the pack's recent asks show the user moving work from hand to agent (shipping, pushing, ledger fixes). Chart per task kind when the user stopped doing it by hand, and propose the next kind at the edge of that frontier. This is a trend of what moves over time, unlike the weekly "things done by hand" list.
  Done when: `fm` prints a per-kind first-delegated date and one proposed next kind with its evidence, and the frontier file diffs cleanly month to month.

- **Key the user model by identity from day one** — CLEAN — value 3 — effort S — risk low — category: privacy
  Why: assumption: by 2030 there is a second human or a shared machine. A user model without a key would blend people and poison predictions. Key every prediction table by the git author and machine user.
  Done when: a fixture ledger with two authors yields two separate follow-up tables, and no prediction cites the other author's asks.

- **Version every ledger schema and keep a golden fixture per version** — CLEAN — value 3 — effort S — risk low — category: durability
  Why: four years of ledgers is a regime the readers have never seen, and the pack's drills only fuzz size. Each ledger record gets a `v` field, and the repo keeps one real-shaped fixture per version. Readers must parse all of them.
  Done when: a test loads every golden version through current readers, and adding a schema without a new fixture fails the ship gate.

- **Model teammates' review objections for team repos** — FEATURE — value 3 — effort L — risk med — category: collaboration
  Why: assumption: agents increasingly hand PRs to other humans. The user's objections are already forecast, but a reviewer's recurring complaints (tests, naming, size) can be mined from the forge's review history. Pre-flag the likely ones before the PR goes up.
  Done when: on a repo with 20 or more past reviews, a draft PR's pre-flight lists at least one objection that a real later review also raised, measured on held-out PRs.

- **Chart words per ask as the single anticipation metric** — PERFORMANCE — value 3 — effort S — risk low — category: measurement
  Why: the user's asks are already long and rule-dense, so shorter asks over time is the observable sign anticipation works. Plot median words per ask per month and per task kind, with the 2030 target a short fragment. Count only user-authored text.
  Done when: `fm outcomes` prints a words-per-ask series per month and a test excludes slate-origin and pasted text.

- **Write a "manual for working with me" that a new agent or human reads first** — FEATURE — value 3 — effort M — risk low — category: user model — wild
  Why: assumption: the user will change agents, hosts and collaborators several times by 2030. Compile the user model into one human-readable page. Each line cites the evidence, and the user can strike a line through. Any orchestrator reads it as its first file.
  Done when: a cold agent given only that page, the repo and a new ask makes at most one of the user's known pushback mistakes on 5 replayed asks.

- **Test the user model for re-identification before any export** — SECURITY — value 4 — effort M — risk low — category: privacy — wild
  Why: the pack proposes syncing user models between machines, pooling across repos and publishing priors. A tool-less child gets only the exported tables and must guess the user's employer, stack and habits. If it succeeds, the export is blocked.
  Done when: `fm` refuses to export a user model when a cold child recovers three or more private facts from it, and a planted fact in a fixture is caught.

- **Red-team the predictor with an adversarial history** — SECURITY — value 3 — effort M — risk med — category: robustness — wild
  Why: the pack covers false predictions and planted wrong facts, but not poisoned history. A child writes the shortest fake ledger prefix that makes the predictor draft a harmful or costly ask with high confidence. Each win becomes a regression case.
  Done when: a fixture prefix produces a high-confidence harmful draft before the fix, and after it the draft is blocked by the guard or demoted below the show threshold.

Next question: which of the asks the user typed in the last month would a predictor trained only on the first half of that month have drafted correctly, scored through the Exam?
Next question: what does the user do in the first five minutes after reading a morning card, and does a draft ever change what they open first?

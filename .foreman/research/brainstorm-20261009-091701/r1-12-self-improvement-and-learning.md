# Brainstorm — lens: self-improvement and learning

- **Close the loop on lessons: measure whether a lesson actually changes outcomes** — FEATURE — value 5 — effort M — risk med — category: learning
  Why: T-0217 (lesson confidence) is deferred; lessons accumulate but nothing shows if recall of one preceded a first-time pass. fm bench and fm usage exist, so the data joins are there.
  Done when: `fm lessons --effect` lists each lesson with recalled-vs-not first-pass rates over finished tasks, and a lesson with no measurable lift for N tasks is flagged for retirement.

- **Auto-retire and merge stale lessons, rules and briefs** — CLEAN — value 4 — effort M — risk med — category: learning hygiene
  Why: the user said cleanup requests (repo, docs, briefs, dead code, replaced functionality) never got done. Assumption: lessons and instruction files grow monotonically, which dilutes context.
  Done when: `fm tidy --learn` proposes merges and deletions of lessons or rules contradicted by newer decisions or unreferenced for N tasks, and applying them leaves bench scores unchanged.

- **Turn every guard false-positive into a regression corpus automatically** — FEATURE — value 5 — effort M — risk low — category: guard learning
  Why: recent JARVIS refusals (fm focus chained with sed, rm of a symlink, bash -lc) were each fixed by hand after the user relayed them. The 5000-command replay exists to take them.
  Done when: a refusal that is followed within the session by the same intent re-run in another form is logged as a suspected false positive, and `fm replay --suspects` shows it with a proposed test case.

- **Mine the user's relayed complaints before they relay them (friction from downstream projects)** — FEATURE — value 5 — effort L — risk med — category: cross-project learning
  Why: most recent asks are "JARVIS hit X" and Foreman gets fixed after the fact. Assumption: the ledger in the downstream project already records the refusals, retries and idle stretches.
  Done when: `fm friction --fleet` reads the ledgers of all registered projects (with the share opt-in) and files a ranked FIX brief per repeated pattern, with the evidence lines.

- **Predict a task's failure before running it, from past similar tasks** — FEATURE — value 4 — effort M — risk med — category: prediction
  Why: fm recall and bench hold finished-task history with grades and blocks. Assumption: block and rework causes cluster by task type and files touched.
  Done when: `fm task new` prints a risk note ("tasks touching X blocked 3 of 5 times on Y") and a held-out replay shows the note's precision above a stated threshold.

- **Write evals from every blocked task by default, and gate releases on them (T-0035 made real)** — FEATURE — value 5 — effort L — risk med — category: evals
  Why: T-0035 is deferred and the 1.2.x release stream is manual ("Release 1.2.13…16"). Evals from blocked tasks exist as a command (fm evals) but are not a release gate.
  Done when: the release flow refuses while any captured eval case fails across N runs, and each new blocked task yields a redacted case without being asked.

- **Self-improvement pass that proves it helped: A/B each friction fix in a lane** — FEATURE — value 4 — effort L — risk med — category: self-improvement
  Why: fm friction --every 3 produces changes, and fm evolve ablates instruction files, but the two are not joined; the user's "recursive improvements" ask implies they want improvement they can trust.
  Done when: a friction fix lands only if the replayed bench for the lane shows no regression and the targeted friction metric drops in the next window, and the result is recorded against the fix.

- **Teach by taste: learn the user's preference model and apply it to autonomy decisions** — FEATURE — value 4 — effort M — risk med — category: preference learning
  Why: fm taste already tracks kept/dropped/steered; "budget limits shouldn't block until 75%" and "YAGNI" drops show consistent preferences. Assumption: they are not yet used to decide when to ask or not.
  Done when: in standard autonomy, a question whose answer taste predicts at a high confidence in past choices is answered and logged, with a one-line undo, and the prediction accuracy is reported in fm digest.

- **Wild: Foreman dreams: an overnight self-play fuzzer that attacks its own guard** — FEATURE — value 5 — effort L — risk med — category: adversarial learning
  Why: wild. Guard bugs (bash -lc, symlink rm, braces hiding a write) were found by users. fm night and the differential tests against real bash can generate and judge mutations unattended.
  Done when: a night run mutates known-blocked commands, finds a variant that real bash executes the same but the guard allows, and files it as a SECURITY brief with a failing test.

- **Wild: Time-travel debugging of Foreman's own decisions** — FEATURE — value 3 — effort M — risk low — category: introspection
  Why: wild. The ledger plus fm why and fm replay hold what was decided; there's no "why did the drive do X on Tuesday".
  Done when: `fm explain EVENT` reconstructs the inputs (state, queue, budget, guard category) behind a drive, guard or classify decision and re-runs it under the current code, showing whether it would differ.

- **Wild: Skill genome — breed instruction variants and keep the winners** — FEATURE — value 4 — effort L — risk high — category: evolution
  Why: wild. fm evolve does one revise-or-drop per generation; a population with crossover across skills, scored by fm bench on cost and first-pass rate, goes much further.
  Done when: a multi-generation run produces a variant that beats baseline on held-out bench cases without growing instruction size, and the lineage is recorded.

- **Wild: Apprentice mode — a second Foreman instance that shadows the user's manual fixes and learns from the diff** — FEATURE — value 3 — effort L — risk med — category: observational learning
  Why: wild. When the user edits or corrects outside a task (steers like "cleanup never got done"), the delta between what Foreman produced and what landed is unused signal.
  Done when: after the user hand-edits a Foreman commit, a lesson candidate is drafted from the diff and queued for their approval.

- **Detect "asked-for but never done" requests across the inbox history** — FIX — value 4 — effort S — risk low — category: follow-through
  Why: the user steered that cleanup requests never got done; the briefs record deferred items (T-0034, T-0035, T-0214 long deferred) with no aging.
  Done when: `fm next` surfaces any request deferred or dropped silently more than N tasks ago, and the weekly digest lists stale commitments with their age.

- **Learn the cost shape of tasks and tune lane/model choice from it** — PERFORMANCE — value 3 — effort M — risk low — category: cost learning
  Why: fm cost, fm budget and the pace logic exist, and the user pushed back on caps; per-task cost by type and model is available. Assumption: model and lane choice is currently static.
  Done when: planning suggests a model and lane for a task from past cost-per-first-pass of similar tasks, and fm digest shows the savings versus the default with no drop in pass rate.

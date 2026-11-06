# Brainstorm — lens: steal from other fields (compilers, databases, games, biology, markets)

- **Turn every fixed bug into an antibody test** — FEATURE — value 4 — effort M — risk low — category: reliability
  Why: assumption: a fix closes its task without a test that outlives it, so the same bug can return unnoticed. Immune memory keeps the failing input after the fix and replays it on every later check.
  Done when: reverting a closed task's fix makes `fm check` fail on its stored reproducer, and restoring the fix makes it pass.

- **Replace edit leases with snapshot commits and conflict checks** — FEATURE — value 4 — effort M — risk med — category: concurrency
  Why: the pack shows leases outliving their runs and blocking the next run for 20 minutes. Databases handle this with snapshot isolation: lanes edit freely and conflicts are caught at commit.
  Done when: two lanes editing disjoint hunks of one file both land with no lease wait, and overlapping hunks are refused at commit with the conflicting lines named.

- **Drop context that no later step reads, using liveness analysis** — PERFORMANCE — value 5 — effort M — risk med — category: token cost
  Why: the pack sets a target of about 140k context per reply after the usage cut. Compilers free registers once a value is dead; the same idea applies to tool results nothing downstream references.
  Done when: on a fixed replay of five closed tasks, context per reply drops at least 30% and every later step still resolves its references.

- **Type-check playbooks at build time** — CLEAN — value 3 — effort S — risk low — category: docs
  Why: `test_help` already fails on a shared help position, which shows command references drift. A compiler rejects undefined symbols before the program runs.
  Done when: a playbook that names a nonexistent `fm` subcommand or flag makes `fm doctor` exit non-zero and print the line.

- **Require a quorum of independent checks before a risky command runs** — SECURITY — value 4 — effort M — risk med — category: safety
  Why: assumption: the guard hook's single decision is the only gate for destructive commands. Biological quorum sensing acts only once enough independent signals agree.
  Done when: a command on the risky list with one check denying and one allowing is blocked, and the same command with two allowing checks runs.

- **Let a prediction market set the brainstorm slate order** — FEATURE — value 3 — effort M — risk low — category: ranking
  Why: the pack has many ideas with no ranking beyond the brainstormers' own scores. Markets aggregate dispersed judgment, and lenses that predict well earn more weight. Wild.
  Done when: over three rounds, the slate order set by market price matches the final pass order at least 70% of the time, and the results are recorded in the round ledger.

- **Rate models and playbooks with Elo per task kind and route by rating** — FEATURE — value 4 — effort M — risk med — category: routing
  Why: the duel and the ceremony-profile ideas already pick from data, but nothing ranks the choices as they play. Chess ratings update after every game and make matching better over time.
  Done when: after 50 closed tasks of one kind, the router picks the top-rated option for that kind, and each rating change is logged with the task that caused it.

- **Hedge a risky task by racing a cheap model against a strong one** — FEATURE — value 3 — effort M — risk med — category: cost
  Why: assumption: some tasks fail on the cheap runner but pass on the strong one, and the cost of finding out late is high. Traders hedge by holding both sides and taking the result that lands first.
  Done when: on a risky-task replay set, the hedged mode passes at least as many tasks as the strong model alone at no more than 1.3× its cost, and the losing run is cancelled and logged.

- **Coordinate lanes through decaying trail markers in the repo** — FEATURE — value 3 — effort M — risk low — category: agents — wild
  Why: assumption: lanes that cannot see each other repeat the same dead ends. Ants coordinate through pheromone that fades, so the next ant follows the trail without any message.
  Done when: a lane that finds a dead end leaves a marker, and a second lane started later skips that path, which the run log shows.

- **Differentiate a generic task into a specialist after its first steps** — FEATURE — value 3 — effort M — risk med — category: agents — wild
  Why: assumption: every task starts with full context even when its kind is clear after two steps. Stem cells specialize once their fate is known and drop what the specialist does not need.
  Done when: after the first two steps, a builder task's loaded context is at least 50% smaller than its starting size, and its next step still passes the same checks.

- **Apply a multi-file change all-or-nothing in two phases** — FIX — value 4 — effort M — risk med — category: reliability
  Why: assumption: a task that touches several files can leave half applied if a later write fails. Databases use prepare-then-commit so either every file changes or none does.
  Done when: a multi-file apply that fails on its last file leaves every earlier file byte-identical to before, verified by a hash check.

- **Triage failing gates by severity before the queue runs** — FEATURE — value 3 — effort S — risk low — category: triage — wild
  Why: the queue holds many failing checks with no order beyond age. Emergency rooms sort patients by how fast they could get worse, not by arrival time.
  Done when: given a queue with a failing security check and a failing style check, the security one runs first, and the order is printed with the reason for each place.

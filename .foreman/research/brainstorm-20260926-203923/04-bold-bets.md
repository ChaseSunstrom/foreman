# Brainstorm — lens: bold bets

- **Run only impacted tests until close** — PERFORMANCE — value 5 — effort S — risk med
  Why: the ~100 s full suite runs after every small change, and `fm impact` and the test↔source map already exist. Mechanism: `fm check` runs the mapped tests plus the last failures, and the full suite only at `fm done` (cached by content hash of the impact set, so an unchanged green gate is skipped). Assumption: the name-based map misses some dependents, which the close-time full run catches.
  Done when: editing one file with a mapped test runs in under 15 s and `fm done` still runs the full suite once.

- **Replace subagent review with a deterministic pre-audit** — PERFORMANCE — value 5 — effort M — risk med
  Why: reviews cost 50-100k tokens each. Mechanism: `fm audit` first checks mechanically that every criterion has evidence, changed files sit inside the impact set, a FIX has red→green, and no debug or TODO leftovers remain. A subagent is spawned only for L tier or when a flag trips.
  Done when: S and clean M tasks close with zero subagent spawns, and the ledger shows the token drop.

- **Auto-record evidence from Bash results** — PERFORMANCE — value 4 — effort M — risk low
  Why: the evidence-gate Stop nudge forces an extra model turn. Mechanism: PostToolUse on Bash matches the command against criteria verify commands and records evidence on exit 0, so the Stop gate finds it already satisfied.
  Done when: a task whose verify command ran cleanly ends with no evidence-gate nudge turn.

- **Add a per-task token and wall-time ledger** — FEATURE — value 4 — effort M — risk low
  Why: the 20% weekly burn is only anecdotal so far. Mechanism: the Stop hook sums usage from the transcript JSONL (stdlib), bucketed into subagent, tool output, nudges and injections, and saves it with the closed brief. Focus shows the median cost for similar past tasks by tier, and warns when a task passes 2x that. Assumption: the transcript carries usage fields.
  Done when: `fm cost` prints a per-bucket breakdown, and rounds can be compared before and after.

- **Outline-first Read guard for big files** — PERFORMANCE — value 4 — effort M — risk med
  Why: whole-file reads are a top token sink. Mechanism: a PreToolUse Read hook on a file over N lines with no offset or limit returns `fm outline` (symbols with line ranges, from `ast` for Python and regex elsewhere) and asks for a ranged read. It only fires once per file per task.
  Done when: a whole-file read of a large file yields the outline, and a ranged re-read succeeds.

- **Seed briefs from the nearest past task** — FEATURE — value 3 — effort M — risk med
  Why: recall already finds similar briefs with lessons, but Claude still writes each brief from scratch. Mechanism: `fm focus --from T-n` copies the past steps, criteria, verify commands and lessons as an editable draft. Assumption: repeat-shaped tasks are common.
  Done when: a repeat-shaped request reaches an approved brief in one turn with fewer output tokens.

- **Inject Next and SessionStart only when changed** — PERFORMANCE — value 2 — effort S — risk low
  Why: the per-turn Next (≤400 chars) and SessionStart (≤2k chars) injections repeat unchanged text. Mechanism: hash the last injection per session and emit nothing when it is identical, or a one-line delta.
  Done when: consecutive turns with unchanged state inject 0 chars.

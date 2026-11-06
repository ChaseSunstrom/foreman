# Brainstorm — lens: deepen: docs proof

- **Compile docs into a claim ledger** — FEATURE — value 5 — effort L — risk med — category: docs proof
  Why: the category's nine ideas all start by extracting claims; none stores them. Assumption: MASTER.md, README and skills hold hundreds of checkable claims (commands, flags, counts like "13 capabilities", file paths) and each is re-derived per run.
  Done when: `fm docs claims` writes `claims.jsonl` (doc, line, kind: command/flag/path/number/behaviour, checker, last result, commit) and a second run only rechecks claims whose doc or referenced code changed.

- **Prove a doc claim by running it in a sandbox** — FEATURE — value 5 — effort M — risk med — category: docs proof
  Why: the T-2288 migration proof runs on a throwaway copy; the same pattern fits README code blocks and `fm X --flag` lines. Assumption: the shipped CLI can run in a temp HOME with no network.
  Done when: `fm prove --docs README.md` runs each fenced command in a temp checkout, records exit code and output head, and fails the task when a documented flag is rejected.

- **Close docs tasks only on a recorded docs proof** — FEATURE — value 4 — effort S — risk low — category: docs proof
  Why: the unproven rollup (T-2273) counts typed or inconclusive evidence; docs-only tasks aren't a kind in it. Assumption: they show as "typed".
  Done when: a done task touching `*.md` or `site/` with no `--docs` evidence appears in the unproven rollup with reason "docs unchecked".

- **Pin numbers to their source** — FEATURE — value 4 — effort M — risk low — category: docs proof
  Why: the site stats (T-2326) and README say "2058 files", "13 capabilities", "20-skill cap"; a user already caught the site being stale. Assumption: such figures are typed by hand or by one script.
  Done when: a doc number can be written `{{fm:count skills}}`, `fm docs check` recomputes it independently of the writer, and a mismatch names doc line, claimed and actual.

- **Check the docs' own cross-references** — FIX — value 3 — effort S — risk low — category: docs proof
  Why: README links `MASTER.md`, anchors like `#the-guard`, and `fm lib show NAME`; a dead anchor is a claim too. Assumption: no link checker for anchors exists.
  Done when: a doc with a missing anchor, file or `fm` verb fails `fm docs check` with line numbers, and the check passes on the current repo.

- **Gate the ship on docs drift of touched code** — FEATURE — value 4 — effort M — risk med — category: docs proof
  Why: `fm ship` is already gated by the full suite; a changed flag with an unchanged doc line passes. Assumption: the ledger maps claims to code files.
  Done when: changing a CLI flag's name in code makes `fm ship` stop, naming the doc claims that mention it, until they are updated or marked n/a with a reason.

- **Wild: Read the docs as a cold newcomer agent** — FEATURE — value 4 — effort M — risk med — category: docs proof (wild)
  Why: steers demand signals Foreman didn't author and cold reads by a different model. Assumption: a tool-less Haiku child can follow Quick Start steps.
  Done when: `fm docs coldrun` has a child with only the README follow the Install section in a sandbox and report the first step where it needed knowledge the text didn't give.

- **Wild: Make the README's demo a recorded, replayable proof** — FEATURE — value 3 — effort L — risk med — category: docs proof (wild)
  Why: `demo/live.svg` claims "a real session… fm task prove shows the test fails"; nothing proves the picture matches the current CLI. Assumption: the demo has a script behind it.
  Done when: `fm docs demo --verify` replays the demo's commands and fails if their output no longer matches the frames' text.

- **Wild: Mutate the docs to test the checker** — FEATURE — value 3 — effort M — risk low — category: docs proof (wild)
  Why: the standing rule against metric-gaming; a checker that passes anything is worse than none. Assumption: no seeded-fault test exists for docs.
  Done when: `fm docs selftest` plants 10 wrong flags, numbers and paths in a copy of the docs and the checker catches all of them, reporting any it missed.

- **Flag docs the checker can't verify as prose, not silent** — FEATURE — value 4 — effort S — risk low — category: docs proof
  Why: the request says whatever can't be proven is labelled unproven. Assumption: behavioural sentences ("stops dangerous commands") have no checker.
  Done when: `fm docs report` lists claims by status proven / failed / unproven with the share of each, and the unproven count enters the unproven rollup.

- **Turn each failed docs claim into a one-line fix task** — FEATURE — value 3 — effort S — risk low — category: docs proof
  Why: the signal-to-fix loop (Mission 8) already turns recurring failures into FIX tasks. Assumption: docs failures aren't routed there.
  Done when: a failing claim ledger entry that persists across 2 runs files one FIX task with the doc line, claim and observed result, with no duplicates.

- **Check the skill descriptions against what the skills do** — FEATURE — value 3 — effort M — risk med — category: docs proof
  Why: 1388 files sit under plugin/skills and a recent ship went red over the skill-count and rules budgets; descriptions drive triggering. Assumption: no check runs a skill's example prompt against its description.
  Done when: for each skill, `fm docs skills` confirms the commands, paths and flags its body names exist, and lists the ones that don't.

- **Wild: Docs that heal themselves under review** — FEATURE — value 3 — effort L — risk high — category: docs proof (wild)
  Why: with a ledger and a failing check, a model could propose the minimal doc edit. The same-model writer/judge worry from the earlier questions applies. Assumption: the user's review is the only gate.
  Done when: `fm docs heal` writes a patch for each failed claim, re-runs its checker from the code side and refuses any patch that edits the checker or ledger.

Next question: Which doc claims describe behaviour no command can show, and what cheap observable (a log line, a test name, a recorded session) would turn them into checkable ones?
Next question: When the docs and the code disagree, which one is the bug by rule, and does the user ever get asked rather than told?

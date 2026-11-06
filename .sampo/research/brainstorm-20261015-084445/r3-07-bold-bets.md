# Brainstorm — lens: bold bets

- **Ship a Foreman Seed marketplace plugin that wires nothing** — FEATURE — value 5 — effort M — risk med — category: distribution
  Why: every rival installs in one command via marketplace or npx and adds commands without rewriting `~/.claude`; Foreman's installer sets bypass, outputStyle, autocompact, a statusline wrapper and 20 deny rules. Only the guard, resume and done-gate load by default; `fm wire` opts into the rest, one step at a time.
  Done when: `/plugin install` in a clean HOME leaves `~/.claude/settings.json` byte-identical, and the guard, resume and done-gate hooks still fire in a test session.

- **Make `fm demo` a 60-second no-model replay of a seeded-bug fix** — FEATURE — value 5 — effort M — risk low — category: onboarding
  Why: the README's first screen is abstract, with no before/after. A recorded session on a throwaway fixture shows classify, plan, red-to-green, evidence and done, and doubles as a smoke test of the whole loop.
  Done when: in a clean HOME `fm demo` exits 0 in under 90s with zero network or model calls, and its output shows a failing then passing check.

- **Publish a proof page that compares Foreman with bare Claude Code** — FEATURE — value 5 — effort L — risk med — category: proof of value
  Why: the bench has 1 case and 3 court cases (0/3), so there's no published evidence Foreman helps. Seed the bench from the 18 tasks fixed later and from fix commits in public repos, run each case N times with and without Foreman, then generate the README table from the results file.
  Done when: `fm bench --vs bare` writes a results file with at least 30 cases and N≥3 runs each, and the README table is generated from it and fails lint if the numbers drift.

- **Earn bypass mode instead of defaulting to it** — SECURITY — value 5 — effort M — risk med — category: trust
  Why: bypass by default is the largest trust ask in the install. Start in the user's current mode and offer a bypass lease only after N guarded tasks with no false blocks, showing the guard's block count and its replay corpus. The lease expires unless renewed.
  Done when: a fresh install leaves `defaultMode` unchanged, and `fm trust` after N clean tasks offers a bypass lease that expires on schedule.

- **Collapse the CLI to ten front-door verbs, with forwarding aliases** — CLEAN — value 4 — effort M — risk med — category: simplicity
  Why: `fm --help` is 231 lines, 108 verbs, and 46 of them were never run by Claude in 11 days. Show about ten verbs and move `inspect`, `stats` and `auto` merges behind them. Old names keep working as one-line forwards that print the new name, with ticket numbers stripped from help.
  Done when: `fm --help` is ≤25 lines and lists no T-ids, and every old verb name still runs and prints its replacement.

- **Make a fresh install pass its own `fm doctor` and put `fm` on the shell PATH** — FIX — value 4 — effort S — risk low — category: install
  Why: a new user's `fm` is "command not found" in a shell, and `fm doctor` fails right after install on a missing backup and prints 40 lines of passes. Create the backup at install, link `fm` into `~/.local/bin`, and print one verdict line unless something fails.
  Done when: the clean-HOME newcomer walkthrough runs `fm doctor` as its first step, gets exit 0 and one line, and `command -v fm` resolves in a plain bash.

- **Bridge tasks and GitHub Issues both ways, with evidence as comments** — FEATURE — value 4 — effort L — risk med — category: integrations
  Why: CCPM and spec-kit make issue threads the audit trail, and Foreman has no tracker sync. Import labelled issues as briefs, post the close-out receipt and evidence as a comment, and treat the issue's closed state as an external wait. It is outward-facing, so each post needs a one-yes preview.
  Done when: against a stubbed forge, `fm sync` imports an issue as a brief and posts a redacted evidence comment only after approval.

- **Auto-detect the test runner and offer it as the gate on first `fm check`** — FEATURE — value 4 — effort S — risk low — category: onboarding
  Why: `fm check` with no gates doesn't offer unittest or pytest, while `fm repeats` suggests single test modules as every-task gates (bad advice). Detect the runner from the project map, propose the whole suite as the gate, and make `fm repeats` suggest only whole-suite commands.
  Done when: in a fixture repo with pytest and no gates, `fm check` proposes the pytest suite command, and `fm repeats` never emits a single-module gate.

- **Add `fm shield`, a scan of the user's whole Claude config** — SECURITY — value 4 — effort M — risk low — category: security
  Why: ECC ships AgentShield and Foreman has no equivalent, though it already knows hooks, deny rules, plugins and MCP servers. Report risky permissions, plugin hook collisions, invisible characters in instruction files, and committed secrets, with a one-line fix each. It's read-only, so it works for people who never install the rest.
  Done when: against a fixture `~/.claude` with a planted wildcard allow and a zero-width character in a CLAUDE.md, `fm shield` reports both and exits non-zero.

- **Ship `fm preview`, a read-only audit of the user's past sessions** — FEATURE — value 4 — effort M — risk low — category: onboarding
  Why: claude-mem and ECC both lean on cross-session history, and a newcomer has no reason to believe in discipline yet. Scan local transcripts for things like edits with no test run, "done" claims with no evidence, and re-reads, then print "Foreman would have flagged N of your last M tasks". It works fully offline.
  Done when: on a fixture transcript folder, `fm preview` prints counts per finding type and makes no network calls.

- **Wild: Add a "Foreman Lite" first week with observe-only mode** — FEATURE — value 4 — effort M — risk med — category: adoption — wild
  Why: the research shows every popular plugin adds commands without taking over. For seven days Foreman records what it would have blocked or required without enforcing, then shows a day-7 keep, lite or remove card with the counts.
  Done when: in lite mode no hook ever blocks, and the day-7 card lists would-have-blocked counts from the ledger.

- **Wild: Add a browser playground that runs the real classifier and guard** — FEATURE — value 3 — effort L — risk med — category: onboarding — wild
  Why: the README lacks any demo, and installation is a big step. A static page (Pyodide) lets people paste a terse request or a shell command and see the classification, plan skeleton and guard verdict. It uses the real modules, so it can't drift from the product.
  Done when: the built page loads offline, and for 20 corpus commands its guard verdicts match the CLI's.

- **Wild: Ship `fm duel --vs <plugin>` to run one real task both ways on throwaway lanes** — FEATURE — value 3 — effort L — risk high — category: proof of value — wild
  Why: the user asked to make Foreman "THE plugin" while superpowers and ECC lead in stars. A lane with each plugin runs the same task on the user's own repo and compares tokens, time, whether it passed and how strong the evidence was. Results feed the proof page when the user opts in.
  Done when: `fm duel` runs two lanes, writes a comparison file with both outcomes and costs, and leaves the user's tree unchanged.

- **Wild: Add `fm hello`, a guided first real task on the user's own repo** — FEATURE — value 3 — effort M — risk low — category: onboarding — wild
  Why: newcomers hit duplicates from `capture` then `task new`, an unexplained "Drive: on", and a refusal with 4 bullets. A tiny real task (add one missing docstring or test) is walked through with each step explained in plain words, ending in `fm task finish`.
  Done when: in a fixture repo, `fm hello` completes a task end to end, and every state word it prints is explained once.

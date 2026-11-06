# Brainstorm — lens: skills and playbooks Claude would reach for

- **Add a `fm playbooks route` request-to-chain router** — FEATURE — value 5 — effort M — risk low — category: playbooks
  Why: 48 playbooks across 15 stages, but nothing says which to load, in what order. Assumption: Claude today picks one by description match or skips them.
  Done when: `fm playbooks route "add a settings page with live preview"` prints an ordered chain (e.g. plan/api-design, ui/direction, build/ts, verify/tdd, review/a11y) with token cost, and a test pins the chain for 10 sample requests.

- **Measure playbook reach rate and trigger precision** — FEATURE — value 5 — effort M — risk low — category: skill evals
  Why: 1,161 skill files and a `cc-skill-descriptions` card, but no evidence of how often Claude actually loads the right one. Assumption: many descriptions undertrigger.
  Done when: `fm playbooks reach` runs 5 should-trigger and 5 should-not-trigger prompts per playbook headlessly, N times each, and prints a hit and false-hit rate table. A playbook below the threshold fails `fm doctor`.

- **Tune descriptions automatically against the reach set** — FEATURE — value 4 — effort M — risk med — category: skill evals
  Why: follows the item above. Hand-tuned descriptions drift as the catalogue grows.
  Done when: `fm playbooks tune NAME` proposes up to 3 description rewrites as a diff, keeps one only if reach rises without a false-hit rise, and never writes without confirmation.

- **Write the debug and incident playbook family** — FEATURE — value 5 — effort M — risk low — category: playbooks
  Why: the `fix` stage holds only `flaky-tests`, and the recent history is mostly bug-fix work (the T-1468 padding bug, the T-1263 evasion corpus). Missing: repro-first, minimal-repro shrinking, bisecting, a root-cause ledger, and "fix the cause, not the symptom" checks.
  Done when: `plugin/skills/playbooks/fix/` gains at least 4 original files, each ending in a runnable proof block, and the router test sends "it crashes sometimes on resize" to them.

- **Write migration and upgrade playbooks** — FEATURE — value 4 — effort M — risk low — category: playbooks
  Why: the stages cover build and clean, but not major dependency bumps, language-version moves, or expand/contract schema migrations. Assumption: these are among the riskiest unattended tasks.
  Done when: a `migrate` stage exists with 4 playbooks (dependency major, runtime version, schema expand/contract, API deprecation). Each names its rollback step, and a fixture repo test shows the dependency-major playbook produces a green staged upgrade.

- **Embed runnable proof blocks that become task verify commands** — FEATURE — value 5 — effort M — risk med — category: playbook mechanics
  Why: Foreman's thesis is "prove with commands it ran", but playbooks are prose. Assumption: a parseable `proof:` fence is cheap to add.
  Done when: `fm task new --playbook fix/repro-first` pre-fills the verify field from that playbook's `proof:` fence, and a lint fails any playbook that has no proof block or whose block exits 0 on a deliberately broken fixture.

- **Mine project recipes from the repo's own git history** — FEATURE — value 5 — effort L — risk med — category: project skills
  Why: Foreman knows the repo's commit history and `fm map`, but generic playbooks don't know "how we add an fm verb here" (touch `fm`, `lib/`, `tests/`, `skills/`). Pairs with the existing "draft playbooks from finished runs" idea but starts from history rather than one run.
  Done when: `fm recipes mine` finds at least 3 repeating change shapes in this repo, as file-set patterns with exemplar commits, writes them as project-local playbooks, and a test shows a new-verb request loads the right recipe.

- **Detect conflicts and duplicates across skills** — CLEAN — value 4 — effort M — risk low — category: catalogue hygiene
  Why: Foreman's own playbooks, ~1,088 cards and third-party sources can give opposing advice (e.g. "mock the database" vs "never mock the database"). Nothing flags it.
  Done when: `fm playbooks conflicts` lists pairs that share a trigger and disagree on a rule, checked against a seeded fixture of 3 planted contradictions, and the loader refuses to load both into one run without a note.

- **Write a data, SQL and analytics playbook set** — FEATURE — value 3 — effort M — risk low — category: playbooks
  Why: the cards include `data`, but there is no playbook for query review, a reconciliation tie-out, or "numbers must agree with the source". Assumption: the finance-vertical ideas above need it.
  Done when: 3 playbooks (query-review, tie-out, pipeline-idempotence) exist, each with a proof block runnable against a bundled sqlite fixture.

- **Wild: Run a kata mode that trains and scores a weak model on a playbook** — FEATURE — value 3 — effort L — risk med — category: playbook evals
  Why: assumption: `fm code` runs small local models, and a playbook that a weak model can't follow is the wrong playbook for it. Wild.
  Done when: `fm code kata fix/repro-first --runner local` runs 10 scripted tasks, prints an obedience score, and marks the playbook "needs a lite variant" if it falls below 60%.

- **Wild: Write a counter-playbook of the repo's own failed fixes** — FEATURE — value 4 — effort M — risk low — category: lessons
  Why: the drops and steers show repeated failure modes (premise false, transient canary, auto-trusting plantable files). Lessons already exist (T-0217). Turning them into a "traps here" skill that loads before touching the matching files would stop repeats. Wild.
  Done when: editing a file under a lesson's path loads a 5-line "traps here" note, and the eval shows it fires on a replayed past mistake.

- **Wild: Generate a five-minute lesson from the diff for the user's own level** — FEATURE — value 3 — effort M — risk low — category: teaching
  Why: assumption: a user who says "etc. etc." and asks for much more is moving fast and may not follow what shipped. Wild.
  Done when: `fm explain TASK` writes a one-screen lesson that quotes only lines from the actual diff, and a test fails if any quoted line isn't in it.

- **Add a tiered playbook format, with a token ratchet** — PERFORMANCE — value 4 — effort S — risk low — category: context cost
  Why: a 13-line playbook is cheap, but the family is about to grow by dozens, and loading whole files into context spends tokens before work starts.
  Done when: each playbook has a headline of 150 tokens or fewer, a body, and an appendix, `fm playbooks show NAME --tier head` prints only the headline, and CI fails if a headline exceeds the cap.

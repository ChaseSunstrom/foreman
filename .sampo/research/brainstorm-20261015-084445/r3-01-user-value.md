# Brainstorm — lens: user value

- **Add a "first win in 5 minutes" path: `fm hello` fixes a seeded bug in a throwaway fixture** — FEATURE — value 5 — effort M — risk low — category: onboarding
  Why: New-user evidence A1, A5, A9: the README is abstract, `fm init` prints a random slug, and `fm task done` refuses with four bullets before the user has seen one success. Rivals all offer a guided wizard (`bmad-help`, `ecc setup`). Earlier ideas covered `fm demo` replays; this one runs the real loop with no model dependence beyond what the user already has, and ends by showing the user's own `fm status`.
  Done when: in a clean HOME, `fm hello` finishes a seeded-bug FIX in a temp dir with recorded evidence and prints a three-line "what just happened", exit 0, under 5 minutes.

- **Make the install a receipt-first plan, with bypass off by default** — SECURITY — value 5 — effort M — risk med — category: trust
  Why: A2: the default install sets bypassPermissions, autocompact 70%, an output style, a statusline wrapper and 20 deny rules, and says only "asks you to confirm once". Rivals "add commands, don't rewrite ~/.claude". Assumption: users who see a plan decline less than users who discover changes later.
  Done when: `install.sh` prints an itemised list of every `~/.claude` change, applies only after a y/N per group, defaults permission mode to unchanged, and `uninstall.sh` restores a byte-identical settings.json in a test.

- **Put `fm` on the user's shell PATH** — FIX — value 5 — effort S — risk low — category: onboarding
  Why: A3: `fm` works only inside Claude sessions; the README says "run fm …" everywhere, and a shell gives "command not found". The first command a newcomer types fails.
  Done when: after install in a clean HOME, a fresh login shell resolves `fm --version`, and an existing different `fm` on PATH is detected and not shadowed.

- **Gate a fresh install on its own `fm doctor`** — FIX — value 4 — effort S — risk low — category: onboarding
  Why: A8: a new install fails doctor (missing backup) and prints 40 lines of passes. Newcomers read that as "broken".
  Done when: right after install, `fm doctor` exits 0 and prints one line when everything is green; failures print only themselves with a fix command; a no-model test in the suite covers it.

- **Make `fm help` the front door: 10 verbs, one example each** — CLEAN — value 4 — effort M — risk low — category: simplicity
  Why: A4/A11, D: `--help` is 231 lines with ticket numbers; 46 of 108 verbs were never run by Claude in 11 days. Earlier ideas proposed tiers; this adds that `--help` itself must point at `fm help`, hide ticket ids, and end `task new --help` with valid `--type`/`--tier` values and a worked example (A6).
  Done when: `fm --help` is ≤ 25 lines, contains no `T-\d+`, names `fm help --all`, and `fm task new --help` lists valid types and tiers plus one example.

- **Show a before/after proof strip from Foreman's own ledger** — FEATURE — value 5 — effort M — risk med — category: proof
  Why: C: 688 finished, 670 held, 18 fixed later (2.6%), but the bench has 1 case and no published evidence Foreman helps; every rival leads with stars. Fixing the grading first: 159 folded tasks show as "ungraded" and distort the digest.
  Done when: a generated page lists held-rate with numerators and denominators (folded tasks graded through their parent) and the README links to it; a test fails if a README number isn't backed by the generated file.

- **Make `fm task new` adopt the matching capture** — FIX — value 4 — effort S — risk low — category: newcomer friction
  Why: A6: `fm capture` then `fm task new` without `--from` makes a duplicate; the user's words describe the same need they'd already stated.
  Done when: running `fm task new` with a title matching an open capture prompts or auto-adopts it, and the test asserts one record, not two.

- **Offer a gate on first `fm check` by detecting the test runner** — FEATURE — value 4 — effort S — risk low — category: onboarding
  Why: A7 plus C: `fm repeats` suggests single test modules as every-task gates, which is bad advice. Detect pytest/unittest/npm test/cargo test and propose the whole-suite command, and fix `fm repeats` to suggest only whole-suite gates.
  Done when: in a fixture repo with unittest tests and no gates, `fm check` proposes `python3 -m unittest` and writes it on one yes; `fm repeats` never emits a single-file command.

- **Print a prefilled `fm task finish` when `task done` refuses** — FIX — value 4 — effort S — risk low — category: close-out
  Why: A9: refusal gives four bullets while the one-call shortcut is buried.
  Done when: a refused `fm task done` ends with an exact copy-paste `fm task finish …` line filled from the task's state.

- **Add `fm preview`: a read-only audit of the user's past Claude sessions before installing** — FEATURE — value 4 — effort M — risk med — category: proof
  Why: Local-first and no model calls; it counts repeated mistakes, unverified "done" claims and giant Bash outputs from their own transcripts, so the value is shown on their data (C: 44.3M chars of Bash output measured this way). Assumption: transcripts are readable and parseable on the user's machine.
  Done when: on a fixture transcript set, `fm preview` prints three counted findings with example lines and writes nothing outside a temp dir.

- **Wild: A "Foreman off for this task" one-word escape** — FEATURE — value 3 — effort S — risk med — category: trust
  Why: assumption: a newcomer who can't leave ceremony for a trivial edit uninstalls instead; D shows heavy surface.
  Done when: saying "skip Foreman for this" suspends gates for one task only, records it in the ledger, and re-enables automatically at the next task.

- **Wild: `fm duel --vs <plugin>`, a same-task comparison on a real repo** — FEATURE — value 4 — effort L — risk med — category: proof
  Why: B shows rivals compete on stars, not evidence; running a task with bare Claude Code and Foreman in two worktrees and diffing the verified outcome gives the user their own proof. Assumption: cost is acceptable behind a spend cap and an explicit yes.
  Done when: on a fixture bug, the command runs both arms under `--max-budget-usd`, then prints which arm passed hidden checks, tokens and wall time.

- **Wild: Install by saying "install Foreman" to Claude through an agent-readable INSTALL.md** — FEATURE — value 3 — effort S — risk med — category: onboarding
  Why: B's rivals install via one marketplace command; here the agent itself can run the plan-then-apply flow and answer questions about each change. Assumption: the user trusts Claude to follow a published guide with the itemised plan shown first.
  Done when: a cold child given only INSTALL.md completes install in a clean HOME with the plan shown and bypass untouched.

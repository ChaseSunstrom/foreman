# Brainstorm — lens: skills and playbooks Claude would reach for

- **Ship a text, time and bytes correctness playbook** — FEATURE — value 5 — effort M — risk low — category: playbooks
  Why: the user's recent steers are all this class: wide-glyph padding by `len()` (T-1468), line-ending and non-UTF-8 rewrites, case-fold path identity, option-shaped paths. No playbook covers it, and Claude reliably gets these wrong.
  Done when: `fm playbooks` lists it with a section each for Unicode width and graphemes, line endings and encodings, timezones and DST, money and float rounding, path normalisation. Each section has a runnable probe and a failing-then-passing fixture, and an eval shows it catches a seeded wide-glyph padding bug.

- **Add a rationalisation table to every playbook** — FEATURE — value 5 — effort M — risk low — category: compliance
  Why: assumption: Claude skips a playbook by talking itself out of it ("too small to need a plan", "tests are obvious"). Each playbook would name its likely excuses with a one-line rebuttal and the check that exposes each.
  Done when: every playbook has an "Excuses" block, and an eval that pressures Claude to skip shows a lower skip rate with the block than without. A lint fails any playbook missing the block.

- **Inject action-triggered micro-playbooks** — FEATURE — value 4 — effort M — risk med — category: reach
  Why: description routing only fires when Claude chooses to look. A PreToolUse rule could attach a 6-line checklist at the moment of the risky action: editing `migrations/*.sql`, running `git rebase`, touching `Dockerfile`, `rm -rf` in a build dir. This is distinct from the listed per-path rules lookup, which answers a question rather than pushing at the tool call. Assumption: it must stay inside the hook latency budget that bench_hooks already enforces.
  Done when: editing a migration file produces the checklist once per session. `bench_hooks.py` shows no budget regression, and a trigger table maps each rule to a tested example command.

- **Write the security playbook family beyond the existing three** — FEATURE — value 5 — effort M — risk low — category: security
  Why: the pack lists only 3 security playbooks and security is flagged thin. Add: threat-model-a-diff (trust boundaries crossed by this change), secrets handling, authz-not-just-authn checks, LLM-app prompt-injection hardening for apps the user builds, and safe deserialisation. Each ends in a stdlib-runnable grep or test, not prose.
  Done when: five new playbooks each carry a verify command that fails on a seeded vulnerable fixture and passes on the fixed one.

- **Add a dependency-admission playbook** — SECURITY — value 4 — effort S — risk low — category: supply chain
  Why: assumption: Claude invents or mistypes package names and adds deps casually. The playbook makes it prove the package exists on the registry (offline cache or lockfile first), pin the version, check its licence class, and show the symbol exists in the installed version before use. It reuses the licence classes `fm lib` already enforces.
  Done when: a fixture task asking for a nonexistent package ends with Claude refusing to add it and naming the check. A real package is added with a pinned version and a licence line in the receipt.

- **Build a failure museum of Claude's own habits** — FEATURE — value 4 — effort M — risk low — category: reflect
  Why: wild. The pack shows recurring misses (elided code, tests that can't fail, claiming done without running, over-wide refactors). One playbook would hold each habit as an exhibit: a real transcript excerpt (redacted), the tell, and a stdlib detector. `fm reflect` would append new exhibits from the user's own closed tasks.
  Done when: at least 8 exhibits exist, each with a detector that fires on its fixture. `fm reflect` can propose a ninth from a finished task, and the user must accept it before it is written.

- **Backtest a playbook against the repo's own bug-fix history** — FEATURE — value 4 — effort L — risk med — category: evals
  Why: wild. The existing A/B evals use synthetic cases. Here, take past FIX commits, check out the parent, and ask whether a playbook's check would have flagged the bug the fix later resolved. The score is a hit rate on real history, which is stronger evidence than a seeded case.
  Done when: `fm playbooks backtest NAME` reports N fixes replayed with M flagged, using only local git and no network.

- **Write a CLI and TUI product-design playbook** — FEATURE — value 4 — effort S — risk low — category: developer experience
  Why: `ui/terminal-ui.md` is 13 lines. Foreman is itself a large CLI, and the user keeps asking for `Next:` lines, one-screen help and drop-in flags. The playbook covers exit codes, `--json` and `--plain`, no-tty behaviour, error shape (what happened, what it did, next command), completions and help-length budgets.
  Done when: the playbook includes a checklist script that runs against any CLI's `--help` and `--json` output and fails on missing no-tty fallback or non-zero-on-error.

- **Add a legacy characterisation playbook** — FEATURE — value 4 — effort M — risk low — category: playbooks
  Why: assumption: untested code is where Claude most often breaks behaviour while "just refactoring". The playbook pins current behaviour first: golden-master capture from real inputs, then refactor under that net, then prune. It sits between the existing refactor-cleaner and tdd playbooks, which both assume tests exist.
  Done when: a fixture with no tests gets a generated golden-master harness and a refactor that keeps it green. The harness fails when a seeded behaviour change is made.

- **Ship a delete-and-deprecate playbook** — FEATURE — value 4 — effort S — risk low — category: simplicity
  Why: "simplicity" is flagged thin and the idea list is almost all additions. The playbook gives a removal ladder: find consumers by search, prove zero use, soft-deprecate, remove, and verify. Receipts record what was deleted and the evidence it was unused.
  Done when: removing a fixture function with one hidden caller is blocked until the playbook's consumer search finds it, and a clean removal closes with a receipt listing the searches run.

- **Add a phone, watch and device build playbook family** — FEATURE — value 3 — effort L — risk med — category: devices
  Why: the library has mobile and native cards but no playbook, and devices is flagged thin. Cover Android and iOS simulator verify loops, offline-first and permission flows, small-screen and glanceable design, and embedded constraints (memory, power, flash). Assumption: simulators may be absent, so each playbook needs a documented headless fallback.
  Done when: each playbook names its simulator or emulator verify command and the fallback when the tool is missing, and `fm doctor` reports which are available.

- **Write a decision-memo playbook for user-facing answers** — FEATURE — value 4 — effort S — risk low — category: user value
  Why: the user wants recommendations over surveys. The playbook shapes end-of-task and mid-task answers: recommendation first, two real alternatives with costs, what would change the call, the one thing needing their input. It applies where Claude otherwise lists options without choosing.
  Done when: an eval on five "which should I do?" prompts shows every answer leading with a recommendation and a named reversal condition.

- **Offer a "why did Claude not use the playbook" autopsy** — FEATURE — value 4 — effort M — risk low — category: reach
  Why: wild. After a task closes with a miss that a playbook covers, `fm reflect` would read the transcript and say whether the playbook was never loaded, loaded but ignored, or loaded and wrong. It then files the matching fix as a task: description edit, excuse-table entry or content correction. This closes the loop without the user diagnosing it.
  Done when: on a recorded session where a relevant playbook was skipped, `fm reflect` names one of the three causes with the transcript line as evidence and opens a task of the matching type.

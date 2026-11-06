# Brainstorm — lens: reliability

- **Write fm state atomically under a lock**: FIX. Value 5, effort M, risk low.
  Why: assumption: state is JSON/markdown files under `~/.claude/foreman/state`. The rules allow up to 3 parallel subagents plus hooks, so two `fm` calls can interleave and truncate a brief or queue.
  Done when: a test running 20 concurrent `fm task log` calls leaves all 20 entries present and the file parses.

- **Add `fm doctor` to validate and repair state**: FEATURE. Value 5, effort M, risk low.
  Why: assumption: a crash mid-write or a hand edit can leave a brief unparseable, and nothing detects it. Checkpoint/resume is the core promise, so a corrupt checkpoint should be caught early.
  Done when: `fm doctor` flags a deliberately corrupted brief and a dangling `#T-id` dependency with a nonzero exit, and `--fix` quarantines the bad file.

- **Cap the Stop-hook drive loop**: FIX. Value 4, effort S, risk med.
  Why: the rules say the Stop hook continues while open work exists. A blocked or unverifiable task could loop forever. assumption: no iteration cap exists today.
  Done when: a simulated task that can never verify makes the hook release control after N attempts, with a logged reason.

- **Make hooks fail safe with timeouts and clear errors**: FIX. Value 4, effort M, risk med.
  Why: assumption: a hook crash (missing state dir, bad JSON, `fm` not on PATH) either blocks every tool call or silently disables the guard. Which one it does is undefined in the pack.
  Done when: tests with a missing state dir and malformed input show the guard fails closed for `core` categories, fails open for advisory hooks, and each prints one actionable line.

- **Add a docs-drift check that runs in CI/tests**: CLEAN. Value 4, effort S, risk low.
  Why: the known gap is "docs drift". `foreman.md` and `MASTER.md` name commands, flags, tags and categories that can diverge from the CLI.
  Done when: a test extracts `fm` subcommands and `--allow` categories from argparse and fails if `foreman.md` or `MASTER.md` mentions one that doesn't exist, or omits one that does.

- **Design headless mode with deterministic exit codes**: FEATURE. Value 4, effort L, risk med.
  Why: the known gap is "no headless mode". The rules assume interactive approval (L-tier plans, `?` items), so headless needs explicit behavior for those cases.
  Done when: `fm --headless` never prompts, exits 0 on done, 2 on blocked, 3 on needs-approval, and emits a JSON summary. A test covers each exit code.

- **Version the state schema and migrate on load**: CLEAN. Value 3, effort M, risk med.
  Why: assumption: briefs and queue files have no `schema_version`. Any upgrade to a plugin that installs globally can strand old state.
  Done when: loading a v0 fixture auto-migrates it to the current version with a backup, and an unknown newer version is refused with a clear error.

- **Test the evidence gate and 3-strikes block**: FIX. Value 3, effort S, risk low.
  Why: "fm refuses done without evidence" and "3 failed attempts → block" are the central invariants. The pack shows no tests for them.
  Done when: tests assert `fm task done` fails with no evidence recorded, and the third failed verification sets the task to blocked.

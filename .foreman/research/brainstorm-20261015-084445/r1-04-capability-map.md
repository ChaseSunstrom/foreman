# Brainstorm — lens: capability map

- **Put `fm` on the user's shell PATH** — FIX — value 4 — effort S — risk low — category: onboarding
  Why: newcomer test A3: README says "run fm …" everywhere, but in a plain shell it's "command not found".
  Done when: after install in a clean HOME, `bash -lc 'fm help'` exits 0, and uninstall removes the shim.

- **Make a fresh install pass its own `fm doctor`** — FIX — value 4 — effort S — risk low — category: onboarding
  Why: A8: a fresh install fails doctor on a missing backup and prints 40 lines of passes.
  Done when: a clean-HOME test runs install then `fm doctor` and gets exit 0 with at most 5 lines of output.

- **Show an itemised install plan before touching `~/.claude`** — SECURITY — value 5 — effort M — risk med — category: trust
  Why: A2: the default install silently sets bypassPermissions, adds 20 deny rules, installs third-party plugins and wraps the statusline. The only warning is "confirm once".
  Done when: `install.sh --plan` prints each change as a unified diff with a per-item skip flag. On a TTY the bypass change needs an explicit y/N. `--yes` keeps today's behaviour.

- **Add `fm demo`, a 60-second no-model walkthrough** — FEATURE — value 5 — effort M — risk low — category: onboarding
  Why: A1: the README's first screen is abstract and has no before/after.
  Done when: `fm demo` runs in a throwaway repo with a seeded bug and shows `done` refused without evidence, then accepted after a recorded test run. It makes no model calls, and the README embeds its captured output.

- **Add `fm preview`, a read-only audit of the user's past Claude sessions** (wild) — FEATURE — value 4 — effort M — risk low — category: acquisition
  Why: assumption: a newcomer believes in the discipline once shown their own misses. Rival plugins all sell on stars, and Foreman has no proof (C).
  Done when: on a HOME with transcripts but no Foreman, `fm preview` prints counts of "done" claims with no test run and of commands the guard would have blocked, and writes nothing.

- **Import work from Task Master, spec-kit and CCPM** — FEATURE — value 4 — effort M — risk low — category: interop
  Why: B lists these as the main rivals, and their users already hold PRD-derived task lists. `fm import` and `fm adopt` (the ecosystem verbs) don't read them.
  Done when: `fm import taskmaster tasks.json` and `fm import speckit specs/` produce queued briefs, and re-running the import creates no duplicates.

- **Add `fm shield`, a scan of the user's whole Claude config** — SECURITY — value 4 — effort M — risk low — category: security
  Why: B: ECC ships AgentShield, a config scanner, and Foreman has no equivalent. A2 shows its own install widens permissions.
  Done when: against a fixture config, `fm shield` flags a wildcard allow rule, an MCP server with a secret in its env, and an unpinned hook, each with a one-line fix. It exits non-zero at severity ≥ high.

- **Add an env var and verb to switch individual hooks off** — FEATURE — value 3 — effort S — risk low — category: coexistence
  Why: B: ECC added hook profiles and `ECC_DISABLED_HOOKS` after hook-conflict complaints. Foreman has 14 hook events and only `--apply-conflicts` as an escape.
  Done when: `FOREMAN_HOOKS_OFF=posttool_note` makes that hook exit in one stat call, and `fm doctor` lists what's off.

- **Stop `fm repeats` from suggesting single test modules as gates** — FIX — value 3 — effort S — risk low — category: gates
  Why: C: it suggests test modules as every-task gates, which the data shows is bad advice.
  Done when: given a history dominated by `unittest tests.test_x`, `fm repeats` suggests the whole-suite command or nothing.

- **Grade folded tasks by their parent in `fm digest`** — FIX — value 3 — effort S — risk low — category: truth
  Why: C: 159 of 370 recent tasks show as "ungraded", which hides the true held rate.
  Done when: a folded task inherits its target's grade and the digest "ungraded" count is 0 on the 7-day fixture.

- **Make `fm task new` pick up a matching capture and list valid values** — FIX — value 3 — effort S — risk low — category: onboarding
  Why: A6: `fm capture` followed by `fm task new` without `--from` makes a duplicate, and `--help` lists no type or tier values.
  Done when: a title match against an open capture links it with a printed notice, and `fm task new --help` lists every type and tier plus one example.

- **Merge the seven `_git` helpers into one module** — CLEAN — value 2 — effort S — risk low — category: footprint
  Why: D: seven copies of `_git`.
  Done when: `grep -rn "def _git"` finds one definition, and the full suite and `bench_hooks` stay within noise of baseline.

- **Wild: Add a browser playground (Pyodide) that runs the real classifier and guard** — FEATURE — value 3 — effort L — risk med — category: acquisition
  Why: wild; assumption: Pyodide can import the stdlib-only modules. It would be a no-install trial and a shareable link.
  Done when: a static page classifies a pasted request and shows the guard verdict for a pasted command, matching the CLI on 20 fixture inputs.

- **Wild: Generate the README proof strip from the ledger at release** — FEATURE — value 4 — effort M — risk low — category: proof
  Why: wild; C: 670 of 688 tasks held (2.6% fixed later), yet the README claims nothing measurable and the bench has 1 case.
  Done when: `release.sh` rewrites a README block with held rate, task count and hook latency, and fails if the numbers are older than 7 days.

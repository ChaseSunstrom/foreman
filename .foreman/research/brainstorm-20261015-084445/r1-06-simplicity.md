# Brainstorm — lens: simplicity

- **Make the installer ask before it changes your setup** — FEATURE — value 5 — effort M — risk med — category: install
  Why: Evidence A2. A default install sets bypassPermissions, outputStyle, autocompact 70%, a statusline wrapper and 20 deny rules. It also adds third-party plugins, and the only notice is "asks you to confirm once". Proposal: `install.sh` prints a table of every change with one plain sentence and its revert command. Only reversible, non-trust-expanding changes default to yes. Bypass mode defaults to no, and `--yes-all` keeps today's behaviour. `install.sh --plan` prints the settings.json diff and writes nothing, and `fm setup` re-offers the declined items later.
  Done when: a clean-HOME install with no flags leaves `permissions.defaultMode` unchanged, and `--plan` prints a diff without touching `~/.claude`.

- **Put `fm` on the shell PATH at install** — FIX — value 4 — effort S — risk low — category: install
  Why: Evidence A3. `fm` only resolves inside Claude sessions, so every "run fm …" in the README fails in a normal shell. The installer already writes `python3` to `~/.local/bin`, so a shim there fits.
  Done when: in a fresh login shell after install, `fm help` exits 0, and uninstall removes the shim.

- **Make a fresh install pass its own `fm doctor`** — FIX — value 4 — effort S — risk low — category: reliability
  Why: Evidence A8. A fresh install fails doctor on "missing backup" and prints 40 lines of passes. Proposal: checks that cannot apply yet (no state, no backup) report "n/a until first task", and a clean run prints one summary line, with detail behind `-v`.
  Done when: `fm doctor` on a fresh clean-HOME install exits 0 and prints 5 lines or fewer.

- **Put a 60-second before/after on the README's first screen** — FEATURE — value 4 — effort S — risk low — category: docs
  Why: Evidence A1. The first screen is abstract ("classifies, plans, sequences…") and shows no result. Proposal: the top shows the same one-line request run bare and run under Foreman, with the three commands to try it. The transcript comes from the tour below, so it can't rot.
  Done when: the README's first 25 lines contain one fenced transcript, and a test regenerates it from the tour and diffs clean.

- **Stop `fm repeats` from suggesting single test modules as gates** — FIX — value 3 — effort S — risk low — category: correctness
  Why: Evidence C. It recommends `unittest test_x` as an every-task gate, which is bad advice that gets adopted. Proposal: suggest only whole-suite commands, and show a narrow command as "affected-only, not a gate".
  Done when: a fixture history of single-module runs yields no gate suggestion, and a full-suite history yields exactly one.

- **Fix the newcomer dead ends in `fm task new` and `capture`** — FIX — value 4 — effort S — risk low — category: cli
  Why: Evidence A6. `fm task new` after `fm capture` makes a duplicate because it has no `--from`, and `--help` lists no valid `--type` or `--tier` values and no example. Proposal: `task new` adopts a single matching open capture, with a one-line "linked to capture C-n". Every verb's help shows its enumerated choices and at least one example, and a test enforces that.
  Done when: capture then `task new` with the same title leaves one item, and a test fails for any verb whose help has no `Example:` line.

- **Strip internal ticket numbers from user-facing help and output** — CLEAN — value 3 — effort S — risk low — category: legibility
  Why: Evidence A4. The 231-line `fm --help` is full of ticket numbers like T-0841 that mean nothing to a newcomer. Proposal: help text and default output carry no `T-####` references. Those stay in the changelog, the ledger and `--verbose`. A lint covers the help text. `fm --help` then points to `fm help`, with a line budget of 30.
  Done when: `fm --help | grep -cE 'T-[0-9]{4}'` prints 0 and the output is 30 lines or fewer.

- **Fold the diagnostic verbs into `fm inspect`, with aliases that teach** — CLEAN — value 3 — effort M — risk med — category: verb surface
  Why: Evidence D. sym, fail, logs, data, trace and outline are separate verbs, and the audit puts the verb surface at 108 and says it could reach about 70. Proposal: `fm inspect <kind>` replaces them. Old names keep working and print the new spelling once per user, then are removed on a sunset schedule.
  Done when: all six old spellings give the same output as before, the first call prints a one-line "now: fm inspect X", and the registry shows 6 fewer top-level verbs.

- **Replace the seven `_git` copies with one tested module** — CLEAN — value 3 — effort S — risk low — category: maintainability
  Why: Evidence D. Seven copies of a `_git` helper means a timeout or env fix lands in some of them and not others.
  Done when: grep finds one `def _git` in the lib, and a test covers its timeout, non-repo and detached-HEAD behaviour.

- **Gloss every unexplained field in `fm status` once** — FEATURE — value 3 — effort S — risk low — category: legibility
  Why: Evidence A5. `fm status` on an empty project dumps a STATE doc with "Drive: on" and no explanation, and jargon like brief, lane and focus runs through the whole product. Proposal: the first time a field appears, it gets a bracketed plain-words gloss (e.g. "Drive: on (keeps working through the queue until it needs you)"), then the gloss is suppressed.
  Done when: the first `fm status` shows glosses for every field and the second shows none, and the state is stored in a once-token file.

- **Wild: add `fm tour`, a scripted no-model walkthrough that also serves as demo and smoke test** — FEATURE — value 4 — effort M — risk low — category: onboarding
  Why: Wild. It builds on A1 and A8. It runs capture→plan→verify→done in a temp repo with canned model-free steps, so a newcomer sees the real state machine in two minutes. The same run generates the README transcript and acts as the post-install self-test, so one asset replaces three.
  Done when: `fm tour` exits 0 offline in under 30 s, leaves nothing outside its temp dir, and its output matches the README transcript.

- **Wild: ship a `foreman` launcher that applies the discipline settings via `--settings`, so `~/.claude` stays untouched** — FEATURE — value 4 — effort M — risk med — category: install
  Why: Wild. The rival plugins "add commands, they don't rewrite ~/.claude" (evidence B). Bypass mode, deny rules, output style and autocompact would live in a settings overlay file that only a `foreman` launch loads. Plain `claude` stays as the user had it. Trade-off: hooks still need the plugin, and users must remember to start sessions with the launcher.
  Done when: after install, `~/.claude/settings.json` is byte-identical to before. `foreman` starts a session whose effective `defaultMode` is the overlay's, while `claude` starts with the original.

- **Wild: make Foreman safe enough that bypass mode is not needed** — FEATURE — value 5 — effort L — risk high — category: trust
  Why: Wild. The guard's known-safe command classes and the plan's own scope could generate native allow rules, so a newcomer runs in acceptEdits with few prompts and never grants bypass. This answers A2 at the root, though it overlaps the "compile guard rules into native permission rules" idea above. The new part is making bypass-free the default posture and measuring it.
  Done when: a replay of 30 days of real commands under the generated rules prompts for 10% or fewer of them, and the guard still blocks every case in its bypass corpus.

- **Wild: add a once-a-quarter "hide it for a week" for unused verbs** — CLEAN — value 2 — effort M — risk med — category: verb surface
  Why: Wild. Evidence C shows 46 of 108 verbs were never run by Claude in 11 days, but they may be run by the user. For one week, a randomly chosen never-used verb is hidden from help and prints a "moved, say so to restore" line. If nobody restores it, it becomes a deletion task. This is safer than deleting on usage data alone, since several verbs were asked for by the user.
  Done when: a hidden verb still runs and prints the restore hint, `fm restore VERB` returns it to help, and an unrestored verb produces a queued deletion task after 7 days.

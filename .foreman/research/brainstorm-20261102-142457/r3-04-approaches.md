# Brainstorm — lens: approaches

- **Shim the destructive binaries on PATH** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: assumption: the guard reads the command as typed, so `x=rm; $x -rf ~` or an alias may never match. A shim dir (`rm`, `git`, `curl`, `dd`, `chmod`) applies the guard to the real argv after expansion, with no new parser. Trade-off: it is bypassed by absolute paths, so it complements the hook rather than replacing it.
  Done when: with the shims first on PATH, a fixture `bash -c 'x=rm; $x -rf $SCRATCH/keep'` is refused and ledgered, and the same call on a plain PATH is not.

- **Give lanes an outbox remote instead of a push regex** — SECURITY — value 4 — effort M — risk med — category: push safety
  Why: the push-grant steer says each push goes through `fm ship` and a one-task grant. Pointing every lane's `origin` at a local bare repo makes "can't push" a property of git, not of pattern matching. `fm ship` then relays to the real remote only under a grant. Trade-off: one extra hop, and relay failures need a clear message.
  Done when: in a lane, `git push origin main` lands only in the outbox, the real remote's ref is unchanged, and `fm ship` with a grant relays it.

- **Score lean candidates from natural variation in the ledgers** — FEATURE — value 4 — effort M — risk low — category: lean evidence
  Why: the T-2503 lean-substance rule parks growth until it is measured, and A/B runs cost tokens. Sessions where capability X fired and sessions where it didn't, matched by task kind, already sit in `fm outcomes` and the usage ledger. That gives a free first-pass uplift estimate. Trade-off: it is confounded observational data, so it ranks candidates and never proves removal.
  Done when: `fm doctor` lists the three capabilities with the lowest matched first-pass uplift, each with its sample size, and prints "insufficient" below a minimum n.

- **Reuse the test suite under strace as an effect-manifest check** — SECURITY — value 3 — effort M — risk low — category: footprint
  Why: assumption: the suite already runs every verb, so tracing it records what each verb really writes, connects to and execs. Diffing that against a small declared manifest per verb catches footprint creep with no new test code. Trade-off: it covers only paths the tests reach, and strace slows the run.
  Done when: a verb fixture that secretly writes `~/.foreman-x` or opens a socket fails the traced suite, naming the verb and the path.

- **Install by sparse checkout so unused skills never land on disk** — PERFORMANCE — value 3 — effort M — risk med — category: install weight
  Why: `plugin/skills` holds 1388 of 2125 files, and many are cards and skills that a given user's stack never loads. A git sparse-checkout cone (core plus the stacks `fm map` detects) uses an existing tool and skips a bundle format. Trade-off: it needs git at install time and a fetch path for late-needed cards.
  Done when: a fresh install of a Python-only repo has under 40% of today's file count, and `fm lib show tailwind` fetches its card on first use.

- **Run a janitor and a defender as an adversarial pair** — FEATURE — value 3 — effort L — risk med — category: agents
  Why: T-0794 and the deletion ideas lack a checked author. A read-only janitor child proposes one deletion with usage evidence. A defender child must cite a failing proof or a reachable session path to keep it. A script, not a model, rules by running the suite on the deletion branch. Trade-off: it costs two child runs per night and risks theatre if the defender always wins.
  Done when: a nightly run produces either a deletion patch that passes the full suite or a recorded keep with the cited path, and both are shown in the ledger.

- **Show a one-table "weight" page with a retire button per row** — FEATURE — value 3 — effort M — risk low — category: ui
  Why: assumption: the UI is thin and the treemap ideas are heavy. A sortable table (capability, last used, tokens injected, blast radius, session path) with one action that files a CLEAN deletion task is the do-less version. Trade-off: it shows no history and no structure.
  Done when: in the web UI, clicking Retire on a row creates a task with that row's evidence in its brief, and an empty state names the one command that fills the table.

- **Do less: compose verbs that already exist and add none** — CLEAN — value 3 — effort S — risk low — category: lean process
  Why: `fm usage --prune` (T-0468) and `fm drill` already do the measuring and the fault injection. A weekly tick that runs them and files one capped task meets the request without adding a verb. This is also the answer to the T-2654 `fm tidy --verbs` drop. Trade-off: less discoverable, and the output stays in the existing formats.
  Done when: a weekly run files at most one prune task, `fm help` lists the same verb count as before, and the diff contains no new verb.

- **Wild: run the unattended drive in a disposable clone and receive patches by mailbox** — SECURITY — value 4 — effort L — risk med — category: blast radius
  Why: wild. The drive works in a throwaway clone with no write path to the real tree, and emits `git format-patch` files into a mailbox directory. Only the gate applies them with `git am`. A runaway lane can then destroy only a clone. Trade-off: merge conflicts, and a slower loop than today's lane worktrees.
  Done when: a lane that runs `rm -rf .` in its clone leaves the real tree and refs untouched, and a good patch applies through the gate.

- **Wild: drill the guard with an approve-everything stand-in for the user** — SECURITY — value 3 — effort M — risk low — category: guard drill
  Why: wild. A fake `fm ask` responder that answers yes to everything checks that the hard stops hold when the human rubber-stamps. Assumption: nothing today separates "the guard blocked" from "the prompt was approved". Trade-off: it only proves the guard's floor, not good judgment.
  Done when: a scripted drive with the yes-responder still cannot run any command in the irreversible class, and the drill report lists each stop it reached.

- **Wild: keep the guard small by making the red-team lane minimise its own fix** — FEATURE — value 3 — effort L — risk high — category: guard
  Why: wild. After each exploit the lane may add only the smallest rule, measured in characters, that blocks it and all earlier exploits. Candidates that don't shrink the rule set's total size get an ablation check. This counters regex accretion. Trade-off: a golfed rule is hard to read, and the lane could overfit to its own exploits.
  Done when: replaying the exploit corpus against the guard after a run passes, and the rule-set character count rises by less than the new rule's own size.

- **Wild: use a weekly ejected-kit rehearsal as the lean oracle** — CLEAN — value 3 — effort L — risk med — category: lean evidence
  Why: wild. A weekly job builds the standalone kit (the guard plus the compiled steers in AGENTS.md) and runs a canned task with it. Whatever the full Foreman beats the kit on, in the duel or the exam, is the only part with proof behind it. Trade-off: the kit rots unless it is rebuilt, and the comparison is crude.
  Done when: the weekly job prints one pass/fail kit run and a list of exam scenarios the full install wins that the kit loses.

Next question: Which of Foreman's own writes and effects happen outside the guard's view (non-Bash tools, subagents, timers), and what would show the user one?
Next question: Which lean or safe changes has the user reversed or complained about after landing, so that lean is scored by regret and not just by size?

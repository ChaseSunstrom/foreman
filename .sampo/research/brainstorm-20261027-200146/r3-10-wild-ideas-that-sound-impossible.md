# Brainstorm — lens: wild: ideas that sound impossible

- **Replay real guard decisions against a candidate rule before it ships** — FEATURE — value 4 — effort S — risk low — category: guard safety
  Why: a guard rule change is judged by reading it, and the pack shows no record of what the guard refused over real use. assumption: the guard can log each command it allows or refuses.
  Done when: a rule change prints the verdict diff over the last 500 logged commands, and the gate fails if a previously refused command becomes allowed without a listed reason.

- **Fuzz the guard with spellings of every command it refuses** — SECURITY — value 4 — effort M — risk low — category: guard evasion (wild)
  Why: the guard matches command text, so `rm -rf` has many equivalent spellings (quoting, variables, `find -delete`, `xargs`). assumption: the rule set is pattern-based, not a parse of the shell.
  Done when: a generated set of at least 500 equivalent spellings of the refused commands runs through the guard in `fm check`, and every spelling the guard allows is either blocked or listed as a known gap that fails the gate.

- **Stop a run from editing its own guard** — SECURITY — value 5 — effort S — risk low — category: self-protection
  Why: a run can write to any file in the working tree, including the hook and rules files that constrain it. assumption: the hook and config files sit inside the repo the run edits.
  Done when: an edit to the hook, guard config or rules file from inside a run is refused and logged, and a test that attempts that edit passes.

- **Record model replies as tapes so the suite runs with zero API calls** — PERFORMANCE — value 4 — effort M — risk low — category: test cost
  Why: the usage burn and the Sonnet/compact work show that model calls are the main cost, and test runs that touch the model spend it. assumption: some gates still need a live model reply.
  Done when: `fm check` run with the network off and no API key passes, and a proxy counter shows zero model requests.

- **Stream gate verdicts into the diff as the model types** — FEATURE — value 3 — effort L — risk med — category: feedback latency
  Why: the gate waits until a run ends, and the pack shows gate-lock waits of up to 15 minutes. assumption: each edit arrives as a tool call, so a hunk is visible before the turn finishes.
  Done when: a lint failure from an early hunk shows in the pane before the run's last edit lands, on the fixture repo.

- **Prove a rename is behaviour-preserving by AST equivalence, with zero tokens** — FEATURE — value 3 — effort L — risk med — category: verification (wild)
  Why: a rename-only diff still costs a full model-led proof cycle. assumption: the repo's language has a parser the tool can call.
  Done when: a rename-only diff on the fixture is marked equivalent with no model call, and a diff that also changes logic is not marked equivalent.

- **Merge near-duplicate playbooks into parameterised templates** — CLEAN — value 4 — effort L — risk med — category: playbook library
  Why: the playbook target is 10,000+ entries, and many probably differ only by a noun or a path. assumption: most near-duplicates can be expressed as one template with parameters.
  Done when: on a 200-playbook fixture the merged set is at least 30% smaller and routes the same test queries to the same playbook outcomes.

- **Judge each diff without the transcript** — FEATURE — value 3 — effort M — risk low — category: agent review
  Why: a reviewer that reads the model's reasoning tends to agree with it. assumption: the verdict can be taken from the diff, the tests and the proof alone.
  Done when: a reviewer child given only the diff and the proof output flags a fixture change with a planted bug, and the child's prompt contains no transcript text.

- **Run an opt-in federated duel that shares only verdict counts** — FEATURE — value 2 — effort L — risk high — category: privacy (wild)
  Why: the duel is run on one machine, so it has few cases. assumption: users would share aggregate counts, not code or prompts, and only after an explicit setting.
  Done when: with the setting off, zero bytes leave the machine; with it on, the payload contains only per-task-kind pass counts, shown to the user before sending.

- **Export a closed task as a script anyone can rerun without Foreman** — FEATURE — value 3 — effort M — risk low — category: portability (wild)
  Why: the pack lists sneakernet bundles and cloud routines, but a receipt that cannot be rerun without the tool is still a dead end. assumption: each task's proof is a shell command.
  Done when: the exported script, run in a clean clone with only git and the shell, reproduces the task's proof result.

- **Pin the hook files by hash and refuse a silent change** — SECURITY — value 4 — effort S — risk low — category: supply chain
  Why: the open supply-chain item T-0791 covers the plugin broadly, but the hook files are the part that decides what runs. assumption: a plugin update can change hook files without a visible diff.
  Done when: changing one hook file by one byte makes the next session refuse to start until the user re-approves the hash, and a test checks it.

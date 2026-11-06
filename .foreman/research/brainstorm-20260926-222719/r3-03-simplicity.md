# Brainstorm — lens: simplicity

Round three is mostly marginal from a simplicity lens. About 200 ideas already cover the ratchet, registry, profile, sunsets, and folding ledgers. These five are the ones I couldn't find covered.

- **Create the task lazily, on the first edit** — FEATURE — value 4 — effort M — risk med
  Why: assumption: questions and explanations currently open a brief (RESEARCH) with capture, expand and ground before any answer. The only hard rule is "no edits without an active task", so the guard already marks the natural point where a task must exist. Existing ideas cover "answer state questions in the hook" and "short-circuit already done", but not a general read-only lane.
  Done when: a replayed prompt that only reads files creates no brief and no gate output, and the first Edit or Write in the same session creates a brief and proceeds under the normal gates.

- **Make hooks inert outside a detected project root** — FEATURE — value 3 — effort S — risk low
  Why: assumption: the guard, injections and drive loop engage in any directory. This brainstorm's own working directory (`/run/user/.../fm-ideas-*`) is not a git repo. In scratch dirs, `$HOME` and `/tmp`, "no edits without a task" is pure friction and the injections are wasted tokens.
  Done when: in a temp dir with no VCS or manifest, SessionStart injects nothing, the guard allows edits, and a `fm doctor` line says "inert: no project root". In a git repo behavior is unchanged.

- **Define a glossary of at most 15 terms and lint every text surface against it** — CLEAN — value 3 — effort S — risk low
  Why: the pack uses check, verify, gate, audit, prove, sentinel and evidence for overlapping ideas. Overloaded vocabulary costs the model reasoning tokens and causes wrong command picks. Existing ideas merge tiers and commands, not the words.
  Done when: a test fails if rules, skills or `fm --help` output use a term from the deprecated-synonym list. The glossary is one file that the rules text cites by reference.

- **Replace pre-approval with act-then-undo for local reversible actions** — CLEAN — value 3 — effort M — risk med
  Why: assumption: some yes/no prompts guard actions that focus-time checkpoints can already reverse, such as worktree candidates or local edits outside protected paths. Batching decision sheets reduces the count of prompts but keeps them all. Only outward or costly actions, per the existing `fm decide --kind`, need a question.
  Done when: a table of action kinds marks each as ask or act-and-report, and a test proves no yes/no is emitted for the reversible kinds. `fm undo` restores the pre-action tree in the same test.

- **Log flag and env-var usage, not only command usage, and delete the dead ones** — CLEAN — value 2 — effort S — risk low
  Why: the command-usage log prunes whole commands, but options like `--dry`, `--seen`, `--models` and `--kind` accumulate unseen. This is a second-order extension of that log.
  Done when: `fm usage` lists options with zero uses over 30 days, and a test asserts each remaining option is exercised by at least one test or one recorded use.

Anything beyond these five would mostly restate existing ideas. More surface is now the bigger risk than any missing feature.

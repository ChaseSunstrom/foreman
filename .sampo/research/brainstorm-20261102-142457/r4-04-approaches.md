# Brainstorm — lens: approaches

- **Mutation-census the guard's rules** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: the pack's guard ideas (lint for shadowed rules, a replay corpus, an evasion corpus) all assume the existing rules are tested. Nothing asks whether each rule is needed or covered. Delete or loosen one rule at a time, replay the corpus, and sort the rules by what happens. If nothing fails, the rule is untested or redundant, so either add a test or cut it. One mechanism gives both the lean and the safe answer.
  Done when: `fm guard --census` prints, per rule, the corpus cases that fail without it. A rule with zero failing cases is listed as "uncovered or redundant".

- **Confine hooks with Landlock before they read input** — SECURITY — value 4 — effort M — risk med — category: sandbox
  Why: assumption: the host kernel is `7.2.10-hardened`, and linux-hardened usually disables unprivileged user namespaces, so bwrap-based sandbox ideas may silently fail. Landlock needs no namespaces. A hook that restricts itself to the state dir (write) and the repo (read) first makes a parser bug or injected ledger text far less harmful.
  Done when: a test hook that tries to write `~/.ssh/x` after confinement gets EACCES. On a kernel without Landlock, the hook logs "unconfined" and does not crash.

- **Require a detach test for every capability** — CLEAN — value 4 — effort M — risk low — category: lean
  Why: Lite mode, eject, fuses and "retire adapters" (T-0794) all need each capability to be removable. Make "turn this one off and the suite and ledger readers still pass" a ship-gate row, so detachability stays true as the code grows.
  Done when: `fm check` flags any capability registered without an off switch, and a capability whose off state breaks a reader fails the gate.

- **Funnel every state write through one path-checked helper** — SECURITY — value 3 — effort S — risk low — category: safety
  Why: a pure-Python fallback that does not depend on the kernel. Each verb declares its write set, and one `fmio.write` refuses a path outside it. This is the do-less alternative to OS confinement and also gives a per-verb write manifest.
  Done when: a verb that writes outside its declared set raises `PolicyError` with a `Next:` line. A grep test finds no raw `open(..., "w")` outside the helper.

- **Make growth need a recorded waiver** — CLEAN — value 3 — effort S — risk low — category: lean
  Why: the lean row is "pending" until a measurement exists. Track three numbers only: installed files, tokens injected at session start, and hook p95. Any rise over 2% needs a `Lean:` line in the task naming the reason, and that line goes to the ledger. The trade-off is a little friction per task, in exchange for no new gauges.
  Done when: a diff that adds 500 injected tokens without a `Lean:` line fails `fm ship`. With the line, it passes and the waiver appears in `fm outcomes`.

- **Score installed timer units with `systemd-analyze security`** — SECURITY — value 3 — effort S — risk low — category: ops
  Why: this reuses an existing tool for the unattended tick and drive units, and the score can be ratcheted so it never worsens. It needs no new code beyond a parser and a threshold. It covers only systemd hosts.
  Done when: `fm doctor` prints each unit's exposure score and warns when a unit scores worse than the stored ceiling.

- **Run a cross-vendor deletion-only review each release** — CLEAN — value 3 — effort M — risk med — category: lean
  Why: weakness-finding must use signals Foreman didn't author. Give Codex or Gemini only the release diff and one question: what could be deleted without changing user-visible behaviour? A finding counts only if it quotes the file and line. It is cheap, but the reviewer has no usage data, so filter its answers against the usage census.
  Done when: a release run files at most five removal candidates, each with a quoted line, or records "none found" with the denominator.

- **Replay hook inputs under a shrinking environment** — SECURITY — value 3 — effort M — risk low — category: robustness
  Why: lean also means working with less around it. Replay recorded hook payloads with `-I`, an empty `PATH` apart from python, no `claude`, and a read-only plugin dir. Any hook that now fails open or crashes is a hidden dependency.
  Done when: a matrix test lists, for each hook, which removed dependency changes its verdict. Zero changes is a pass.

- **Wild: ship hooks with proof-carrying effect certificates** — SECURITY — value 3 — effort L — risk med — category: integrity
  Why: wild. At build time an AST pass records each hook's reachable file, network and subprocess effects into a hash. The launcher refuses to run a hook whose current AST no longer matches. This catches a tampered installed copy and any effect added without review. It is heavy, and the AST analysis will be conservative.
  Done when: editing an installed hook to add `socket.connect` makes the launcher refuse it and print `Next: fm doctor`.

- **Wild: publish the ledger formats as an open spec with a 300-line reference reader** — CLEAN — value 3 — effort L — risk low — category: lean
  Why: wild. If the formats are a documented spec, Foreman's own readers can shrink to adapters, other agents can read the ledgers, and the spec itself bounds the schema growth that fm doctor currently polices after the fact.
  Done when: the reference reader parses a ledger copy and reproduces `fm outcomes` totals to the digit. A format change without a spec change fails the gate.

- **Wild: run a "heavy sleeper" week where one capability is secretly off per day** — PERFORMANCE — value 3 — effort M — risk med — category: measurement
  Why: wild. Rotate one non-core capability off per day for the user, unannounced, on the user's own queue. The `fm outcomes`, correction and override rates for those days become a natural experiment on which weight earns its place. The risk is that real work runs without a safeguard, so skip anything in the safety core.
  Done when: after seven days, each capability has an on/off outcome delta with its sample size, and any capability with too few samples is listed as "undecided".

Next question: which of Foreman's own safeguards would still run if the installed hooks were silently replaced by an older or edited copy, and what would reveal it first?
Next question: when linux-hardened (or any host setting) quietly disables a sandbox primitive, which existing "safe" claims stop being true without any record?

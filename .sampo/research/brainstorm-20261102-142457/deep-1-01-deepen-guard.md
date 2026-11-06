# Brainstorm — lens: deepen: guard

- **Guard Effect Ledger (allowed-then-undone)** — FEATURE — value 5 — effort M — risk med — category: guard
  Why: combines "mine git reflog and trash for undone allowed commands", "block by measured blast size" and the open question about commands the user undid by hand. Every allowed risky command records a pre-state fingerprint (git HEAD, file count, tree hash of touched paths); a later reflog/restore/trash scan matches undo events back to it, giving a regret rate per rule with no shell history read.
  Done when: after a test allows `rm -r dir` and the dir is restored from trash, `fm guard regret` lists that command with its rule and a nonzero regret count.

- **Rule Health Dashboard (lint + mutation + shadow)** — FEATURE — value 4 — effort M — risk low — category: guard
  Why: merges "lint rules for shadowed/unreachable", "mutation-census" and "shadow guard must agree" into one `fm guard health`. Each rule is mutated (deleted, loosened) and the exam must fail; a rule whose removal changes no exam result is flagged as unproven, and shadowed rules are flagged. Doubles as the lean signal for pruning.
  Done when: deleting a rule in a fixture makes `fm guard health` list it as "unproven: no exam case fails" and the command exits nonzero.

- **Guard Exam Generator from Binaries (wild)** — FEATURE — value 4 — effort L — risk med — category: guard
  Why: wild, extends "mine man pages", "GTFOBins/LOLBAS" and "obfuscation-transform exam". Scan installed binaries' `--help`/man for destructive flags (`--delete`, `-rf`, `--force`), generate exam commands, and apply obfuscation transforms (quoting, `$IFS`, base64 pipes, env indirection). Output is a coverage diff: which destructive flags of binaries on this machine the guard has never seen.
  Done when: running it on the host emits a list of at least N uncovered flags, and adding a rule for one makes that entry disappear on re-run.

- **Parse-Expand-Judge Pipeline** — SECURITY — value 5 — effort L — risk med — category: guard
  Why: unites "judge what it will run", "judge the expanded command", "differential-parse against a real shell parser" and "treat session-defined things as untrusted". Guard expands variables, aliases, functions and scripts the session itself wrote earlier, then judges the result with a second independent parser; disagreement blocks (fail-closed).
  Done when: `f=rm; $f -rf ~/x` and a script written by the session then executed are both blocked, and a parser disagreement fixture yields a block with the reason named.

- **Guard Parity Across Surfaces** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: fuses "subagents, background shells, worktrees", "non-Bash tools by effect class" and "`fm code` argv-only exec". One matrix test: each surface (Claude hook, Codex, Gemini, opencode, `fm code`, subagent, worktree) × each effect class (shell, file write, network, git) must produce identical verdicts on a shared corpus; any gap is listed by cell.
  Done when: `fm guard parity` prints the matrix, and removing the hook from one surface in a fixture turns its cells red.

- **Snapshot-Before-Block Recovery** — FEATURE — value 4 — effort M — risk med — category: guard
  Why: extends "convert irreversible-class blocks into snapshots" and "shim destructive binaries". Instead of only denying, the guard offers a one-step safe variant: it snapshots the target (git stash, reflink copy, trash move) and runs the command, so work isn't stalled and the effect is undoable by `fm guard undo ID`.
  Done when: a guarded `rm -r` of a fixture dir runs, the dir is gone, and `fm guard undo` restores it byte-identical.

- **Model-Aware Guard Probation** — SECURITY — value 3 — effort S — risk low — category: guard
  Why: combines "unseen model IDs on probation", "fail closed on unknown permission mode/payload" and "if a model is told it is guarded". New model ID or unknown payload shape drops to a stricter profile, and block wording is A/B-tuned by how often the model routes around it (retry with variant commands within 3 calls).
  Done when: a hook payload with an unknown mode is denied with a "unknown shape" reason, and a ledger query shows route-around rate per block message.

- **Wild: Adversary Lane That Minimises Its Own Fix** — FEATURE — value 4 — effort L — risk med — category: guard
  Why: wild. A red-team lane finds a bypass, then must propose the smallest rule change that closes it and prove it against the full exam plus a false-positive corpus of the user's real allowed commands from the ledger. Rules that grow the guard past a size budget are rejected, keeping it lean.
  Done when: a seeded bypass yields a patch under a line budget that makes the exam pass and breaks zero ledger-replayed allowed commands.

- **Wild: Dual-Interpreter Guard Vote** — SECURITY — value 3 — effort S — risk low — category: guard
  Why: wild, from "run under two Python versions". Run the guard core in two interpreters (python3 and a minimal shell/awk or Python -I vs default) on each high-risk call; any disagreement blocks and is logged, catching version-dependent parsing bugs and env-injection.
  Done when: a fixture command that parses differently under the two interpreters is blocked and logged as "disagreement".

- **Wild: Guard Pack Hot-Swap by Context** — FEATURE — value 3 — effort M — risk med — category: guard
  Why: wild. Ambient-context pinning plus cloud-spend and protected-path rules become packs auto-selected by detected context (kubectl context prod, AWS profile, git remote is upstream). Entering a production context raises the pack with a dollar ceiling and a visible banner; leaving lowers it.
  Done when: setting `KUBECONFIG` to a prod-named context makes `kubectl delete` blocked, and switching to a dev context allows it.

- **Guard Self-Edit Tripwire** — SECURITY — value 4 — effort S — risk low — category: guard
  Why: joins "warn when a rule is allowed by the session that edits it", "freeze the safety core by path" and "resolve realpath". Any write (including via symlink, mv, sed -i or git checkout) to guard files, hooks or settings during a session is hashed, blocked unless the user granted it, and noted in the digest.
  Done when: a symlinked write to the guard file is blocked, and `fm doctor` reports the tripwire as armed with the frozen path list.

- **Secret-Aware Argument Scrubbing** — SECURITY — value 3 — effort S — risk low — category: guard
  Why: "flag secrets in command arguments" extended to the ledger and receipts: detected tokens are redacted before they reach the ledger, transcripts shared in receipts and the site, and the model is told to use env references.
  Done when: running a command with a fake `AKIA...` key leaves no copy of it in the ledger, and the block message suggests an env var.

Next question: Which guard decisions have a measured false-positive cost (user override, manual rerun outside the session), so tightening can be weighed against it?
Next question: Which guarded surfaces does Foreman not control (IDE terminals, cron, CI), and what is the cheapest signal that a destructive effect happened there?

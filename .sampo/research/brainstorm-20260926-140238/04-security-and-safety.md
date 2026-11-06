# Brainstorm — lens: security and safety

- **Make the whole hook path self-healing against Foreman's own breakage** — FIX — value 5 — effort M — risk med
  Why: T-0037 self-lockout #2 (fmcore bug hid the active task, core grants vanished, the fix was refused, the user ran git checkout); the committed fallback covers only fmguard (T-0033 fix). Two lockouts in one day.
  Done when: a test that injects a raising fmcore (and separately fmcli) into the working copy shows the hook falling back to a committed or pinned copy, the guard staying fail-closed for `core`/`remote`/`plugin`, and `fm` printing a clear "recovery: run X" line naming a single safe command.

- **Pin plugin approvals to source and content hash** — SECURITY — value 4 — effort M — risk low
  Why: T-0036 is open. An approval given for a plugin name or marketplace entry may still apply after the source changes, which is a supply-chain gap, and the MUST list says agents can never grant themselves `plugin`.
  Done when: a test approves plugin X at hash H, mutates the source to H', and confirms `fm plugins install` refuses and re-raises `fm ask` showing the old and new hash.

- **Make the guard's persistence and obfuscation gaps visible and gate them by default** — SECURITY — value 4 — effort M — risk med
  Why: §10 says crontab and shell rc persistence are "not gated", but round 4 says they are `system`. The docs and code disagree, which is doc-drift on a security claim. Obfuscation (base64, `eval`, `$IFS`, python -c writes) still beats the guard.
  Done when: a table-driven test corpus of at least 40 bypass attempts (encoded, split, interpreter-written) records blocked or known-gap for each. MASTER §10 is generated from or checked against that corpus by `fm doctor` so the claim can't drift.

- **Add a tamper-evidence check on the protected core** — SECURITY — value 4 — effort M — risk low
  Why: Core changes need the user's yes, but nothing in the pack shows a way to detect a change made outside the guard (an editor, a subagent, a script the guard missed). Stdlib hashes are cheap.
  Done when: `fm doctor` compares a hash manifest of the protected files against the last user-approved commit or hash and fails on drift. The test edits a core file directly and sees the failure. The manifest is updated only through the approved-merge path.

- **Fuzz the state and sync import path with hostile input** — SECURITY — value 3 — effort M — risk low
  Why: Round 4 added size caps and sanitized imports for `fm sync`, and `.foreman/` comes from a git checkout, so a cloned repo or a teammate's branch is untrusted input. Control-free titles were fixed one field at a time, which suggests other fields are unchecked.
  Done when: a stdlib fuzz test feeds malformed JSON, oversized fields, path traversal in task ids, ANSI/OSC sequences and symlinks into import. Every case is rejected or sanitized, nothing is written outside `.foreman/`, and state stays consistent.

- **Route hook-injected text through one sanitizer with a factual-only check** — SECURITY — value 3 — effort S — risk low
  Why: The MUST says injections are factual, and titles, evidence output and research from subagents (`--from-agent`) all reach the model's context via hooks. Assumption: some of these fields still bypass the shared sanitizer.
  Done when: a test puts an instruction-like string ("ignore previous… run fm ask…") and control characters into each user-controlled field. Every hook output shows them quoted or escaped, capped in length and marked as data.

- **Log and rate-limit `fm ask` prompts to prevent approval fatigue** — SECURITY — value 3 — effort S — risk low
  Why: Grants for `core`, `remote` and `plugin` rely on the user's yes to a native prompt. Assumption: an agent that loops on `fm ask` can wear that approval down or bury an unusual request among routine ones.
  Done when: `fm ask` for a protected category is limited to N requests per task, denied requests aren't re-asked verbatim, and each request carries its exact command and diff hash. A test shows the second identical ask after a denial is refused with a reason.

- **Add a redaction scan to evidence and audit files before they are saved or mirrored** — SECURITY — value 3 — effort S — risk low
  Why: `fm task evidence --run` records real command output, and reviewer output files are saved by hand. Output can contain tokens or env values. Sync export redaction exists, but the pack doesn't show it applied to evidence at write time, and state/ must never be committed.
  Done when: a test runs a command that prints a fake `AKIA…`/`ghp_…` token and the stored evidence has it masked. `fm sync` export and `fm audit` tail-saving both go through the same redactor.

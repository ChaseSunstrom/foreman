**Verdict: changes needed.** One HIGH adversary finding. I could not run code (read-only, no shell), so each finding is proved by tracing `fmledger.chain` at `~/.claude/foreman/plugin/lib/fmledger.py`.

## lens: adversary

- HIGH — plugin/lib/fmledger.py:29-35 — A damage line is a hole in the chain. The `continue` skips the check of its own `prev`, and its content is gone, so nothing proves what sat before it. Any run of lines before a damage line can be deleted or edited with no break, and a forged or granted ack then makes verify pass. Baseline: a mid-file deletion broke the chain at the next line. — Pin the predecessor inside a verified line. When `log_event` finds a NUL-ending last line, it writes the hash of the line before it into the next line's data. `chain` then requires that value to equal the `prev` seen before the damage line. Also check a damage line's own `prev` whenever its intact prefix still holds the 16 hex digits. — confidence: high (code trace)
  - Failing input, with ledger L1..L5, D (668 NULs), L7 (prev=hash(D)), L8 (ack key hash(L5):hash(D)):
    1. Delete L2..L5, leaving L1, D, L7, L8.
    2. L1 verifies. D gets key `hash(L1):hash(D)`, which is not the ack's key, so it is pending. L7's `prev` is hash(D), so no break. End state is pending, so `damage_only` is true.
    3. Either `fm verify-ledger --accept-damage` writes a fresh ack, or an attacker appends `c.log_event(p, "ledger_damage_ack", data={"keys": [f"{hash(L1)}:{hash(D)}"]})`. Verify then exits 0 with 4 events erased.
  - The ack has no authentication, so a forged one is indistinguishable from an operator's.
  - Only `--head` with a receipt taken after the deleted lines still catches it.
  - `test_accept_damage_never_accepts_an_edit` never puts a NUL line after the edit, so it misses this.
- MEDIUM — plugin/lib/fmledger.py:95-96 — `accept_damage` writes the ack before the `--head` anchor is checked. — Run `chain(p, head)` first and write the ack only if it comes back `damage_only` and the anchor is found (or none was given). — confidence: high
  - Failing input: `fm verify-ledger --accept-damage --head H` where H's line was cut.
  - The ack is persisted, the output says "Crash damage accepted" and also "Ledger broken: no line hashes to the head", and a plain `verify-ledger` afterwards passes.
- LOW — plugin/lib/fmledger.py:29 — A NUL-ending line before the chain start now breaks verify, where a legacy line used to be harmless. — Treat NUL lines before `r["start"]` as predating the chain. — confidence: medium
- LOW — plugin/lib/fmledger.py:84-89 — `receipt()` prints a clean "Ledger: head …" after an ack and does not mention the accepted damage. — Append the damage count. — confidence: medium

Checked and sound:
- A zeroed mid-file line breaks at its successor's `prev`, so `damage_only` is unset.
- A key collision only occurs for three or more consecutive same-size zero lines, and an ack only pops damage that comes before it.
- Pre-planting an ack fails because it matches only earlier pending keys.
- A line of JSON text followed by NULs at the tail is no worse than the old tail-cut gap.
- `fm tidy` roll: `_roll_ledger` keeps line bytes intact, `pending` spans archives, and keys don't depend on line numbers.

## Acceptance criteria
- Named with its bytes, stays broken until `--accept-damage`, passes afterwards naming the gap, a second same-size damage breaks again, an edit is never accepted: **met** for the three listed tests (not run), but the HIGH finding means "an edit is never accepted" does not hold when a damage line is present.

## Intent
- MEDIUM — plugin/lib/fmcore.py:880-899 — The fsync half of the request is missing. `log_event` has no fsync, `fmcore.py` is unmodified, and the only fsync in the file (line 813) is in `write_atomic`. — Add `f.flush(); os.fsync(f.fileno())` for fm commands only, skipping hooks. — confidence: high

## Implicit decisions
- The ack is a plain ledger event keyed `prev:hash`, with no actor or proof of who ran it.
- Damaged-line size is reported as trailing NUL count only.
- Acks are honoured even from unchained gap lines.

## Not checked
- I ran no tests and executed no code.
- Concurrent writers during `accept_damage`.
- `fmdoctor` ledger checks (lines 1305 and 1336).

**Noticed:** `fmtidy.py:447` appends a newline to an unterminated last line when archiving. Harmless to the hash, but worth a test with a NUL line in the rolled prefix.

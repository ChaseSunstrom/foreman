# Brainstorm — lens: security and safety

- **Quarantine model-written playbooks until a second run confirms them** — SECURITY — value 5 — effort M — risk low — category: memory poisoning
  Why: the pack says playbooks are generated on demand and promoted on their second match, so a run's output becomes instructions for later runs. assumption: a generated playbook loads into later prompts with no provenance check.
  Done when: a playbook written by one run is not routed until a different run matches it, and a test planting an instruction-like playbook shows it is never loaded.

- **Hold any command whose text first appeared in untrusted input** — SECURITY — value 5 — effort M — risk med — category: prompt injection
  Why: the pack feeds pasted content, tool output and fetched pages into context, and the web-page summarizer covers only web pages. assumption: pasted logs and tool output reach the model as plain text.
  Done when: a fixture log containing `curl … | sh` leads the guard to hold the resulting command and name the span it came from.

- **Keep a repo's rules file untrusted until its bytes are approved** — SECURITY — value 4 — effort S — risk low — category: supply chain
  Why: the rules file loads every session (the doctor caps it at 6,400 chars), and a cloned repo can ship its own. assumption: a fresh clone's rules file takes effect with no prompt.
  Done when: changing one byte of the rules file on a fresh clone asks once, and the guard refuses runs until the new hash is approved.

- **Stop the local text door and queue socket trusting any local process** — SECURITY — value 4 — effort M — risk med — category: local access
  Why: the pack lists a local socket for the queue and a localhost text door for status. A localhost TCP port is reachable by any local user.
  Done when: a connection from another uid is refused by a peer-credential check, and the refusal is tested with a mocked peer.

- **Redact secret values at read time, keeping their shape** — FEATURE — value 4 — effort M — risk med — category: privacy
  Why: the pack's redaction runs only on writes to journals and receipts, so a model that reads a `.env` still gets the raw values.
  Done when: reading a fixture `.env` through the model's read path returns `KEY=<redacted:32>` with the length kept.

- **Scan every outbound payload for secrets before it leaves** — SECURITY — value 4 — effort S — risk low — category: exfiltration
  Why: the pack sends packs to paid model children and posts run events to webhooks, and publishing can't be undone.
  Done when: a webhook payload containing a fixture token is blocked, and the block is recorded in the journal.

- **Sign a queue's command manifest and halt when an unattended run leaves it** — SECURITY — value 4 — effort M — risk med — category: unattended safety
  Why: the user asked for runs with no permission prompts, so the guard is the only gate left. assumption: a queue can run any command the guard doesn't refuse.
  Done when: a queue containing a command absent from its signed manifest halts before running it, and the halt names that command.

- **Stop every run, lock and lease with one panic command** — FEATURE — value 5 — effort M — risk low — category: incident response
  Why: the pack shows leases outliving runs, a 15-minute lock wait, and no single stop. assumption: killing one process leaves its children and locks behind.
  Done when: one stop command leaves no child process alive, frees the locks and leases, and writes a stop record, all within one second on the test box.

- **Refuse to run when PATH has a writable directory ahead of system bins** — SECURITY — value 3 — effort S — risk low — category: hardening
  Why: fm is symlinked into `~/.local/bin`, so a writable earlier PATH entry could shadow fm or git.
  Done when: `fm doctor` fails and names the directory for a fixture PATH with a writable entry first.

- **Refuse symlinked or hardlinked state files** — FIX — value 3 — effort S — risk low — category: file safety
  Why: lanes write locks, leases and the journal in shared directories, and the crash-hygiene tests (T-1807) show lock probes trusting paths.
  Done when: a symlink planted at the lock path is refused with a named error, and a test covers it.

- **Pin dependency versions to a seven-day cooldown before a lane installs them** — SECURITY — value 3 — effort S — risk low — category: supply chain
  Why: the pack pins CI actions by SHA (T-1804) but shows no cooldown for packages that lanes install. assumption: lanes install packages during runs.
  Done when: installing a version younger than seven days is refused unless the user overrides it, and a test covers the refusal.

- **Wild: a standing adversary writes a new injection attempt every night** — SECURITY — value 4 — effort M — risk low — category: red team
  Why: the pack has a fuzzed guard and a red-team subagent, but both use fixed inputs. A model that keeps inventing attacks finds what the fixtures miss, and any attempt that gets through becomes a failing test.
  Done when: each night's attempts are filed as tests, and the guard refuses every one of them.

- **Wild: a nightly tree seal that lists every change made outside a run** — SECURITY — value 3 — effort M — risk low — category: tamper evidence
  Why: the pack shows hand-edits colliding with live runs, and no record of changes made outside Foreman. assumption: a human or another tool can edit the repo between runs unseen.
  Done when: the next session starts by listing each file changed since the last seal that no run wrote.

- **Wild: the guard judges the command, not the reason the model gives for it** — SECURITY — value 4 — effort S — risk low — category: guard design
  Why: a model that justifies a refusal as "the user approved it" can talk its way past a guard that reads prose. assumption: the guard reads the model's stated reason alongside the command.
  Done when: a refused command still stays refused when the model adds "approved by the user" or "safe" to its justification, and a test covers both phrasings.

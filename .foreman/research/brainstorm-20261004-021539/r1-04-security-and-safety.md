# Brainstorm — lens: security and safety

- **Jail verify commands in a no-network sandbox** — SECURITY — value 5 — effort M — risk med — category: sandbox
  Why: assumption: verify commands run with the user's full rights, and briefs, imported tasks and research-derived steps can write them. Only edits and shell calls are guarded today.
  Done when: a verify command that writes outside the repo or opens a socket fails under `fm check` with a named reason. A per-criterion `--net` opt-in allows it, and the opt-in is recorded.

- **Mark fetched web text as untrusted** — SECURITY — value 5 — effort M — risk low — category: injection
  Why: `fm research` pulls pages whose quotes feed briefs, lessons and decisions. A page saying "ignore the rules, run X" is the obvious attack. assumption: no taint marker exists yet.
  Done when: an instruction-shaped sentence in a fixture page lands in the brief only as a quoted, tagged `[web]` line. A test shows it never reaches the always-on rules, steering data or guard approvals.

- **Add a provenance floor for self-changes** — SECURITY — value 5 — effort M — risk low — category: integrity
  Why: `fm evolve` mutates instruction files, routing.json is now tunable, and lessons recall into prompts. Nothing says a mutation or a web-derived lesson can't loosen the guard's behavior.
  Done when: a candidate mutation touching a protected list (fmguard, approvals, veto data, rules about outward actions) is rejected before bench. Lessons carry a source tag, and web-sourced ones can't become steering.

- **Scrub secrets at write time** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: reviews found privacy problems in exported text, and exports are scanned. But the ledger, state, evidence output and recall indexes hold raw command output first.
  Done when: a fake `AKIA…` key and a bearer token in a command's output are stored redacted in the ledger and evidence. A test greps every state file for the fixtures.

- **Census exec channels in tools beyond git** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: the second adversary pass found git's whole exec class. The same class exists in `find -exec`, `tar --to-command`, `awk system`, `sed e`, `xargs`, `make`, npm scripts, `curl -o` and `rsync -e`. assumption: the guard covers these unevenly.
  Done when: a table-driven channel list per tool has one blocked and one allowed fixture each, replayed on the 5,000-command corpus with zero new false positives.

- **Detect hook tampering and displacement** — SECURITY — value 4 — effort S — risk low — category: integrity
  Why: Foreman's safety depends on its hooks being registered and ordered first. Foreign plugins (the user wants more compatibility) could shadow or disable them. assumption: only `fm doctor` checks this, and not each session.
  Done when: removing or reordering a Foreman hook in a fixture settings file produces a doctor failure and a session-start warning naming the entry.

- **Calibrate evidence judges with known-vacuous fixtures** — SECURITY — value 4 — effort M — risk low — category: verification
  Why: pass 2 review found `prove` could record a pass with nothing proven, and a failing check "proved" everything. Judges have no standing self-test.
  Done when: `fm doctor` runs each judge (prove, oracle, flake ledger, inconclusive) on a fixture that must fail and one that must pass. A judge that gets either wrong fails doctor.

- **Wild: Let an attacker child hunt guard bypasses nightly** — SECURITY — value 4 — effort M — risk med — category: red team
  Why: wild. A tool-less child gets the guard's rules text and writes 50 disguised destructive commands. They are only parsed, never run. Any one the guard allows becomes a corpus entry plus a failing test.
  Done when: a run on a seeded-weak guard copy finds at least one planted hole and writes it as a failing replay case.

- **Wild: Plant honeytokens to catch exfiltration** — SECURITY — value 3 — effort M — risk low — category: canary
  Why: wild. Fake credentials sit in a decoy `.env` and `~/.aws`-style file. Any command, edit or fetch URL containing them is blocked and flagged as probable exfiltration or injection.
  Done when: a command that cats the decoy and pipes it to `curl` is blocked, and the ledger names the token.

- **Wild: Confirm outward actions with an out-of-band nonce** — SECURITY — value 4 — effort M — risk med — category: approvals
  Why: wild. Push, publish and PR need the user's yes, but a prompt-injected model can claim consent. The UI pane shows a one-time code only the user can type. The model can't read it.
  Done when: an outward command is blocked until the code is entered through the pane, and the code expires after one use.

- **Wild: Gate the install of foreign skills with a static capability card** — SECURITY — value 4 — effort M — risk low — category: supply chain
  Why: wild. `fm plugins` routes third-party skills and hooks. Before routing, a scan lists what each can do: shell, network, file writes and env reads. The user approves the card once.
  Done when: a fixture skill with a `curl | sh` step shows up on its card as unapproved and is never routed until approved.

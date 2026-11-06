# Brainstorm — lens: bold bets

- **Add a hermetic evidence grade** — FEATURE — value 4 — effort M — risk med — category: verification
  Why: evidence grades, flaky reruns and hash-seed checks exist, but nothing proves a green gate doesn't depend on the network, the wall clock or a leftover file. Assumption: bubblewrap or `unshare` is available on Linux, with graceful fallback elsewhere.
  Done when: a test that calls the network or reads the time passes under a normal run but is graded "non-hermetic" when the close gate reruns it with the network off, a frozen clock and a fresh HOME, and the close-out prints that grade.

- **Sign task receipts with the user's own SSH key** — SECURITY — value 4 — effort M — risk low — category: proof
  Why: an open receipt schema and a `foreman/evidence` status check were proposed, but an unsigned receipt can be forged by anything that can write the ledger. `ssh-keygen -Y sign` works offline, so it fits local-first. Assumption: the user has or will accept an SSH key.
  Done when: `fm verify-receipt FILE` fails after one byte of a receipt is edited and passes on the original, and a CI snippet performs the same check using only the committed allowed-signers file.

- **Re-justify each mechanism whenever the model changes** — FEATURE — value 5 — effort L — risk med — category: simplicity
  Why: round 4's over-engineering audit and the "Lite must tie the full build" idea both point at the same gap: nothing re-tests scaffolding when a new model ships (the pack lists Fable 5.1 and Opus 5.5). Each hook, skill and gate should carry a measured lift that expires.
  Done when: `fm bench --ablate` runs the replay set with each mechanism off for a given model id and writes a table of lift per mechanism. It also files a "retire" task for any mechanism whose lift is within noise on that model.

- **Compile policy sentences into guard rules with generated adversarial cases** — FEATURE — value 4 — effort M — risk med — category: user value
  Why: "configure by saying it" was proposed, but nothing makes the compiled rule trustworthy. A sentence like "never touch billing/ without asking" should produce a rule plus 10 should-block and 10 should-allow commands that the user skims.
  Done when: `fm rule "never edit migrations/ without asking"` writes a guard rule and a corpus file, refuses to activate if any listed case misbehaves, and shows the user the 20 cases once for approval.

- **Footnote every claim in the final message** — FEATURE — value 4 — effort M — risk low — category: trust
  Why: the Stop hook already checks "tests pass" claims against the tool log (round 5). The user never sees the support, so a verified claim and a guessed one look the same.
  Done when: a finished turn's closing message gains numbered footnotes such as "[2] pytest -k login, 14 passed, 09:41" for each checkable claim, and a claim with no matching tool call is flagged "unbacked".

- **Mine the repo's own definition of mergeable** — FEATURE — value 4 — effort M — risk low — category: user value
  Why: close warnings are generic, and the pack shows tuning work on warning precision. The last 200 merged commits or PRs show whether this repo adds a changelog line, touches docs, or pairs migrations with tests. Assumption: enough git history exists.
  Done when: `fm norms` prints inferred rules with their hit rates (for example "changelog touched in 91% of src changes"). Closing a task that breaks a rule at over 80% prints one warning naming the rule.

- **Hold out lessons to measure their effect** — FEATURE — value 4 — effort M — risk low — category: learning
  Why: T-0217 gives lessons a confidence, but recall followed by a pass is only a correlation. Randomly withholding a lesson on a small share of eligible tasks gives a causal read, and dead lessons cost injected tokens.
  Done when: with the holdout enabled, `fm lessons --effect` lists each lesson's first-pass rate with and without it, and a lesson with no lift after N paired tasks is proposed for retirement.

- **Review diffs hunk by hunk, with rejections as steers** — FEATURE — value 4 — effort M — risk low — category: ui
  Why: `fm tour` ranks files by risk, but the user's reaction to a hunk goes back as free text typed into chat. A keypress on a hunk should capture file:line plus a short note as a typed steer and feed the taste signal.
  Done when: in `fm tour --review`, pressing `r` on a hunk and typing a note creates a captured task or step amendment citing that hunk, and the note appears in the next brief.

- **Compile the guard fast path to a static binary** — PERFORMANCE — value 3 — effort L — risk high — category: hook latency
  Why: the pack tracks hook latency (bench_hooks, the zipapp idea, shell prefilters), but every hook still starts Python. A tiny compiled binary could decide the provably safe majority of commands and defer the rest to Python.
  Done when: bench shows the median PreToolUse time for read-only commands at least 5x lower, and a parity test replays the guard corpus and finds no decision differences.

- **Wild: plant honeytoken credentials** — SECURITY — value 3 — effort S — risk low — category: tripwire
  Why: assumption: a prompt-injected agent goes hunting for `~/.aws/credentials` or `.env`. Existing ideas match real secrets and plant decoy skills, but no fake credential file that nothing legitimate should read.
  Done when: `fm doctor --honey` creates a decoy credentials file. Any tool call reading or echoing its fake key is blocked and logged as an incident, and a test proves a normal session never touches it.

- **Wild: run an understudy on a local model when quota runs out** — FEATURE — value 3 — effort L — risk med — category: local-first
  Why: privacy-first users and usage-window limits both leave Foreman idle with a queue. Sleeping until the window resets was proposed, but not continuing read-only prep (recon, test linking, brief drafts) on a local engine such as Ollama. Assumption: the user has a local model installed.
  Done when: with the quota blocked and `understudy` enabled, Foreman writes briefs for the next three queue items using only a local endpoint. A network trace shows no outbound calls, and the briefs are marked "draft by local model".

- **Wild: radar for contradictions between teammates' decisions** — FEATURE — value 3 — effort M — risk med — category: teams
  Why: committed `.foreman/project.toml` and an invite flow were proposed, but nothing compares a new plan with decisions and vetoes a teammate already recorded. Assumption: decisions are committed and shared in the repo.
  Done when: planning a task that touches files covered by another author's recorded decision prints the quoted decision and its author before the first edit, and the user can override it with one key.

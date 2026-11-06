# Brainstorm — lens: deepen: guard

- **Fuse the guard into a closed-loop "adversary–defender–judge" engine** — FEATURE — value 5 — effort L — risk med — category: guard
  Why: the list has red-team, fuzz-vs-real-bash, replay delta-debugging and counterexample synthesis as separate ideas; the pack shows a steady stream of hand-found holes (T-0414/0421/0422, `bash -lc` missed, symlink `rm`, `fm focus;` hint). Combined, an adversary agent proposes bypasses, real bash is the oracle for what a command does, the defender lane patches, and the judge accepts only if replay of the 5000-command corpus shows no new false refusals.
  Done when: `fm night` runs one round unattended and produces a branch with ≥1 new differential test plus a replay report showing zero regressions in allowed commands.

- **Compile the guard into an effect IR with a verified interpreter** — FEATURE — value 5 — effort L — risk high — category: guard
  Why: heuristics like `_drives_fm`, `_shell_c` and "python -c judged by what runs before it" are ad-hoc effect analysis. Assumption: a single IR (reads, writes, execs, network, deletes with resolved paths and symlink awareness) lets every category be a query over effects. This merges "abstract-interpret shell", "declarative policy table" and "write-then-execute provenance".
  Done when: for the replay corpus, the IR-based verdict equals the current verdict on ≥99% of commands, and every disagreement is listed with a reason.

- **Give every approval a signed, content-bound capability** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: `fm ask` grants and `standing` yeses are per task or project, while the pack shows approvals being applied to changed commands (the `focus && edit` refusals). Capabilities are bound to a hash of the effect IR, task, expiry and path set, so an approved `rm -rf build` can't be reused as `rm -rf $HOME`. This extends "bind approvals to content hashes".
  Done when: a test edits an approved command by one token and the guard re-asks, while an equivalent reformatting reuses the grant.

- **Make refusals a conversation: refuse with a fix, not a wall** — FEATURE — value 5 — effort M — risk low — category: guard
  Why: many user asks are refusal-wording fixes (focus in the same line, no active task naming the task to resume, symlink rm, lane rm caches). Combine "rewrite into allowed form" and "stop the refusal loop": each refusal carries a machine-checked rewrite (verified by the guard itself to be allowed and effect-equivalent), and after two refusals of the same intent the guard escalates to `fm ask` instead of letting the agent loop.
  Done when: for the last 100 recorded refusals, ≥70% produce a rewrite the guard allows, and a simulated 3rd repeat triggers the escalation message.

- **Close the loop: turn each refusal into a labelled example automatically** — FEATURE — value 4 — effort M — risk low — category: guard
  Why: guard_block events now keep the tripping fragment (T-0423). Add the next step: after the task ends, link each refusal to the outcome (user override, work abandoned, rewrite succeeded, user complaint such as the JARVIS reports). Those labels feed scoring, replay promotion from warn to enforce, and `fm bench`. This combines "score decisions against outcomes" with "promote warn→enforce".
  Done when: `fm friction` reports per-rule precision (refusals later overridden or contradicted by the user) and a rule below a threshold is flagged for review.

- **Run the guard as a cross-harness conformance suite** — FEATURE — value 4 — effort M — risk med — category: guard
  Why: Codex, Gemini and opencode adapters exist, with blocked live verification (T-0335/6/7), and the `bash -lc`/`zsh -ic` miss came from Codex's shell form. Assumption: each harness invokes shells differently (wrappers, argv arrays, login shells). A conformance table of every real invocation shape per harness, run through the guard and real shells, prevents shape-specific bypasses.
  Done when: `fm agents verify` runs ≥30 invocation shapes per adapter through the guard and the output matches real-bash behaviour for each.

- **Keep a taint ledger across the whole session, not per command** — SECURITY — value 4 — effort L — risk med — category: guard
  Why: T-0275 (script files run via bash/sh/source) and the download-feeds-shell rule are the same problem, files written or fetched earlier then executed later. Track provenance of files by origin (network, model-written, user-written, repo) across hooks, and judge execution by the file's origin and current hash, with PostToolUse feeding the ledger.
  Done when: a test writes a script via Edit, modifies it with `sed -i`, then runs it. The guard judges the final content, and a network-origin script is refused unless approved.

- **Tune strictness with the budget of trust: graduated, earned autonomy** — FEATURE — value 4 — effort M — risk med — category: guard
  Why: the user steered "budget/pace limits shouldn't block anything until 75% usage" and wants less friction in full autonomy mode. Guard strictness should vary on evidence: lanes in isolated worktrees with clean replay history get fewer prompts, while sensitive repos or unknown binaries get more. Assumption: strictness is currently mostly static per category.
  Done when: the same destructive-looking command is allowed in a disposable lane worktree and refused in the main checkout, with the reason shown in the verdict.

- **Wild: Let the guard run a shadow universe and diff reality** — FEATURE — value 4 — effort L — risk high — category: guard
  Why: wild. Execute an uncertain command in an overlayfs or copy-on-write snapshot of the repo under bubblewrap with no network, then show the guard the actual filesystem diff and network attempts. The verdict is made on observed effects, and it commits to the real tree only if the diff is within the task's scope. This merges the sandbox and shadow-filesystem ideas into an "uncertain means simulate" tier.
  Done when: a command the static analysis marks "unknown" is run in the shadow, its diff is reported, and an out-of-scope write is refused while an in-scope one is replayed for real.

- **Wild: Publish a guard "fuzz league" where models try to break it** — FEATURE — value 3 — effort M — risk low — category: guard
  Why: wild. Run multiple adversary models against each guard version, scoring bypasses found per dollar. Each release carries a leaderboard; any bypass auto-opens a task (T-04xx) with a minimal repro from delta-debugging. It turns the duel idea into a standing measure of guard strength over time.
  Done when: `fm bench` reports a "bypasses found per 1000 attempts" number per release and fails the release gate if it rises.

- **Wild: Guard that learns the project's normal and flags anomalies** — FEATURE — value 3 — effort L — risk med — category: guard
  Why: wild. From the 5000-command replay and per-project history, build a profile of typical commands, paths and tools per task type. A command far from the profile (a first-ever `curl | sh`, a write outside any prior directory) is routed to a stricter tier regardless of rules. This catches novel evasions no rule anticipates. Assumption: a decent corpus exists per project.
  Done when: on held-out history, anomaly scoring flags the known past bypass commands in the top 5% while flagging under 2% of ordinary commands.

- **Prove guard monotonicity: a rule change can't silently loosen** — CLEAN — value 4 — effort M — risk low — category: guard
  Why: the pack's drop of loosening the `focus && edit` brief gate ("adds guard surface") shows the user is wary of widening it. Every guard change should be accompanied by an auto-generated "loosened/tightened" diff over the replay corpus plus a generated differential set. Any newly allowed command requires explicit sign-off in the task's brief before `fm task done`.
  Done when: finishing a task that touches `fmguard` fails unless the loosening report is attached, and the report lists exactly the commands whose verdict flipped to allowed.

- **Wild: A guard "explain" mode that narrates verdicts as a trace** — FEATURE — value 3 — effort S — risk low — category: guard
  Why: wild. `fm guard why 'cmd'` prints the parse tree, resolved paths, symlink resolution, which category fired, and which lines of the rule produced it. Refusals like the symlink `node_modules` one would be self-diagnosing, and users could paste the trace into a bug report that becomes a regression test automatically.
  Done when: running it on a refused command prints the rule and fragment, and `--as-test` writes a failing/passing test case into the replay corpus.

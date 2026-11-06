# Brainstorm — lens: bold bets

- **Settle hand-vs-Foreman precedence in one table** — FIX — value 4 — effort M — risk med — category: reliability
  Why: an earlier brainstorm left the question "when the user's hand and Foreman's hand both change the same thing (tree, queue, ledger), which side does each reader trust?" Each reader decides ad hoc today. Prior ideas cover detecting user edits and tagging authors, but no single rule says who wins.
  Done when: `fm hands` prints a precedence table (tree, queue, steers, ledger) and a fault test where both hands edit the same record gives the table's answer in every reader.

- **Suspend a real microVM mid-drive** — FEATURE — value 4 — effort M — risk low — category: reliability
  Why: the open question is which unattended paths have never run on a real clock while the machine slept or lost its network. The fake-clock and suspend-test ideas simulate time; they don't freeze the process.
  Done when: a nightly script boots a microVM with `fm drive`, truly pauses it for 6 hours of wall time, resumes it, and asserts that no task was double-closed, no grant outlived its expiry, and the receipt names the gap.

- **Show the user a harmless fail-open on install day** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: the open question is what the user sees in the first minute after a silent fail-open, and whether that moment is ever tested. Ideas so far add a "running degraded" line, but none makes the user meet it once on purpose.
  Done when: `fm demo-degrade` disables one hook in a scratch home and the user sees the degraded banner. A test fails if that banner text drifts from the real one.

- **Rebuild a module from MASTER.md alone** — FEATURE — value 3 — effort M — risk low — category: docs
  Why: assumption: MASTER.md claims to be sufficient but is never tested for it. A tool-less child writes a small module (for example `fmcore`'s `c.more`) from the clauses only, and the module's existing tests grade it. Failed assertions point at doc gaps. This differs from rebuilding the whole product and from the cold-newcomer README test.
  Done when: the exam prints, per clause, which tests the rebuilt module failed, and one doc gap found this way is fixed in MASTER.md.

- **Mine `--help` examples from real invocations** — FEATURE — value 2 — effort S — risk low — category: docs
  Why: 1388 skills and many verbs, with the user asking "what does this do" via "Show why a line exists" and "man pages" ideas. No idea uses the user's own redacted successful calls as the examples.
  Done when: `fm help VERB` ends with up to 3 real redacted examples drawn from the ledger, and a secret-scan test passes on all of them.

- **Open one intake socket for mail, Matrix and share-sheet** — FEATURE — value 3 — effort M — risk med — category: devices
  Why: phone approval and webhook replies exist as ideas, but captures arrive through scattered paths. A single local socket accepting mail, a self-hosted Matrix room and an Android share-sheet, with every item tainted by source, would cover them all.
  Done when: a forwarded email creates a task whose record shows `source: mail, taint: untrusted`, and an instruction embedded in that email does not run a verb.

- **Bootstrap taste from the user's merged PR reviews** — FEATURE — value 3 — effort M — risk med — category: user value
  Why: assumption: the user's review comments across their repos hold their standards. Steers today come only from messages typed to Foreman. The reviews would be mined locally, proposed as steers with checks, and nothing would be stored without a keep or drop tap.
  Done when: on a repo with at least 20 review comments, `fm taste` proposes at least 3 steers, each quoting its source comment.

- **Ship a hermetic Nix flake for Foreman** — FEATURE — value 2 — effort M — risk low — category: developer experience
  Why: the standing rule says Foreman works with no `claude` on PATH. A pinned toolchain flake makes the clean-container proof reproducible on any distro. Arch AUR is the only packaging idea so far.
  Done when: `nix run .#fm -- doctor` passes in a container with only nix installed.

- **Guard the user's own typing (wild)** — FEATURE — value 3 — effort M — risk med — category: security
  Why: wild. The guard blocks agents, but the user also runs destructive typos by hand. `fmsh` would be an opt-in interactive shell wrapper that runs the same guard on human commands, with a one-key override. Ideas so far cover only dry-running pasted clipboard text.
  Done when: typing `rm -rf ~/x/ *` in `fmsh` prints the block with its reason, and the override is recorded as an override and not as proof.

- **Publish DisciplineBench for any harness (wild)** — FEATURE — value 3 — effort L — risk med — category: agents
  Why: wild. The held-out scenarios and the finders arm already exist. Turning them into a harness-agnostic, versioned benchmark with a public leaderboard gives Foreman an outside referee. Earlier ideas stop at a duel scoreboard of Foreman vs plain.
  Done when: running a documented command against Codex or Gemini CLI produces a score file in the published schema, and the site renders it beside Foreman's.

- **Hold a lesson-trial court that sentences rules to expire (wild)** — FEATURE — value 3 — effort M — risk low — category: simplicity
  Why: wild. Steers, lessons and guard rules only accumulate. Each rule would face a monthly "trial" in which a cold child must show a past case where the rule changed an outcome; no case means it gets a 30-day sunset and the user gets a one-tap reprieve.
  Done when: `fm trial` lists rules with their last evidence date and writes sunset dates, and a reprieve restores one rule.

- **Run a zero-token self-explaining doctor (wild)** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild. `fm doctor` flags a problem but the user must still find the fix. Each warning would print a one-line cause and the exact repair command, validated by running `fm doctor` in a scratch home with the fault planted.
  Done when: every doctor warning has a cause line and a repair command, and a test plants each fault and confirms the repair clears it.

Next question: which of Foreman's own surfaces does the user never open, and would removing them help more than any idea here?
Next question: for each idea slated this round, what is the cheapest way to learn whether the user would actually notice it was built?

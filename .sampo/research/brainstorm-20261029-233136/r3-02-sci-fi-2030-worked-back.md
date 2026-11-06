# Brainstorm — lens: sci-fi 2030 worked back

- **Write the tower's win as a replayable certificate** — FEATURE — value 5 — effort M — risk low — category: verification
  Why: selection says a rewrite wins if it closes more scenarios, but the claim is only a line in lineage.md. In 2030 a claim like that ships with a certificate. assumption: `fm task prove` already records commands and outputs that can be reused.
  Done when: `fm genesis verify <gen>` replays the recorded exam commands in a clean worktree, reproduces the closed-scenario list, and flags any mismatch by scenario id.

- **Sign an attestation for each published tower** — SECURITY — value 4 — effort M — risk low — category: provenance
  Why: auto-publish puts scores on the public site (T-2090) with no way for a reader to tell they weren't edited. assumption: `ssh-keygen -Y sign` is available, so no new dependency is needed.
  Done when: `fm genesis attest` writes a signed statement (commit, tower hash, exam scores, harness version), and `fm genesis verify` fails after one byte of exam.jsonl is changed.

- **Plan the tower backward from a date** — FEATURE — value 4 — effort M — risk low — category: user value
  Why: the user's asks are deadline-flavored (site polish, "keep it live") but Genesis only takes a budget. Given "demo Friday", it forecasts generations from past cost per scenario and states what it will leave out. assumption: the cost ledger idea gets built first.
  Done when: `fm genesis run --by <date>` prints a quote of generations, dollars and the not-yet items it will skip, and stops at the date with a one-screen shortfall report.

- **Drive the product with persona bots and mint scenarios from what breaks** — FEATURE — value 4 — effort L — risk med — category: exam
  Why: the pack lists web UI as the surface, but the 11 scenario kinds are code-level. A 2030 harness would use the product as strangers do. assumption: a headless browser or HTTP driver is available locally.
  Done when: on plugin/tests/fixtures/instruments/repo/app.py, a persona run produces at least one scenario with a hidden key that the empty arm fails and the oracle passes.

- **Add an "agent-consumable" cell to every project's grid** — FEATURE — value 4 — effort M — risk low — category: coverage
  Why: by 2030 other agents are a main reader of a repo. The grid covers human surfaces. The repo already has an mcp-server template and a skill index. assumption: the cell applies to libraries and CLIs, and is marked n/a for apps.
  Done when: for a held-out fixture project, Genesis adds llms.txt, AGENTS.md and a `--json` mode, and a tool-less agent given only those files completes a scripted task.

- **Compile the charter into each harness's native format** — FEATURE — value 3 — effort M — risk low — category: portability
  Why: T-0335, T-0336 and T-1207 show Codex, Gemini and opencode support is blocked or unverified. In 2030 the MUSTs and NEVERs must travel with the project. Genesis already holds them as data.
  Done when: one command writes AGENTS.md, a GEMINI.md section and a Claude rules block from the charter, and a lint confirms every MUST and NEVER appears in all of them.

- **Perturb the environment to find hidden gaps** — FIX — value 4 — effort M — risk low — category: reliability
  Why: the open ask about test_ship failing when a hash ends in "add" is a data-dependent flake that no scenario kind would catch. Run the gates under shifted locale, timezone, clock, hash seeds and offline mode. Each flip that changes a result becomes a scenario.
  Done when: a fixture with a planted locale-dependent test is flagged by a perturbed run and becomes a held-out scenario.

- **Reopen grid cells when the ecosystem moves** — FEATURE — value 3 — effort M — risk low — category: maintenance
  Why: the spec is written once ("complete for this kind of project") but the world changes. Local lockfiles plus cached advisories can show a major bump or an advisory. assumption: nothing is fetched unless the user turns it on.
  Done when: bumping a pinned dependency in a fixture adds a dated grid cell marked "upstream moved" and queues one task.

- **Predict a rewrite's blast radius to skip exam runs** — PERFORMANCE — value 3 — effort M — risk med — category: economics
  Why: fmmap.drift already learns co-change from git. A model of "which scenarios this diff can touch" could skip scenarios that cannot change. assumption: past towers hold enough runs to calibrate it.
  Done when: replayed over past towers, the predictor's skip decisions agree with the full exam in at least 95% of cases and save at least 30% of runs, with the disagreements listed.

- **Wild: let a user-model proxy answer Genesis's low-stakes questions** — FEATURE — value 4 — effort L — risk med — category: autonomy
  Why: wild. The steers show the user wants Foreman to "just be smarter" and to batch its asks. A local model distilled from their steers and drops answers forks with a confidence, logs each substitution, and sends anything below threshold to one batched card.
  Done when: on 20 past decisions, proxy answers match the user's actual choice at least 80% of the time, and every substitution is listed for ratification.

- **Wild: let two towers negotiate a cross-repo contract** — FEATURE — value 3 — effort L — risk med — category: federation
  Why: wild. When project A depends on project B and both have towers, each publishes its interface MUSTs and contract-tests the other.
  Done when: with two fixture repos, a breaking change in B's public function fails A's tower exam within one generation and names the clause.

- **Wild: speculate the next generation while the exam runs** — PERFORMANCE — value 3 — effort M — risk med — category: pipelining
  Why: wild. A CPU-style branch predictor for the tower: start the likeliest next mission in a lane (fm lane spike exists) and discard it if selection goes the other way. assumption: lane cost is small next to exam wait time.
  Done when: on a fixture, wall-clock for three generations drops at least 25%, and the discard rate and wasted cost are reported.

- **Wild: give the user a morning gallery of speculative futures** — FEATURE — value 3 — effort L — risk med — category: taste
  Why: wild. The user keeps asking for polish (motion, logos, site look). Overnight, three worktree variants of the web UI are rendered to labelled screenshots. The user's pick is recorded as taste, not as a spec.
  Done when: `fm genesis gallery` writes three screenshot sets from separate worktrees and records the pick, and the next run's Seed cites it.

Next question: Which of the above only pays off after a first generation has run on a real stranger repo, and does Foreman have any such repo with a known answer to test against?
Next question: When two self-written MUSTs conflict, who decides, and where does the tower record the choice?

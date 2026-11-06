# Brainstorm — lens: inversion: what makes Foreman obsolete

- **Run a hooks-off drill on the goal path** — SECURITY — value 4 — effort M — risk low — category: resilience
  Why: assumption: the done-gate, resume card and clause re-injection all ride on Stop, PreCompact and SessionStart hooks. T-0337 already shows Gemini's AfterAgent deny discards the answer, so a host changing or dropping hooks would silently disable the whole goal path.
  Done when: `sampo drill goal --no-hooks` runs a planted-fault goal with every hook disabled and prints, per clause, "still enforced via verb or MCP" or "lost". Each lost clause has a filed task.

- **Run the six false dones against every harness's native goal mode** — FEATURE — value 5 — effort M — risk low — category: benchmark
  Why: the pack shows a plain-Claude arm only. T-0336 says Codex, Gemini and opencode were never live-verified. "Not needed" could be true on one host and false on another.
  Done when: `sampo exam long --hosts` prints a host × scenario matrix with one dated cell per pair. A host that cannot run a scenario shows "could not run", never a pass.

- **Date the first host and model version that passes each false done** — FEATURE — value 4 — effort S — risk low — category: obsolescence
  Why: assumption: "unchanged since gen 2" reads as stuck. Without a record of when plain Claude first passes a scenario, the date a clause stops earning its place can't be known.
  Done when: each false-done scenario has a `first_plain_pass: <host@version, date>` field filled by the nightly run. A clause with that field set and zero Sampo-only catches in 30 days is flagged "candidate to retire".

- **Bind clause evidence to the repo's own CI and test commands** — CLEAN — value 4 — effort M — risk med — category: delegation
  Why: the evidence commands fail inside the builder worktree, but the repo's own `make test` or CI job runs there fine. Delegating removes both the failure and the duplicate machinery.
  Done when: in a repo whose manifest names a test command, a goal closes with every clause pointing at that command and its tree hash. No Sampo-authored evidence file is written in the worktree.

- **Report the share of goals finished with no user message after the first** — FEATURE — value 5 — effort S — risk low — category: user value
  Why: the user's steers are "stop asking me, keep going" and "never interrupt mid-run". The Mission is "carried over days", yet no metric says how often that happens. If Sampo does not raise this share, it has no case against the host.
  Done when: `sampo goal report` prints "closed with 0 further user messages: X of Y", split by sampo and plain arms on the long tier.

- **Tie every README and site claim to a measured delta** — CLEAN — value 3 — effort M — risk low — category: docs
  Why: the README says the agent "proves its work" and "keeps to one task". Models improve, so each claim rots. This is the honest-docs form of obsolescence.
  Done when: each capability claim carries a `delta:` id into the long-tier results. A claim whose delta is zero fails `sampo doctor` until it is reworded or removed.

- **Sample-audit a dormant goal path and re-arm it on a miss** — PERFORMANCE — value 4 — effort M — risk med — category: lean
  Why: assumption: when plain passes, the cheapest safe form is off by default plus a small hidden audit. Full ceremony on every goal is the cost that makes users bypass.
  Done when: with dormancy on, 1 in N goals runs the shadow done-gate. One caught false done re-arms full mode for that repo and logs why. A test plants a false done and sees it re-arm.

- **Export the user's definition of done as a host-neutral profile** — FEATURE — value 4 — effort M — risk low — category: portability
  Why: assumption: the lasting asset is the user's taste, not the runtime. Their "done" shows up in drops and corrections (e.g. "not that wild"). A plain text profile survives a host switch.
  Done when: `sampo goal profile` writes a file of the user's recurring done-clauses with evidence counts. A plain-host session given that file closes the planted scenario's missing clause.

- **Census the environments where goal verbs fail** — FIX — value 4 — effort S — risk low — category: reliability
  Why: the evidence and lease failures inside the builder worktree are one environment, not the only one. Each goal start can record cwd kind, worktree, sandbox, permission mode and hook presence, plus whether the verbs resolved state.
  Done when: a local table lists environment signature → verb success rate. Any signature below 100% for a goal-path verb yields a task with its resolution trace.

- **Wild: Race two hosts on the same goal and let the verdict pick** — FEATURE — wild — value 3 — effort L — risk med — category: portability
  Why: assumption: if Sampo is the discipline layer for any agent, it can referee two. Running Claude Code and Codex in separate worktrees on one goal gives a direct host comparison. The winner is whichever host first meets every clause with evidence.
  Done when: `sampo goal race A B` returns one merged-ready branch plus a per-clause table of who proved what.

- **Wild: Have a successor model write the retirement notice for each gate** — FEATURE — wild — value 3 — effort M — risk low — category: obsolescence
  Why: assumption: a gate's author is the worst judge of whether it is still needed. Each new model ID gets the gate text and its false-done evidence. It writes "I no longer need this because…" or "I still fail this because…", which a cold read then checks.
  Done when: for the current model, every done-gate clause has a signed "needed / not needed" note and a mismatch against the long-tier results is listed.

- **Wild: Give the goal path a public, hard sunset test** — FEATURE — wild — value 4 — effort S — risk med — category: honesty
  Why: assumption: no cost of being wrong keeps a layer alive past its use. Before the end-of-run exam, fix one rule in `decide --check`: if plain matches Sampo's true-done rate on the long tier, the goal path ships in lite mode.
  Done when: the rule is stored, `sampo genesis sweep` runs it, and the final report states which side of it the result landed on.

Next question: which goal-path capability is the user's own experience most likely to find unnecessary, and what would show it besides a benchmark?
Next question: is a goal path that is correct but slower than plain, in wall-clock or review minutes, a failure the long tier would show?

# Brainstorm — lens: grid

Grid used: surfaces are hooks (SessionStart and the per-turn line), CLI, MASTER.md and Read, the state dir, the web UI, the site, and non-Claude harnesses. Actors are the user, the agent, other agents (lanes and subagents), and the unattended drive. Failure modes are missing, wrong, slow, unsafe and unclear.

- **Gate a prune with a hook-latency drill** — PERFORMANCE — value 4 — effort S — risk low — category: hooks×state
  Cell: unattended × hooks × slow.
  Why: the pack's state is 2.4 GB and the hook bench runs only on a quiet machine. Nothing shows a hook stays fast while `sampo prune` or a lane compaction is running. Assumption: prune and hooks share a lock or the page cache.
  Done when: `bench_hooks.py --during-prune` reports hook p95 under the existing bar while a prune of a 2 GB fixture runs, and the ship gate fails on a breach.

- **Log every doc search that finds nothing** — FEATURE — value 4 — effort S — risk low — category: docs
  Cell: agent × MASTER.md × missing.
  Why: MASTER.md is 75,758 tokens and Read refuses it. Sharding it is planned, but nobody knows which questions the shards will fail to answer. Assumption: a `sampo doc` verb exists or will.
  Done when: `sampo doc <q>` with no hit appends a line to a miss log, and `sampo doc --misses` lists the top 10 by count.

- **Make the per-turn line three-state: ok, stale or silent** — FIX — value 4 — effort S — risk low — category: Ward visibility
  Cell: agent × per-turn line × wrong.
  Why: the line is 48–76 characters, so its absence is the only signal a hook died, and the agent can't tell "quiet" from "dead". Assumption: the line carries no freshness stamp today.
  Done when: killing the hook state makes the next turn show a 3-character `?` marker, and a test asserts all three states render under 80 characters.

- **Print what the injected context gained and lost since the previous release** — FEATURE — value 3 — effort S — risk low — category: context diff
  Cell: user × CLI × unclear.
  Why: the lean work will cut text across several releases, and the user has no way to see what the agent no longer hears. Assumption: injected blocks are built from named templates.
  Done when: `sampo ctx diff v1 v2` prints removed and added lines with character deltas per owner.

- **Pause lanes while a prune applies** — SECURITY — value 4 — effort M — risk med — category: state safety
  Cell: other agents × state × unsafe.
  Why: lanes write ledgers concurrently, and prune apply moves files under them. Assumption: lanes have no quiescence signal today.
  Done when: a test runs `prune --apply` while two fake lanes append, then verifies no record is lost and no lane errors.

- **Mark injected steers with their origin and fence them** — SECURITY — value 4 — effort M — risk med — category: injection safety
  Cell: agent × SessionStart × unsafe.
  Why: steers come verbatim from pasted user text, and the pack's pasted-content rule says such text may carry instructions. A hash-signed "user-typed" mark would separate real steers from pasted ones. Assumption: steers are injected without a trust marker.
  Done when: a steer containing "ignore the Ward" is rendered fenced as data, and a test shows an unmarked entry is never injected as a rule.

- **Time the resume start against a full-size state** — PERFORMANCE — value 3 — effort S — risk low — category: resume
  Cell: unattended × resume × slow.
  Why: T-2900 made a resumed session close its dead process's work, which scans background tasks and ledgers. At 2.4 GB that scan could dominate start. Assumption: nobody has timed it at that size.
  Done when: a resume benchmark on a generated 2.4 GB fixture stays under 300 ms, or a cap on the scan is added.

- **Check that lanes believe in real verbs only** — FIX — value 3 — effort M — risk low — category: lane context
  Cell: other agents × injected card × wrong.
  Why: the plugin renames (foreman to sampo) leave stale spellings in injected and sharded text. A lane that reads one runs a command that doesn't exist. Assumption: some old spellings survive in skills.
  Done when: a zero-token check extracts every `sampo …` or `fm …` command from injected text and skills, and runs `--help` on each. Any non-zero exit fails the build.

- **Block ship on a lean ratchet only when two runs agree** — FIX — value 3 — effort S — risk low — category: ship gate
  Cell: unattended × ship gate × wrong.
  Why: timing-based bars flake on a loaded machine and can stall the overnight drive. Character counts are exact, so they should block immediately. Assumption: the ratchet mixes both kinds.
  Done when: a character-budget breach fails at once, and a latency breach needs two consecutive failures on separate runs.

- **Ship a one-file Ward that every lane worktree carries** — SECURITY — value 4 — effort M — risk med — category: Ward portability
  Cell: other agents × Ward × missing.
  Why: lanes on other harnesses, or in worktrees where the plugin isn't installed, run unguarded. The listed "git-hook floor" idea covers git, not other tools. Assumption: lanes can read one vendored file.
  Done when: a lane started with the plugin disabled still blocks a planted `rm -rf ~` through the vendored copy.

- **Print a one-page "Sampo is broken" card** — FEATURE — value 3 — effort S — risk low — category: recovery
  Cell: user × CLI × unclear (wild).
  Why: if a hook crashes at import, no `sampo` verb can explain itself. The card is generated at install from doctor's checks and lives outside the plugin tree, as plain text.
  Done when: `cat ~/.local/share/sampo/RESCUE.txt` lists 6 or fewer commands, and a test that breaks the plugin still finds the file.

- **Run a ghost session without the injection** — FEATURE — value 3 — effort M — risk low — category: lean proof (wild)
  Cell: agent × SessionStart × unclear.
  Why: the lean claim "context small" has no measure of what the removed text did. Replay the last 5 session prompts on a local model with and without each injected block, and score the answers with a cold judge. Assumption: a local model is available.
  Done when: `sampo lean ghost` prints a per-block table of answer differences, and one block is shown to have none.

- **Let a cold child use Sampo from the injected card alone** — FEATURE — value 3 — effort M — risk low — category: usability exam (wild)
  Cell: agent × injected card × missing.
  Why: the new 2,733-character card is only lean if it is still enough to act on. Give a tool-less child the card, ask it to find the next task and block a risky command, and record what it can't do. Assumption: a tool-less child can be scripted.
  Done when: the exam passes 5 of 5 scripted tasks on the current card and fails on a deliberately truncated one.

- **Inject a fake bait command every start and check the Ward answers** — SECURITY — value 4 — effort S — risk low — category: Ward liveness (wild)
  Cell: unattended × Ward × unsafe.
  Why: a Ward that silently fails open is the worst outcome, and the listed canary idea is about the reading, not about unattended runs on resume. Assumption: the check can run in under 5 ms.
  Done when: a resumed unattended session records a canary pass or a loud failure line, and a test disables the Ward and sees the failure.

**Cells left empty:**
- Site × any actor: it is static, with no hooks and no state, so the lean risk is page weight, which the pack's ideas already gate.
- Web UI × slow: the render budget idea already covers it.
- User × Ward × unsafe: the user is the owner, and the listed freeze and fuse ideas cover it.

Next question: which of the three gaps (2,733 characters twice, the 75,758-token MASTER.md, the 2.4 GB state) does a normal user pay for every day, and which only the owner's machine?
Next question: after sharding and deduping, what is the measured behaviour change in a fresh session, and who checks it without Sampo's own gauges?

# Brainstorm — lens: bold bets

- **Fence-check every edit against the history of the lines it touches** — FEATURE — value 4 — effort S — risk low — category: edit safety
  Why: assumption: "why is this line here?" is only answered on request, and agents delete old guards because nothing tells them the guard was a fix. A PreToolUse hook on Edit runs `git blame -L` on the target range and maps the commits to T-ids and the user's steers.
  Done when: editing a line last changed by a FIX commit injects a one-line "this exists because T-xxxx: <reason>" note, and editing an untouched line injects nothing.

- **Keep a belief ledger of the agent's claims about the code** — FEATURE — value 4 — effort M — risk med — category: memory
  Why: assumption: the pack has "audit the final message" and lessons, but no store of claims like "only `fmx.py` calls `load()`". Each claim is saved with the hashes of the files it depends on. When a file hash changes, the claim is marked stale and shown the next time that file is edited.
  Done when: after a claim is recorded and its file is edited, `fm beliefs` lists it as stale, and an unrelated edit leaves it fresh.

- **Build the test map from traced runs, not static guesses** — PERFORMANCE — value 4 — effort M — risk med — category: test impact
  Why: T-0214's edit-time sentinel depends on `fm map` test→src links, which are name-based (`test_agents.py→fmagents.py`). Running each test under `strace -f -e trace=openat` (Linux) gives the real read-set of any language without a coverage tool.
  Done when: `fm map tests --trace` records the read-set for 5 tests, and editing a file outside every read-set selects no tests.

- **Synthesize a codemod, prove it on samples, then apply it with zero tokens** — FEATURE — value 4 — effort M — risk med — category: refactor
  Why: "fan a migration into verified shards" still spends model tokens on every file. Instead the model writes a Python `ast`/regex rewrite once, it must pass three sample before/after pairs, and then it runs mechanically over the tree.
  Done when: a rename migration over 30 files passes its gates with a single codemod-writing call, and a codemod that fails a sample is refused.

- **Attach machine-checked assumption probes to every plan** — FEATURE — value 4 — effort S — risk low — category: plan integrity
  Why: assumption: plans rest on facts ("the API returns paged JSON", "Python ≥3.11") that later go false silently. Each assumption carries a one-line shell probe. SessionStart and `fm night` re-run the probes and reopen the task or flag the decision when one fails.
  Done when: a probe changed to fail makes `fm digest` list the dependent task as "assumption broke: <text>".

- **Broker secrets into commands so lanes never hold them** — SECURITY — value 4 — effort M — risk med — category: privacy
  Why: the pack has output secret scans but nothing that keeps secrets out of the agent's reach. A `.foreman/broker.toml` maps a command pattern to a secret source (pass, keyring or env), and PreToolUse injects it into that command's environment only. Output redaction already exists.
  Done when: `deploy.sh` runs with its token while `env` and `cat .env` in the same lane show none, and the ledger stores only the key name.

- **Gossip public-symbol changes between sibling lanes** — FEATURE — value 4 — effort M — risk med — category: fleet
  Why: lanes are only told to avoid file overlap, so one lane renaming `parse()` breaks another that is still calling it. A PostToolUse hook diffs ctags-level signatures and writes the change to a shared inbox, and sibling lanes receive it on their next prompt.
  Done when: lane A changing a function signature puts a "signature changed" note into lane B's next injected context within one step.

- **Tap the dev server and browser console as live evidence** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: assumption: UI and web tasks are checked only by tests and screenshots. `fm tap <cmd>` tails a dev server's stderr into a ring file, and the Stop gate surfaces new errors that appeared after the last edit.
  Done when: introducing a runtime exception in a served route blocks the close with the first stack line, and a clean run closes normally.

- **Cache what the agent learned about each file, keyed by blob hash** — PERFORMANCE — value 4 — effort M — risk med — category: tokens
  Why: after `/compact` or a resume the agent re-reads the same files. Store a short digest per blob hash, and when a file is unchanged, offer the digest first.
  Done when: a post-compact re-read of an unchanged file gets a digest hint, and a changed file gets none.

- **Cluster sessions into failure archetypes across all projects** — FEATURE — value 3 — effort M — risk low — category: self-learning
  Why: obstacle ranking is per error text. A feature vector per session (stage times, interventions, retries, tool mix) clustered with plain k-means or MinHash gives named archetypes such as "plans too big then stalls", each paired with the intervention that helped most.
  Done when: `fm learn archetypes` prints at least 3 clusters from existing ledgers, each with a count and a suggested rule.

- **Weight rigor by repo hotspots** — FEATURE — value 3 — effort S — risk low — category: risk
  Why: reviewer tiering uses diff risk only. File churn multiplied by past fix-commit density from git history is a cheap hotspot score, and edits in hot files get the stricter tier and an extra test requirement.
  Done when: an S task touching the top-5% hotspot file is escalated one tier and the receipt names the score.

- **Keep a graveyard of rejected approaches and surface it on a lookalike plan** — FEATURE — value 3 — effort S — risk low — category: decisions
  Why: assumption: the refuted-hypotheses ledger covers FIX tasks only. Rejected designs from plan pivots and user vetoes are stored with reasons, and a new plan with a similar title or file set gets "already rejected in T-xxxx because…".
  Done when: replanning a previously vetoed approach prints the veto reason before the first edit.

- **Wild: Play "brief golf" to find which phrases of a request cause rework** — FEATURE — value 3 — effort M — risk low — category: user coaching
  Why: wild. After a close, a cheap child rewrites the minimal brief that would have produced the final diff. The difference from the user's actual ask is logged against the number of replans and steers, giving a weekly "ask patterns that cost you" note.
  Done when: `fm learn asks` lists 3 phrase patterns correlated with extra steers, each with an example.

- **Wild: Retrieve from the user's own notes vault, locally** — FEATURE — value 3 — effort M — risk med — category: local-first
  Why: wild. Index a configured folder (Obsidian or markdown) in SQLite FTS5, read-only and never sent anywhere unless a setting allows it. The recall step then pulls the user's own decisions into plans.
  Done when: with a vault configured, a plan touching "billing" cites the matching note path, and with no setting nothing is indexed.

- **Wild: Show a focus-drift meter against the day's one-sentence objective** — FEATURE — value 3 — effort S — risk low — category: intent
  Why: wild. The user pins a standing objective in the pane. Each tool call is scored by keyword and path overlap with it, and the pane shows a rolling meter and nudges when the last 10 calls scored near zero.
  Done when: ten off-topic edits push the meter below the threshold and a note appears in the pane, and on-topic work keeps it green.

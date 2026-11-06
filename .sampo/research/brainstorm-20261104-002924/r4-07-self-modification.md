# Brainstorm — lens: self-modification

Lens: self-modification, meaning how Sampo changes its own hooks, injected text, docs, state layout and Ward while the Ward stays intact. I skipped the many overlapping ideas already listed. Each item below is a mechanism the list doesn't show.

- **Confirm every live self-apply or revert it** — SECURITY — value 5 — effort M — risk low — category: self-edit safety
  Why: assumption: Mission 5 will land hook and injection edits on the live install, and a bad edit can silently disarm the Ward. The router "commit-confirmed" pattern fits: apply, start a 10-minute timer, and revert unless a real headless session reports the Ward armed.
  Done when: a planted hook import error in a self-apply reverts the install on its own and logs why, and a good edit confirms and cancels the timer.

- **Measure delivered bytes from the host transcript** — PERFORMANCE — value 4 — effort S — risk low — category: injection budget
  Why: SessionStart injects 2,733 characters twice, and only the receiving side shows that. Hook stdout can't, because the duplicate comes from registration. A reader takes the first-turn context records from a headless run's transcript and treats that as the one truth for every injection budget.
  Done when: `sampo doctor` prints delivered characters at start, and a deliberately duplicated hook registration makes the number double.

- **Map each path to exactly one self-edit class** — SECURITY — value 4 — effort S — risk low — category: self-edit gates
  Why: assumption: gates are currently chosen by hand per change. A table maps every file under plugin/ to one class (prose, doc, hook, Ward, state-layout), each with its own gate stack, and the commit trailer is checked against it.
  Done when: a test fails if any tracked path matches zero or two classes, and a Ward-class diff is refused without that class's gates.

- **Bisect lean regressions to the commit automatically** — PERFORMANCE — value 4 — effort M — risk low — category: regression forensics
  Why: bench_hooks.py and the per-turn gauge (48 to 76 characters) already produce numbers, but nothing names the commit that moved them. When a ratchet trips, git bisect runs the bench with the median of 5 runs and files a task naming the commit.
  Done when: on a planted slow import in a scratch history, the filed task names the exact commit.

- **Shrink injected text with the local model, keeping a clause index** — FEATURE — value 4 — effort M — risk med — category: privacy, local-first
  Why: the steers and standing intent are the user's verbatim words, and the user already runs local qwen models. The Ward's required clauses form a fixed list, and the local model rewrites shorter text that must still pass a clause-by-clause check. The user's words never leave the machine.
  Done when: a shrink run makes zero network calls (verified in a network-off scratch run), and its output is accepted only if every listed clause is present.

- **Warn before a retirement hits the user's own habits** — FIX — value 3 — effort S — risk low — category: developer experience
  Why: the lean mission will rename, merge or hide verbs. A pre-merge check greps the user's shell history and the ledgers' verb-use counts for the last 30 days against the verbs being removed.
  Done when: removing a verb the user typed last week blocks the change until the alias or tombstone message is included.

- **Detect Sampo generation skew across synced machines** — FIX — value 3 — effort M — risk low — category: devices
  Why: assumption: state under a synced or shared path can be written by two machines on different Sampo generations. A generation stamp on each ledger writer lets doctor flag a mix, and the older writer goes read-only when it sees a newer schema.
  Done when: simulating two writer versions on one ledger makes the older one refuse to append and print the exact upgrade command.

- **Sign Sampo's own injected text with a per-session tag** — SECURITY — value 3 — effort M — risk med — category: injection defense
  Why: a tool result or fetched page can imitate "Sampo says…" text. Each session gets a short random tag that the SessionStart hook writes in its injection and into a ledger. The Ward treats any "Sampo instruction" lacking the tag as untrusted data.
  Done when: a fixture file containing a forged Sampo directive is flagged by the Ward, while the real injection passes.

- **Wild: let wording perturbation prove the text isn't brittle** — SECURITY — value 3 — effort M — risk low — category: robustness (wild)
  Why: the existing muting trials remove a line. This one reorders and rephrases lines without changing meaning, then runs the Ward exam on a Haiku-class model. If rule-following depends on accidental wording, the failing paraphrase shows which line is fragile.
  Done when: a weekly job prints the count of paraphrases that flipped any Ward verdict, and the Genesis report records it.

- **Wild: self-heal host-protocol drift with a patch that must earn its way in** — FEATURE — value 4 — effort L — risk med — category: self-repair (wild)
  Why: Claude Code releases change hook payloads, and the 2.1.301 mod and hooks are tied to specific versions. A lane reads the new host release notes and its own failing canary, drafts a compatibility patch in a worktree, and offers it only if the hook bench and the Ward exam pass on a recorded corpus.
  Done when: against a simulated payload-field rename, the lane produces a patch that passes the gates without hand edits and does not apply it until the user says yes.

- **Wild: replay a self-edit as a before/after "what the model sees" film** — FEATURE — value 3 — effort M — risk low — category: delight (wild)
  Why: the web UI could show the first turn of a recorded session under the old and new injection side by side, with the Ward clauses lit and deleted words struck through. People trust a cut they can see.
  Done when: each lean task page has a page-weight-limited before/after view where deleting a Ward clause turns its marker red.

- **Keep a "why this sentence exists" provenance for every injected line** — CLEAN — value 3 — effort S — risk low — category: self-edit hygiene
  Why: a line that survives has no recorded reason, so the next lean pass guesses. A sidecar maps each injected line to the steer, failure or exam that justified it, and a line with no entry is a deletion candidate.
  Done when: `sampo doctor` lists injected lines without provenance, and a deleted line's entry moves to the tombstone.

Next question: which self-edits did the lean missions of earlier generations make that were later reverted by hand, and what do they share?
Next question: when a self-edit's gates disagree (bench green, Ward exam red), which gate has historically been right?

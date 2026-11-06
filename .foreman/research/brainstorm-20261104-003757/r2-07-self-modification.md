# Brainstorm — lens: self-modification

- **Add "missing tool" as a planted fault in the long-horizon tier** — FEATURE — value 4 — effort M — risk low — category: exam
  Why: the long tier already plants compaction, killed-session and misleading-test faults, but none removes a binary the task needs. Without this, #5 has no held-out measure of whether it fires.
  Done when: a scenario deletes `jq` from PATH mid-run, and the scorecard shows foreman and plain on the same scenario, including which arm found or built a substitute.

- **Track time-to-first-use per gap and per model** — FEATURE — value 4 — effort S — risk low — category: observability
  Why: the pack covers gap records and retirement, but nothing says how long a gap takes to close, which is the number that shows whether a 9B model is catching up with the frontier.
  Done when: `sampo tool stats` prints the median minutes from gap record to first successful call, split by model profile and by find versus build.

- **Fail a built tool's close until a replayed gap transcript triggers it** — FEATURE — value 5 — effort M — risk med — category: reach
  Why: the standing rule says every capability needs a real session path. A forged tool with no triggering skill description or hook would be a verb nobody calls.
  Done when: closing the tool task replays the original failing transcript, and the close is refused unless a session path invoked the tool.

- **Route all acquired tools through one `sampo tool <name>` dispatcher** — FEATURE — value 4 — effort M — risk low — category: lean
  Why: plugin/skills already holds 1,396 files, and the lean steers forbid growing injected text. One dispatcher with a search verb adds zero per-tool descriptions.
  Done when: acquiring 20 tools leaves SessionStart and per-turn characters unchanged, and `sampo tool find "<need>"` locates each of them.

- **Run forged tools under a landlock or bwrap profile with no network and write access only to a scratch directory** — SECURITY — value 5 — effort M — risk med — category: sandbox
  Why: quarantine is proposed in the pack, but without a named mechanism. The host is a hardened-kernel Linux box, and a forged script is untrusted code written by a small model.
  Done when: a test tool that tries to open a socket or write outside scratch exits non-zero, and the attempt is logged.

- **Keep a per-source yield ledger for tool search** — FEATURE — value 3 — effort S — risk low — category: acquisition
  Why: the user dismissed a "Source rea moved" notice as unrelated to the discipline loop. Sources that never produce an adopted tool should stop interrupting.
  Done when: each source shows finds, adoptions and the date of its last adoption, and a source with 0 adoptions in 60 days is auto-muted.

- **Write an uninstall receipt for every acquisition** — SECURITY — value 4 — effort M — risk low — category: reversibility
  Why: install grants are queued and the user may revoke them. Today nothing lists the exact files, PATH entries and config a tool touched.
  Done when: `sampo tool rm X` restores a before/after file listing taken at install, and a test shows a byte-identical tree.

- **Tag commits made with a forged tool in a trailer** — CLEAN — value 2 — effort S — risk low — category: provenance
  Why: if a tool is later retired or found faulty, there is no way to find the commits it produced.
  Done when: `git log --grep "Built-with: "` lists the affected commits, and retiring a tool prints that list.

- **Wild: Have the user's repo scripts absorb a forged tool, or the reverse** — FEATURE — value 3 — effort M — risk med — category: adoption
  Why: assumption: repos often hold a hand-written script that duplicates what Sampo just forged, or the forged tool duplicates one. Offer a diff proposal to merge them instead of leaving two.
  Done when: for a planted duplicate script, Sampo files one task that names both and proposes deleting one, and it never edits anything without that task.

- **Wild: Write a README and doctests first, then let the model make them pass** — FEATURE — value 3 — effort M — risk low — category: small-model scaffold
  Why: small models drift when asked to build a tool freeform, but do better against concrete examples, as in the pack's spec-example-to-criteria ideas. The README is the spec and also the card.
  Done when: a 9B model builds three planted-gap tools this way, passing a held-out check at a higher rate than freeform.

- **Wild: Let a failed build leave a "scar card" that the next attempt must read** — FEATURE — value 3 — effort S — risk low — category: learning
  Why: the standing rule says a failed spike gets 2 or more different approaches, but nothing carries what the first approach did wrong into the second.
  Done when: the second attempt's prompt contains the first failure's scar card, and approach numbers are recorded and differ.

- **Wild: Hold an overnight "forge audition" on idle local hardware** — PERFORMANCE — value 3 — effort L — risk med — category: local-first
  Why: the 27B model is available at no marginal cost overnight, and models switch at roughly 3 minutes each, so batching by model is cheap. Pre-forge the ten most likely missing tools for the repo's stack and shelve them in quarantine, unlisted until needed.
  Done when: by morning the shelf holds tested tools, none exposed to a session, and a hit rate against later real gaps is reported.

- **Gate acquisition on a stdlib-only path under `python3 -I`** — SECURITY — value 3 — effort S — risk low — category: supply chain
  Why: the environment guidance says planted modules in the script's directory run on import. A forged tool must not load code from its own directory by accident.
  Done when: a planted `json.py` beside a forged tool is ignored, and the tool's check runs with `-I`.

Next question: Which gap, in the user's real history, ended with them hand-installing or hand-writing a tool, and would the forge have been faster than their hand?
Next question: When a forged tool and a host-native feature overlap, who decides which wins, and does the push grant allow deletion of the loser unattended?

# Brainstorm — lens: false done

- **Grade the long tier instead of scoring it 0/6** — FEATURE — value 5 — effort M — risk low — category: measurement
  Why: tier is 0/6 true done and "unchanged since gen 2", so no fix can show movement. Score each replayed run by clause recall, footprint recall against the real following commit, and share of the real commit's tests passing.
  Done when: `fm exam long` prints three fractions per scenario, and a deliberately half-working builder scores strictly between the empty and oracle arms.

- **Refuse done while the last evidence or lease call errored** — FIX — value 5 — effort S — risk low — category: done gate
  Why: evidence and lease commands fail inside the builder worktree, so the gate likely sees "no evidence" and passes it. Assumption: the six false dones overlap with those errors. Join the transcript's verb exit codes to the done claim, and treat an unresolved failed `fm evidence` or `fm lease` call as "could not verify", not as a pass.
  Done when: a scenario where the builder's evidence call exits non-zero and is never retried ends with the goal marked stopped-open, not done.

- **Audit the Stop hook's loop breaker** — FIX — value 5 — effort S — risk med — category: done gate
  Why: assumption: Claude Code's `stop_hook_active` re-entry tends to let a stop through after a denial, which would produce a false done the gate "refused". Treat re-entry as a third state, `stopped-open`, written to the ledger and shown first at the next SessionStart.
  Done when: a test that denies twice and then lets the agent stop leaves a `stopped-open` row and no "done" row.

- **Flag done claims made under suspicious conditions** — FEATURE — value 4 — effort S — risk low — category: done gate
  Why: resume is the worst area, and a summary saying "mostly complete" can turn into a done claim in the first turns after compaction or resume. Mark any done claim within N turns of a compaction or resume, or at high context fill, as suspect and require a fresh-context verification pass.
  Done when: the ledger tags such claims, and a replayed post-compaction false done is held instead of closed.

- **Scan the diff for stubs and test-fitting** — FEATURE — value 4 — effort S — risk low — category: done gate
  Why: the six false dones are unclassified in the pack. Zero-token checks catch added `NotImplemented`/`pass`/TODO returns, empty handlers, and literals copied from a test's expected values.
  Done when: planted stub and test-fitted-literal diffs are each flagged, and a clean diff isn't.

- **Reject additions nothing calls** — FEATURE — value 4 — effort M — risk med — category: done gate
  Why: new code that no entry point, test or caller reaches is the commonest "written but not wired" false done. Check each added symbol for a reference outside its own definition, using the repo's existing parsers, and list the orphans.
  Done when: a diff adding an uncalled function lists it, and wiring it in clears the flag.

- **Require each satisfied clause to cite a changed line** — FEATURE — value 4 — effort M — risk low — category: evidence
  Why: the reverse of attributing hunks to clauses. A clause marked satisfied must name a `file:line`, and a checker confirms that line is inside this goal's diff, so "already worked" claims show up as unproven.
  Done when: a clause citing an unchanged or nonexistent line is rejected, and one citing a real hunk passes.

- **Flag goals that finish suspiciously fast** — FEATURE — value 3 — effort S — risk low — category: done gate
  Why: the ledger already holds duration, tool-call and diff-size figures for closed goals. A done claim well below the p10 of comparable goals gets the cold-verify pass. This is a cheap prior, not a verdict.
  Done when: an artificially short goal run is held for verification, and a typical-length one isn't.

- **Revert one hunk at a time and rerun the proofs** — FEATURE — value 4 — effort L — risk med — category: evidence
  Why: proofs that pass with a hunk reverted show that hunk is unproven. Run this in a scratch worktree on the final diff and list hunks no proof notices.
  Done when: a planted unneeded hunk is listed, and every hunk of a tight fix is covered.

- **Probe for sycophancy at the done moment** — FEATURE — wild — value 4 — effort M — risk low — category: measurement
  Why: assumption: reopen-on-challenge may be a reflex rather than a judgement. Inject "the user says X is still missing" into both a truly done twin and a not-done twin of each long scenario, and score whether the agent separates them.
  Done when: `fm exam` reports reopen rates for the done twin versus the not-done twin, and a gap under a set threshold shows as a gap.

- **Audit a random share of live done claims** — FEATURE — wild — value 5 — effort M — risk low — category: measurement
  Why: the benchmark says 0/6, but there's no estimate of the false-done rate in real use. Audit about 1 in 10 real done claims with the full hermetic cold review, and report the rate with its sample size on `fm outcomes`.
  Done when: the figure appears with its n, and a planted false done in the audit sample is caught.

- **Run a seeded post-mortem on every closed goal** — FEATURE — wild — value 3 — effort M — risk low — category: measurement
  Why: the user's follow-ups often reveal a false done. A tool-less child reads the goal, the final message and the user's next three messages, and says whether the goal was really done and what was missing. Label the result, and feed the labelled cases into the long tier.
  Done when: closed goals carry a `truly_done` label, and at least one label becomes a new scenario file.

- **Show a stopped-open card in place of silence** — FEATURE — value 3 — effort S — risk low — category: user value
  Why: the user can't tell "finished" from "gave up and stopped". The card gives the next session or phone a plain list of unmet clauses and the one command that resumes.
  Done when: a goal stopped by a failed gate shows its unmet clauses and the resume command in the first output of the next session.

Next question: which of the six false dones had a done gate that never ran at all, and which ran and passed it?
Next question: what share of the user's reopened goals followed a post-compaction or post-resume done claim?

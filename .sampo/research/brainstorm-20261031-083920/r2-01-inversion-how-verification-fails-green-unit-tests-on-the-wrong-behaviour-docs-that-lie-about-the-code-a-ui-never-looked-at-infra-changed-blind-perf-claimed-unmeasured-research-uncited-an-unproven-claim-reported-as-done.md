# Brainstorm — lens: inversion: how verification fails: green unit tests on the wrong behaviour, docs that lie about the code, a UI never looked at, infra changed blind, perf claimed unmeasured, research uncited, an unproven claim reported as done

- **Plant a fault before trusting a green** — FEATURE — value 5 — effort M — risk low — category: verification
  Why: the pack's recurring failure is green tests on the wrong behaviour (T-2273 rollup counts typed evidence, but nothing shows the test could fail). Existing `fm task prove` shows fail-without-change once; no mutation of the changed lines.
  Done when: `fm task finish` on a code task runs a mutated copy of the diff (flipped condition or removed line) and records "survived" or "killed". A surviving mutant puts the criterion in the unproven rollup with the mutant's diff quoted.

- **Detect proof that never touched the change** — FIX — value 5 — effort M — risk med — category: verification
  Why: a verify command can pass without executing the changed files (the pack's "test module doesn't exist" check, T-1208, covers only the missing module).
  Done when: a verify command whose coverage or trace misses every changed line is labelled "unrelated to diff" in the evidence record and counted in the unproven rollup. A planted test showing this is red first.

- **Make the claim list come from the diff, not the author** — FEATURE — value 4 — effort M — risk low — category: unproven rollup
  Why: the rollup counts UI changes with no visual check, but a perf, schema or docs change the author never labelled slips through (assumption: kinds are chosen by the author at `fm task new`).
  Done when: `fm task finish` infers the proof kinds the diff demands (migration file → migration, `*.md` code spans → docs, hot-path edit → bench) and lists any kind demanded but absent as unproven.

- **Run every command in the docs on a fresh checkout** — FEATURE — value 4 — effort M — risk low — category: docs proof
  Why: "docs against code" is a Mission 7 item; README and MASTER.md quote many `fm` verbs and flags that can drift.
  Done when: a docs proof extracts fenced `fm ...` examples and flags, runs them with `--help` or in a scratch repo, and fails on any unknown verb or flag. A renamed flag in a fixture doc turns it red.

- **Make the judge a different house from the writer** — SECURITY — value 4 — effort S — risk low — category: independence
  Why: the earlier question "which verbs have a model on both sides with no user-owned check" is open. Cold reads use Haiku, but nothing records that writer and judge were the same model.
  Done when: every model-judged evidence record stores writer and judge model ids; same-model verdicts are labelled "self-judged" and never clear a criterion alone. A test with equal ids is red first.

- **Expire evidence when its inputs change** — FEATURE — value 4 — effort M — risk low — category: proof decay
  Why: a task closed green stays green after a later commit changes the files it proved. The rollup doesn't re-check (assumption).
  Done when: each evidence record stores a hash of the files it covered; `fm doctor` lists done tasks whose covered files changed since, as "stale proof" with a one-command re-run.

- **Require a source and a refetch for each research claim** — FEATURE — value 4 — effort M — risk med — category: research proof
  Why: the request lists research under "Beyond code", and the pack shows no citation check for research tasks.
  Done when: a research task can't close while a claim line has no URL or file:line, and `fm prove --sources` fetches each and checks that the quoted phrase appears. A fabricated quote fails the check.

- **Print "what this does not prove" on every receipt** — FEATURE — value 3 — effort S — risk low — category: honest reporting
  Why: the pack's rule is that anything unprovable gets labelled; today the label is a count, not a sentence.
  Done when: the finish receipt lists, per criterion, the gap in plain words (such as "ran on a copy, not the live service"). Criteria with no gap say so explicitly.

- **Re-measure a perf claim across noise** — PERFORMANCE — value 3 — effort S — risk low — category: perf proof
  Why: T-2284 and T-2303 record medians; one run can be a lucky draw (assumption: the sample count is small).
  Done when: `--bench` runs at least 7 interleaved before/after rounds and records the spread. An overlapping spread is labelled "inconclusive", not "faster".

- **Wild: Hire a saboteur lane** — FEATURE — value 4 — effort L — risk med — category: adversarial
  Why: wild. The shipped proofs are written by the same side that wants green; a separate lane that breaks the finished code measures what the proofs catch.
  Done when: the lane applies five planted faults to a closed task's tree, reruns its proofs, and reports the catch rate. A proof that catches none is flagged.

- **Wild: Replay the ask as a blind re-implementation** — FEATURE — value 4 — effort L — risk med — category: intent
  Why: wild. "Does it do what the user meant" has no machine check. A tool-less child that sees only the user's words and the public behaviour can write the acceptance script.
  Done when: a child that never sees the diff writes a script from the ask; if it fails on the real tree, the task is marked "intent-unproven" with the script attached.

- **Wild: Fire drill the runbooks** — FEATURE — value 3 — effort L — risk high — category: ops proof
  Why: wild. Incident and ops docs go untested until the real outage.
  Done when: in a throwaway worktree a drill breaks a service on purpose, follows the doc's recovery steps verbatim, and reports pass or the first step that failed.

- **Wild: Show a proof-age heatmap on the site** — FEATURE — value 2 — effort M — risk low — category: transparency
  Why: wild. The site already follows Genesis data, and proof freshness per area is a number nobody else checked.
  Done when: the Genesis page shows a per-area grid of proven, stale and unproven shares, generated from the evidence files by the daily publish.

Next question: When a proof is "unproven", who sees it before the user stops reading — does any surface interrupt, or does it sit in a count?
Next question: Which evidence records could a builder have edited by hand, and does anything outside the builder's reach seal them?

# Brainstorm — lens: inversion: how verification fails: green unit tests on the wrong behaviour, docs that lie about the code, a UI never looked at, infra changed blind, perf claimed unmeasured, research uncited, an unproven claim reported as done

- **Calibrate perf proofs with an A/A run** — FEATURE — value 4 — effort M — risk low — category: performance
  Why: T-2284 and T-2303 record medians from `--bench` on the start tree vs the current tree, but nothing says how big a difference is real on this machine.
  Done when: `fm task evidence ID --bench` also times the unchanged tree against itself, interleaved ABAB with the first run dropped. A claimed gain smaller than that spread is recorded as "within noise, unproven" and a test covers it.

- **Run verify commands without network and label the ones that need it** — SECURITY — value 4 — effort M — risk med — category: hermetic proof
  Why: assumption: a proof that quietly depends on the network, a live service or a pulled package is green for the wrong reason, and it can leak data. Foreman has the guard and sandbox ideas, but none that marks a proof as non-hermetic.
  Done when: a verify command run under `unshare -n` that fails only for lack of network records "needs network: unproven offline", and the rollup counts it.

- **Re-run each proof in a perturbed environment** — FEATURE — value 4 — effort M — risk low — category: environment twin
  Why: assumption: green proofs often depend on the author's locale, `TZ`, `HOME`, cwd or `PATH` order. The skewed-clock idea covers time only.
  Done when: `fm prove --twin` re-runs a task's verify command with `LANG=C`, `TZ=Pacific/Kiritimati`, an empty `HOME` and a different cwd. A fixture that passes only in the original environment is reported as environment-dependent.

- **Show which hosts each capability is proven on** — FEATURE — value 4 — effort M — risk low — category: host matrix
  Why: T-0335, T-0336 and T-0337 are blocked on live checks for Codex, Gemini CLI and opencode, while the standing rule says Foreman isn't Claude-specific. Today the Claude-only proof reads as proof for all hosts.
  Done when: `fm doctor` prints a capability × host grid with proven, unproven or n/a in each cell, and the unproven rollup counts a host-specific claim whose host was never run.

- **Scan genesis publish output for leaks before it reaches main** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: the latest commits make `genesis publish` push `site/genesis` data to main daily. Emails, home paths and tokens in quoted evidence would be published and cached.
  Done when: the publish step refuses and names the file and line when the staged site data contains the user's email, an absolute `/home/…` path or a token-shaped string, with a red-first test for each.

- **Prove that compact output never hides a failure** — FIX — value 5 — effort M — risk med — category: output integrity
  Why: T-0828 (compact output rollout) is deferred. If a compaction drops a `FAIL`, a traceback or the exit code, a red run reads as green, which is the exact failure this lens looks for.
  Done when: a property test feeds recorded failing outputs through every compactor. The exit code and every line matching error, fail or traceback survive, and a compactor that breaks this is excluded.

- **Re-prove each task on the merged tree** — FEATURE — value 5 — effort M — risk med — category: post-merge proof
  Why: the router already tracks "red after merge" per lane, so lane-green is known not to mean main-green. Under parallel lanes (Missions 5-8) a proof passes alone and breaks after another merge.
  Done when: after `fm ship` merges, each merged task's verify commands re-run on the result. A failure reopens that task with the interfering merge named, and a two-lane fixture shows it.

- **Make a blind reproducer confirm every FIX ticket first** — FEATURE — value 4 — effort M — risk med — category: agents
  Why: a red-first test proves the builder's reading of the bug, not the user's. The ask list shows many tickets are misread, for example the T-2285 plan-gate miss.
  Done when: a separate tool-less child sees only the ticket text and the repo. Its reproduction command is stored beside the builder's, and a mismatch between the two is shown at close.

- **Flag installed-vs-source skew in proofs** — FIX — value 3 — effort S — risk low — category: developer experience
  Why: T-0418 (installed foreman-ui is behind 0.6.1) shows installed copies drift. A proof that ran the installed copy proves nothing about the changed source.
  Done when: `fm doctor` and `fm prove` name any gate that resolved to an installed copy whose hash differs from the repo's, and mark that proof unproven.

- **Print a rerun line and the first difference on every red proof** — FEATURE — value 3 — effort S — risk low — category: developer experience
  Why: assumption: a red proof that says only "failed" leads people to loosen the check instead of fixing the cause.
  Done when: each failing `fm prove` and `fm task finish` prints one copy-paste rerun command and the first differing expected/actual line, covered by a test.

- **Lock a criterion's verify command once accepted** — SECURITY — value 4 — effort S — risk low — category: gate integrity
  Why: assumption: weakening the check after a red run, for example editing `pytest -k x` to `true`, is the cheapest way to fake done. The writer/judge-gap question in the pack points the same way.
  Done when: any edit to an accepted verify command is recorded with before and after and needs a reason. Close shows "check changed after first red", and a test covers it.

- **Wild: Retrodict each new proof across history** — FEATURE — value 4 — effort L — risk med — category: proof discrimination
  Why: wild. A proof that cannot tell a known-bad commit from a good one is theatre. Foreman's own git history holds both kinds.
  Done when: for a FIX task, `fm prove --retrodict` runs the new test on the parent of the fix and on a recent bad commit, and reports "discriminates" or "cannot tell".

- **Wild: Spot-check closed tasks by random lottery for the user** — FEATURE — value 4 — effort M — risk low — category: user-owned check
  Why: wild. It answers the pack's question on writer and judge with no user-owned check. One close in N asks the user a 10-second yes/no on a one-line behaviour demo, and the answers calibrate every proof kind.
  Done when: `fm` raises the card for 1 in N closes (N set by the user). Answers are stored in a ledger the builder cannot write, and `fm doctor` shows the user-confirmed rate beside the proven rate.

- **Wild: Set an unproven-debt ceiling** — FEATURE — value 4 — effort S — risk low — category: unproven rollup
  Why: wild. T-2273 counts the unproven tasks but nothing limits how many pile up.
  Done when: the user sets a ceiling with `fm mandate`. Above it, `fm task focus` for new FEATURE work refuses and names the oldest unproven task to upgrade first, and the user can override it.

Next question: Which of Foreman's proofs would still pass if the code under test were replaced by a stub that prints the expected output?
Next question: When a lane is green alone but red after merge, which proof was blind to the interaction, and is that class counted anywhere?

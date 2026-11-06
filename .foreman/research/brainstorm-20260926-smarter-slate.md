# "Make Foreman make everything smarter" slate (T-0041), from research/brainstorm-20260926-195613 (6 lenses, ~44 ideas)

## Grounded out
- Secret redaction before evidence/ledger/sync (security): premise false: fmcore.redact runs on typed and --run evidence (add_evidence, run_command) and on fm sync export.
- Hook-latency benchmark in doctor (performance): exists as the bench_hooks gate in fm check.

## Slate (value/effort/risk; lenses that proposed it)
1. FIX T-0042 fm task new --ac can pair --verify (S, v3, low; reliability)
2. FIX T-0040 git fetch isn't a tree write (S, v3, low; reliability)
3. Recall: `fm recall <text>` (stdlib token overlap/TF-IDF over past briefs with outcomes, decisions with scope, research, audit findings, lessons); printed as "Related" at fm task new/focus and recorded in the brief; recalled text capped, labelled as data and stripped of control characters; decisions gain --scope; similar past tasks' tiers give a tier hint (M, v5, low; every lens)
4. Project map: `fm map` (test/gate commands, layout, entry points, churn hot files, test↔source links by name/import) refreshed when HEAD moves, pointed to at focus; `fm impact <path>` lists likely tests and dependents (M, v5, med; user value, performance, simplicity, bold)
5. Red→green proof: FIX tasks can't be done without a failing then passing [ran] run of the same command, or a recorded reason there is no regression test (S, v5, med; reliability, security, simplicity, bold)
6. Failure memory: fingerprints of failed runs (evidence --run, fm check, Bash failures) with the resolution recorded at done; a recurring fingerprint surfaces "seen in T-x, fixed by …" (M, v4, low; user value, reliability, bold)
7. Smarter fm check: a failing gate is rerun once (flaky), compared with its last result before the task started (pre-existing vs new), and timed (S/M, v4, low; user value, reliability, performance, bold)
8. Lessons at done for M/L (`fm task done --lesson`), indexed by recall (S, v4, low; user value, simplicity, bold)
9. Sensitive-path audits: a diff touching auth/crypto/secrets/exec/deserialization paths needs the adversary lens at any tier (S, v4, low; security)

## To the inbox (followup)
tier calibration model beyond the recall hint · hint-compliance rates → gates · eval cases from blocked tasks · model routing in fm run by tier · opt-in cross-project lessons with a privacy filter · scope-drift check at done · retire unused playbooks · reversibility columns on decisions · flag instruction-like text in grounded evidence · proving a regression test against the reverted tree in a temp worktree (stronger than 5)

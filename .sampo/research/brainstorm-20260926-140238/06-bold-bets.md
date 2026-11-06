# Brainstorm — lens: bold bets

- **Ship a two-slot plugin lib with promote-on-green** — FIX — value 5 — effort M — risk med
  Why: T-0037 was the second self-lockout in one day, and the committed fallback covers only fmguard. Hooks and `fm` would always run from a promoted "live" copy of all of `plugin/lib`. Edits go to the working copy, and `fm promote` copies it to live only after tests and a hook smoke test pass.
  Done when: a deliberately injected `raise` in fmcore's working copy leaves hooks and `fm` working from the live copy, and `fm doctor` names the divergence.

- **Build `fm audit run` with findings triage** — FEATURE — value 5 — effort L — risk med
  Why: T-0034. Three reviewers found real bugs every round, and the agent saves reviewer output tails by hand. It would launch read-only headless lens reviewers that write a structured findings file. Findings would be deduped and turned into tasks, and the done gate would read them.
  Done when: `fm audit run` on a diff produces per-lens findings JSON, and `fm task done` refuses while any high finding is unresolved or waived.

- **Add guard differential replay over a real command corpus** — SECURITY — value 4 — effort M — risk low
  Why: each round's guard regressions were caught only by the full suite, and the heuristics blocked the agent's own legitimate edits. `fm guard replay` would run a redacted corpus of logged allow/block decisions through the working guard and the committed guard, and print every verdict that changed.
  Done when: changing one guard rule shows exactly the affected corpus entries, and the corpus contains no secrets.

- **Fuzz the guard with obfuscation mutators** — SECURITY — value 4 — effort M — risk low
  Why: MASTER §10 says "obfuscation beats it" without measuring. Mutators (quoting, `$IFS`, variables, base64, split paths) would be applied to every blocked-category seed. The result is a bypass-rate report, and the reproducible bypasses become tests or documented limits.
  Done when: `fm guard fuzz` prints a bypass count per category, and at least one found bypass is fixed with a regression test.

- **Add a guard-aware `fm edit` primitive** — FEATURE — value 4 — effort M — risk med
  Why: the agent wrote multi-line Python heredocs to edit files, and text heuristics blocked quoted paths and "claude plugin" strings. A structured patch or replace command would let the guard check target paths instead of parsing shell text. It would also be the only state and file write path that logs itself.
  Done when: editing a file containing a "claude plugin" string through `fm edit` is allowed, and the same edit aimed at a protected path is refused.

- **Learn recurring audit finding classes into pre-checks** — FEATURE — value 3 — effort M — risk low
  Why: reviewers repeatedly found the same kind of bug after the agent was satisfied (unsanitized titles, path handling, fail-open). `fm reflect` would tag findings with a class, and a class seen twice would become a lens-brief line and a suggested test stub.
  Done when: after two findings share a class, `fm audit prep` includes that class in the matching lens brief.

- **Pin plugin approvals to source and content hash** — SECURITY — value 3 — effort M — risk low
  Why: T-0036. An approval given for one plugin version could cover different content later. The approval record would store the source and a tree hash, and any change would require a new yes.
  Done when: changing a byte in an approved plugin's tree makes `fm plugins install` ask again.

- **Generate the rules copies from one source** — CLEAN — value 3 — effort S — risk low
  Why: every behaviour change touches MASTER.md, CHANGELOG, rules, and the eval copies of the rules, and the rules file is near its 60-line budget. Assumption: the eval copies can be generated verbatim from the rules file.
  Done when: `fm docs check` fails if the eval rules copy differs from the generated output, and a rules edit needs one file change.

# Brainstorm — lens: deepen: guard

- **Build a guard refusal workbench (`fm guard mine`)** — FEATURE — value 5 — effort M — risk low — category: guard
  Why: round 4 review says friction analysis needed a hand-written transcript miner, and two premises (data-only cat writes, literal variables) were false only after mining; the digest counts refusals without showing commands.
  Done when: a test with a transcript fixture holding 3 refusals makes `fm guard mine` print each full command, the guard's verdict, and the replay verdict through `fm guard try`, grouped by rule.

- **Gate guard tasks on a standing replay premise check** — FEATURE — value 5 — effort S — risk low — category: guard
  Why: dropped items (literal-variable resolution, data-only relaxation reverted at 0 of 31) were wasted builds; assumption: mined corpus is stored by T-1162 labelled cases.
  Done when: `fm task start` on a task tagged guard prints "would change N of M mined refusals" from the corpus, and a test with a zero-effect proposal shows 0 of M.

- **Auto-label mined refusals as right or wrong from what followed** — FEATURE — value 4 — effort M — risk med — category: guard
  Why: `fm guard wrong` needs a manual call per case; the transcript shows whether the user or agent then retried a rewritten command or overrode it. Assumption: a rewrite-then-success within 3 calls signals a false-positive-ish refusal.
  Done when: a test transcript where a refused command is followed by an equivalent allowed one yields a proposed labelled case marked "inferred", awaiting confirm.

- **Make the "it could be …" guess print only existing, whole paths** — FIX — value 3 — effort S — risk low — category: guard
  Why: guess shows `/repo/cd/w.out`, a word glued to the root (listed five times in the category). Merge into one fix: candidate must be a token in the command and exist, or be omitted.
  Done when: a test with `cd w && cat w.out` produces no `/repo/cd/w.out` and a test with a real file still gets its hint.

- **Replace regex scanning with a shell tokenizer shared by every guard rule** — CLEAN — value 4 — effort L — risk high — category: guard
  Why: premise failures on variables and pipes come from regexes seeing text rather than words; T-0275 (guard reads scripts it runs) needs real parsing. Prove safe by running the full labelled corpus before and after.
  Done when: the corpus and guard tests give identical verdicts on all labelled cases, with a diff report listing any changes, and quoted/heredoc/subshell cases parse correctly.

- **Show the refusal message with a one-line safe rewrite** — FEATURE — value 4 — effort M — risk med — category: guard
  Why: weak agents retry or guess after refusals; 31 mined refusals suggest repeated shapes. Assumption: most have a mechanical alternative (split command, run the test first, use the edit tool).
  Done when: for the top 5 refusal rules, the message includes a rewrite that `fm guard try` allows, checked by a test per rule.

- **Run guard drift as a night job with a verdict diff** — FEATURE — value 3 — effort S — risk low — category: guard
  Why: `fm night` already replays labelled cases (T-1162); extend by replaying the freshly mined week and reporting verdicts that changed since the last release.
  Done when: a test changing one rule makes `fm night` capture a FIX naming the command and old/new verdict.

- **Track guard cost per rule in the friction digest** — PERFORMANCE — value 3 — effort S — risk low — category: guard
  Why: hooks run on every call and the hot path cost was a recurring review defect; the 80 ms claim was wrong, so measure per rule.
  Done when: `bench_hooks.py` prints per-rule milliseconds and fails over a set budget in a test.

- **Ship migration and infra guard packs, opt-in** — FEATURE — value 3 — effort M — risk med — category: guard
  Why: already in the category list; assumption: terraform apply, `DROP TABLE`, kubectl delete on prod are the common bypass-mode regrets.
  Done when: enabling a pack makes `fm guard try "terraform destroy"` block, and with it off the command is allowed.

- **Wild: Dry-run sandbox preview for blocked commands** — FEATURE — value 3 — effort L — risk high — category: guard — wild
  Why: assumption: many refusals are of commands whose effect is knowable. Run in a throwaway overlay copy and show the file diff before the user decides.
  Done when: a refused `rm -r build` shows "would delete 214 files" from an overlay run without touching the real tree.

- **Wild: Guard fuzzer that mutates allowed commands to find bypasses** — SECURITY — value 4 — effort M — risk low — category: guard — wild
  Why: guard defects are found by mining after the fact; mutating (quotes, `$IFS`, base64, variable splits) known-blocked commands finds holes first.
  Done when: a run over the blocked corpus reports any mutant that the guard allows, and a seeded hole in a test is found.

- **Wild: Guard "court" that replays the day's refusals to the user as a one-minute verdict page** — FEATURE — value 3 — effort M — risk low — category: guard — wild
  Why: the user is AFK and labelling is manual; a page in the web UI with each refusal and allow/block buttons turns return-after-gap into cheap labelling feeding `fm guard wrong`.
  Done when: the page lists the day's refusals and a click stores a labelled case that `fm replay` loads.

- **Make lane builders see their own `fm` flags when testing guard changes** — FIX — value 3 — effort S — risk low — category: guard
  Why: bare `fm` resolves to the main checkout, so guard changes in a lane are tested against old code.
  Done when: inside a lane worktree, `fm guard try` uses that worktree's code, shown by a test with a lane-only rule.

**Verdict** — changes needed. Nothing here is a HIGH. The in-process mutant is coarser than the rule it claims to drop. The mutation test can also pass vacuously. I could only read files, so nothing below was run.

## lens: adversary
- MEDIUM — plugin/tests/test_guard_hardening.py:171-175 — The mutant returns `None` for the whole verdict whenever the top category equals `cat`. Dropping one rule would instead fall through to the next finding. `check` (fmguard.py:121-131) takes the first match in `CATEGORIES` order. The new case `rm -rf ~/.claude/plugins/cache/x` probably also yields `rm-outside` (fmguard.py:4471-4476), so with `plugin` genuinely dropped the case would still block. The test would still report "plugin" as caught. Fix: `real(tool, ti, ctx, found=[f for f in fmguard.findings(tool, ti, ctx) if f[0] != cat])`, since `check` already takes `found`. — PLAUSIBLE
- MEDIUM — gen_evasions.py:182-185 — A stacked variant only has to stay "block". A generic refusal of the opaque shape (`| sh`, `sh <<<`, "eval of computed text", fmguard.py:3185) passes as "stays block" even if the guard no longer reads the payload. Fix: store the plain command's category in each case and require the variant to match it. — PLAUSIBLE

## lens: edge
- MEDIUM — test_guard_hardening.py:173-175 — The test never checks that the corpus is green before the mutant. Any existing `should=block` drift, including a guard error, which `drift` returns as "unable", makes every mutant look red. Fix: assert `fmreplay.drift(self.cases) == []` in `setUpClass`, or count only drifts that are new compared with the baseline. — CONFIRMED by reading
- LOW — test_guard_hardening.py:195-202 — The `if "+" in r[0]` / "same seed" assertion calls `_rows()` twice in one process, so it can't catch a difference between machines or Python versions. The committed-file subset check next to it does that job. The `>= 2*len(dangerous)` floor lets one command have no stacks. Fix: assert at least 3 stacks for every dangerous command.
- LOW — The Mutation class runs `drift` over the whole corpus once per category (about 10 times). No timing was recorded.

## lens: maintainer
- MEDIUM — test_guard_hardening.py:201-212 — The "stack still runs the original" check skips every stack that contains `here_string`, `script_file` or `base64_sh`. That is most of the 57 stacks. The claim that sh-fed wrappers take POSIX inners only is therefore never observed. The check is green for `echo '… | sh' >> ~/.bashrc` only because all three of its stacks happen to be base64_sh. `echo` is a builtin, so `ran(orig)` is empty and `assertTrue(want and …)` would fail on any other seed or command list. Fix: for sh-fed stacks, run `ran()` on the inner text instead, and skip commands whose `ran()` is empty instead of failing them.
- MEDIUM — guard_untested.json:1 and MASTER.md — "May only shrink" is not enforced. The test checks equality, so adding a category to the JSON in the same commit as dropping its last case passes. Fix: store a count and require `len(untested) <= committed_max`, or compare against `git show HEAD:` — CONFIRMED
- LOW — test_guard_hardening.py:4 — `import shlex` is unused.

## lens: intent
- LOW — test_guard_hardening.py:171 — The acceptance criterion says "(fm mutate)", but the test does not use `fmmutate`'s AST rule mutants. It wraps `check` instead. The criterion's verify command passes, but the stated mechanism is not exercised.

**Acceptance criteria** — partly met. `Mutation` exists and checks both the mutant and the seeded stacks, but see the findings above.

**Answers to your questions**
- Stack selection: sha256 ordering, no random, no dict or set order. The wrappers are sound by inspection. `eval_literal`, `here_string` and `script_file` return `None` on `'`, so `quote_split` and `dollar_quote` only reach `func_def` or `base64_sh`. Quoting transforms skip assignment-led commands.
- Machine independence: the stack text is independent; only the labels depend on the guard.
- The three new cases don't depend on the machine. Bare `fm` is accepted anywhere (fmguard.py:1555), and `~` follows HOME.
- Hidden gaps: `guard_gaps.jsonl` is unchanged and has only allow-side gaps. Staleness is caught by `test_guard_evasions`. The only way a stack hides a gap is the generic-refusal case in the first adversary finding.

**Implicit decisions** — a category is treated as a rule; the in-process `check` wrapper stands in for `fm mutate`; seed 1605 and 3 stacks per command; the whole class is skipped when HOME is in a git tree.

**Not checked** — I ran no tests, so I haven't confirmed the plugin case's `rm-outside` overlap, the timings or the generated JSONL. CHANGELOG.md and MASTER.md only for the wording about the ratchet.

**Noticed:** none

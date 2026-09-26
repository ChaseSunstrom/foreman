# Foreman eval suite (PROTECTED CORE)

`claude plugin eval` cases that referee Foreman changes (BUILD_PROMPT §4.9). They encode the §12 scenarios that fit a
single fresh session: 1 (intake block), 2 (mid-task capture, self-contained), 13 (guard in bypass mode), plus the
"plain one-liner gets classified" behavior. Scenarios that need seeded Foreman state across turns (4, 5, 6, 7, 12…)
are covered by `plugin/tests/e2e/` and the unit tests.

Run (live plugin; compare with a candidate worktree by running the same command on its plugin/ and diffing
`cases[].aggregates.score` in the two JSON files):

```
claude plugin eval ~/.claude/foreman/plugin --trust-plugin --scaffold --runs 1 --ablation none \
  --max-cost-usd 5 --no-publish --json /tmp/foreman-eval.json --allow-tools Bash Write Edit
```

Note: eval runs use a temporary HOME, so `~/.claude/rules/foreman.md` (installed by `fm install-user`) is not loaded;
the cases exercise the plugin's hooks and skills as shipped.

Verdict: approve with nits (3 MEDIUM, 5 LOW); fixed or accepted with reason. Reviewer: one foreman:fm-reviewer, six lenses, read-only.

## lens: adversary
- MEDIUM — child regexes run in-process with no timeout; only `\)[*+{]` guarded, so `.*.*.*.*x` slips through. FIXED: `_regex` also refuses more than two open-ended repeats. Test: a "greedy" docs reply is dropped with the reason.
- LOW — non-ASCII names pass `\w`. FIXED: re.ASCII on the name match. `_fill` on child text: accepted (a stray @token@ only becomes a real name).

## lens: edge
- MEDIUM — flaky/docs regexes were validated against BASE tests, not BASE+REGRESSION, so a never like `len\(` passed then failed on clean. FIXED: validated against the clean suite's own tests.
- MEDIUM — the C prototype came from `src.split("{")[0]`, wrong for a brace before the signature. FIXED: the signature up to its parameter list, refused when none (test: a typedef struct on the same line is refused).
- LOW — Rust non-pub fn. FIXED: `pub` added. Test added.
- LOW — a 'fixed' flaky test that still leans on chance passed once; the flaky test replaced the function's original assertions. FIXED: the clean suite runs twice for flaky, and the flaky test is added beside the original.

## lens: operator
- LOW — one child call per scenario, no retry. Accepted (bounded).

## lens: maintainer
- LOW — no tests for the regex guard and bad-regex branches, Rust. FIXED: badre and greedy drop cases, Rust render case.

Noticed: `_static` matches any file whose name holds "test" (broad); fm exam check never runs a flaky repo test repeatedly (the planted side is exempt by design).

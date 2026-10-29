<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Regex backtracking

Use when a regular expression is slow or hangs on long or hostile input (catastrophic or quadratic backtracking, ReDoS), or a pattern runs on untrusted text.

1. **Time it on an adversarial input:** 50,000 characters built to almost match (spaces then no end, `a` repeated then `!`). Seconds where a short input takes microseconds is the bug.
2. **Test first:** assert the adversarial input finishes under a small time bound and the normal inputs still match the same groups.
3. **Find the overlap:** two parts that can match the same characters, such as `.*?` followed by `\s*$`, nested quantifiers like `(a+)+`, or alternatives that share a prefix.
4. **Make the parts disjoint:** end a capture on a non-space (`(\S(?:.*\S)?)\s*$`), use a negated class (`[^"]*`) instead of `.*?`, or an atomic group or possessive quantifier where the engine has them.
5. **Or drop the regex:** `split`, `strip`, `partition` or a small loop are linear and often clearer.
6. **Bound the input** before matching untrusted text, and keep the timing test beside the pattern.

Mined from T-1616.

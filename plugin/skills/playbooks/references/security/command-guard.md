<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Command guard rules

Use when a command guard, policy hook or shell allowlist blocks harmless work (a false block) or lets a dangerous command through (a miss), or a guard rule is added or changed.

1. **Reproduce through the real guard**, not a reading of the rule: feed the exact command to its dry-run or try verb and record the category, the rule that fired and the words it said.
2. **Classify:** a miss (dangerous and allowed) outranks a false block. Count how often the false block fired in the logs: one a week is a hint fix, ten a day is a rule fix.
3. **Corpus case first:** add the command as a labelled case (should allow / should block) and watch it fail. For a miss, add its dangerous variants beside it: `env`/`command`/`builtin` prefixes, an absolute path to the binary, `python -m`, a pipe into a shell, a variable or `IFS` trick, a quoted or escaped name.
4. **Fix the reading, not the string:** parse the command (words, operators, redirects, substitutions) and judge what runs. A wider regex fixes one spelling and misses the next; refuse what the parser can't read rather than guess it is safe.
5. **Say the rewrite that passes:** every block names the form that would be allowed (name the path literally, use the scratch dir, use the tool's own verb), so the next attempt isn't a third collision.
6. **Replay the history:** run every logged command through the new guard. A new block on something allowed before is a regression unless it was a miss; a miss that still passes means the fix is incomplete.
7. **Keep the grant path user-only:** the agent may ask for a category, never grant it. A rule change never widens what an agent can approve for itself.

Mined from T-0715, T-0740, T-1146, T-1289, T-1553.

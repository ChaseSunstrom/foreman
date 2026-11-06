**Verdict: changes needed.** One race and one privacy gap are verified. One self-triggering effect is likely but I did not confirm it by running anything.

**Findings**

1. **MEDIUM (race, double spend, duplicate captures)** — `plugin/lib/fmsecond.py:150-155,163-175` and `plugin/lib/fmhooks.py:224`. The hook only reads `second_session`. The child writes it at line 155, after an unlocked read at line 150 and a glob. Two sessions starting together both pass `second_due` and both spawn a child. Both children read an unset `second_session` and both call the model, so the spend doubles. The title dedupe at line 163 runs before the lock at line 170 and is not repeated inside it. Both children can therefore capture the same missed request. Fix: claim the day atomically. Take `c.lock`, re-read meta, return if `second_session == today`, set it, and release. Or have the hook set it under its existing lock at line 217 before spawning. Also recompute `titles` inside the lock before each `_create`.

2. **MEDIUM (privacy)** — `plugin/lib/fmsecond.py:132,159-161`. Transcript messages and open-task titles go to the child through `c.plain` and `c.fit` only, with no `c.redact`. `redact` is applied only to the child's replies, in `_bullets` at line 72. A secret the user typed into a session, such as a token or a pasted `.env`, is sent to the model verbatim. Fix: wrap with `c.redact(c.plain(t))` at line 132 and for the titles at line 161. The sensitive-project skip is sound. The hook refreshes `sensitive` at `fmhooks.py:217` before `second_due`, and the child re-reads meta at line 148.

3. **MEDIUM (false captures)** — `plugin/lib/fmhooks.py:224`. The spawn ignores `busy`, which is true when another session was active under 15 minutes ago. `session()` then reviews the newest transcript by mtime (line 152), which is likely that live session. Its last request is probably still being answered, so it gets captured as "missed". Fix: skip the spawn when `busy`, or require the chosen transcript's mtime to be older than about 30 minutes.

4. **LOW-MEDIUM (unconfirmed)** — `plugin/lib/fmideas.py:32` and `plugin/lib/fmsecond.py:49-51`. The child `claude -p` has no flag that disables hooks, and it runs in a fresh temp directory. If user-scope Foreman hooks fire in `-p` mode, then each child's SessionStart calls `find_project(create=True)`. That creates a junk state project per run. It also passes `second_due` and spawns another `fm second session --if-due`. The nested run stops with "no earlier session", so I see no unbounded recursion. I did not run it. Fix: set `FOREMAN_NO_BACKGROUND=1` in the child's `env`. If the hook doesn't treat that as "do not create a project", add a guard for it.

5. **LOW (design note)** — `plugin/lib/fmsecond.py:155`. The day is marked as tried before the child runs. A budget refusal (line 46-48), a missing `claude` or junk output therefore costs the whole day with no retry. The failure is not logged anywhere durable. This is probably intended, so I'd record the failure in the ledger.

5. **LOW (injection)** — `plugin/lib/fmsecond.py:171`. Defanging only prepends a marker when `_INSTRUCTION` matches. A pasted web page in a user message can steer the child into emitting a "missed request". That becomes an inbox item with `source=self` carrying up to 300 characters of attacker text. It is flattened to one line because `plain` strips newlines, and the child has no tools, so the damage is bounded. I did not check whether self items run without the user's review. If they do, that is the real risk.

**Checked and fine**
- Budget check: `fmbudget.check` runs before the single child in `_child`.
- A missing `claude` raises `OSError`, which becomes `ValueError`. Junk output is handled by `result`, then by the empty-text and exit-code check.
- Nothing blocks SessionStart. `Popen` is detached, uses a `DEVNULL` stdin and `start_new_session`, and is wrapped in try/except. `plugin/bin/fm` exists.
- `debate`: the `--review` name regex cannot traverse paths, since slashes are excluded.

**Acceptance criteria**
- Sensitive-project skip: met (line 148 and `second_due`).
- Once a day: met for sequential starts, not met under concurrent starts (finding 1).
- Privacy and redaction of what is saved: saved text is redacted, but outbound text is not (finding 2).
- The test suites were not run.

**Not checked**
- Test coverage.
- `fm audit prep` lens skills.
- Docs.
- The `fmcli.mutate` and `_create` internals.

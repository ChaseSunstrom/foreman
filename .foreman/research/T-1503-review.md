**Verdict:** approve with nits. I found no destructive command and no outright false SQL, Unicode, time zone or money claim, but a few steps give wrong or incomplete advice. I read the seven files in `~/.claude/foreman/.claude/worktrees/agent-a2be3c96ddc34eed7/plugin/skills/playbooks/`. I couldn't run the snippets because I had no shell, so I checked the snippet claims by reading them.

## lens: technical accuracy and actionability

- MEDIUM — references/clean/deprecation.md:20-22 — Step 4 says "warn where the caller will see it, once per process" and names `DeprecationWarning`. Python ignores `DeprecationWarning` by default unless the code the warning is attributed to (the caller's module) is `__main__`, or the code runs under pytest or `-W`. A library user calling `old_total()` from their own module sees nothing. The default action is once per location (module and line), not once per process. The same sentence puts HTTP headers under "once per process", but a header goes on every response. Fix: use `FutureWarning` when end users must see it, or say plainly that `DeprecationWarning` is only visible under `-W`, pytest and `__main__`. Split the HTTP header out of the "once" rule. — confidence high
- MEDIUM — references/clean/deprecation.md:22 — "a `Deprecation` or `Sunset` response header" gives no value formats. `Sunset` (RFC 8594) is an HTTP-date. `Deprecation` (RFC 9745) is a structured-field date such as `Deprecation: @1688169599`. A header cannot name the replacement. That needs `Link: <…>; rel="deprecation"` or `rel="successor-version"`, but step 4 requires naming it. Fix: add one concrete header example with those three fields. — confidence high
- MEDIUM — references/release/dependency-admission.md:23-25 — Step 5 says to run the audit "on a branch with it added" and, in the same step, to check for install scripts "you haven't read". Adding the package means `npm install` or a `pip` sdist build, which runs the candidate's and its dependencies' lifecycle scripts before anyone has read them. Fix: read `npm view <pkg> scripts` first, or use `npm install --package-lock-only --ignore-scripts` or `pip download --no-deps --only-binary :all:`, and audit from that lockfile. — confidence high
- MEDIUM — references/fix/migration.md:26-28 — Step 1 lists unique constraints, foreign keys and `NOT NULL` as tightening changes, but step 6 gives only `ADD CONSTRAINT … NOT VALID` plus `VALIDATE`. That does not work for two of the three. Unique constraints cannot be `NOT VALID`: they need `CREATE UNIQUE INDEX CONCURRENTLY`, then `ADD CONSTRAINT … USING INDEX`. On Postgres 17 and earlier `NOT NULL` needs `CHECK (col IS NOT NULL) NOT VALID`, then `VALIDATE`, then `SET NOT NULL`. Fix: give those two recipes. Also add that a failed `CONCURRENTLY` build leaves an `INVALID` index that must be dropped before retrying (step 2). — confidence high
- MEDIUM — references/clean/characterisation-tests.md:16-17, 22-23 — Step 2 tells you to pick "production samples, logged requests", and step 4 tells you to commit the recorded pins. Real PII, tokens or emails would land in git. Fix: add "scrub or synthesise secrets and personal data before pinning; grep the pin files before committing". — confidence medium
- LOW — references/fix/migration.md:28 — The lock budget is step 7, after the DDL steps 2 and 6, so it reads as an afterthought. It also names only Postgres, and a plain `SET` leaks past a migration on a pooled connection. Fix: move it before step 2, use `SET LOCAL lock_timeout` inside the migration transaction, add MySQL's `lock_wait_timeout`, and say to retry on timeout. — confidence medium
- LOW — references/clean/characterisation-tests.md:41-43 — The snippet evaluates `repr(fn(*args))` before the key `repr(args)`, so a function that mutates its argument gets a post-mutation key and the mutation is never pinned. `open(path, "w")` also fails with `FileNotFoundError` if `tests/pins/` is missing. Fix: compute the key first, and add `os.makedirs(os.path.dirname(path), exist_ok=True)`. — confidence high
- LOW — references/fix/text-time-bytes.md:23-24 — The pass check "no naive … `Date()` without a zone" is wrong for JavaScript, where `Date()` is an instant, and it misses `datetime.utcnow()`, which is also naive. The step 2 grep for `open(` without `encoding=` will flag `"rb"` opens and miss `Path.read_text()` and `text=True`. Fix: reword both checks. — confidence medium
- LOW — references/fix/sql.md:21-22 — "Stale statistics: run `ANALYZE`" sits beside `EXPLAIN ANALYZE` and is easy to confuse with it. On MySQL, `ANALYZE TABLE` takes a brief lock on the table. Fix: write "`ANALYZE <table>` (Postgres) / `ANALYZE TABLE` (MySQL)". — confidence low
- LOW — references/fix/text-time-bytes.md:1 — The file is named `text-time-bytes`, but its heading and SKILL.md entry say "money". Fix: add "money" to the filename or to the SKILL.md entry. — confidence medium

## Acceptance criteria

- **The seven playbooks exist with a "Use when" line and a numbered procedure: met.** All seven files exist at the stated paths. Each has "Use when" and a numbered list, and SKILL.md lists them. The check only tests for the substring `1.`, so it is weak. See the Noticed line.
- **Checked and correct:** every `fm lib show` card name resolves to a real card. `fm decide` accepts `--rejected` and `--revisit` (fmcli.py:4879,4885). The cross-links `dependency-upgrade.md` and `../reflect/architecture-decision-records.md` exist. The decomposed "é" is present in the snippet. London's clocks go forward on 2026-03-29, so the 23-hour assertion holds. The Decimal half-even and float assertions are correct. The SQLite plan comments are plausible.

## Implicit decisions

- Postgres is the default engine for lock advice, with SQLite for runnable snippets.
- British spelling "characterisation" against the library card's "characterization-tests".
- Python stdlib for every snippet.
- Thresholds: about 1 year for dependency health, about 50 lines for "write it yourself", 10× for estimate-versus-actual row mismatch.
- The "Foreman's own playbook" header comment on every file.

## Not checked

I did not run the snippets. I did not check the three unrelated trailing hunks you told me to ignore (`CHANGELOG.md`, `fmguard.py`, `test_guard.py`). I did not check SKILL.md description-length conventions or any test that scans the playbook index. I did not check the contents of the library cards themselves.

**Noticed:**
- The task's acceptance check only looks for the substring `1.`, so any file containing "0.1" would pass. A stricter check would be a regex for `^1\. \*\*`, plus a check that SKILL.md links each file.
- `fm lib show` card names are never validated against the card directory by a test. A short test could catch a typo in these "Built on library cards" lines.

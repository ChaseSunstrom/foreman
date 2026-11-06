## Verdict: changes needed

## Findings

**HIGH — `~/.claude/foreman/plugin/lib/fmguard.py:188-198` (`_protected_roots`) and `:146-147` (`_CRED_DIRS`/`_CRED_FILES`) — tree-write credential-file bypass**

`_protected_roots()` builds the roots that `classify_tree()` (line 201) checks a tree write against, but it only loops over `_CRED_DIRS` (`.ssh`, `.aws`, `.config/gcloud`, `.kube`, `.gnupg`, `.config/gh`). It never adds `_CRED_FILES` (`.netrc`, `.npmrc`, `.pypirc`, `.git-credentials`, `.claude/.credentials.json`, `.docker/config.json`) as roots. `.docker` is not itself a `_CRED_DIR`, so a directory-scoped tree write whose destination is exactly `~/.docker/` is invisible to both `classify_tree` (no protected root lies under it) and `classify_write` (the destination path `~/.docker` matches neither a `_CRED_DIRS` entry nor an exact `_CRED_FILES` path).

Exact input that breaks it (verified by tracing `_tree_targets` → `_write_targets` → `classify_tree`/`classify_write`, no protected root ends up under `~/.docker`):
```
cp -r payload/. ~/.docker/
```
or
```
tar -xf evil.tar -C ~/.docker
```
Both return `[]` from `check_bash`, so the write is never blocked. `~/.docker/config.json` can carry registry auth tokens and `credsStore`/`credHelpers` entries that get executed as `docker-credential-<name>` on the next `docker` invocation — a credential-theft and code-execution vector, exactly the "protected core / credentials tree write" case round 4/5 claims to have closed.

Fix: add `_CRED_FILES` as roots too, e.g. `roots += [(os.path.join(ctx.home, f), "credentials") for f in _CRED_FILES]` in `_protected_roots`.
Confidence: high (verified by code trace, no execution needed).

**MEDIUM — `~/.claude/foreman/plugin/lib/fmcli.py:128-145` (`task_done_in`) — never-started requests can be marked "done" with zero evidence on either side**

`task_done_in` correctly blocks folding a task that was actually started (`b.status not in ("captured","planned") or b.evidence()` at line 136). But it never checks anything about the host `h` — not that `h` is done, has evidence, or even references the folded work. Two never-started tasks can be used to launder each other into fabricated "done" status, with no evidence and no audit ever recorded for the closed request:
```
fm task new "Umbrella" --type FEATURE --tier S --step "x" --ac "y"   # T-0001, never executed
fm capture "do the actual work"                                       # T-0002
fm task drop T-0002 --done-in T-0001
```
T-0002 now shows `status=done`, permanently, while T-0001 (the claimed host) has done nothing. This matches the threat-model concern "close started work without evidence or audits" in spirit — it closes *any* work without evidence or audits, provided the closed task itself never began.
Fix: require `h.status == "done"` (or at least reject when `h` has no evidence either), so `--done-in` only ever points at work that genuinely happened.
Confidence: high (verified by code trace and by the module's own test at `plugin/tests/test_cli.py:510-527`, which never exercises an undone host).

**MEDIUM — `~/.claude/foreman/plugin/lib/fmdoctor.py:290-308` (`check_hook_errors`) — unsanitized log text reaches `fm doctor`'s terminal output**

This round's own changelog and tests (`test_the_latest_error_is_named`, and the round-4/5 title fixes via `c.plain`/`c.plain_lines` in `fmcore.py:577,600` and `fmsync.py:83`) establish the policy that text an untrusted party can influence must be stripped of control/escape sequences before it reaches the terminal. `check_hook_errors` extracts `event` and `cause` straight from `state/logs/hooks.log` (line 305-306) and interpolates them unsanitized into the printed `WARN` detail (line 307-308). That log is populated by `traceback.format_exc()` (`fmhooks.py:49,159,191,322,402,417,426,443,454,877`), whose exception messages can embed attacker-influenced values (a Bash command string, a file path, a title) formatted into an error message elsewhere in the code. Unlike the title path, no `plain()`/`c.fit(c.plain(...))` call guards this output, so a crafted string that trips an exception and is echoed in its message can carry ANSI/OSC sequences straight into `fm doctor`'s terminal output.
Fix: wrap `event` and `cause` with `c.plain(...)` before formatting into the `Result` detail.
Confidence: medium (the missing-sanitization fact is verified directly in code; a full exploit chain producing a specific attacker string inside a specific traceback message was not executed/confirmed).

## Not checked
- Runtime behavior of git's actual option parsing for attached short-option values (e.g. whether `git -ccore.hooksPath=...` without a space is accepted by real git) — could not execute git to confirm; the regex in `_check_system`/`check_bash` (fmguard.py:481, 794) only matches tokens that start with `core.hookspath=`/`--config-env=core.hookspath=`, so an attached-form bypass is plausible but unverified.
- `fm sync` import of `decisions.md` and `research/*.md` (`fmsync.py:197-208`) is not run through `plain_lines`, unlike briefs — flagged only as a low-confidence observation since this content is read by the agent/via file reads, not printed directly to the real terminal by fm itself, so it's a lesser instance of the same class of issue.
- The plugin's Python test suite was not executed; findings are based on static code tracing only.
- Full round-4 changes already merged into `main`/previous commits (`d8479e2` and earlier) were treated as baseline, not re-audited except where this diff touches the same functions.

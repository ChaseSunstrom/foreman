**Verdict: changes needed.** One MEDIUM plus several LOW/MEDIUM findings. Markdown renders no HTML, and the Rust allow-list holds. I only read the code. I ran no tests and built nothing, so the findings below are from reading, not from running.

**Findings**

1. MEDIUM — `fmclaude.py:140,302`. Liveness is the transcript mtime or the statusline snapshot, both under 90 s. A terminal session that has been idle for more than 90 s counts as not live. `send` then resumes the same id without `--fork-session`, so two writers share one transcript. Input: leave a terminal open for 2 minutes with no snapshot refresh, then run `fm claude send <id> hi`. Fix: always pass `--fork-session`; the cost is one extra session.

2. MEDIUM — `fmclaude.py:361`. Non-follow `show` does `f.read()` on the whole file, then `buf += chunk` and `split`, which copy it again. A transcript of hundreds of MB, such as one full of base64 images, takes about 3 times its size in memory. The app also starts `show --follow` with no `--from`, and `SessionDetail.svelte:56,38` pushes every event into `$state`. Fix: read in 1 MB chunks, and have the app pass `--from` (tail only).

3. MEDIUM, intent — the app calls `claude list` without `--limit` (`app.svelte.ts:103`), so the default 150 applies and older sessions vanish silently. `Files.svelte:27` slices to 500 of up to 2000 files with no "more" control. `fmclaude.py:273` returns at the 2000 cap with no truncated flag. The user asked for "all" and "no caps". Headless sessions are also hidden unless `--all` is passed.

4. LOW — `fmclaude.py:53`. `_entries` uses `str.splitlines()`, which also splits on U+2028, U+0085, `\x0b`, `\x0c` and `\x1c`–`\x1e`. Claude writes these raw inside JSON strings. A first prompt containing U+2028 breaks the line in two and both halves fail `json.loads`. The summary then loses `cwd`, `prompt` and `entrypoint`, so `send` fails with "folder isn't on this device". Fix: `text.split("\n")`.

5. LOW — non-string content crashes the stream. `_text_of` (line 66) joins `b.get("text","")`, and line 194 calls `.strip()` on it. `{"type":"text","text":123}` or `null` raises TypeError/AttributeError, which `cmd_claude` doesn't catch (only ValueError), so `show` dies with a traceback. `image()` (line 229) fails the same way on `src.get` when `source` is a string, because AttributeError isn't in its except list.

6. LOW — `SessionDetail.svelte:104`. `copyResume` builds `cd ${JSON.stringify(s.cwd)} && …`. Inside double quotes the shell expands `$(…)` and backticks. A cwd like `/tmp/$(touch pwn)` runs when the user pastes it. Fix: single-quote the path with `'\''` escaping.

7. LOW — terminal escapes. Text-mode `list`, `files` and `agents` (lines 325, 334, 341) print titles, descriptions and file names unfiltered, and `c.fit` doesn't strip control characters. A model-created scratchpad file named `\x1b]0;…` reaches the terminal. Fix: strip C0/C1 characters in text mode. The `--json` path is fine.

8. LOW — `read_file` (`fmclaude.py:279-281`). `realpath(root)` resolves a symlinked scratchpad root, so confinement then holds against the symlink's target. A local user who pre-creates `/tmp/claude-1000/<dir>/<sid>/scratchpad` as a symlink to `~/.ssh` gets that directory read. There is also a check-then-open race: the session's own model could swap in a symlink after the check. Fix: require the root's owner to be `getuid()` and not a symlink, and open with `O_NOFOLLOW`. The `..`, absolute-path and symlink-file cases are handled. A symlinked `x.png` is listed as kind "image" (line 272) but then fails to read.

9. LOW — `fmclaude.py:255`. The scratchpad path uses `tempfile.gettempdir()`, which honours the fm process's `TMPDIR`. Over ssh, `TMPDIR` can differ from the session's, giving an empty file list. I did not verify where Claude puts it.

10. LOW — `fmclaude.py:28,98`. `_memo` is keyed by `(path, mtime, size)` and never evicted, so a busy session adds an entry on every write during `list --follow`. Fix: key by path and store the stat tuple alongside.

**Acceptance criteria.** None of the five was run.
- The `fm claude` criterion and the `Serve` criterion are code-present but not verifiable without running the tests.
- The build and Rust-test criterion is not verifiable. The allow-list code at `lib.rs:110-122` includes `claude` and restricts `serve` to status/start/stop.
- The screenshot criterion is not verifiable.

**Verified safe**
- `Markdown.svelte` builds elements only, and there is no `@html` or link rendering anywhere under `src`.
- Image data URLs are only used in `<img>`, so SVG scripts don't run.
- Session and agent ids are strictly validated.
- `send` guards option injection in the prompt and the resume id (`fmsession.py:71-72`).

**Not checked**
- `Transcript`, `Gallery` and `Palette` internals.
- The `ProjectView` state refetch.
- `_follow` churn behaviour.
- The ssh quoting path.
- Whether `--` parses correctly under argparse for `send`.

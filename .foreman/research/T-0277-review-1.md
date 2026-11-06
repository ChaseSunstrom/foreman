**Verdict: changes needed.** I found no HIGH issues. Several MEDIUM issues let the support and conflict labels mislead, and `--quorum` and `--file` have failure-handling gaps.

All line numbers are in `~/.claude/foreman/plugin/lib/fmresearch.py`. I only read the code; I ran nothing.

**Findings**

1. **MEDIUM, 159-185 (`cross_check`)**: `also: <domain>` ignores verification, and `verify` runs before it.
   - `agree` is built from every similar claim, including ones marked ✗ (quote not found) or ? (no source or quote).
   - A claim therefore reads `also: blog.x.io` when that second source's quote is not on its page. The line carries both `✓ quote found` and `also:`, which reads as corroboration.
   - Fix: count only `y.status == "verified"` as support. Otherwise label it `also: X (unverified)`.

2. **MEDIUM, 155-156, 175 (independence)**: `_domain` returns the full hostname.
   - `docs.alpha.dev` and `blog.alpha.dev`, or `alpha.dev` and `www2.alpha.dev`, count as two independent domains. The task asked for "different domains".
   - Fix: compare the registrable domain (last two labels at minimum) or document the limit.

3. **MEDIUM, 181 (`y.sub != x.sub`)**: under `--quorum`, the two models answer the same sub-question, so `sub` is equal for them.
   - If sonnet says "supports streaming" and opus says "does not support streaming", it is not flagged as a conflict.
   - The two claims also drop out of each other's `agree` list, so each is labelled `single source · only <model>`. The one signal quorum exists to give is lost.
   - The test (`test_quorum_marks_what_both_models_support`) only covers agreement.
   - Fix: allow cross-model pairs (`y.sub != x.sub or y.model != x.model`).

4. **MEDIUM, 179-184 (duplicate conflicts)**: under quorum each real contradiction is reported up to four times.
   - Both models repeat the same claims, so the sonnet/sonnet, opus/opus and cross-model pairs each become a separate `(x, y)` entry.
   - The note's Conflicts section, `res["conflicts"]` and the pane's ⟷N all inflate. The same duplication inflates the `single` count (331) and `claims`.
   - Fix: dedupe by `(x.text, y.text)` pairs before counting and printing.

5. **MEDIUM, 317, 350, 369 (`--quorum` second model fails)**: `answers = runs[args.model]`, so only the primary model's errors become `(failed: …)` lines in the note.
   - If the second model times out or returns nothing, its `parse_claims("")` is empty and the note has no failure line. The error appears only in the JSON `failed` list, and the exit code is 0.
   - `len(models) > 1`, so every claim is labelled `· only sonnet`. That reads as "opus did not find this" rather than "opus never ran".
   - Fix: add a note line naming the failed model and skip the `only <model>` marker when that model returned no answer. Warn on stderr.

6. **MEDIUM, 275 (`--file` mid-batch failure)**: `_ask` raises `UsageError` on a budget cap, a planner failure or "no claims came back".
   - Notes already written are kept on disk. The list comprehension aborts, so no summary or JSON is printed and the user never learns which notes exist.
   - The exit code is nonzero, which is correct, but the partial results are invisible. Questions after the failure are not run.
   - The batch path also drops the "N claims quote words not on the page" stderr warning that the single-question path prints.
   - Fix: catch `UsageError` per question, collect it, print the successful notes plus the failures, and exit 1 if any failed.

7. **MEDIUM, 356 (note name collisions)**: the note name is the first 40 slug characters plus a minute-resolution timestamp.
   - Two batch lines sharing a 40-character prefix, or a repeated line, finish in the same minute (cache hits and fast stubs make this likely). The second note silently overwrites the first.
   - `notes` then lists the same path twice. This breaks the "two questions yield two notes" promise.
   - Fix: add a numeric suffix when `path` already exists.

8. **MEDIUM, 138-145 (cache stores soft-error pages)**: `fetch` returns `(page, None)` for any 200 response. Cloudflare challenges, "Access denied" pages and truncated reads (deadline or `MAX_PAGE` cut-off) are cached for the whole day.
   - Every later ask that day marks its claims ✗ "not found". Before this change a retry could succeed.
   - Fix: skip caching suspiciously short or truncated pages, or mark the cached entry so ✗ results from it say "(cached page)".

9. **LOW, 268 (`--file` input)**: the list comprehension reads every line before `[:20]` is applied.
   - A huge or binary file (a multi-GB file with no newlines) builds one giant "question" in memory and sends it to the planner.
   - Anything past 20 lines is dropped silently, and a positional question given alongside `--file` is ignored without a message.
   - Fix: use `itertools.islice`, cap line length, error if there are more than 20 lines, and reject `question` together with `--file`.

10. **LOW, 170-185 (negation false positives)**: `_NEG` matches "no" and "deprecated" anywhere in the claim, for example "not only … but also" or "no longer".
    - `similar` needs only two shared stems and 50% of the shorter claim. Claims of three or four words that share generic stems such as "library" or "version" count as similar.
    - Wrong `also:` labels and false conflicts are possible. Cost is not a concern: the pairwise loop is about n² set intersections, fine at hundreds of claims.
    - Fix: raise the similarity floor, for example Jaccard at least 0.5 and at least 3 shared stems.

11. **LOW, 152-155, 297-300 (labels read as verification)**: the note header disclaims ✓ (the quoted words are on the page, not proof the claim is true). The `also:` and `single source` suffixes and the "## Conflicts … disagree" heading carry no such disclaimer. They are lexical guesses stated as fact.
    - Fix: add one header sentence saying support and conflicts are word-overlap heuristics, and word the heading "possible conflicts".

**Checked and fine**
- Concurrent cache writers use per-pid temp files and `os.replace`, and `verify` dedupes URLs within a process, so there is no temp-file clash.
- Pruning only removes directories whose names are dates, and write errors are caught.
- The shared state dir is not a project-isolation leak, because the cache holds public pages only.
- Cache size is bounded in practice by claims per day (at most 3 MB per page, no cap).

**Acceptance criteria**
- **T-0239:** met (cache and two notes), apart from findings 6 and 7.
- **T-0229:** partly met. The conflict section, the single-source marker and `--quorum` all exist, but findings 1, 3 and 5 undermine their reliability.

**Not checked:** UI code, the TypeScript tests, and budget estimation. I did not run the test suite.

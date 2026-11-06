**Verdict:** changes needed. Two MEDIUM findings: a duplicate-brief path and an `fm inbox ticket #7` call that bash silently breaks. The rest is LOW.

## lens: intent
- MEDIUM — plugin/lib/fmeco.py:291 vs :684 — `fm inbox gh` dedupes on `CONTEXT: <url>, `, but a brief made by `fm inbox ticket` holds `CONTEXT: ticket github OWNER/REPO#N sha`. The ticket-then-gh direction is not deduped, so `fm inbox ticket gh:acme/app#7` followed by `fm inbox gh --repo acme/app` makes a second brief for #7. — in `inbox_gh`, also skip when a brief's Raw request has `CONTEXT: ticket github <owner/repo>#<n> ` (the repo comes from the URL) — high
- MEDIUM — plugin/lib/fmeco.py:775, plugin/commands/backlog.md:31, CHANGELOG — the docs and error text say `fm inbox ticket #7`. Interactive bash treats an unquoted `#7` as a comment, so `args.file` is empty and the user gets "which file…". Zsh interactive does not (comments off by default), so only bash is hit. — document `'#7'` in quotes and have the empty-file error say "quote it: '#7'" — high
- LOW — plugin/lib/fmeco.py:703 — only captured and planned briefs refresh. A deferred or blocked brief that was never started gets a second brief when the issue changes, though the request said "unstarted". — include `deferred` and `blocked` when the brief has no evidence or current step, or state the limit in the docs — medium
- LOW — plugin/lib/fmeco.py:701-702 — a brief made by `fm inbox gh` is returned as-is even if the issue changed, and the message says "already in the inbox". The request says a changed issue refreshes. — say so in the docs, or refresh it too — medium

## lens: edge
- LOW — plugin/lib/fmeco.py:699-715 — the scan runs outside the lock and `refresh()` doesn't recheck status. A session that starts the brief in that window has its Steps and Acceptance criteria wiped. Rare. — in `refresh`, return unchanged if `x.status` is no longer captured or planned — plausible
- LOW — plugin/lib/fmeco.py:703 — the loop takes the first captured or planned brief that lacks `key`. If another brief already holds the current text, as T-1859's one-brief-per-edit behaviour can leave, an older sibling is rewritten into a duplicate instead of returning the one that matches. — before the loop, return any brief whose Raw request has `key`, as `capture_once` does — high
- LOW — plugin/lib/fmeco.py:545 — a URL with a `#issuecomment-…` fragment, or a `/pull/N` URL, fails the `fullmatch`. The user gets "can't read <url>" rather than a hint. — accept an optional `#…` fragment, or name the supported forms in the error — high

## lens: adversary: ok
- gh args can't start with `-`: the repo regex needs `\w` first, `--repo=` is one argv item, and `n` is digits only. Issue text is quoted with `| ` and redacted, so it can't forge `CONTEXT:` lines at the dedupe regexes. stderr is redacted.

## lens: operator: ok
- One gh call per fetch, 60 s timeout, no loop or hook added. MASTER.md and CHANGELOG match the code.

## lens: maintainer
- LOW — plugin/lib/fmeco.py:710 — `type` is updated on refresh but `tier` (from `guess_tier`) is not. — recompute the tier when `whole`.
- LOW — plugin/lib/fmeco.py:715, :777-785 — `new` is now `True | False | "refreshed"`, so the `--json` field changes type. — keep the bool and add `refreshed: true`.
- LOW — plugin/tests/test_inbox_more.py:273-278, :279-295 — the "gh-captured" test hand-writes the `inbox_gh` format instead of calling `inbox_gh`. The "closed gets a new brief" half of the criterion is untested (only `active` is). The deferred case, the "Ticket refreshed" message and the JSON shape are untested. — drive `inbox_gh` with a mocked gh, and add a `done` case.

## Acceptance criteria
- gh refs fetch through `gh issue view`: met (fmeco.py:629, test at :260).
- A changed issue refreshes a captured or planned brief in place: met (tests :279-288).
- A started brief gets a new one: met for `active`. Closed: met by the code at :703, not tested.
- I did not run `python3 plugin/tests/run.py test_inbox_more`.

## Implicit decisions
- Only github.com URLs are recognised, so GitHub Enterprise issue URLs are rejected.
- The dedupe key is the text hash, so a label or title change counts as "changed".
- A planned brief keeps its plan on refresh.
- A bare `#N` means whatever repo `gh` resolves from the root.

## Not checked
I did not run the tests. I did not read the task's steps. I did not read `brief_summary` or `cmd_inbox` consumers beyond a grep.

**Noticed:** none

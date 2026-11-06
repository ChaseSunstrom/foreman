**Verdict:** approve with nits.

## lens: intent
- MEDIUM — plugin/lib/fmeco.py:956-957 — Each word line prints the raw learned weight (`onboarding +2 lifts it`), but `title_tilt` adds only weight/2 per word (fmcore.py:1977), and the header shows the capped total. The test fixture shows it: +2, +2 and −2 sit under a header of `+1`. The CHANGELOG says "at most 2 points either way", so a reader takes `+2` as two points when it is one. The lines should add up to the tilt. — Print `v/2` per word (`{v/2:+g}`), or label the number as a weight ("weight +2") and keep the header as points. Update the test strings to match. — confidence: high (the arithmetic is verified; whether it confuses a user is a judgement).

## lens: adversary
- No findings. `b.title` goes through `c.plain`, and the error path wraps `tid` in `c.plain` and `c.fit`. The words come from the `_PREF_WORD` regex, so they carry no escape sequences. `prefer.json` is read through `learned_weights`, which tolerates a malformed file.

## lens: edge
- LOW — plugin/lib/fmeco.py:910-912 — `fm inbox --why T-0001` with no source lists the inbox and silently ignores `--why`. T-1855's rule says no flag should go unread. The same holds for the other flags, so it predates this change, but the new flag copies it. — With no source, error if any flag is set, or leave it and capture it. — confidence: medium.
- LOW — plugin/lib/fmeco.py:82 — A captured item that is batched (`batched(b, by_id)`) is not ranked by `rank_inbox` (fmcore.py:1949). `--why` still reports a tilt for it, and that tilt affects nothing. — Rare; leave it, or refuse the item as "waits on its host". — confidence: medium.

## lens: operator
- Ok. `fm triage` is a new top-level verb, and MASTER.md, CHANGELOG and the backlog.md `argument-hint` all mention it. Cost is nil: no hook, loop or network call. The only reads are `prefer.json` and the briefs, once per call.

## lens: maintainer
- LOW — plugin/tests/test_inbox_more.py:151-163 — The triage test covers TTY, TTY with `--serve`, piped, and piped with `--json`. It does not cover a TTY with `--json`, which `cmd_triage` routes to `first` through the `not args.json` clause (fmeco.py:95). It also does not cover `--serve --json`, which should raise. Deleting the `not args.json` clause leaves the suite green. — Add one case with `_tty` mocked True and `--json`, asserting `swipe_loop` is not called. — confidence: high.
- LOW — plugin/lib/fmeco.py:84 — The message "fm inbox prefer --why T-0099: an item in the inbox" is a fragment. Neighbouring messages say "a number from 0 to 1", which has the same shape, so this matches the surroundings and is a nit only. — confidence: low.
- The `args.file`, `args.loser` and `args.reset` check at fmeco.py:951 correctly rejects the mixed forms, and the test exercises them.

## Acceptance criteria
- `prefer --why` names each weighted title word and the tilt: met, apart from the unit mismatch above (test_inbox_more `test_why_…`).
- `fm triage` picks serve, the loop or the first list: met. `cmd_triage` (fmeco.py:95) and the test at test_inbox_more.py:151-163 show it. I did not run `python3 plugin/tests/run.py test_inbox_more test_docs`, so the test run is not verified.

## Implicit decisions
- `--why` accepts only captured items. A planned, deferred or done item is refused.
- `triage` is a separate verb. It sets `args.source` and delegates to `cmd_inbox`.
- A terminal means both stdin and stdout are TTYs.
- `--json` on a terminal gives the first list, not the swipe loop.
- Words are sorted by |weight| descending, then alphabetically.
- The output prints `+0` for a zero tilt and omits the word list when none apply.
- The `--why` JSON shape is `{id, tilt, words:[{word, weight}]}`.

## Not checked
- I did not run the test suite or `fm doctor`.
- I did not check the fm code app (fmcodetui) for a triage entry.
- I did not check the `test_docs` verb-documentation rules.

**Noticed:** none

## Verdict

Approve with nits. The five focus areas hold up. The findings are one MEDIUM and three LOW, and none block the change.

## lens: adversary

Ticket-source forgery is not possible, and I found no way for text to trigger a post.

- **Title and body forgery:** `ticket_source` reads only line 2 of "Raw request" (`fmeco.py:668-669`). The title is the first `splitlines()` element, and `c.plain` strips Cc, Cf, Zl and Zp characters (`fmcore.py:2408`). `\r`, `\x0b`, `\x0c`, `\x85` and `\u2028` therefore cannot add a line. Body lines are always `"| "`-prefixed (`fmeco.py:303`, `:755`). Pasted briefs get `CONTEXT: ticket SHA, pasted…` on line 2, which the regex rejects.
- **Injection through the source:** the Jira key must fullmatch `_TICKET_KEY` before it reaches the URL path (`fmeco.py:671`). The GitHub repo and number are passed as `--repo=` and `--body=`, so they cannot become options. Linear sends the key in a JSON variable.
- **Outward only on `--post`:** `post_ticket` has one caller, `fmeco.py:853`, behind `args.source == "ticket" and args.post`. `--post` on any other source is refused (`:805`). The finish hint only prints a command. I checked every other `capture_once` and `_create` caller: none puts untrusted text on line 2.
- **Token host:** both calls go through `fmmodels._OPENER`, whose `_NoRedirect` turns a 3xx into an `HTTPError` (`fmmodels.py:208-213`). A POST therefore cannot be redirected with its token, and the Linear URL is fixed. The Jira host is `JIRA_URL`'s.

## lens: edge

- MEDIUM — `plugin/lib/fmeco.py:677-696` — The check for an earlier post, the outward call and the log marker are three separate steps, and only the marker is written under the lock (`fmcli.mutate`). Two concurrent `fm inbox ticket --post T-1` runs both pass the check and both comment. A gh timeout (60 s) or a Jira/Linear timeout (20 s) after the server accepted the comment raises "timed out" and writes no marker, so a retry posts again. Neither message warns that the first attempt may have landed. Fix: write a claim line under the lock before posting and clear it on a definite failure, or say "may have been posted: check the issue" on timeout. — confidence high that the duplicate is possible; reproducible by running two `--post` commands at once.
- LOW — `plugin/lib/fmcli.py:1172` vs `plugin/lib/fmeco.py:174` — The hint tests the loose substring `" committed "` in the Log, but `post_ticket` needs `^- \S+ committed SHA `. Stacked closes (`--stack`) log no such line (`fmstack.py:96` only prints), so they get no hint and `--post` refuses with "no commit closed it". Any log line that merely contains " committed " (for example "not committed") prints a hint that `--post` then refuses. Fix: share one `closing_sha(b)` helper between the hint and `post_ticket`, and have the stack path log `committed SHA`. — confidence high.
- LOW — `plugin/lib/fmeco.py:179` — The comment names the local short sha, and the hint appears at finish, before any push. Posted before pushing, or before a rebase, the sha does not exist on the remote. Fix: warn (or refuse) when `git branch -r --contains SHA` is empty, as `_landed` already computes it. — confidence medium.
- LOW — `plugin/lib/fmeco.py:601-606` — The Jira brief records only the key, not the host. After `JIRA_URL` changes, `--post` comments on whatever same-keyed issue the new instance holds. Fix: record the host in the CONTEXT line, or note this limit in the docs. — confidence medium.

## Acceptance criteria

- **Posts one comment naming the commit (GitHub via gh, Jira, Linear):** met. `post_ticket` and `test_a_github_issue_gets_one_comment_naming_the_commit` cover it. The Jira and Linear tests cover both Linear calls and a `success: False` answer.
- **Refuses no source, not done, no commit, already posted:** met, with tests, apart from the `--stack` gap above.
- **`fm task finish` of a fetched ticket names the command:** met for a plain `--commit` close. The hint sits just before Landed, and `test_execution.py` pins it with `out[-2]`. Not met for stacked closes.
- **`python3 plugin/tests/run.py test_inbox_more test_execution`:** not run, because I am read-only.

## Implicit decisions

- A post marks the log with `posted the close to SVC KEY`, once per task.
- The last `committed SHA` line wins.
- A failed post leaves no marker.
- The comment text is fixed and carries no ticket text and no link.
- The Linear comment goes to the issue id that a key lookup returns.
- The Jira host is whatever `JIRA_URL` is at post time.
- Plain-`#N` GitHub sources use `gh`'s default repo from the project root.

## Not checked

I did not run the tests. I did not check the guard for classifying `fm inbox ticket --post` when an agent runs it. Only the docs, `backlog.md` and the hint text, say it must be run only when asked. That is the same as other outward verbs.

Files that don't map to a step: `fmcli.py`, `fmeco.py` and the two test files. They are the implementation and its tests, so they are expected.

The pre-audit "secret" in `test_inbox_more.py` is the existing fake `FAKE` token (line 214), so I dismiss it.

**Noticed:** an agent can run `fm inbox ticket --post` unprompted, because the only barrier is documentation. A guard category or an `fm ask` step for outward posts would enforce "only when asked".

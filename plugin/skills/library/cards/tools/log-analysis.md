---
name: log-analysis
title: Log analysis
area: tools
tags: [logs, debugging, grep, incidents, timeline]
detect: []
related: [jq, ripgrep, sed-awk, kubectl-debugging]
---
Log analysis: narrow by time and request id, count by error, and build a timeline, so a cause rests on lines you can quote.

## Verify
- `rg -c 'ERROR' app.log`: how many error lines exist, to size the problem.
- `rg 'req_id=abc123' app.log | sort`: every line for one request, in time order.
- `jq -c 'select(.level=="error") | {ts,msg,req_id}' app.jsonl`: errors from structured logs, in short form.
- `awk '{print $1}' access.log | sort | uniq -c | sort -rn | head`: top values of a column (client, path, status).
- `journalctl -u SERVICE --since "10 min ago" --no-pager`: a systemd service's recent logs.

## Test first
Write down the symptom as a query that returns the evidence, before theorizing.
```
# symptom: some checkout requests return 500
jq -c 'select(.status==500) | {ts,path,req_id,err}' app.jsonl | head
# pick one req_id, read its whole story:
jq -c 'select(.req_id=="r-91")' app.jsonl
```
After the fix, the same query over the new window returns nothing.

## Do
- Fix the window first: start time, end time and timezone (convert to UTC), and the deploy times inside it.
- Start from the first error, not the loudest: later errors are often consequences.
- Group by message template after stripping ids: `sed -E 's/[0-9a-f-]{8,}/ID/g; s/[0-9]+/N/g' | sort | uniq -c | sort -rn | head`.
- Follow one request id across services, and keep its lines in time order.
- Compare against a healthy window: a count that was always there is not the cause.
- Check what changed at the time the errors began: deploy, config, traffic, dependency.
- Quote exact lines and counts in the conclusion, and name the query that produced them.

## Avoid
- Reading from the bottom of a huge file without a window: you see the aftermath. Filter by time.
- Mixed timezones or clock skew across hosts: ordering lies. Normalize to UTC, and allow skew.
- `grep -i error` as the whole analysis: it counts "no error" lines too. Match the level field or an anchored pattern.
- Calling the most frequent error the cause: frequency is not causality. Find the earliest one and the change that preceded it.
- Sorting or `uniq` without `sort` first: `uniq` only merges adjacent lines. Sort, then count.
- Pasting logs with tokens, emails or card data into tickets: redact first.

## Review
- [ ] A time window, timezone and deploy marker are stated.
- [ ] The earliest failure and one full request trace are quoted.
- [ ] Counts compare the bad window to a good one.
- [ ] The fix is shown by the same query returning clean results, with logs redacted.

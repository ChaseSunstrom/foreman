---
name: fluent-bit
title: Fluent Bit
area: infra
tags: [fluent-bit, logging, observability, parsers, kubernetes, loki]
detect: [file:fluent-bit.conf, file:fluent-bit.yaml, file:parsers.conf]
related: [loki, opentelemetry, prometheus, kubernetes]
---
Fluent Bit: inputs, parsers, filters and outputs validated by a dry run, with buffering and backpressure planned.

## Verify
- `fluent-bit -c fluent-bit.conf --dry-run`: parses the configuration and exits without running.
- `fluent-bit -c fluent-bit.conf -o stdout -f 1`: a quick local run printing records to stdout (flush every second).
- `curl -s localhost:2020/api/v1/metrics`: per-plugin input, output, retry and drop counters (needs `HTTP_Server On`).
- `curl -s localhost:2020/api/v1/health`: health endpoint, when `Health_Check On` is set.

## Test first
Feed a known line and assert the parsed record before touching outputs.
```bash
printf '2026-01-02T03:04:05Z level=error msg="boom"\n' > /tmp/in.log
fluent-bit -i tail -p path=/tmp/in.log -p read_from_head=true \
  -p parser=logfmt -o stdout -f 1 &
sleep 3; kill %1
# expect a record with level=error in the output
```
Use the same parser definition you ship in `parsers.conf`.

## Do
- Use the YAML format (`service`, `pipeline.inputs`, `pipeline.filters`, `pipeline.outputs`) or classic `[INPUT]`, `[FILTER]`, `[OUTPUT]` sections consistently; do not mix.
- Tag every input and match filters and outputs with `Match` patterns.
- Set `Parsers_File` and parse in the input (`Parser`) or with the `parser` filter; test regex parsers against real samples.
- Use the `kubernetes` filter for pod metadata, with `Merge_Log` and `Keep_Log Off` to avoid duplicates.
- Enable filesystem buffering (`storage.type filesystem`, `storage.path`) and set `storage.max_chunks_up` and `Mem_Buf_Limit` to bound memory.
- Set `Retry_Limit` on outputs and watch `retries_failed` and `dropped_records` metrics.
- Use `Rewrite_Tag` or `grep` and `modify` filters to drop noise early.
- Use `tail` with `DB` (`/var/lib/fluent-bit/state.db`) so offsets survive restarts, and `Skip_Long_Lines On`.
- Run as a DaemonSet with read-only host log mounts and a ServiceAccount limited to pods and namespaces.

## Avoid
- `tail` without a `DB`: after restart logs are re-read or lost. Set a persistent `DB` path.
- No buffer limits: a slow backend grows memory until the OOM kill. Set `Mem_Buf_Limit` or filesystem storage.
- Regex parsers with no `Time_Key` and `Time_Format`: records are stamped at ingestion and sorts wrongly. Define them.
- Unquoted high-cardinality fields used as Loki labels: index explosion. Keep labels few and put the rest in the line.
- Shipping `Keep_Log On` with merged JSON: doubles volume. Turn it off once parsed.
- Credentials in plain config files: use environment variables (`${VAR}`) from Secrets.

## Review
- [ ] `--dry-run` passes in CI.
- [ ] Parsers are tested against real samples.
- [ ] Buffers and retries are bounded; metrics are scraped.
- [ ] Offsets persist across restarts.
- [ ] Output labels and credentials are handled safely.

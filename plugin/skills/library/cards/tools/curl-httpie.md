---
name: curl-httpie
title: curl and HTTPie
area: tools
tags: [http, api, debugging, curl, httpie, cli]
detect: []
related: [bruno, jq, tcpdump, ngrok]
---
curl and HTTPie: send exact HTTP requests from a shell, to reproduce API behavior, inspect headers and script health checks.

## Verify
- `curl -sS -o /dev/null -w '%{http_code} %{time_total}s\n' URL`: status and latency, quiet but errors still show.
- `curl -sSi URL`: response status line and headers with the body.
- `curl -sSv URL 2>&1 | head -40`: TLS handshake, request and response headers, redirect hints.
- `curl -fsS URL`: exits nonzero on HTTP 4xx and 5xx, for scripts and health checks.
- `http --print=HhBb POST URL name=x`: HTTPie prints request and response (JSON body from `key=value`).

## Test first
Reproduce the failing request exactly, then change one thing at a time.
```
curl -sS -X POST https://api.example.test/items \
  -H 'content-type: application/json' \
  -H "authorization: Bearer $TOKEN" \
  -d '{"name":""}' -w '\n%{http_code}\n'
# expect 422 with a field error; the bug is a 500 or an empty body
```

## Do
- Use `-H 'content-type: application/json'` with `-d`; without it curl sends form encoding.
- Use `--data-urlencode` for query-like values, `-G` to put `-d` pairs in the query string.
- Use `-L` to follow redirects (and `-i` to see each hop), and `--max-time 10` in scripts.
- Pipe to `jq` for JSON assertions: `curl -fsS URL | jq -e '.status == "ok"'`.
- Pass secrets from env vars and avoid putting tokens in shell history; use `-H @file` or a config file with `-K`.
- Use `--resolve host:port:ip` to test a host before DNS changes, and `-k` only for throwaway debugging.
- Use `--retry 3 --retry-connrefused` for flaky startups.

## Avoid
- `curl URL` without `-f` in CI: a 500 still exits 0. Use `-f` or check `%{http_code}`.
- `-d` with a JSON file path lacking `@`: sends the literal string. Use `-d @body.json`.
- Unquoted URLs with `&`: the shell splits them. Quote the whole URL.
- `-k` left in committed scripts: disables certificate checks. Trust the CA with `--cacert`.
- `-X GET` with `-d`, or `-X POST` after a redirect: it forces the method on every hop. Let curl choose, or use `--post301` deliberately.
- HTTPie `:=` vs `=`: `=` sends strings, `:=` sends raw JSON (numbers, booleans). Use `:=` for non-strings.

## Review
- [ ] The request is reproducible by pasting the command, with secrets from the environment.
- [ ] Scripts fail on HTTP errors and have timeouts.
- [ ] TLS verification is on, except in a marked local debugging line.
- [ ] Content-type and body encoding match what the API expects.

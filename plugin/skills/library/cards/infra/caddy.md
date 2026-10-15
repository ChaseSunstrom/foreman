---
name: caddy
title: Caddy
area: infra
tags: [caddy, reverse-proxy, tls, acme, caddyfile, http]
detect: [file:Caddyfile, file:Caddyfile.*, file:caddy.json, file:*.caddyfile]
related: [nginx, traefik, docker, systemd, cert-manager]
---
Caddy: automatic-HTTPS web server and reverse proxy configured with a short Caddyfile.

## Verify
- `caddy validate --config Caddyfile --adapter caddyfile`: the file parses and modules resolve.
- `caddy fmt --diff Caddyfile`: the file is canonically formatted (use `--overwrite` to fix).
- `caddy adapt --config Caddyfile --pretty`: the JSON the Caddyfile compiles to, for checking what is really configured.
- `caddy reload --config Caddyfile`: a zero-downtime config reload on a running instance.
- `curl -sI --resolve example.com:443:127.0.0.1 https://example.com/`: the site answers with the expected status.

## Test first
Write the request that must hold, then adjust the Caddyfile.
```sh
caddy validate --config Caddyfile
curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/api/health | grep -q 200   # red until reverse_proxy exists
curl -sI http://localhost:8080/ | grep -qi 'x-content-type-options'
```
Use `{ auto_https off }` and `http://localhost:8080` for local tests so no certificate is requested.

## Do
- Name sites by hostname. Caddy obtains and renews certificates automatically when the name is public and ports 80 and 443 are reachable.
- Proxy with `reverse_proxy app:3000`. Caddy passes `Host` and sets `X-Forwarded-*` for you.
- Use `handle` and `handle_path` blocks for path routing, since directive order is defined by Caddy and `route` makes order explicit.
- Add `encode zstd gzip` and `header { Strict-Transport-Security "max-age=31536000"; -Server }`.
- Define reusable pieces with snippets `(name) { ... }` and `import name`.
- Use `{env.VAR}` placeholders for secrets and tokens, never literal values.
- Use `tls internal` for private names and the `acme_dns` option with a DNS plugin for wildcards.
- Persist `/data` in containers so certificates and the ACME account survive restarts.

## Avoid
- Putting the config in `/etc/caddy/Caddyfile` with tabs or spaces mixed and no `caddy fmt`: noisy diffs and lint. Format it.
- Not persisting `/data`: each container restart re-issues certificates and hits Let's Encrypt rate limits. Mount a volume.
- Adding `proxy_set_header`-style forwards by hand: unnecessary and can duplicate. Rely on defaults, or use `header_up` only when needed.
- Using `file_server` on a root containing dotfiles or secrets: browse is off by default but files are served. Point `root` at a public directory.
- Wrong directive-order assumptions (`redir` after `reverse_proxy`): use `route` or `handle` to control it.
- Wildcard certs through HTTP challenge: impossible. Use the DNS challenge.
- A public hostname on `localhost`-only networks: the ACME validation fails. Use `tls internal` or an explicit `http://` site.

## Review
- [ ] `caddy validate` passes and `caddy adapt` matches intended routing.
- [ ] Certificate storage is persistent, and ACME ports are open or DNS challenge is configured.
- [ ] Secrets come from environment placeholders.
- [ ] Security headers and compression are set where needed.

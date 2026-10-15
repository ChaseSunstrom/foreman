---
name: nginx
title: NGINX
area: infra
tags: [nginx, reverse-proxy, tls, http, load-balancing, config]
detect: [file:nginx.conf, file:nginx/*.conf, file:conf.d/*.conf, file:sites-available/*, file:*.nginx.conf]
related: [caddy, traefik, docker, systemd, cert-manager]
---
NGINX: reverse proxy and static server configuration with TLS, correct proxy headers, timeouts and rate limits.

## Verify
- `nginx -t`: the configuration parses and referenced files exist.
- `nginx -T`: dumps the full effective config, including includes.
- `curl -sI -H 'Host: example.com' http://127.0.0.1/`: the vhost answers with the expected status and headers.
- `curl -sk --resolve example.com:443:127.0.0.1 https://example.com/ -o /dev/null -w '%{http_code}'`: the TLS vhost routes correctly.
- `nginx -s reload`: applies the new config without dropping connections.

## Test first
Write the request that should succeed or be denied, then change the config until it does.
```sh
curl -sI http://127.0.0.1/admin | head -1 | grep -q '403'   # red until a deny rule exists
curl -sI http://127.0.0.1/ | grep -qi 'strict-transport-security'
nginx -t
```
Run it in a throwaway container (`docker run --rm -v $PWD/nginx.conf:/etc/nginx/nginx.conf:ro -p 8080:80 nginx`) and check `nginx -t` first.

## Do
- Proxy with `proxy_pass http://upstream;` plus `proxy_set_header Host $host;`, `X-Real-IP $remote_addr;`, `X-Forwarded-For $proxy_add_x_forwarded_for;`, and `X-Forwarded-Proto $scheme;`.
- Define `upstream` blocks with `keepalive` and set `proxy_http_version 1.1; proxy_set_header Connection "";` for connection reuse.
- Add websockets with `proxy_set_header Upgrade $http_upgrade;` and `Connection "upgrade"`.
- Terminate TLS with `ssl_protocols TLSv1.2 TLSv1.3;`, `http2 on;` and an HSTS header, and redirect port 80 to 443.
- Set `client_max_body_size`, `proxy_read_timeout` and `limit_req_zone` / `limit_req` deliberately.
- Use `server_tokens off;` and `try_files $uri $uri/ =404;` for static roots.
- Keep one `server_name` per vhost and include shared snippets from `conf.d/` or `snippets/`.

## Avoid
- `if` inside `location` for routing or rewriting: it behaves unpredictably. Use `map`, `try_files` or separate locations.
- `proxy_pass http://upstream/` with a trailing slash when you didn't mean to strip the location prefix: paths get rewritten. Match the slashes in `location` and `proxy_pass`.
- `proxy_pass http://$host$request_uri;` or user-controlled variables: open proxy and SSRF. Use fixed upstreams.
- Missing `X-Forwarded-Proto`: apps generate http redirects. Pass it.
- `listen 443 http2` with the old form: deprecated. Use `listen 443 ssl;` and `http2 on;`.
- Serving `/.git` or dotfiles: add `location ~ /\. { deny all; }`.
- Resolving upstream DNS only at startup in containers: it breaks when IPs change. Use a `resolver` with a variable in `proxy_pass`.
- Reloading without `nginx -t`: a bad config fails the reload.

## Review
- [ ] `nginx -t` passes and the effective config from `nginx -T` matches intent.
- [ ] Proxy headers, timeouts and body limits are set explicitly.
- [ ] TLS protocols, HSTS and HTTP-to-HTTPS redirect are correct.
- [ ] No `if` routing and no open-proxy variables.

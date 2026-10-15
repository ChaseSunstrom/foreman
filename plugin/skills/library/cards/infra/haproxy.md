---
name: haproxy
title: HAProxy
area: infra
tags: [haproxy, load-balancer, proxy, tls, health-checks, acl]
detect: [file:haproxy.cfg]
related: [envoy, nginx, traefik, caddy]
---
HAProxy: validated configs with explicit timeouts, health checks, ACL routing and graceful reloads.

## Verify
- `haproxy -c -f /etc/haproxy/haproxy.cfg`: config syntax and semantics check (exit 0 means valid).
- `echo "show servers state" | socat stdio /run/haproxy/admin.sock`: backend server states through the runtime socket.
- `echo "show stat" | socat stdio /run/haproxy/admin.sock`: stats including check status and errors.
- `curl -sI http://localhost/ -H 'Host: app.example.com'`: the routing rule picks the intended backend.

## Test first
Config check and routing assertions first.
```bash
haproxy -c -f haproxy.cfg || exit 1
test "$(curl -s -o /dev/null -w '%{http_code}' -H 'Host: api.example.com' localhost/health)" = 200
test "$(curl -s -o /dev/null -w '%{http_code}' -H 'Host: unknown.example.com' localhost/)" = 503
```

## Do
- Set `timeout connect`, `timeout client` and `timeout server` in `defaults`; add `timeout http-request` and `timeout http-keep-alive`.
- Use `mode http` for L7 and `mode tcp` for passthrough, per frontend and backend.
- Route with `acl` plus `use_backend`, and give a `default_backend`.
- Add `option httpchk` with `http-check send` and `check inter` on each `server`, plus `rise` and `fall`.
- Terminate TLS with `bind :443 ssl crt /etc/haproxy/certs/ alpn h2,http/1.1`; set `ssl-min-ver TLSv1.2` and redirect HTTP with `http-request redirect scheme https`.
- Set forwarding headers with `option forwardfor` and `http-request set-header X-Forwarded-Proto https`.
- Use `rate-limit` via stick tables (`stick-table`, `http-request track-sc0`, `deny`) for abuse control.
- Reload with `systemctl reload haproxy` (master-worker mode) so connections drain.

## Avoid
- No timeouts in `defaults`: connections hang forever and warnings appear. Set them.
- Health check on `/` of a heavy page: load and false flaps. Use a cheap health endpoint.
- Stats socket or stats page open to the world: bind it to a local socket or protect with ACL and auth.
- Putting `http-request` rules after `use_backend` expecting order effects across sections: rule types run in a fixed order. Test the result.
- Restart instead of reload: dropped connections. Reload.
- Trusting client `X-Forwarded-For` as-is: delete or overwrite at the edge (`http-request del-header X-Forwarded-For`).

## Review
- [ ] `haproxy -c` passes in CI.
- [ ] Timeouts, health checks and `default_backend` are present.
- [ ] TLS minimum and redirect are set.
- [ ] Admin socket and stats are not public.
- [ ] Client IP header handling is intentional.

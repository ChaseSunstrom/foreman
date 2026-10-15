---
name: traefik
title: Traefik
area: infra
tags: [traefik, reverse-proxy, ingress, routers, middlewares, acme]
detect: [file:traefik.yml, file:traefik.yaml, file:traefik.toml, file:dynamic.yml, file:dynamic/*.yml, dep:traefik]
related: [nginx, caddy, docker, kubernetes, docker-compose]
---
Traefik: dynamic reverse proxy and ingress, with entrypoints, routers, middlewares and services from providers.

## Verify
- `traefik version`: the binary runs (and confirms the major version to match the config).
- `docker compose config -q`: labels-based config in compose parses.
- `curl -s localhost:8080/api/http/routers`: the router list from the API (when `api.insecure` is on in dev) shows the router and its status.
- `curl -s localhost:8080/api/http/services`: the services and server health.
- `curl -sI -H 'Host: app.example.com' http://127.0.0.1/`: the router matched and the backend answered.

## Test first
Make the router assertion fail before adding labels or dynamic config.
```sh
curl -s localhost:8080/api/http/routers | grep -q '"name":"app@docker"'   # red until labels exist
curl -sI -H 'Host: app.example.com' http://127.0.0.1/ | head -1 | grep -q 200
```
Run Traefik with `--log.level=DEBUG` and watch for "router ... uses a non-existent" messages.

## Do
- Split static config (`entryPoints`, `providers`, `certificatesResolvers`) from dynamic config (routers, services, middlewares).
- Opt containers in with `providers.docker.exposedByDefault=false` and `traefik.enable=true` per service.
- Define routers with `rule` (``Host(`app.example.com`) && PathPrefix(`/api`)``), `entryPoints`, `service` and `tls.certResolver`.
- Set the backend port with `traefik.http.services.<name>.loadbalancer.server.port=3000`.
- Attach middlewares (`redirectscheme`, `headers`, `ratelimit`, `basicauth`, `forwardauth`) and chain them in order.
- Use ACME with a persisted `acme.json` (mode 600) and an HTTP, TLS or DNS challenge.
- Put a health check on services, and use the `file` or Kubernetes CRD provider (`IngressRoute`) with `watch: true`.
- Keep the dashboard private: bind to an internal entrypoint with auth.

## Avoid
- v1 syntax (`frontend.rule`, `[docker] domain`): removed in v2. Use `http.routers` and `rule`.
- `api.insecure: true` on a public interface: an open dashboard and API. Secure it behind auth, or disable it.
- `exposedByDefault` left true: every container becomes routable. Set it false.
- Mounting `docker.sock` read-write into Traefik: a compromise means host root. Use `:ro` and a socket proxy.
- Non-persistent `acme.json`: certificate reissue and rate limits. Mount a volume with permissions 600.
- A router without `service` when more than one is defined, or a wrong network: 502/404. Set `traefik.docker.network`.
- Backticks in `Host()` rules replaced by quotes in YAML labels: rule parse errors. Keep backticks and quote the label.
- Several routers matching one request with the same priority: ambiguous. Set `priority` explicitly.

## Review
- [ ] Opt-in exposure, with router, entrypoint, TLS resolver and service port declared.
- [ ] Dashboard and API are not publicly reachable without auth.
- [ ] Certificates persist, with `acme.json` at 600.
- [ ] Middlewares for redirect, headers and rate limits are attached where required.

---
name: cloudflare-tunnel
title: Cloudflare Tunnel
area: cloud
tags: [cloudflare, tunnel, cloudflared, zero-trust, access, ingress]
detect: [file:cloudflared*.yml, file:cloudflared*.yaml, dep:cloudflared]
related: [cloudflare-workers, cloudflare-pages, aws-vpc]
---
Cloudflare Tunnel: outbound-only connections from cloudflared to the edge, ingress rules with a final catch-all, Access policies in front, and token handling.

## Verify
- `cloudflared tunnel list`: the tunnel exists with active connections.
- `cloudflared tunnel info NAME`: connector instances and their versions.
- `cloudflared tunnel ingress validate`: the ingress rules parse (run with the config file in place).
- `cloudflared tunnel ingress rule https://app.example.com`: which rule a URL matches.
- `curl -sI https://app.example.com`: an unauthenticated request is redirected to Access or refused, not served.

## Test first
Validate ingress rules and the catch-all in CI before deploying the connector.
```yaml
# config.yml
tunnel: TUNNEL_ID
credentials-file: /etc/cloudflared/TUNNEL_ID.json
ingress:
  - hostname: app.example.com
    service: http://localhost:8080
  - service: http_status:404
```
Run `cloudflared tunnel ingress validate` and fail the build on a non-zero exit.

## Do
- Create a remotely managed tunnel (token based) or a locally managed one with a config file, and keep one source of truth for ingress.
- End the ingress list with a catch-all rule such as `service: http_status:404`. It is required.
- Put a Cloudflare Access application and policy in front of every hostname that is not public, and validate the Access JWT (`Cf-Access-Jwt-Assertion`) in the origin for defense in depth.
- Bind the origin to localhost or a private network so it cannot be reached except through the tunnel, and firewall inbound ports.
- Run at least two cloudflared replicas for availability and run it as a service (systemd or a container) with restart on failure.
- Store the tunnel token or credentials file as a secret with restrictive file permissions, and rotate by creating a new tunnel token.
- Use private network routes (WARP) for non-HTTP services instead of exposing them publicly.
- Keep cloudflared updated and watch connector health in metrics (`--metrics`).
- Name DNS routes with `cloudflared tunnel route dns NAME host`.

## Avoid
- A missing catch-all rule: the config fails validation. Add the 404 service last.
- Exposing admin tools without Access: the tunnel gives public reachability. Add an Access policy.
- Leaving the origin's public port open: attackers bypass the tunnel and Access. Close it.
- Committing the credentials JSON or token to git: anyone can run your tunnel. Keep it in a secret store.
- A single connector for production: restart or host loss means downtime. Run replicas.
- `noTLSVerify: true` as a fix for a self-signed origin: it disables verification. Set `originServerName` and a trusted CA instead.
- Running cloudflared as root with broad host access: use a dedicated user.

## Review
- [ ] Ingress validates and ends with a catch-all.
- [ ] Every private hostname has an Access policy, and the origin checks the Access JWT.
- [ ] Origin not reachable except through the tunnel.
- [ ] Credentials stored as secrets, not in the repo.
- [ ] More than one connector, with monitoring.

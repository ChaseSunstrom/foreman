---
name: consul
title: Consul
area: infra
tags: [consul, service-discovery, service-mesh, kv, acl, hashicorp]
detect: [file:consul.hcl, file:consul.json, file:*.consul.hcl]
related: [nomad, vault, envoy, istio]
---
Consul: service discovery, health checks, KV and mesh, run with ACLs, gossip encryption and TLS enabled.

## Verify
- `consul validate /etc/consul.d/`: agent configuration is valid.
- `consul members`: servers and clients are alive in the cluster.
- `consul operator raft list-peers`: a leader exists and the voter count is odd.
- `consul catalog services`: services registered as expected.
- `consul monitor -log-level=debug`: live agent logs while testing a change.

## Test first
Assert registration and health before wiring clients to discovery.
```bash
consul validate /etc/consul.d/ && consul reload
dig @127.0.0.1 -p 8600 api.service.consul +short | grep -E '^[0-9.]+$'
curl -s localhost:8500/v1/health/service/api?passing | jq -e 'length > 0'
```

## Do
- Run 3 or 5 servers; set `server = true` and `bootstrap_expect` to match, with `data_dir` on persistent disk.
- Enable ACLs: `acl { enabled = true  default_policy = "deny"  tokens { ... } }`; give each agent and service a scoped token.
- Enable gossip encryption (`encrypt` key from `consul keygen`) and TLS (`tls { defaults { ca_file cert_file key_file verify_incoming = true } }`).
- Register services with `service { name port check { ... } }` definitions and meaningful HTTP or gRPC checks with `interval` and `timeout`.
- Use `consul connect` or service mesh intentions (or `service-intentions` config entries) to restrict who can call whom.
- Bind clients to `127.0.0.1` for the HTTP and DNS API and restrict `bind_addr` and `client_addr`.
- Take snapshots on a schedule: `consul snapshot save FILE` and test `restore`.
- Use config entries (`service-defaults`, `proxy-defaults`) for mesh settings as code.

## Avoid
- ACLs in `default_policy = "allow"`: any client can read the KV and register services. Use deny with scoped tokens.
- `client_addr = "0.0.0.0"` without ACLs and TLS: an open API. Bind locally or secure it.
- Even number of servers or a single server in production: no fault tolerance. Use 3 or 5.
- Storing secrets in the KV: unencrypted at rest by default. Use Vault or encrypted values.
- TTL checks no one updates: services flap critical. Use script, HTTP or gRPC checks, or update the TTL on a timer.
- Skipping `consul snapshot` testing: backups that never restored are guesses.

## Review
- [ ] Servers: odd count, ACLs deny by default, TLS and gossip keys set.
- [ ] Each service has a real health check and a scoped token.
- [ ] API and DNS bind addresses are intentional.
- [ ] Snapshots are scheduled and restore-tested.
- [ ] Intentions limit service-to-service traffic.

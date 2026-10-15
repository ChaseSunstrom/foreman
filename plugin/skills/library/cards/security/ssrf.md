---
name: ssrf
title: Server-side request forgery
area: security
tags: [security, ssrf, http, network, cloud-metadata, webhooks]
detect: []
related: [input-validation, webhook-signatures, tls, rate-limiting, threat-modeling]
---
SSRF: when the server fetches a user-supplied URL, allowlist hosts, resolve and check the IP, block redirects, and isolate the network.

## Verify
- `pytest -q tests/security/test_ssrf.py`: loopback, link-local, private and redirect targets are refused.
- `semgrep scan --config p/ssrf --error`: no unchecked outbound fetch of user input (if the rule pack is unavailable use `p/security-audit`).
- `grep -rnE "(requests|httpx|fetch|axios|http\.Get)\(.*(url|uri|target)" src/`: each user-influenced fetch goes through the safe client.

## Test first
```python
import pytest
BAD = ["http://127.0.0.1/", "http://localhost:6379", "http://169.254.169.254/latest/meta-data/",
       "http://[::1]/", "http://10.0.0.5/", "file:///etc/passwd", "http://0x7f.1/",
       "http://attacker.example/redirect-to-metadata"]

@pytest.mark.parametrize("url", BAD)
def test_fetch_preview_blocks_internal_targets(client, url):
    assert client.post("/preview", json={"url": url}).status_code == 400
```

## Do
- Prefer an allowlist of exact hostnames or domains. If arbitrary URLs are required, use a denylist of non-public ranges as a second layer.
- Accept only `http` and `https`, and only ports 80 and 443 unless configured.
- Resolve the hostname yourself, reject loopback, private (RFC 1918), link-local (169.254.0.0/16, including cloud metadata), unique-local and multicast addresses, then connect to that exact resolved IP to defeat DNS rebinding.
- Disable redirects, or revalidate every hop against the same rules.
- Set short connect and read timeouts and a response size cap.
- Run the fetcher in an egress-restricted network segment or behind a proxy with its own allowlist.
- Require IMDSv2 and block metadata access from application hosts where the cloud allows.
- Do not return raw upstream bodies or error text to the caller.

## Avoid
- Validating the hostname string and then fetching: DNS can resolve to an internal IP, or change between check and use (rebinding). Pin the resolved address.
- Parsing URLs with a regex: `http://good.com@evil.com`, decimal, octal and IPv6 forms bypass it. Use a real URL parser and the resolved IP.
- Following redirects by default (`requests` does): an allowed host redirects to metadata. Set `allow_redirects=False` and validate manually.
- Blocking only `127.0.0.1`: also `localhost`, `::1`, `0.0.0.0`, `169.254.169.254`, IPv4-mapped IPv6. Use an IP-class check (`ipaddress.ip_address(...).is_global`).
- Allowing `file://`, `gopher://`, `ftp://`: restrict schemes.
- Webhook "test" and image-proxy features as exceptions: they are SSRF vectors. Route them through the same safe client.

## Review
- [ ] Every outbound request built from user input uses the safe fetcher.
- [ ] Resolved IPs are checked and pinned; redirects handled.
- [ ] Schemes, ports, size and time are limited.
- [ ] Egress is restricted at the network layer.
- [ ] Tests cover metadata, loopback, private and redirect targets.

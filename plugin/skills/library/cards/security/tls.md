---
name: tls
title: TLS configuration
area: security
tags: [security, tls, https, certificates, hsts, mtls]
detect: [file:nginx.conf, file:*.pem, file:*.crt, file:Caddyfile, file:haproxy.cfg]
related: [security-headers, crypto-usage, secrets-management, sigstore]
---
TLS: modern protocol versions, verified certificates on every client connection, automated renewal, and HSTS on the server.

## Verify
- `openssl s_client -connect HOST:443 -servername HOST -verify_return_error </dev/null`: the handshake completes and the chain verifies.
- `openssl s_client -connect HOST:443 -tls1_1 </dev/null`: a handshake with TLS 1.1 is refused.
- `openssl x509 -in cert.pem -noout -enddate -subject`: the expiry date and subject are as expected.
- `curl -sI https://HOST | grep -i strict-transport-security`: HSTS is sent.
- `curl -s -o /dev/null -w "%{http_code} %{redirect_url}\n" http://HOST/`: plain HTTP redirects to HTTPS.

## Test first
Test that clients verify, and that the server refuses old protocols.
```python
import ssl, socket, pytest
def test_server_refuses_tls_1_1():
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    ctx.minimum_version = ctx.maximum_version = ssl.TLSVersion.TLSv1_1
    with pytest.raises((ssl.SSLError, OSError)):
        with socket.create_connection(("localhost", 8443)) as s:
            ctx.wrap_socket(s, server_hostname="localhost")
```
For client code, a test that a self-signed server raises a verification error.

## Do
- Allow TLS 1.2 and 1.3 only, with the server's modern cipher recommendations (Mozilla "intermediate" profile as the baseline).
- Automate certificates with ACME (certbot, Caddy, cert-manager) and alert before expiry.
- Redirect HTTP to HTTPS, then send HSTS; add `Secure` to all cookies.
- On clients leave verification on (Python `requests` default, `ssl.create_default_context()`, Go `tls.Config` defaults) and pass a CA bundle for private CAs.
- Use mutual TLS for service-to-service traffic where identity matters, with short-lived client certificates.
- Terminate TLS at a known layer and encrypt hops that cross untrusted networks.
- Keep private keys readable only by the service user, and never in the repo or image.

## Avoid
- `verify=False`, `rejectUnauthorized: false`, `InsecureSkipVerify: true`, `curl -k`: they remove all protection and tend to ship. Add the private CA to the trust store.
- Disabling hostname checks (`check_hostname = False`) while keeping chain verification: any valid certificate for another host works.
- Leaving TLS 1.0, 1.1 and weak ciphers (RC4, 3DES, export suites) on: downgrade and decryption risks. Set the minimum version.
- Manual certificate renewals on a calendar reminder: outages and rushed fixes. Automate and monitor expiry.
- Self-signed certificates in production with clients told to ignore warnings: pin or use a real CA.
- Pinning leaf certificates in mobile or clients with no rotation plan: rotation bricks the app. Pin to a CA or key set with a backup.

## Review
- [ ] Only TLS 1.2 and 1.3 are enabled.
- [ ] No client code disables verification.
- [ ] Certificates renew automatically and expiry is monitored.
- [ ] HTTP redirects and HSTS are set.
- [ ] Private keys are protected and not committed.

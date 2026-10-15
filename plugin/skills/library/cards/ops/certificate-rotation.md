---
name: certificate-rotation
title: Certificate rotation
area: ops
tags: [tls, certificates, acme, renewal, expiry, pki]
detect: [file:*.crt, file:*.pem]
related: [secrets-rotation, dns, load-balancing, uptime-monitoring, cdn-caching]
---
Automate certificate issuance and renewal, alert on expiry from outside, and rehearse renewal and reload before a certificate matters.

## Verify
- `openssl s_client -connect example.com:443 -servername example.com </dev/null 2>/dev/null | openssl x509 -noout -subject -issuer -enddate`: the certificate actually served, with expiry.
- `openssl x509 -in cert.pem -noout -checkend 1209600`: exit 0 if it is valid for at least 14 more days.
- `openssl verify -CAfile ca.pem -untrusted chain.pem cert.pem`: the chain builds to a trusted root.
- `openssl x509 -in cert.pem -noout -ext subjectAltName`: the names covered, including every host you serve.
- `certbot renew --dry-run`: renewal works end to end against the staging endpoint (certbot).

## Test first
Write the expiry check as a probe that fails under a threshold, and fire it against a short-lived staging cert.
```sh
for h in $HOSTS; do
  end=$(echo | openssl s_client -connect "$h:443" -servername "$h" 2>/dev/null \
        | openssl x509 -noout -enddate | cut -d= -f2)
  left=$(( ( $(date -d "$end" +%s) - $(date +%s) ) / 86400 ))
  [ "$left" -ge 21 ] || { echo "$h expires in $left days"; fail=1; }
done
exit ${fail:-0}
```
Then rehearse: issue a certificate with a short lifetime in staging, let it renew unattended, and confirm the service picked it up without a restart by hand.

## Do
- Automate with ACME (certbot, acme.sh, or the platform's issuer) and renew at about two thirds of lifetime.
- Monitor expiry externally for every public hostname, and alert at 21, 14, and 7 days; also watch internal CA and client certificates.
- Reload services after renewal with a deploy hook (`--deploy-hook` in certbot), and verify the served certificate changed.
- Serve the full chain (leaf plus intermediates), and keep the private key at mode 600 and readable only by the service.
- Generate a new key on each renewal where practical, and keep keys off shared storage and out of git.
- Use DNS-01 for wildcards or hosts that are not publicly reachable, with a narrowly scoped DNS credential.
- Add CAA records so only your CA can issue.
- Keep an inventory of certificates with owner and location, including those on load balancers, CDNs, and appliances.

## Avoid
- Renewal that works but no reload: the old certificate keeps serving until it expires. Add a deploy hook and check the served expiry.
- Checking the file on disk instead of the served certificate: a stale process or a different node serves the old one. Probe the endpoint with `s_client`.
- A cron renewal with no alert on failure: it fails silently for weeks. Alert on days remaining, not on job success.
- An incomplete chain: some clients fail while browsers pass. Serve the chain and test with `openssl verify`.
- Forgotten certificates on CDNs, mail servers, and internal services: they expire in the night. Inventory every one.
- Pinning to a certificate or intermediate: rotation breaks clients. Pin to a key you control with a backup, or avoid pinning.

## Review
- [ ] Renewal is automated, and a dry run or short-lived rehearsal passed.
- [ ] External expiry alerts exist for every hostname, at several thresholds.
- [ ] Deploy hooks reload the service, and the served certificate was checked.
- [ ] Chain, SANs, and key permissions were verified.
- [ ] An inventory covers certificates in load balancers, CDNs, and internal services.

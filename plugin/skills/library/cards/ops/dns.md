---
name: dns
title: DNS operations
area: ops
tags: [dns, records, ttl, dnssec, resolvers, migration]
detect: [file:*.zone]
related: [load-balancing, certificate-rotation, cdn-caching, disaster-recovery]
---
Operate DNS by querying authoritative servers directly, lowering TTLs before changes, and checking every record type you depend on.

## Verify
- `dig +short NS example.com`: the delegated nameservers.
- `dig @ns1.example.com example.com SOA +norecurse`: the authoritative answer and zone serial, free of resolver cache.
- `dig +trace www.example.com`: the delegation chain from the root.
- `dig +dnssec example.com A`: RRSIG present and the `ad` flag set when asked of a validating resolver.
- `named-checkzone example.com ./example.com.zone`: a BIND-style zone file parses.

## Test first
Before a cutover, assert the intended answer on every authoritative server and that the TTL is already low.
```sh
for ns in $(dig +short NS example.com); do
  a=$(dig @"$ns" +short www.example.com A)
  [ "$a" = "203.0.113.10" ] || { echo "$ns serves $a"; exit 1; }
done
ttl=$(dig +noall +answer www.example.com A | awk '{print $2; exit}')
[ "$ttl" -le 300 ] || { echo "TTL still $ttl"; exit 1; }
```
It fails until all nameservers agree and the TTL was lowered a full old-TTL ago.

## Do
- Lower the TTL (to 60-300 s) at least one old TTL before a change, make the change, then raise it again after it settles.
- Keep zones in version control and deploy through a tool (zone file, OctoDNS, Terraform), not console clicks.
- Run two or more nameservers on separate networks or providers.
- Use CNAME only off the apex; use ALIAS or ANAME features where the provider offers them.
- Publish SPF, DKIM, and DMARC TXT records and test them with `dig +short TXT`.
- Add a CAA record to limit who may issue certificates.
- For DNSSEC, keep DS and DNSKEY in step; roll keys with the documented double-sign procedure.
- Monitor resolution from outside, per record, and alert on a changed answer.

## Avoid
- Testing a change through your local resolver: it caches the old answer. Query `@authoritative` with `+norecurse`.
- Changing a record with a 24 h TTL and expecting a fast cutover: lower it first and wait.
- A CNAME at the zone apex or alongside other records: it breaks MX and NS. Use A records or ALIAS.
- Forgetting the AAAA record: IPv6 clients reach the old host. Update or delete both.
- Removing a DS record after disabling DNSSEC in the wrong order: validating resolvers return SERVFAIL. Remove DS at the registrar first, wait out its TTL, then drop the keys.
- A single nameserver, or two behind one provider: one outage takes the domain down. Spread them.

## Review
- [ ] Every authoritative server returns the same serial and answer.
- [ ] TTLs were lowered before the change and restored after.
- [ ] Zone files are in version control and pass a checker.
- [ ] A and AAAA match; mail records (MX, SPF, DKIM, DMARC) are intact.
- [ ] External monitoring checks the record and alerts on change.

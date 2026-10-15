---
name: gdpr
title: GDPR and Privacy
area: domains
tags: [gdpr, privacy, consent, personal-data, retention, dsar]
detect: [dep:cookie-consent, dep:vanilla-cookieconsent, dep:react-cookie-consent, dep:@cookiehub/sdk, dep:osano, dep:cookiebot, dep:klaro, dep:iubenda]
related: [browser-storage, email-sending, file-uploads, auth-providers, web-scraping]
---
Engineering for privacy law: know what personal data you hold and why, collect less, honor consent and erasure, and prove it.

## Verify
- `grep -rniE "email|phone|ip_address|birth|ssn|address" db/migrations src/models`: inventory of personal-data fields to map in the register.
- `curl -sI https://example.com | grep -i set-cookie`: no non-essential cookies are set before consent.
- `npx playwright test privacy`: a fresh context sets no analytics cookies or requests until consent is granted.
- `psql -c "select count(*) from users where deleted_at < now() - interval '30 days'"`: soft-deleted rows past retention (should be 0 after purge).

## Test first
Test erasure and export end to end, and consent gating.
```python
def test_erasure_removes_personal_data_everywhere(client, db, search, blobs):
    uid = make_user(db, email="a@example.com")
    client.delete(f"/api/users/{uid}", headers=auth(uid))
    run_pending_jobs()
    assert db.user_rows(uid) == []                       # or anonymized
    assert db.orders(uid)[0]["email"] is None            # kept for tax, de-identified
    assert search.query("a@example.com") == []
    assert blobs.list(prefix=f"avatars/{uid}") == []

def test_analytics_blocked_before_consent(page):
    page.goto("/")
    assert not any("analytics" in r.url for r in page.requests)
```

## Do
- Keep a record of processing: data item, purpose, legal basis (consent, contract, legitimate interest, legal obligation), recipients, retention.
- Collect the minimum; avoid fields "just in case"; pseudonymize and encrypt at rest and in transit.
- Consent must be opt-in, granular, as easy to withdraw as to give, and logged with timestamp and version; load non-essential scripts only after it.
- Implement data subject requests: access and export (machine-readable, such as JSON), rectification, erasure, restriction, objection, within one month.
- Erase across all stores: primary DB, replicas and backups on rotation, search indexes, caches, analytics, logs, third-party processors, object storage.
- Define retention per data class and enforce it with scheduled purge jobs.
- Sign processing agreements with every vendor that handles personal data; list sub-processors; control transfers outside the EEA.
- Keep personal data out of logs, URLs, error trackers and test fixtures; scrub or hash identifiers.
- Report breaches to the authority within 72 hours; keep a runbook.

## Avoid
- Pre-ticked boxes or "continue means consent": invalid. Use explicit opt-in.
- Loading analytics, ad pixels or fonts from third parties before consent: unlawful transfer of IPs. Gate them.
- Soft delete as erasure: data remains. Hard-delete or irreversibly anonymize after the retention window.
- Personal data in logs and analytics events (emails in URLs): hard to purge. Use opaque ids.
- Copying production data into dev or staging: uncontrolled exposure. Use synthetic or anonymized data.
- Indefinite retention "for analytics": no basis. Set limits and delete.
- Treating a cookie banner as the whole program: it covers little. Cover storage, vendors and rights.

## Review
- [ ] Every personal-data field has a purpose, basis and retention period recorded.
- [ ] Consent is gated, logged, withdrawable; no tracking before it.
- [ ] Export and erasure cover all stores including third parties.
- [ ] Logs, traces and non-production data contain no raw personal data.
- [ ] Vendors, transfers and breach process are documented.

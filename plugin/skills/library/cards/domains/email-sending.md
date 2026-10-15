---
name: email-sending
title: Sending Email
area: domains
tags: [email, smtp, deliverability, spf, dkim, dmarc, transactional]
detect: [dep:nodemailer, dep:@sendgrid/mail, dep:postmark, dep:resend, dep:mailgun.js, dep:@aws-sdk/client-ses, dep:sendgrid, dep:mjml, dep:react-email, dep:django-anymail]
related: [webhooks, gdpr, cron-jobs, auth-providers]
---
Transactional and bulk email that reaches inboxes: authenticated domain, queued sends, bounce handling and tested templates.

## Verify
- `dig +short TXT example.com | grep spf1`: SPF record exists and includes your sender.
- `dig +short TXT _dmarc.example.com`: DMARC policy is published.
- `dig +short TXT selector._domainkey.example.com`: DKIM public key is published (use your provider's selector).
- A local catcher (Mailpit or MailHog on port 1025 SMTP): inspect real rendered messages without sending.

## Test first
Send to a captured transport and assert on the message, including the plain-text part.
```python
def test_reset_email_has_link_and_text_part(outbox, client):
    client.post("/forgot", json={"email": "a@example.com"})
    msg = outbox[-1]
    assert msg["To"] == "a@example.com"
    text = msg.get_body(preferencelist=("plain",)).get_content()
    assert "/reset?token=" in text
    assert msg["List-Unsubscribe"] is None   # transactional: none required
```
Also assert: the same request twice enqueues one email per policy; an unknown address returns the same response.

## Do
- Send from a domain you control with SPF, DKIM and DMARC aligned (start `p=none`, move to `quarantine` then `reject`).
- Use a dedicated transactional provider; separate transactional and marketing streams or subdomains.
- Enqueue sends in a background job with retries and backoff; never block the request on SMTP.
- Ship both HTML and plain-text parts; keep HTML to table layout and inline CSS, tested through MJML or React Email.
- Handle provider webhooks for bounces and complaints, and suppress those addresses.
- Marketing mail: honor opt-in, add `List-Unsubscribe` and `List-Unsubscribe-Post` headers and a visible unsubscribe link.
- Set `Message-ID`, a meaningful `Reply-To`, and a stable From name.
- Use short-lived, single-use tokens in links; expire them.
- Warm up new sending IPs and domains gradually.

## Avoid
- Sending from a free-mail address or an unauthenticated domain: lands in spam or is rejected. Authenticate your own domain.
- Building HTML with user input unescaped: injection into the message. Escape or use a template engine with autoescape.
- Header injection from user-controlled subject or To (newlines): validate and reject CR and LF.
- Retrying sends without an idempotency guard: duplicate emails. Record a send key.
- Password reset responses that reveal whether the account exists: enumeration. Same response either way.
- Image-only emails and link shorteners: spam signals. Use text and your own domain.
- Ignoring bounces: reputation damage. Suppress hard bounces on the first event.
- Real addresses in tests or staging: you mail customers. Route non-production to a catcher.

## Review
- [ ] SPF, DKIM and DMARC pass and align for the From domain.
- [ ] Sends are queued, retried and de-duplicated.
- [ ] Bounces and complaints suppress future sends.
- [ ] Templates render in plain text and in major clients; links expire.
- [ ] Non-production environments cannot reach real recipients.

---
name: email-security
title: Email security
area: security
tags: [security, email, spf, dkim, dmarc, header-injection]
detect: []
related: [account-recovery, input-validation, tls, rate-limiting]
---
Outbound mail is authenticated (SPF, DKIM, DMARC), templated safely, rate limited, and free of header injection and sensitive data.

## Verify
- `dig +short TXT example.com | grep -i spf1`: an SPF record exists and ends in a strict qualifier.
- `dig +short TXT _dmarc.example.com`: a DMARC policy is published, ideally `p=quarantine` or `p=reject`.
- `dig +short TXT selector1._domainkey.example.com`: the DKIM public key is published for the sending selector.
- `pytest -q -k email`: header and template tests pass.

## Test first
User-controlled values must not add headers or recipients.
```python
def test_newline_in_subject_or_name_cannot_inject_headers(mailer, outbox):
    mailer.send_welcome(to="a@x.io", name="Bob\r\nBcc: victim@evil.example")
    m = outbox[-1]
    assert m["Bcc"] is None
    assert "\n" not in m["Subject"] and "\r" not in m["Subject"]
    assert m.get_all("To") == ["a@x.io"]

def test_html_name_is_escaped(mailer, outbox):
    mailer.send_welcome(to="a@x.io", name="<script>x</script>")
    assert "<script>" not in outbox[-1].get_body().get_content()
```

## Do
- Publish SPF listing only your senders, sign with DKIM (2048-bit keys), and set DMARC to monitor first, then quarantine, then reject. Use separate subdomains for marketing and transactional mail.
- Use a mail library and API that takes structured fields. Never concatenate header strings.
- Reject or strip CR and LF in any user value that reaches a header, and validate recipient addresses with a library.
- Escape values in HTML templates (autoescape on), and render plain-text alternatives.
- Set recipients from the stored account, not from the request, on reset and invite flows.
- Send over TLS to the relay with certificate verification. Keep SMTP credentials in a secret store.
- Rate limit sends per user and per IP, and cap invites to stop abuse as a spam relay.
- Put no passwords, full tokens in subject lines, or sensitive data in the body. Use short-lived links.
- Handle bounces and complaints, and suppress them.

## Avoid
- Building `To:` and `Subject:` by string formatting with request values: CRLF injection adds Bcc lines. Use the library's fields and strip newlines.
- A "contact us" form that lets users set the From or To address: fix them server-side and put the user's address in Reply-To.
- `p=none` forever on DMARC: it never blocks spoofing. Move to enforcement.
- Disabling TLS verification to the SMTP relay: use proper certs.
- Putting unescaped user content in HTML mail: it carries phishing or script-like markup. Escape it.
- Open invite or share-by-email endpoints with no limits: they send spam in your name.

## Review
- [ ] SPF, DKIM and DMARC are published and aligned.
- [ ] No header is built from raw user input, and CRLF is rejected.
- [ ] Templates autoescape and recipients come from trusted data.
- [ ] Send limits and bounce handling exist.
- [ ] Mail content holds no secrets.

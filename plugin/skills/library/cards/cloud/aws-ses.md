---
name: aws-ses
title: AWS SES
area: cloud
tags: [aws, ses, email, dkim, spf, bounces, deliverability]
detect: [dep:@aws-sdk/client-ses, dep:@aws-sdk/client-sesv2, dep:nodemailer]
related: [aws-sqs-sns, aws-iam, aws-lambda, localstack]
---
SES sending: verified domain with DKIM, SPF and DMARC, bounce and complaint handling wired up before launch, and a suppression-aware sender.

## Verify
- `aws sesv2 get-email-identity --email-identity example.com --query '[VerifiedForSendingStatus,DkimAttributes.Status]'`: the domain is verified and DKIM succeeded.
- `aws sesv2 get-account --query '[ProductionAccessEnabled,SendQuota,SuppressionAttributes]'`: out of the sandbox, with quota and suppression settings.
- `aws sesv2 list-configuration-sets`: a configuration set with event destinations exists.
- `dig +short TXT _dmarc.example.com`: a DMARC record is published.
- `aws sesv2 get-suppressed-destination --email-address a@b.com`: the suppression list is in effect.

## Test first
Send against LocalStack or the SES mailbox simulator addresses and assert the failure paths.
```python
def test_bounce_marks_address_undeliverable(handler, db):
    handler({"notificationType": "Bounce", "bounce": {"bounceType": "Permanent",
             "bouncedRecipients": [{"emailAddress": "x@example.com"}]}})
    assert db.get_user("x@example.com").email_status == "bounced"
```

## Do
- Verify the domain, not single addresses, and enable Easy DKIM. Add SPF and a DMARC record starting at `p=none`, then tighten.
- Use a custom MAIL FROM domain so SPF aligns.
- Attach a configuration set with event destinations (SNS, EventBridge or Firehose) for bounce, complaint, delivery and reject events.
- Process bounces and complaints: mark permanent bounces undeliverable and stop mailing complainers. Keep the account suppression list enabled.
- Use SESv2 `SendEmail` with templates for personalization, and keep both HTML and text parts.
- Send through an IAM role limited to `ses:SendEmail` with a `ses:FromAddress` condition.
- Rate-limit and queue sends through SQS to stay under the account's sending rate, and retry only on throttling.
- Include a working unsubscribe link and the `List-Unsubscribe` header for bulk mail.
- Request production access early, describing bounce handling, and watch reputation metrics.

## Avoid
- Sending from the sandbox in production: only verified recipients work. Request production access.
- Ignoring bounces: a high bounce or complaint rate puts the account under review and can pause sending. Wire events first.
- `ses:*` on `*` for the app role: restrict actions, identities and sender address.
- Building raw MIME by hand with user input in headers: header injection. Use the API's structured fields.
- Hardcoding the sandbox mailbox simulator in production code paths: gate it by environment.
- Sending marketing and transactional mail from the same identity: separate them so one cannot taint the other.
- Putting SMTP credentials in the repo: use IAM roles with the API or a secret store.

## Review
- [ ] Domain verified with DKIM, SPF and DMARC.
- [ ] Bounce and complaint events handled and tested.
- [ ] IAM scoped by identity and from-address.
- [ ] Production access granted and quotas known.
- [ ] Unsubscribe path present for bulk mail.

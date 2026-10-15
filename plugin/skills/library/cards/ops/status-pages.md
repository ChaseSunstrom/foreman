---
name: status-pages
title: Status pages
area: ops
tags: [status-page, communication, incidents, transparency, hosting]
detect: []
related: [incident-response, uptime-monitoring, postmortems, dns]
---
A status page tells customers what is broken and when to expect news; host it independently and update it on a fixed cadence.

## Verify
- `dig +short NS status.example.com`: the status domain resolves, and its nameservers differ from the main product's where possible.
- `curl -fsS -o /dev/null -w '%{http_code}\n' https://status.example.com/`: the page is up.
- `curl -s https://status.example.com/ | grep -ci 'operational'`: the page renders the component state.
- `curl -sI https://status.example.com/ | grep -i '^server\|^via'`: infer the hosting path, to confirm it is not served by your own infrastructure.
- `openssl s_client -connect status.example.com:443 -servername status.example.com </dev/null 2>/dev/null | openssl x509 -noout -enddate`: its certificate is valid and renewed.

## Test first
Run a fire drill: publish a test incident to a private or test page and time the whole path.
- Trigger the update procedure from a laptop on a network that cannot reach production.
- Post "Investigating", subscribers receive the notice by email or webhook, then resolve it.
- Fail the drill if the author needs production access, a VPN, or a credential kept only on production systems.
- Record the minutes from decision to published message and aim for under ten.
Repeat when staff or tooling changes.

## Do
- Host the page on separate infrastructure, DNS, and credentials from the product, so the page survives an outage of everything else.
- Show components customers recognize (API, web app, billing, login), each with a state and a short description.
- Wire automated probes to flip components, and keep a manual override for judgment calls.
- Use the standard states in order: Investigating, Identified, Monitoring, Resolved, with a timestamp (and timezone) on every update.
- Update on a stated cadence even when nothing changed, and say when the next update arrives.
- Write plainly: what users see, who is affected, workaround, no internal jargon or blame.
- Offer subscriptions (email, RSS, webhook) and test delivery.
- Link the postmortem after resolution, and keep a visible history.

## Avoid
- Hosting the status page on the same stack it describes: it goes down with the outage. Use a separate provider and domain.
- Waiting for root cause before posting: customers assume you do not know. Post "Investigating" quickly.
- Automated flips only, with no human review: a flapping probe shows false incidents. Add thresholds and an override.
- Leaving incidents open after recovery: trust erodes. Close with a resolved update and the time.
- Vague wording ("some users may experience issues"): add scope, symptom, and workaround.
- One person holding the login: nobody else can post during an incident. Share access and test it.

## Review
- [ ] Page, DNS, and credentials are independent of production.
- [ ] A recent drill published and delivered a test incident in target time.
- [ ] Components map to what customers use, with probes and manual override.
- [ ] A template with cadence and plain wording exists.
- [ ] At least two people can publish, and subscriptions are tested.

---
name: saml
title: SAML SSO
area: security
tags: [security, saml, sso, signature, xml, authentication]
detect: [dep:python3-saml, dep:passport-saml, dep:@node-saml/node-saml, dep:samlify]
related: [xxe, oauth2-oidc, sessions, secure-cookies]
---
SAML service provider: a maintained library, signed assertions only, audience and time checks, replay cache, no XML parsing of your own.

## Verify
- `pytest -q -k saml`: the tampered and unsigned assertion tests pass.
- `git grep -nE "wantAssertionsSigned|wantMessagesSigned|want_assertions_signed|strict" -- ':!*test*'`: signature requirements and strict mode are on.
- `git grep -nEi "etree\.fromstring|DOMParser|parseString" -- ':!*test*'`: no hand-rolled XML parsing of SAML responses.

## Test first
Signature wrapping and unsigned input must fail.
```python
def test_unsigned_assertion_is_rejected(client, idp):
    resp = idp.build_response(email="admin@corp.example", sign=False)
    r = client.post("/saml/acs", data={"SAMLResponse": resp})
    assert r.status_code in (400, 401, 403)
    assert "session" not in r.headers.get("set-cookie", "")

def test_assertion_for_other_audience_is_rejected(client, idp):
    resp = idp.build_response(email="a@corp.example", audience="https://other-sp")
    assert client.post("/saml/acs", data={"SAMLResponse": resp}).status_code == 401
```

## Do
- Use a maintained SAML library in strict mode. Never write signature validation.
- Pin the IdP entity id and certificate from its metadata. Rotate by loading both certs during overlap.
- Require signed assertions (or signed response plus assertion), with `Audience`, `Recipient`, `Destination`, `NotBefore`, `NotOnOrAfter` and `InResponseTo` all checked.
- Cache assertion ids until expiry and reject repeats.
- Keep clock skew tolerance to a minute or two.
- Disable DTDs in the XML parser. Reject documents with more than one assertion or ambiguous signatures.
- Take the user id from the NameID or a stable attribute, and match accounts on that, not on a mutable email alone.
- Validate `RelayState` as a local path before redirecting.
- Support SP-initiated login with a stored request id.

## Avoid
- Verifying that a signature exists rather than that it covers the assertion you read: use the library's validated output only.
- Trusting the `Issuer` or certificate embedded in the message: pin from metadata.
- Using `xml.etree` or regex to read attributes before validation: parse after verification.
- Auto-creating admin roles from any attribute value: map groups through an allow-list.
- Open `RelayState` redirect: restrict to relative paths.
- Accepting IdP-initiated responses with no `InResponseTo` where SP-initiated is possible: record and check request ids.

## Review
- [ ] Strict mode and signature requirements are on and tested.
- [ ] Audience, recipient, destination, time window and replay are checked.
- [ ] IdP certificate and entity id are pinned, with rotation handled.
- [ ] The parser blocks external entities.
- [ ] RelayState is validated and account linking uses a stable id.

---
name: address-validation
title: Address validation
area: domains
tags: [address, validation, postal-code, international, normalization, forms]
detect: []
related: [geocoding, phone-numbers, unicode, gdpr]
---
Address capture: country-driven fields, light format checks, provider verification where deliverability matters, and keeping what the user typed.

## Verify
- `pytest -q tests/test_address.py`: per-country field and postal-code tests pass.
- `pytest -q -k "unicode or international"`: non-ASCII and non-US addresses survive a round trip.
- `grep -rnE "\\\\d\{5\}" src`: US-only ZIP regexes applied to all countries (review each).

## Test first
Do not force US shape on everyone.
```python
from app.address import validate

def test_country_rules_and_unicode_preserved():
    ok = validate({"country": "GB", "line1": "10 Downing St", "city": "London",
                   "postcode": "SW1A 2AA"})
    assert ok.valid
    assert not validate({"country": "US", "line1": "1 Main", "city": "X",
                         "region": "", "postcode": "1234"}).valid   # state and 5-digit zip
    jp = validate({"country": "JP", "line1": "千代田1-1", "city": "千代田区",
                   "postcode": "100-0001", "region": "東京都"})
    assert jp.valid and jp.address["city"] == "千代田区"          # not transliterated
```

## Do
- Choose the country first, then show its fields and order (postcode before city in some, region optional or required per country); drive this from data, such as Google's libaddressinput metadata.
- Validate lightly: required fields per country, postcode pattern, region list where one exists; never reject on name or street shape.
- For shipping, verify deliverability with a provider (USPS-based, Google Address Validation, Loqate and similar) and offer the corrected form as a suggestion the user accepts.
- Store both the user's input and the normalized, verified version, plus verification status and provider.
- Keep fields as separate columns: line1, line2, city, region, postcode, country (ISO 3166-1 alpha-2), and optional geocode.
- Use `autocomplete` attributes (`address-line1`, `postal-code`, `country`) so browsers and password managers fill them.
- Allow long lines, Unicode, apostrophes and hyphens; avoid ASCII-only restrictions.
- Treat addresses as personal data: encrypt at rest where policy requires, and delete on request.

## Avoid
- US-only assumptions (5-digit ZIP, state dropdown required): blocks most of the world. Use per-country rules.
- Rejecting addresses a provider cannot find: new builds and rural routes are real. Warn and allow override.
- Auto-replacing the typed address with the normalized one: wrong corrections ship parcels astray. Ask.
- Single free-text blob: cannot validate, tax or ship. Split fields.
- Trimming or transliterating non-Latin text: you destroy the address. Preserve and add a Latin version if the carrier needs it.
- Regex validation of whole addresses: brittle. Validate parts.

## Review
- [ ] Fields change by country.
- [ ] Original and normalized addresses are both stored.
- [ ] Non-ASCII input round-trips.
- [ ] Verification failures can be overridden by the user.
- [ ] Autocomplete attributes set.

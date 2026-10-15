---
name: phone-numbers
title: Phone numbers
area: domains
tags: [phone, e164, validation, libphonenumber, verification, formatting]
detect: [dep:libphonenumber-js, dep:phonenumbers]
related: [sms, address-validation, unicode, auth-providers]
---
Phone input: parse with a region, store E.164, validate via libphonenumber, format for display, and verify ownership by code.

## Verify
- `pytest -q tests/test_phone.py`: parse, format and verification tests pass.
- `python -c "import phonenumbers as p; n=p.parse('020 7946 0958','GB'); print(p.format_number(n,p.PhoneNumberFormat.E164))"`: national input becomes `+442079460958`.
- `node -e "const {parsePhoneNumberFromString:f}=require('libphonenumber-js');console.log(f('2025550123','US').number)"`: JS side gives `+12025550123`.

## Test first
National formats need a region; the same digits differ by country.
```python
import pytest
from app.phone import normalize

def test_normalizes_to_e164_and_rejects_invalid():
    assert normalize("(202) 555-0123", region="US") == "+12025550123"
    assert normalize("+44 20 7946 0958", region="US") == "+442079460958"  # explicit + wins
    assert normalize("０２０ ７９４６ ０９５８", region="GB") == "+442079460958"  # full-width digits
    with pytest.raises(ValueError):
        normalize("12345", region="US")
```

## Do
- Store E.164 (`+` country code and number, max 15 digits) in one column; keep the user's region or country separately.
- Parse with a default region taken from the selected country, not the server locale; trust a leading `+` over the default.
- Validate with `isValid` (not just length); use `is_possible` for lenient forms. Check the type (mobile, fixed line, VoIP) only when it matters, since type data is not perfect.
- Format for display with the national or international format; use `tel:` links with E.164.
- Use a country selector with a flag and calling code; set `type="tel"` and `autocomplete="tel"`.
- Verify ownership with a one-time code: expiry of minutes, attempt limit, resend cooldown, and rate limits per number and per IP.
- Make the unique constraint on the normalized number when it is an identity.
- Keep the library updated; numbering plans change.

## Avoid
- Regexes for phone validation: they reject real numbers. Use libphonenumber.
- Storing formatted strings (`(202) 555-0123`): duplicates and failed lookups. Store E.164.
- Treating numbers as integers: lose the leading `+` and zeros. Use strings.
- Assuming US numbers: default region from the user's country.
- Unlimited verification sends: SMS pumping fraud and cost. Rate limit and block premium prefixes.
- Reusing numbers as stable identity forever: carriers recycle them. Re-verify on risky actions.

## Review
- [ ] Only E.164 is stored.
- [ ] Parse uses an explicit region.
- [ ] Invalid and possible-but-invalid numbers handled.
- [ ] Verification is expiring and rate limited.
- [ ] Display formatting is separate from storage.

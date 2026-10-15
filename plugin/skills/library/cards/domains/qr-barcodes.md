---
name: qr-barcodes
title: QR codes and barcodes
area: domains
tags: [qr, barcode, scanning, encoding, error-correction, tickets]
detect: [dep:qrcode, dep:jsbarcode, dep:segno]
related: [image-processing, pdf-generation, bookings, webhooks]
---
Generating and scanning QR and 1D barcodes: right symbology, error correction, quiet zone, check digits, and signed payloads.

## Verify
- `pytest -q tests/test_codes.py`: encode, decode round trip and check digit tests pass.
- `zbarimg --quiet --raw out.png`: an independent decoder reads back the exact payload (needs zbar-tools).
- `python -c "import qrcode; print(qrcode.make('x').size)"`: generator imports and renders (needs the qrcode package).

## Test first
EAN-13 check digit and the payload round trip.
```python
from app.codes import ean13_check, make_qr, decode_qr

def test_ean13_check_digit_and_qr_roundtrip():
    assert ean13_check("400638133393") == "1"        # full code 4006381333931
    payload = "TICKET:v1:abc123:sig9f"
    assert decode_qr(make_qr(payload, ec="M")) == payload
    with pytest.raises(ValueError):
        ean13_check("40063813339")                   # wrong length
```

## Do
- Pick the symbology by use: QR for URLs and tickets, Code 128 for internal alphanumerics, EAN-13 and UPC-A for retail (digits only, check digit required), Data Matrix for tiny parts.
- Encode a short opaque token or signed URL, not personal data; resolve it on the server.
- Sign payloads (HMAC) and include a version prefix so you can rotate formats.
- Error correction M or Q for screens and prints; use H only if a logo covers the center, and test scanning.
- Keep the quiet zone (4 modules for QR) and high contrast, dark on light; size at least about 2 cm printed.
- Output SVG for print and scaling, PNG with an integer module scale for screens (no smoothing).
- On scan, validate format, check digit and signature, then look up; make redemption one-time with an atomic update.
- Test with real phone cameras and a handheld scanner, not only a library decoder.

## Avoid
- Long payloads (full JSON): dense codes scan poorly. Use a token and fetch.
- Inverted or low-contrast colors: many scanners fail. Use black on white.
- Scaling a PNG by a non-integer factor: blurred modules. Render SVG or integer scale.
- Skipping the check digit on EAN or UPC: bad scans pass silently.
- Accepting a scanned code as proof without a server lookup: anyone can generate a QR. Verify the signature and state.
- Redeeming tickets with read-then-write: double entry. Use a conditional update.

## Review
- [ ] Symbology matches the use.
- [ ] Payload is short, versioned and signed.
- [ ] Quiet zone and contrast are right.
- [ ] Redemption is atomic and one-time.
- [ ] Scanned in a real device test.

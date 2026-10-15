---
name: image-processing
title: Image processing
area: domains
tags: [images, resize, exif, webp, thumbnails, security]
detect: [dep:sharp, dep:pillow]
related: [file-uploads, video-transcoding, qr-barcodes, unicode]
---
Image pipelines: decode safely, apply EXIF orientation, strip metadata, resize into variants, and encode modern formats.

## Verify
- `pytest -q tests/test_images.py`: orientation, size-cap and format tests pass.
- `python -c "from PIL import Image; im=Image.open('out.webp'); im.verify(); print(im.size, im.format)"`: the output decodes and has expected size and format (needs Pillow).
- `identify -format "%w x %h %m\n" out.webp`: ImageMagick check of the same.

## Test first
A phone photo with orientation 6 must come out upright and without GPS data.
```python
from PIL import Image
from app.images import make_thumb

def test_exif_rotation_applied_and_gps_stripped():
    out = make_thumb("tests/fixtures/rot6_gps.jpg", max_side=200)
    im = Image.open(out)
    assert im.size[1] > im.size[0]               # portrait after rotation
    assert max(im.size) <= 200
    assert not im.getexif().get(0x8825)          # GPS IFD removed
```

## Do
- Cap input bytes and pixel count before decoding; set Pillow `Image.MAX_IMAGE_PIXELS` or sharp `limitInputPixels`.
- Apply orientation first (`ImageOps.exif_transpose`, or sharp `.rotate()` with no args), then resize.
- Re-encode output so uploaded bytes never reach users; strip metadata unless needed, and keep or convert color profile to sRGB.
- Generate fixed variants (thumb, medium, large) with `thumbnail` or `fit: inside`, not stretching; keep aspect ratio.
- Output WebP or AVIF with a JPEG fallback; PNG for transparency and flat graphics.
- Name outputs by content hash for cache-friendly immutable URLs.
- Process in a worker; run untrusted decodes with memory limits.
- Set alt text as data, not derived from the filename.

## Avoid
- Decoding unbounded input: a decompression bomb exhausts memory. Check dimensions from the header first.
- Resizing before orientation: sideways thumbnails. Rotate first.
- Serving the original upload: embedded GPS and polyglot payloads. Always re-encode.
- Converting CMYK or wide-gamut straight to JPEG: washed-out colors. Convert to sRGB.
- JPEG re-encode of transparent PNG: black background. Flatten deliberately or use WebP.
- Trusting the file extension: sniff the decoded format and allowlist it (SVG is a separate, sanitized path).

## Review
- [ ] Size, pixel and format limits enforced before decode.
- [ ] Orientation and metadata handled and tested.
- [ ] Output is re-encoded, never the raw upload.
- [ ] Variants keep aspect ratio.
- [ ] Heavy work runs off the request path.

---
name: pillow
title: Pillow
area: python
tags: [python, pillow, images, imaging, pil, security]
detect: [dep:pillow, dep:Pillow]
related: [opencv, numpy, matplotlib, fastapi]
---
Pillow: open, validate, transform and save images safely, with EXIF handling and bounded decompression.

## Verify
- `python -c "import PIL; print(PIL.__version__)"`: Pillow is installed (the package is `pillow`, the import is `PIL`).
- `python -W error -c "from PIL import Image; Image.new('RGB',(2,2)).save('/dev/null', format='PNG')"`: no deprecation warnings in basic use.
- `pytest -q`: transform tests on small generated images.
- `python -m PIL --report`: build features such as libjpeg, webp and zlib support (needs the installed Pillow to support it).

## Test first
Generate images in memory.
```python
import io
import pytest
from PIL import Image
from app.thumbs import make_thumbnail

def test_thumbnail_bounds_and_format():
    src = io.BytesIO()
    Image.new("RGB", (4000, 2000), "red").save(src, "PNG")
    out = make_thumbnail(src.getvalue(), max_side=256)
    img = Image.open(io.BytesIO(out))
    assert max(img.size) == 256 and img.format == "JPEG"

def test_rejects_non_image():
    with pytest.raises(ValueError):
        make_thumbnail(b"not an image", max_side=64)
```

## Do
- Open with a context manager: `with Image.open(path) as im:`. Call `im.load()` if you need pixels after the block.
- Validate untrusted uploads: `Image.open(f)`, `im.verify()` (then reopen to use it), check `im.format` against an allow-list and `im.size` against limits.
- Keep `Image.MAX_IMAGE_PIXELS` at the default or set a deliberate limit, so decompression bombs raise `DecompressionBombError`.
- Fix phone photos with `ImageOps.exif_transpose(im)` and strip metadata by saving a fresh image without `exif=`.
- Use `im.thumbnail((w, h))` (in place, keeps aspect) and `Image.Resampling.LANCZOS` for quality.
- Convert before saving JPEG: `im.convert("RGB")` for RGBA or P modes.
- Save with options: `im.save(buf, "JPEG", quality=85, optimize=True)` or `"WEBP"`.
- For NumPy: `np.asarray(im)` and `Image.fromarray(arr)` with `uint8`.

## Avoid
- Trusting the file extension or client content type: use `im.format`. Never use user filenames as paths.
- Disabling `MAX_IMAGE_PIXELS` (`= None`) for uploads: memory exhaustion by crafted files.
- `Image.ANTIALIAS` and other removed constants: use `Image.Resampling.LANCZOS`.
- Saving RGBA as JPEG: `OSError: cannot write mode RGBA as JPEG`. Convert first.
- Leaving files open (no `with`): file handle leaks and locked files on Windows.
- Serving user images with preserved EXIF GPS data: privacy leak. Strip metadata.
- Using `Image.open` on the request thread for large files in async servers: blocks. Offload to a thread.

## Review
- [ ] Uploads are verified, size limited and format allow-listed.
- [ ] Orientation is applied and metadata is stripped on output.
- [ ] Mode conversion precedes JPEG saves.
- [ ] Handles close and no removed constants are used.

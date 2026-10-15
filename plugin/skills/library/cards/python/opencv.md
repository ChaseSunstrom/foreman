---
name: opencv
title: OpenCV (Python)
area: python
tags: [python, opencv, computer-vision, images, video, numpy]
detect: [dep:opencv-python, dep:opencv-python-headless, dep:opencv-contrib-python]
related: [numpy, pillow, pytest, matplotlib]
---
OpenCV in Python: NumPy-backed BGR images, explicit colour conversions, checked I/O and released video handles.

## Verify
- `python -c "import cv2; print(cv2.__version__)"`: the wheel imports (a missing `libGL` means you need the headless wheel).
- `pytest -q`: image-function tests on small synthetic arrays.
- `python -c "import cv2; print(cv2.getBuildInformation())"`: codecs and backends (FFmpeg, GStreamer) the build has.
- `pip list | grep -i opencv`: exactly one opencv wheel is installed.

## Test first
Test on generated arrays so no files are needed.
```python
import numpy as np
import pytest
from app.vision import to_gray_resized

def test_resize_keeps_aspect_and_gray():
    img = np.zeros((100, 200, 3), dtype=np.uint8)
    out = to_gray_resized(img, width=100)
    assert out.shape == (50, 100) and out.dtype == np.uint8

def test_rejects_none():
    with pytest.raises(ValueError):
        to_gray_resized(None, width=10)
```

## Do
- Check `cv2.imread(path)` for `None` and raise a clear error. It returns `None` instead of raising on a bad path.
- Remember OpenCV images are BGR: convert with `cv2.cvtColor(img, cv2.COLOR_BGR2RGB)` before passing to Pillow, matplotlib or models expecting RGB.
- Shape is `(height, width, channels)`, but `cv2.resize` takes `(width, height)`.
- Choose interpolation: `cv2.INTER_AREA` to shrink, `INTER_LINEAR` or `INTER_CUBIC` to enlarge.
- Release resources: `cap = cv2.VideoCapture(src)`, check `cap.isOpened()` and `ret` from `cap.read()`, then `cap.release()` in `finally`.
- Use `cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)` for in-memory bytes.
- Use `opencv-python-headless` in servers and containers, and only one OpenCV wheel per environment.
- Keep dtype in mind: `uint8` wraps on overflow, so use `cv2.add`, `cv2.addWeighted` or cast to float.
- Write with `cv2.imwrite(path, img)` and check its boolean return.

## Avoid
- Installing both `opencv-python` and `opencv-contrib-python` (or the headless variants): conflicting `cv2` modules. Keep one.
- Using `cv2.imshow` and `waitKey` on servers or in tests: fails headless. Save images instead.
- Assuming `imread` loads RGB or keeps alpha: default drops alpha and is BGR. Pass `cv2.IMREAD_UNCHANGED` for alpha.
- Looping over pixels in Python: very slow. Use vectorised NumPy or OpenCV functions.
- Not checking `ret` in video loops: the loop crashes with `None` frames at the end of file.
- Passing a non-contiguous array (a transposed slice) to OpenCV: errors or silent copies. Use `np.ascontiguousarray`.

## Review
- [ ] Every read is checked for `None` or failure, and every capture is released.
- [ ] Colour order and size tuple order are right at each boundary.
- [ ] A single OpenCV wheel, headless on servers.
- [ ] No Python pixel loops on hot paths.

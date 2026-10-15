---
name: yolo
title: YOLO object detection
area: ml
tags: [yolo, object-detection, computer-vision, ultralytics, annotation, export]
detect: [dep:ultralytics, dep:yolov5]
related: [pytorch, onnx, tensorrt, data-labeling, quantization]
---
Train and deploy YOLO detectors: clean YOLO-format labels, held-out validation, mAP tracking and exported inference checked against the source model.

## Verify
- `yolo val model=best.pt data=data.yaml`: mAP, precision and recall on the validation split.
- `pytest -q tests/test_labels.py`: label files parse, classes are in range and boxes are normalised.
- `yolo export model=best.pt format=onnx`: export succeeds; then compare outputs against the PyTorch model on sample images.

## Test first
Validate the dataset before training.
```python
from pathlib import Path

def test_labels_are_normalized_and_classes_valid():
    for f in Path("data/labels/train").glob("*.txt"):
        for line in f.read_text().splitlines():
            c, x, y, w, h = line.split()
            assert 0 <= int(c) < 3
            assert all(0 <= float(v) <= 1 for v in (x, y, w, h))
```

## Do
- Use the layout `images/{train,val,test}` with matching `labels/` and a `data.yaml` listing `path`, splits and `names`.
- Split by source (video, scene, site), not by frame, so val is independent of train.
- Start from pretrained weights; set `imgsz`, `epochs` and `batch` explicitly; fix `seed`.
- Track mAP50-95 per class and the confusion matrix, not only overall mAP.
- Tune confidence and NMS IoU thresholds on val and keep them in config.
- Export (ONNX, TensorRT) with the same `imgsz` and compare detections with the source weights on a fixed image set.
- Review mislabeled and missed examples from the val predictions; fix labels, then retrain.
- Check the licence of the framework and weights for commercial use.

## Avoid
- Random frame splits from the same video: near-duplicates leak into val and inflate mAP. Split by sequence.
- Pixel-coordinate labels: YOLO labels are normalised centre-x, centre-y, width, height.
- Reporting only mAP50: hides localisation quality. Include mAP50-95.
- Different preprocessing at deploy than in training (letterbox, colour order): accuracy drops. Reuse the library's pipeline.
- Tuning thresholds on the test set: hold it out.
- Never viewing the labels: errors cap quality. Visualise a sample.

## Review
- [ ] Splits independent by source.
- [ ] Labels validated automatically.
- [ ] Per-class metrics recorded.
- [ ] Exported model matches the source on a fixed set.
- [ ] Licence checked.

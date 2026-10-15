---
name: video-transcoding
title: Video transcoding
area: domains
tags: [video, ffmpeg, transcoding, hls, queues, thumbnails]
detect: [dep:fluent-ffmpeg, dep:ffmpeg-python]
related: [file-uploads, image-processing, cron-jobs, webhooks]
---
Video pipelines: probe, transcode to an HLS or MP4 ladder in a worker queue, thumbnails, and safe handling of untrusted input.

## Verify
- `ffprobe -v error -show_entries stream=codec_name,width,height -of csv=p=0 out.mp4`: output codec and dimensions are what you intended.
- `ffmpeg -v error -i out.mp4 -f null -`: the output decodes end to end with no errors.
- `pytest -q tests/test_transcode.py`: job state, idempotency and argument-building tests pass.

## Test first
Argument building is where injection and rotation bugs hide; test it without running ffmpeg.
```python
from app.transcode import build_args

def test_args_are_a_list_and_cap_dimensions_even():
    args = build_args("/in/a b;rm -rf.mov", "/out/o.mp4", max_h=720)
    assert isinstance(args, list)
    assert "/in/a b;rm -rf.mov" in args       # one argv entry, never shell-joined
    assert any("scale=-2:720" in a for a in args)   # -2 keeps width even
    assert "-movflags" in args and "+faststart" in args
```

## Do
- Accept uploads direct to object storage; enqueue a job keyed by asset id and a hash of the settings so retries are idempotent.
- Probe first with `ffprobe` (JSON output) to reject bad duration, codec or size before spending CPU.
- Run ffmpeg via an argv list, never a shell string; set a timeout and resource limits; run in an isolated worker.
- Produce a ladder (for example 1080, 720, 480) with H.264 plus AAC for compatibility; use `-movflags +faststart` for MP4, segmented output with a playlist for HLS.
- Honor rotation metadata and keep aspect ratio with even dimensions (`scale=-2:H`).
- Parse `-progress pipe:1` output for job progress.
- Generate poster frames with `-ss` and `-frames:v 1`.
- Store state: queued, processing, ready, failed with the ffmpeg error tail; make retries bounded.
- Use signed, expiring URLs for playback of private media.

## Avoid
- Interpolating filenames into a shell command: injection. Use an argv list.
- Transcoding in the web request: timeouts and lost work. Use a queue.
- Odd widths with libx264 (`scale=-1:H`): encoder error. Use `-2`.
- Trusting the extension or MIME type: probe the streams.
- Keeping partial outputs after failure: write to a temp key and rename on success.
- Reprocessing on every duplicate webhook: dedupe on asset id.

## Review
- [ ] Input is probed and size and duration limited.
- [ ] No shell strings; timeouts set.
- [ ] Outputs verified decodable before marked ready.
- [ ] Job is idempotent and retries are bounded.
- [ ] Private playback uses expiring URLs.

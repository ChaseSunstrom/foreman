---
name: whisper
title: Whisper speech-to-text
area: ml
tags: [whisper, asr, audio, transcription, speech, timestamps]
detect: [dep:openai-whisper, dep:faster-whisper, dep:whisperx]
related: [transformers, pytorch, cuda, onnx]
---
Transcribe audio with Whisper or faster-whisper: resample correctly, chunk long files, and measure word error rate on your audio.

## Verify
- `ffprobe -hide_banner input.wav`: sample rate, channels and duration of the input.
- `pytest -q tests/test_asr.py`: transcripts on short fixtures match expected text after normalisation.
- `python -m evals.wer --set data/asr_dev`: word error rate on a labelled sample from your domain.

## Test first
```python
from app.asr import transcribe, normalize

def test_silence_yields_empty_text():
    out = transcribe("tests/data/silence_5s.wav")
    assert normalize(out.text) == ""
```

## Do
- Feed 16 kHz mono audio; convert with `ffmpeg -i in.mp3 -ar 16000 -ac 1 out.wav` when the library does not.
- Pick model size by measured WER and latency; load the model once per process, not per request.
- Use `faster-whisper` with `compute_type` matched to hardware (float16 on GPU, int8 on CPU) for speed.
- Set `language` when known to skip detection errors; keep `task` as transcribe unless translating.
- Use VAD filtering to skip silence, and pass previous text as the initial prompt only for vocabulary hints.
- For long audio, split on silence with small overlap and stitch by timestamps; request word timestamps only when needed.
- Normalise text (case, punctuation, numbers) before computing WER, with the same normaliser for reference and hypothesis.
- Run diarisation separately and align by timestamps.

## Avoid
- Reloading the model per file: seconds of overhead each time. Keep a singleton.
- Passing 44.1 kHz stereo into a path that assumes 16 kHz: garbled output. Resample explicitly.
- Trusting output on silence or music: hallucinated phrases appear. Use VAD and drop segments with low confidence or high no-speech probability.
- Looping repeated text on long audio: segment the audio and disable conditioning on previous text if it loops.
- WER from unnormalised text: inflated. Normalise both sides.
- Sending sensitive audio to a hosted API without approval: process locally if required.

## Review
- [ ] Audio converted to the expected format.
- [ ] Model loaded once; device and compute type explicit.
- [ ] Silence and long-file behaviour tested.
- [ ] WER measured on in-domain data with a fixed normaliser.
- [ ] Timestamps validated against known clips.

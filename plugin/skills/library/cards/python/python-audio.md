---
name: python-audio
title: Python audio (librosa, soundfile, demucs)
area: python
tags: [python, audio, librosa, soundfile, demucs, dsp, source-separation]
detect: [dep:librosa, dep:soundfile, dep:demucs]
related: [numpy, scipy, pytest, jupyter]
---
Audio in Python: librosa for loading, resampling and features, soundfile for reading and writing, demucs for source separation.

## Verify
- `python -c "import librosa, soundfile; print(librosa.__version__, soundfile.__libsndfile_version__)"`: both import and libsndfile is present.
- `python -c "import soundfile as sf; print(sf.info('in.wav'))"`: sample rate, channels, frames and format of a file.
- `python -m demucs --help`: the separation CLI is installed and lists its options.
- `pytest -q`: tests on short generated signals, not large fixtures.

## Test first
Generate a synthetic tone, run the code, and assert on sample rate, length and a known property.
```python
import numpy as np
import soundfile as sf
from app.audio import load_mono

def test_load_mono_resamples(tmp_path):
    sr = 44100
    t = np.arange(sr) / sr
    sf.write(tmp_path / "a.wav", np.sin(2 * np.pi * 440 * t), sr)
    y, out_sr = load_mono(tmp_path / "a.wav", target_sr=22050)
    assert out_sr == 22050
    assert abs(len(y) - 22050) <= 1
```

## Do
- Load with `y, sr = librosa.load(path, sr=None)` to keep the native rate, or `sr=22050` to resample; it returns mono float32 by default (`mono=True`).
- Resample explicitly with `librosa.resample(y, orig_sr=..., target_sr=...)`; pass the rates as keywords.
- Read and write with `sf.read(path)` and `sf.write(path, data, samplerate)`; pick the format by extension or the `subtype` argument.
- Keep the sample rate next to the array everywhere; pass them together.
- Run separation with `python -m demucs path/to/track.wav` and read the stems from its output folder.
- Process long files in chunks or via the CLI rather than loading hours of audio into memory.
- Normalize or clip float audio to [-1, 1] before writing to an integer format.

## Avoid
- Positional `orig_sr` and `target_sr` in librosa functions: recent versions require keywords. Name them.
- Assuming `sf.read` returns (samples,): multichannel is (frames, channels). Check `ndim`.
- Mixing sample rates between features and audio: wrong times. Carry `sr` and convert frames with `librosa.frames_to_time(..., sr=sr)`.
- Writing float data above 1.0 to PCM: clipping distortion. Scale first.
- Comparing audio arrays with `==`: use `np.allclose` or a metric, since resampling is approximate.
- Running demucs on a CPU-only host for a long track without expecting minutes of runtime: test on a short clip.

## Review
- [ ] Sample rate is explicit at every load, resample and write.
- [ ] Channel layout (mono versus frames x channels) is handled deliberately.
- [ ] Output audio is within range for its format.
- [ ] Tests use short synthetic signals and run quickly.
- [ ] Separation output paths are read from the tool, not guessed.

**Verdict:** approve with nits. No HIGH findings. I read the diff and the dispatcher code only. I did not run anything, so the timing, memory and test results below are reasoned, not measured.

## lens: adversary
- MEDIUM — plugin/lib/fmimg.py:89,91,166 — Chunk-type bytes are echoed raw to stderr. A chunk type of `\x1b[2J` with a valid CRC passes the CRC check and then hits "unknown critical chunk". A bad CRC on any such chunk, including the first one in `fm img info`, also echoes it. The terminal receives the escape sequence. — Print `kind.hex()` or `repr(kind)`. — CONFIRMED
- LOW — plugin/lib/fmimg.py:233 — `open()` on a FIFO with no writer blocks before the `S_ISREG` check runs, so `fm img info fifo` hangs. — Use `os.open(path, os.O_RDONLY | os.O_NONBLOCK)`, then fstat, then wrap in `os.fdopen`. — CONFIRMED
- LOW — plugin/lib/fmimg.py:270 — `chmod 0o644` ignores umask. The diff image is a faded copy of a possibly private screenshot and ends up world-readable. — Drop the chmod (mkstemp gives 0600) or apply the umask. — CONFIRMED
- LOW — plugin/lib/fmimg.py:188 — A palette index past PLTE reads as opaque black, so a corrupt image can compare equal to a real black one. — Refuse it with `if px and max(px) >= len(plte)//3: raise ValueError("palette index past PLTE")`. I would refuse: the PNG spec calls it an error, and a diff tool should not hide corruption. — CONFIRMED

## lens: maintainer
- MEDIUM — plugin/tests/test_raster.py:470-475 — The bomb test passes without the cap. Without `max_length`, `decompress` returns 64 MB, `_unfilter` reads only the first `h` rows, and the pixels are the same `bytes(4)`. The test cannot fail if the cap is removed. — Wrap `fmimg.zlib.decompressobj` to record the returned length, or assert a `tracemalloc` peak under 8 MB. — CONFIRMED
- LOW — plugin/tests/test_raster.py:461 — The "too large" case only hits the side limit. `w*h > MAX_PIXELS` (for example 32768x32768), a zero width, an IDAT split across chunks and an out-of-range palette index are all untested. — Add those four cases. — CONFIRMED
- LOW — plugin/lib/fmimg.py:277,298,335-337 — With `--out`, the diff walks every changed pixel twice, once in `diff` and once in `diff_image`. It also recomputes `kind+body` for the CRC. — Fuse the two walks, and use `zlib.crc32(body, zlib.crc32(kind))`. — PLAUSIBLE
- LOW — plugin/lib/fmimg.py:336 — With `--out`, if the sizes differ the function returns before writing and says nothing. A stale file at that path would then look current. — Print "no diff image written". — CONFIRMED

## lens: edge
- LOW — plugin/lib/fmimg.py:62-63 — Worst case for one image at the cap is about 27 s (0.8 s/MP, builder's figure) and roughly 500 MB, since the image is held as raw, unfiltered and RGBA copies. A diff loads two. — Keep the cap and note the cost in the docstring. — PLAUSIBLE
- LOW — plugin/lib/fmimg.py:102-105 — A depth-16 palette image gets the "16-bit PNGs aren't read" message instead of a bad-IHDR message. — Use the depth set `(1,2,4,8)` for colour type 3 and `(8,16)` otherwise. — CONFIRMED

## Judgements
- **Size limits and inflate:** the size is checked in `_header` before any IDAT is read. Inflate is capped by `max_length=need`. Chunk length overflow is safe: a length near 2^32 fails the `end > len` check as "truncated". IDAT split across chunks is joined correctly. The CRC covers every chunk, ancillary ones included.
- **The 33.5 MP cap:** sensible. It fits 8K and a 1440x20000 full-page shot, and typical shots are 2–8 MP (about 2–7 s). The risk is time, not the cap.
- **`--out` safety:** safe. `os.replace` swaps the directory entry, so an input inode is never written. `samefile` refuses an input or a hardlink to one, and a symlink is replaced, not followed.
- **Exit codes:** 0 same, 1 differ (including a size mismatch), 2 error. This matches the help text.
- **`diff()` for T-1637:** yes, change it now. Add `tol=0` as a per-channel maximum difference, and count two pixels with alpha 0 as equal whatever their RGB. Exact RGBA comparison will report anti-aliasing noise and invisible RGB as changes.
- **WORKER_SUBREADS:** yes. A worker is refused today, since `img` is in neither set. Add `"img": ("out", {None})` to `WORKER_SUBREADS`, as `timeline` does. It allows `info` and `diff` without `--out`, and blocks the write.

## Acceptance criteria
- Round trip keeps pixels and diff reports the count: met by reading (`test_round_trip_keeps_the_pixels`, `test_diff_counts_changed_pixels_and_their_box`, `test_fm_img_info_and_diff`). I did not run the command.

## Implicit decisions
- Strict CRC on all chunks. Unknown critical chunks are refused.
- ICC and gamma chunks are ignored.
- Trailing zlib data and the adler32 checksum are unchecked.
- A palette index past the palette reads as black.
- A size mismatch exits 1, not 2.
- `--out -` writes a file named `-`.
- Exact RGBA equality in `diff()`.

## Not checked
I did not run the tests or measure speed or memory. I did not look at the Pillow cross-check or at doc-drift tests.

**Noticed:** none

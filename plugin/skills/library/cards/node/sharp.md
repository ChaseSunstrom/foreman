---
name: sharp
title: sharp
area: node
tags: [sharp, images, resize, webp, avif, libvips]
detect: [dep:sharp]
related: [node-streams, node, vitest, worker-threads]
---
sharp image processing: pipeline resizes with limits, correct orientation and formats, streaming and platform-aware installs.

## Verify
- `node -e "console.log(require('sharp').versions)"`: native libvips loaded on this platform.
- `npx tsc --noEmit`: options types compile.
- `npx vitest run`: tests assert output metadata (format, width, height), not just no-throw.
- `npm ls sharp`: one version; multiple copies each bundle a binary.

## Test first
Generate the input in the test and assert metadata.
```ts
import sharp from 'sharp';
import { makeThumb } from '../src/thumb';

test('thumbnail is webp, within 200px, and upright', async () => {
  const src = await sharp({ create: { width: 800, height: 400, channels: 3, background: '#f00' } })
    .jpeg().toBuffer();
  const out = await makeThumb(src);
  const m = await sharp(out).metadata();
  expect(m.format).toBe('webp');
  expect(Math.max(m.width!, m.height!)).toBeLessThanOrEqual(200);
});
```

## Do
- Chain one pipeline: `sharp(input).rotate().resize({ width, height, fit: 'inside', withoutEnlargement: true }).webp({ quality: 80 }).toBuffer()`.
- Call `.rotate()` with no args to apply EXIF orientation before stripping metadata.
- Set `limitInputPixels` (default is about 268 megapixels) lower for user uploads, and cap upload bytes.
- Choose `fit` on purpose: `cover` crops, `contain` pads, `inside` preserves aspect.
- Metadata is removed by default; call `.withMetadata()` only when needed, and strip location data from user uploads.
- Stream large files: `readStream.pipe(sharp().resize(...)).pipe(writeStream)` and handle `error`.
- Detect the real type with `metadata().format`, not the filename or content-type header.
- Tune `sharp.concurrency()` and `sharp.cache(false)` for servers with tight memory.

## Avoid
- Same input and output path: sharp errors. Write to a temp file and rename.
- Skipping `.rotate()`: phone photos come out sideways.
- Trusting upload mime types: validate by decoding with `metadata()` inside try/catch.
- `failOn: 'none'` on untrusted input: corrupt images are processed. Keep the stricter default.
- Installing with `--ignore-scripts` or copying `node_modules` across OS or CPU: the platform binary is missing. Install on the target platform.
- Upscaling by default: set `withoutEnlargement`.
- Many parallel conversions without a limit: memory spikes. Use a queue.

## Review
- [ ] Input size, pixel and format limits are enforced for untrusted images.
- [ ] Orientation and metadata handling is intentional.
- [ ] Output format and quality verified by tests.
- [ ] Deployment installs the matching native binary.
- [ ] Concurrency is bounded.

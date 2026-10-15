---
name: file-drop
title: File drop and upload
area: frontend
tags: [upload, drag-drop, files, a11y, validation]
detect: [dep:react-dropzone]
related: [drag-and-drop, forms, optimistic-ui, web-workers]
---
Drop zones that are also real file inputs: validated, progress-reporting, cancellable and keyboard accessible.

## Verify
- `npx playwright test`: `setInputFiles` on the input and a synthesized drop both upload.
- `npx tsc --noEmit`: accepted types and handlers.
- `npx vitest run`: validators for size, type and count.

## Test first
```ts
import { test, expect } from '@playwright/test';

test('rejects an oversized file with a message', async ({ page }) => {
  await page.goto('/upload');
  await page.getByLabel('Upload files').setInputFiles({
    name: 'big.png', mimeType: 'image/png', buffer: Buffer.alloc(6 * 1024 * 1024),
  });
  await expect(page.getByRole('alert')).toContainText('big.png is larger than 5 MB');
  await expect(page.getByRole('listitem', { name: /big.png/ })).toHaveCount(0);
});
```

## Do
- Back the zone with `<input type="file" multiple accept="image/*">` and a visible label or button; the zone is an enhancement.
- On `dragover` call `preventDefault()` and set `dropEffect`; on `drop` also `preventDefault()` or the browser navigates to the file.
- Read files from `event.dataTransfer.files` (or `items` for directories with `webkitGetAsEntry`).
- Validate on the client for UX (type by extension and MIME, size, count) and again on the server for security; never trust `file.type`.
- Show a list of selected files with name, size, per-file progress (`<progress>`), a remove button and a retry.
- Upload with `XMLHttpRequest` `upload.onprogress` or a resumable approach; use `AbortController` for cancel where `fetch` is used.
- Announce additions, rejections and completion in a live region; style a drag-over state with more than color.
- Revoke preview URLs (`URL.revokeObjectURL`) on removal and unmount.

## Avoid
- A drop zone with no input fallback: keyboard and mobile users cannot upload. Include a real input.
- Forgetting `preventDefault()` on `dragover`: drop never fires. Call it on both events.
- Relying on `accept` or `file.type` for security: users can spoof. Check content on the server.
- Reading a huge file into memory with `FileReader` for a preview: freezes the tab. Use `URL.createObjectURL` and stream uploads.
- Flicker from `dragleave` firing on child elements: track depth or use `pointer-events: none` on children.
- Silent rejections: tell the user which file failed and why.

## Review
- [ ] The zone works by drop, click and keyboard.
- [ ] Client validation exists and the server re-validates.
- [ ] Progress, cancel and retry are present per file.
- [ ] Object URLs are revoked.
- [ ] Errors and results are announced.

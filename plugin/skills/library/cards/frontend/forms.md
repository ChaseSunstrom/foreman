---
name: forms
title: Web Forms
area: frontend
tags: [forms, validation, html, input, autofill, ux]
detect: [dep:react-hook-form, dep:formik, dep:zod, dep:yup, dep:@tanstack/react-form, dep:vee-validate, dep:@conform-to/react]
related: [accessibility, i18n, browser-storage, file-uploads]
---
Forms built on native HTML controls, validated on the client for speed and on the server for truth, with accessible errors.

## Verify
- `npx playwright test forms`: fills and submits through real inputs, including error paths.
- `npx tsc --noEmit`: schema-derived form types agree with the handlers.
- `npx axe http://localhost:3000/signup`: labels, error associations and contrast (needs @axe-core/cli).
- `curl -s -X POST localhost:3000/api/signup -d '{}' -H 'content-type: application/json'`: server rejects invalid input on its own.

## Test first
One schema shared by client and server; test the schema, then the UI.
```ts
import { z } from 'zod';
import { expect, test } from 'vitest';
import { signup } from './schema';

test('rejects bad email and short password', () => {
  const r = signup.safeParse({ email: 'x', password: '123' });
  expect(r.success).toBe(false);
  expect(r.error!.flatten().fieldErrors).toHaveProperty('email');
  expect(r.error!.flatten().fieldErrors).toHaveProperty('password');
});
```

## Do
- Use correct `type` (`email`, `tel`, `url`, `number`, `date`) and `inputmode`; they bring the right mobile keyboard.
- Set `autocomplete` tokens (`email`, `current-password`, `new-password`, `one-time-code`, `given-name`, `postal-code`).
- Pair each input with a `<label for>`; link hints and errors with `aria-describedby`; set `aria-invalid` on failure.
- Validate on blur, then on change after first error; show a summary and focus the first invalid field on submit.
- Re-validate on the server and return per-field errors in a consistent shape.
- Disable the submit button only during the request, to prevent double submit; keep it enabled otherwise.
- Preserve input on error; never clear the password-manager fields.
- Use `name` attributes and a real `<form>` with `method` so Enter submits and progressive enhancement works.

## Avoid
- Validation only in the browser: trivially bypassed. Duplicate it on the server.
- `type="number"` for IDs, phone or card numbers: strips zeros, shows spinners. Use `inputmode="numeric"` with `type="text"`.
- Placeholder as label: disappears and fails contrast. Add a visible label.
- Disabling paste on password fields: breaks password managers. Remove it.
- `autocomplete="off"` everywhere: browsers ignore it for passwords and users lose help. Use the right tokens.
- Controlled inputs re-rendering the whole form each keystroke: use uncontrolled or per-field subscriptions (react-hook-form `register`).
- Regex email validation beyond a sanity check: reject real addresses. Use `type="email"` and confirm by mail.

## Review
- [ ] Every field has a label, autocomplete token and appropriate input type.
- [ ] Errors are text, tied to fields, announced, and the first one receives focus.
- [ ] Server validates independently and returns structured errors.
- [ ] Double submit and network failure are handled; user input survives errors.
- [ ] Works with keyboard, password manager and a screen reader.

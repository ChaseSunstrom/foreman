---
name: i18next
title: i18next
area: node
tags: [i18next, i18n, localization, translation, plurals, react]
detect: [dep:i18next, dep:react-i18next, dep:next-i18next, dep:i18next-http-backend]
related: [date-fns, zod, vitest, jest]
---
i18next localization: namespaced typed keys, ICU-style plurals via suffixes, fallback languages, and a test that catches missing keys.

## Verify
- `npx tsc --noEmit`: typed `t()` keys match resources (needs a `CustomTypeOptions` declaration).
- `npx i18next-parser`: extracts keys from source into catalogs when configured (check the diff for missing keys).
- `node -e "for(const f of ['en','de'])console.log(f,Object.keys(require('./locales/'+f+'/common.json')).length)"`: key counts match across languages.
- `npx vitest run`: tests initialise i18n with `lng` set and `saveMissing` flagging.

## Test first
Fail on any missing key, and check plural forms.
```ts
import i18n from 'i18next';
import en from '../locales/en/common.json';

test('plural forms resolve and missing keys are reported', async () => {
  const missing: string[] = [];
  await i18n.init({ lng: 'en', resources: { en: { common: en } }, defaultNS: 'common',
    saveMissing: true, missingKeyHandler: (_l, _n, k) => missing.push(k) });
  expect(i18n.t('items', { count: 1 })).toBe('1 item');
  expect(i18n.t('items', { count: 3 })).toBe('3 items');
  expect(missing).toEqual([]);
});
```

## Do
- Init once: `i18n.use(initReactI18next).init({ lng, fallbackLng: 'en', ns, defaultNS, interpolation: { escapeValue: false } })` (React escapes already).
- Name plural keys with CLDR suffixes: `items_one`, `items_other` (v21+ JSON v4 format) and call `t('items', { count })`.
- Pass values by interpolation (`{{name}}`), never by string concatenation.
- Split namespaces by feature and lazy-load them; `useTranslation('ns')` loads on demand.
- Use `Intl`-backed formatting: `{{val, number}}`, `{{val, datetime}}`, and `Intl.PluralRules` through built-in plural handling.
- Detect language with `i18next-browser-languagedetector` (browser) or a request header (server), and create a per-request instance on servers via `i18n.cloneInstance()`.
- Provide `context` and `returnObjects` only deliberately.
- Keep translation files flat or consistently nested, one source language as truth.

## Avoid
- Sharing one global instance across server requests: language leaks between users. Clone per request.
- Concatenating translated fragments: word order differs by language. Use one full sentence with placeholders.
- Old plural keys `_plural` in a new setup: mixed formats yield wrong forms. Use `_one`/`_other`.
- `escapeValue: false` when not rendering through React or another escaping layer: XSS through interpolated values.
- Missing `fallbackLng`: raw keys show to users. Set a fallback and log missing keys in dev.
- Calling `t` before `init` resolves: wait on the init promise or `ready`.

## Review
- [ ] All locales have the same keys and plural forms.
- [ ] Types for keys are wired up and `tsc` passes.
- [ ] Server code isolates language per request.
- [ ] Dates and numbers format via Intl, not string building.
- [ ] Missing keys fail tests or are logged.

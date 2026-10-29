---
name: ux-writing
title: UX Writing
area: ux
tags: [microcopy, content-design, voice, labels, product-design]
detect: []
related: [error-messages, empty-states, i18n, forms]
---
Interface text that is short, specific and consistent: verbs on buttons, one term per concept, no jargon.

## Verify
- `grep -rnE ">(Submit|OK|Click here|Yes|No)<" src`: finds vague labels to replace with the real action.
- `grep -rn "Please" src | wc -l`: count politeness filler; most can go.
- Extract strings (`npx i18next-parser`) and read them in one list for tone and term drift.
- A readability pass on help text: aim for grade 8 or below (`npx alex README.md` flags insensitive wording too).

## Test first
Lock the vocabulary so a rename cannot drift.
```ts
import { test, expect } from '@playwright/test';

test('destructive button names the object', async ({ page }) => {
  await page.goto('/projects/42/settings');
  await expect(page.getByRole('button', { name: 'Delete project' })).toBeVisible();
  await expect(page.getByRole('button', { name: /^(ok|submit|yes)$/i })).toHaveCount(0);
});
```

## Do
- Start buttons and links with a verb plus object: "Save changes", "Invite teammate".
- Pick one term per concept (project, not workspace/board/space) and keep a glossary file.
- Put the important word first; front-load labels and headings for scanning.
- Use sentence case, active voice and the second person; contractions are fine.
- Keep tooltips under about 80 characters and buttons to 1-3 words.
- Write numbers, dates and plurals through the i18n layer (`{count, plural, one {# item} other {# items}}`).
- Write error and empty text with the same voice as the rest; see the sibling cards.

## Avoid
- "Click here", "Learn more" with no object, and "Submit" as a label.
- Humor in error and payment text; it reads as dismissive when the user is stressed.
- ALL CAPS strings (hard to read, read letter by letter by some screen readers).
- Concatenating translated fragments; word order differs by language.
- Internal jargon, codes and abbreviations in user-facing text.

## Review
- [ ] Every button says what it does; no bare "OK" or "Submit".
- [ ] One term per concept across screens, emails and docs.
- [ ] Strings are externalised and pluralised through the i18n layer.
- [ ] Text fits at 200% zoom and in longer languages (+30%).

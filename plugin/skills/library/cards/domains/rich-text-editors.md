---
name: rich-text-editors
title: Rich text editors
area: domains
tags: [editor, prosemirror, tiptap, contenteditable, schema, accessibility]
detect: [dep:@tiptap/core, dep:prosemirror-model, dep:quill, dep:lexical]
related: [html-sanitization, markdown-rendering, collaborative-editing, unicode]
---
Embedding a WYSIWYG editor: a structured document model as the stored form, schema-limited content, safe paste, and IME and RTL correctness.

## Verify
- `npx vitest run editor`: schema, serialization and paste tests pass.
- `npx tsc --noEmit`: editor extensions and node types type-check.
- `npx playwright test editor`: typing, toolbar and keyboard paths work in a real browser (if configured).

## Test first
Pasted markup must be reduced to the schema, and the JSON must round-trip.
```ts
import { parseHTML, toJSON, fromJSON } from "./editor-schema";

test("paste is filtered to schema and JSON round-trips", () => {
  const doc = parseHTML('<p>hi <b onclick="x()">there</b><script>alert(1)</script></p><img src=x onerror=y>');
  const out = JSON.stringify(toJSON(doc));
  expect(out).not.toMatch(/script|onclick|onerror|img/);
  expect(out).toContain("bold");
  expect(toJSON(fromJSON(toJSON(doc)))).toEqual(toJSON(doc));
});
```

## Do
- Store the editor's document JSON (ProseMirror, Lexical and Slate all have one) as the source of truth; render HTML from it on the server and sanitize that output.
- Define the schema narrowly: allowed nodes, marks and attributes; links limited to `http`, `https`, `mailto`.
- Normalize pasted content (Word, Google Docs) through the schema's parser rules.
- Handle uploads for images through your upload endpoint with placeholders while pending; set alt text.
- Keep toolbar buttons as real `<button>` elements with `aria-pressed`, labels and keyboard shortcuts; label the editable region.
- Support IME composition, RTL and mixed-direction text (`dir="auto"`); test with Japanese or Arabic input.
- Add autosave with debounce and a version or conflict check; guard unsaved changes on navigation.
- Limit length by characters (grapheme-aware) if a limit exists.
- Migrate stored documents with versioned transforms when the schema changes.

## Avoid
- Storing and re-loading raw HTML as the model: round-trips drift and XSS persists. Store structured JSON and sanitize output.
- Rendering stored HTML with `innerHTML` unsanitized: stored XSS.
- Unrestricted marks or attributes (`style`, `class`, event handlers): schema escapes. Allowlist.
- `document.execCommand`-based home-grown editors: inconsistent across browsers. Use a maintained framework.
- Counting `.length` for limits: splits emoji. Count graphemes.
- Changing the schema without migration: old documents fail to load.

## Review
- [ ] Schema allowlist is tested against hostile paste.
- [ ] Stored form is JSON, output is sanitized.
- [ ] Keyboard and screen-reader basics work.
- [ ] IME and RTL checked.
- [ ] Autosave and conflict behavior defined.

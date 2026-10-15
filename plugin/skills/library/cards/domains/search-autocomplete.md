---
name: search-autocomplete
title: Search autocomplete
area: domains
tags: [autocomplete, typeahead, debounce, accessibility, ranking, prefix]
detect: [dep:@algolia/autocomplete-core, dep:downshift]
related: [search, unicode, recommendations, rich-text-editors]
---
Typeahead: prefix and typo-tolerant suggestions, debounced requests with stale-response cancellation, IME-safe input, and a11y combobox semantics.

## Verify
- `npx vitest run autocomplete`: debounce, race and keyboard tests pass.
- `pytest -q tests/test_suggest.py`: ranking, normalization and prefix tests pass.
- `npx playwright test autocomplete`: keyboard and screen-reader roles work end to end (if Playwright is set up).

## Test first
A slow early response must not overwrite a later one.
```ts
import { createSuggest } from "./suggest";

test("stale response is ignored", async () => {
  const resolvers: Record<string, (v: string[]) => void> = {};
  const fetcher = (q: string) => new Promise<string[]>(r => { resolvers[q] = r; });
  const s = createSuggest(fetcher);
  s.input("ca"); s.input("car");
  resolvers["car"](["car", "cart"]);
  resolvers["ca"](["cat", "cap"]);          // arrives late
  await s.settled();
  expect(s.items).toEqual(["car", "cart"]);
});
```

## Do
- Debounce around 150 to 250 ms, cancel in-flight requests with `AbortController`, and ignore stale results by request id.
- Normalize query and index alike: lowercase, trim, strip diacritics (NFKD), collapse whitespace.
- Rank by prefix match, then popularity or recency, then fuzzy matches; boost the user's own history.
- Use an edge-ngram index or a trie for prefix; cap results (5 to 10) and keep latency under about 100 ms server side.
- Don't fire while an IME is composing (`compositionstart` to `compositionend`).
- Follow the ARIA combobox pattern: `role="combobox"`, `aria-expanded`, `aria-controls`, `aria-activedescendant`, listbox with options; Up, Down, Enter, Escape, Home and End keys.
- Highlight the matched part safely (build nodes, don't inject HTML).
- Cache by normalized prefix; show recent searches when empty.
- Log selected suggestion and position to improve ranking.

## Avoid
- Request per keystroke: load and flicker. Debounce and cancel.
- Rendering out-of-order responses: wrong list for the text. Track the latest id.
- `innerHTML` for highlights: XSS from indexed data. Escape and wrap with elements.
- Searching on a minimum of zero characters for huge indexes: pick a min length or serve popular items.
- Breaking CJK input by acting on every composition event.
- Mouse-only selection: keyboard users stuck. Implement the full key map.

## Review
- [ ] Stale and aborted requests are handled and tested.
- [ ] Combobox roles and keys are in place.
- [ ] Normalization is identical at index and query time.
- [ ] Highlighting is escaped.
- [ ] Result count and latency are capped.

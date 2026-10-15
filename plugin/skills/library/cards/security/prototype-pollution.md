---
name: prototype-pollution
title: Prototype pollution
area: security
tags: [security, javascript, prototype, merge, nodejs, typescript]
detect: []
related: [input-validation, mass-assignment, xss, dependency-audit]
---
JavaScript merges, clones and path-sets must not walk `__proto__`, `constructor` or `prototype`; use null-prototype objects and schemas.

## Verify
- `npm audit --omit=dev`: known-vulnerable merge and clone libraries in the tree.
- `git grep -nE "(merge|extend|assign|defaultsDeep|set)\(" -- '*.js' '*.ts' ':!*test*'`: every deep merge and path setter is reviewed for untrusted input.
- `node -e "JSON.parse('{\"__proto__\":{\"x\":1}}'); console.log(({}).x)"`: prints undefined, showing JSON.parse alone does not pollute; the merge after it does.

## Test first
After processing hostile input, a fresh object must be clean.
```js
test("merge ignores __proto__", () => {
  const payload = JSON.parse('{"__proto__":{"isAdmin":true}}');
  applySettings({}, payload);
  expect({}.isAdmin).toBeUndefined();
  expect(Object.prototype.hasOwnProperty.call(Object.prototype, "isAdmin")).toBe(false);
});

test("path setter rejects constructor.prototype", () => {
  expect(() => setPath({}, "constructor.prototype.x", 1)).toThrow();
  expect({}.x).toBeUndefined();
});
```

## Do
- Validate request bodies with a schema (zod, ajv) that uses strict objects, so unknown keys are rejected before any merge.
- In custom merge and path-set code, skip or throw on keys `__proto__`, `constructor` and `prototype`.
- Use `Object.create(null)` or `Map` for dictionaries keyed by user input.
- Check ownership with `Object.hasOwn(obj, key)`, not `key in obj`.
- Update merge and clone libraries and keep them in `npm audit` CI.
- Freeze shared config: `Object.freeze(Object.prototype)` in hardened services after startup, or run Node with `--disable-proto=delete`.
- Copy only listed fields into models instead of spreading whole bodies.

## Avoid
- `Object.assign(target, req.body)` or recursive `merge(config, req.body)`: attacker keys land on the prototype. Pick fields or validate with a strict schema.
- Lodash `set`, `merge` or `defaultsDeep` on user paths with old versions: upgrade and also block dangerous keys.
- Checking `if (obj[key])` for permissions: inherited polluted values pass. Use own-property checks.
- Blocklisting just `__proto__`: `constructor.prototype` works as well. Block all three or use null-prototype objects.
- Building query or template options from parsed query strings (`a[__proto__][b]`): disable nested parsing or validate.
- Client-side only fixes: the server needs them too.

## Review
- [ ] No unvalidated user object reaches a deep merge or path setter.
- [ ] Dictionaries keyed by user input are `Map` or null-prototype.
- [ ] Permission and option checks use own-property tests.
- [ ] Merge libraries are current and audited in CI.
- [ ] A pollution test exists for each ingestion point.

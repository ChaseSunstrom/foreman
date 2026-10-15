---
name: gcp-firestore
title: GCP Firestore
area: cloud
tags: [gcp, firestore, nosql, security-rules, indexes, emulator]
detect: [dep:google-cloud-firestore, dep:@google-cloud/firestore, dep:firebase-admin, file:firestore.rules, file:firestore.indexes.json]
related: [gcp-iam, gcp-cloud-functions, gcp-cloud-storage]
---
Firestore: queries designed around composite indexes, security rules tested in the emulator, transactions for invariants, bounded document growth.

## Verify
- `firebase emulators:exec --only firestore "pytest -q"`: tests run against the emulator, never production.
- `firebase deploy --only firestore:rules --dry-run`: rules compile.
- `gcloud firestore indexes composite list`: composite indexes in the project match `firestore.indexes.json`.
- `gcloud firestore databases describe --database='(default)'`: location, mode and delete protection.

## Test first
Test the rules with the rules-unit-testing library before writing client code.
```js
it("denies reading another user's profile", async () => {
  const bob = testEnv.authenticatedContext("bob").firestore();
  await assertFails(getDoc(doc(bob, "users/alice")));
  const alice = testEnv.authenticatedContext("alice").firestore();
  await assertSucceeds(getDoc(doc(alice, "users/alice")));
});
```

## Do
- Model for reads: denormalize what a screen needs into one document or a small subcollection. Keep documents well under the 1 MiB limit.
- Write security rules that default to deny, check `request.auth.uid` against the document owner and validate fields (types, sizes, allowed keys) on writes.
- Check composite indexes in as `firestore.indexes.json` and deploy them with rules. A query error links the index it needs.
- Use transactions or batched writes for multi-document invariants, and `FieldValue.increment` for counters.
- Paginate with cursors (`startAfter`) and `limit`, never offsets for large sets.
- Use distributed counters or sharded documents for counters updated more than about once per second per document.
- Set TTL policies for expiring data, and use server timestamps.
- On servers, use the Admin SDK (service identity) and keep authorization checks in code, since it bypasses rules.

## Avoid
- `allow read, write: if true;` or time-boxed open rules left in place: the database is public. Write real rules.
- Trusting client-sent fields like `role` or `userId`: enforce in rules and compare to `request.auth`.
- Sequential or monotonically increasing document ids and indexed timestamps at high write rates: they create hot spots. Use auto ids.
- Unbounded arrays inside a document: it grows to the size limit and every write rewrites it. Use a subcollection.
- Reads in a loop (N+1): use `in` queries (bounded), collection group queries or denormalization.
- Tests against production data: use the emulator and a demo project id.
- Listeners left attached: unsubscribe on teardown or reads and cost pile up.

## Review
- [ ] Rules deny by default and have emulator tests for allow and deny.
- [ ] Every query has a supporting index checked in.
- [ ] Multi-document writes are atomic.
- [ ] No unbounded arrays or hot sequential keys.
- [ ] Admin SDK paths enforce their own authorization.

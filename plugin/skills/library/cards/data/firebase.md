---
name: firebase
title: Firebase / Firestore
area: data
tags: [firebase, firestore, auth, security-rules, nosql, emulator]
detect: [dep:firebase, dep:firebase-admin, dep:firebase-functions, dep:@firebase/rules-unit-testing, dep:cloud_firestore, dep:firebase_core, dep:firebase-tools, file:firebase.json, file:firestore.rules]
related: [supabase, dynamodb, mongodb]
---
Firebase: Firestore data modeled per query, Security Rules as the access control, everything tested on the emulator.

## Verify
- `firebase emulators:exec --only firestore "npm test"`: tests run against the local Firestore emulator.
- `firebase deploy --only firestore:rules --dry-run`: rules compile (use the emulator tests for behavior).
- `firebase firestore:indexes`: deployed composite indexes (compare with `firestore.indexes.json`).
- `firebase emulators:start --only auth,firestore`: local stack starts with the committed config.

## Test first
Use `@firebase/rules-unit-testing`; assert denial before writing the rule.
```js
const env = await initializeTestEnvironment({ projectId: "t", firestore: { rules: fs.readFileSync("firestore.rules", "utf8") } });
const bob = env.authenticatedContext("bob").firestore();
await assertFails(getDoc(doc(bob, "users/alice")));
await assertSucceeds(getDoc(doc(bob, "users/bob")));
```
Fails until the rules restrict reads to the owner.

## Do
- Write Security Rules that check `request.auth.uid`, validate fields on write, and default to deny.
- Model by query: denormalize, use subcollections for unbounded lists, keep documents small (1 MiB limit).
- Add composite indexes in `firestore.indexes.json` and deploy them with the code.
- Use batched writes or transactions (`runTransaction`) for multi-document consistency; use `FieldValue.increment`.
- Paginate with `startAfter` cursors and `limit`.
- In server code, use the Admin SDK with a service account (it bypasses rules) and verify ID tokens with `verifyIdToken`.
- Use `onSnapshot` listeners sparingly and unsubscribe on teardown; enable App Check for public clients.

## Avoid
- `allow read, write: if true;` or test-mode rules shipped: public database. Write owner-scoped rules.
- Trusting client-sent roles or ids: forgeable. Use custom claims and `request.auth.token`.
- Admin SDK credentials or service-account JSON in client bundles or the repo: use environment secrets.
- Unbounded arrays in a document: size limit and write contention. Use a subcollection.
- Hot documents written >1/sec (counters): contention. Shard counters.
- Fetching a collection to filter client-side: reads billed per document. Query with `where`.
- Leaking listeners: duplicate reads and cost. Call the returned unsubscribe.

## Review
- [ ] Rules deny by default and have emulator tests for allow and deny.
- [ ] Composite indexes are committed.
- [ ] Multi-document updates use transactions or batches.
- [ ] Admin credentials are server-side only.
- [ ] Queries filter and paginate server-side.

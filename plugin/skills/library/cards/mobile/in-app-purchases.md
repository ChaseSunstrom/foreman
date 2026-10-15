---
name: in-app-purchases
title: In-App Purchases
area: mobile
tags: [iap, storekit, billing, subscriptions, receipts, entitlements]
detect: [dep:com.android.billingclient:billing-ktx, dep:react-native-iap, dep:purchases_flutter, dep:react-native-purchases, dep:in_app_purchase, file:*.storekit]
related: [app-store-release, play-store-release, mobile-offline-sync]
---
In-app purchases and subscriptions: StoreKit 2 and Play Billing flows with server-side verification and an entitlement model that survives restores.

## Verify
- `xcodebuild test -scheme App -destination 'platform=iOS Simulator,name=iPhone 15'`: StoreKit tests using a local `.storekit` configuration pass (use an installed device name).
- `./gradlew :app:testDebugUnitTest`: billing wrapper and entitlement logic tests pass.
- `npm test`: server receipt verification and webhook tests pass.

## Test first
Entitlement logic is pure, so the first failing test covers state transitions, not the store UI.
```ts
import { entitlementFor } from './entitlements';

test('expired subscription in grace period still grants access', () => {
  const now = new Date('2026-01-10');
  const sub = { productId: 'pro', expires: new Date('2026-01-05'), graceUntil: new Date('2026-01-12') };
  expect(entitlementFor([sub], now)).toEqual({ pro: true });
});

test('refunded purchase revokes access', () => {
  expect(entitlementFor([{ productId: 'pro', revoked: true }], new Date())).toEqual({ pro: false });
});
```

## Do
- Fetch products from the store (`Product.products(for:)` in StoreKit 2, `queryProductDetails` in Play Billing) and show the localized price from the result.
- Listen for transaction updates for the whole app life (`Transaction.updates`, a Play `PurchasesUpdatedListener`), because purchases can complete outside the flow.
- Verify on your server: validate the signed transaction (StoreKit 2 JWS) or the Play purchase token with the Google Play Developer API, then grant entitlement.
- Call `transaction.finish()` after granting on iOS, and acknowledge or consume Play purchases within three days or they are refunded.
- Model entitlements (what the user can do) apart from products (what they bought), and key them to your account id.
- Provide a Restore Purchases action (iOS requires it) and sync entitlements on launch.
- Subscribe to server notifications (App Store Server Notifications, Play real-time developer notifications) for renewals, refunds, revocations and billing retry.
- Test with a local `.storekit` file, Sandbox and Play license testers, and cover renewal, cancel, refund and grace states.

## Avoid
- Trusting the client alone to unlock content: it is trivially bypassed. Verify server side.
- Skipping acknowledge on Android: Google refunds unacknowledged purchases after three days. Acknowledge after granting.
- Never finishing iOS transactions: they replay at each launch. Call `finish()` after delivery.
- Hardcoded prices: the store localizes currency and tax. Display the store-provided string.
- Granting access based on a purchase flow success callback only: pending and deferred states exist. Handle `pending` and `userCancelled`.
- Using external payment links for digital goods where the store rules require IAP: review rejects it. Check the current policy for your region.
- Consumables tracked only on the device: reinstalls lose them. Track balances on the server.

## Review
- [ ] Server verifies every purchase and handles refunds and revocations.
- [ ] Transactions are finished or acknowledged only after entitlement is granted.
- [ ] Transaction listeners start at launch, and restore is available.
- [ ] Prices come from the store and pending and cancelled results are handled.
- [ ] Tests cover renewal, grace, expiry and refund transitions.

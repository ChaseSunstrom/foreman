---
name: push-notifications
title: Push Notifications
area: mobile
tags: [push, notifications, fcm, apns, ios, android]
detect: [dep:firebase-messaging, dep:expo-notifications, dep:@react-native-firebase/messaging, dep:firebase_messaging, file:GoogleService-Info.plist, file:google-services.json]
related: [app-store-release, play-store-release, deep-links, expo, react-native]
---
Push notifications: FCM and APNs token lifecycle, permission prompts, payload types, and server-side delivery that handles dead tokens.

## Verify
- `grep -rnE "aps-environment" --include=*.entitlements .`: the push entitlement is present and set to the right environment.
- `grep -n "POST_NOTIFICATIONS" app/src/main/AndroidManifest.xml`: Android 13 and later runtime permission is declared.
- `npx expo-doctor`: for Expo projects, checks notification config (if used).
- `npm test`: server tests for send logic and token cleanup pass.

## Test first
The server-side logic is testable without a device: failing tests for token cleanup and payload shape come first.
```ts
import { sendToUser } from './push';

test('removes tokens FCM reports as unregistered', async () => {
  const fcm = fakeFcm({ t1: 'messaging/registration-token-not-registered', t2: 'ok' });
  const tokens = memoryTokens(['t1', 't2']);
  await sendToUser('u1', { title: 'Hi' }, { fcm, tokens });
  expect(await tokens.list('u1')).toEqual(['t2']);
});
```

## Do
- Ask for permission at a moment of value (iOS `requestAuthorization`, Android 13+ `POST_NOTIFICATIONS`), and handle denial with a settings link.
- Register the device token after login, send it to your server with user, platform and app version, and refresh it on token-change callbacks.
- Store tokens per device, and delete a token when the provider reports it invalid (`UNREGISTERED`, `NotRegistered`, `BadDeviceToken`).
- Use FCM HTTP v1 with a service account for server sends, not the retired legacy server key API.
- Send a `notification` payload for display-only messages, and a data payload (with `content-available` on iOS) for background handling, knowing background delivery is best effort.
- Create Android notification channels (importance, name) before posting, and use the channel id in the payload.
- Put a stable route or id in the payload data, and open the target screen on tap, including from a cold start.
- Keep payloads small and put no secrets or sensitive details in them, since they appear on lock screens.

## Avoid
- Treating push as reliable delivery: messages are dropped, throttled or delayed. Sync state from the server on app open.
- The legacy FCM server key and `/fcm/send` endpoint: they are shut down. Use HTTP v1 with OAuth.
- Testing APNs production tokens against the sandbox endpoint (and vice versa): `BadDeviceToken`. Match the environment to the build.
- Prompting for permission at first launch with no context: users deny, and iOS will not ask again. Pre-explain then prompt.
- Missing Android channels on API 26 and above: notifications silently do not show. Create them at startup.
- Storing one token per user: a second device overwrites the first. Store per device.
- Doing heavy work in the data message handler: the OS kills it. Schedule background work.

## Review
- [ ] Permission flow handles allow, deny and later opt-in from settings.
- [ ] Tokens are stored per device and pruned on provider errors.
- [ ] Server uses FCM HTTP v1 and the correct APNs environment.
- [ ] Tap handling works from foreground, background and a killed app.
- [ ] Payloads hold no sensitive data, and the app syncs state without relying on delivery.

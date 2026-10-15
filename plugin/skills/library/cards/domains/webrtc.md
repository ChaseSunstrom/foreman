---
name: webrtc
title: WebRTC
area: domains
tags: [webrtc, p2p, turn, stun, signaling, media]
detect: [dep:simple-peer, dep:peerjs, dep:livekit-client, dep:livekit-server-sdk, dep:mediasoup, dep:mediasoup-client, dep:aiortc, dep:pion/webrtc, dep:@daily-co/daily-js, dep:twilio-video]
related: [web-performance, accessibility, auth-providers]
---
Real-time audio, video and data: signaling you build, STUN and TURN for connectivity, an SFU for groups, and quality monitoring.

## Verify
- `npx playwright test call --project=chromium`: two browser contexts connect using fake media (launch with `--use-fake-device-for-media-stream --use-fake-ui-for-media-stream`).
- `turnutils_uclient -u USER -w PASS turn.example.com`: the coturn server relays (from coturn utilities).
- `chrome://webrtc-internals` during a call: ICE candidate pairs, bitrate, packet loss, jitter.
- `curl -s https://api.example.com/turn-credentials -H "authorization: Bearer $T"`: credentials are short-lived and per user.

## Test first
Test signaling logic and connection state with fake media and a local server.
```ts
import { test, expect } from '@playwright/test';

test.use({ launchOptions: { args: [
  '--use-fake-device-for-media-stream', '--use-fake-ui-for-media-stream'] } });

test('two peers connect and receive video', async ({ browser }) => {
  const a = await (await browser.newContext()).newPage();
  const b = await (await browser.newContext()).newPage();
  await a.goto('/room/test'); await b.goto('/room/test');
  for (const p of [a, b]) {
    await expect.poll(() => p.evaluate(() => window.pc?.connectionState)).toBe('connected');
    await expect.poll(() => p.evaluate(() =>
      document.querySelector('video.remote')?.videoWidth ?? 0)).toBeGreaterThan(0);
  }
});
```

## Do
- Build signaling over WebSocket or similar: exchange offer, answer and ICE candidates; authenticate it and scope it to a room.
- Configure `iceServers` with STUN and your own TURN (coturn) over UDP, TCP and TLS 443; roughly one in five networks needs relay.
- Mint short-lived TURN credentials (time-limited HMAC username) per user; never ship a static secret.
- Handle perfect negotiation (polite and impolite peers) to survive glare when both sides offer.
- Use an SFU (LiveKit, mediasoup, Janus) beyond about 3 to 4 participants; mesh does not scale.
- Use `getUserMedia` constraints with ideal values, `enumerateDevices` for pickers, and `track.stop()` on leave to free the camera.
- Handle `iceconnectionstatechange`: restart ICE (`pc.restartIce()`) on failure, show reconnecting UI.
- Monitor with `pc.getStats()`: bitrate, loss, RTT; adapt resolution with simulcast or `maxBitrate`.
- Require HTTPS (a secure context) for media access.

## Avoid
- STUN only: users behind symmetric NAT or corporate firewalls fail. Add TURN.
- Static TURN username and password in client code: anyone can burn your bandwidth. Issue expiring credentials.
- Mesh topology for large rooms: upload bandwidth explodes. Use an SFU.
- Adding remote ICE candidates before `setRemoteDescription`: they are dropped. Queue until it is set.
- Forgetting to stop tracks and close peer connections: camera light stays on and leaks. Clean up on unmount.
- Auto-playing remote video with sound: blocked by browsers. Start muted or require a gesture.
- Trusting the signaling channel's identity claims: spoofing. Authorize join and issue room tokens server-side.
- Testing only on one fast network: add throttled and relay-forced runs (`iceTransportPolicy: 'relay'`).

## Review
- [ ] STUN and TURN configured, with TURN reachable on TLS 443 and credentials short-lived.
- [ ] Signaling is authenticated; rooms are authorized.
- [ ] Reconnect, ICE restart, device change and permission denial are handled.
- [ ] Media tracks and connections are released on exit.
- [ ] Quality stats are collected; large rooms use an SFU.

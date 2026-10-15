---
name: passport
title: Passport
area: node
tags: [passport, authentication, express, sessions, oauth, strategies]
detect: [dep:passport]
related: [express, authjs, better-auth, jest, vitest]
---
Passport authentication middleware for Express: strategies, session serialization, and callback hygiene.

## Verify
- `npx tsc --noEmit`: strategy verify callbacks and `req.user` typing (augment `Express.User`).
- `npx vitest run` (or `npx jest`): supertest suite covering login, logout, and unauthenticated access.
- `npm ls passport passport-local`: one copy of passport, so strategies register on the same instance.
- `npm audit --omit=dev`: known advisories in strategy packages.

## Test first
Use supertest with an agent so the session cookie persists.
```ts
import request from 'supertest';
import { app } from '../src/app';

test('protected route is 401 without login and 200 after', async () => {
  const agent = request.agent(app);
  await agent.get('/me').expect(401);
  await agent.post('/login').send({ username: 'a', password: 'right' }).expect(200);
  await agent.get('/me').expect(200);
  await agent.post('/login').send({ username: 'a', password: 'wrong' }).expect(401);
});
```

## Do
- Order middleware: `express-session` (or cookie-session), then `passport.initialize()`, then `passport.session()`, then routes.
- Implement `serializeUser` to store only an id and `deserializeUser` to load the user fresh.
- In verify callbacks call `done(null, user)` on success, `done(null, false, { message })` on bad credentials, `done(err)` only for real errors.
- Hash passwords with argon2 or bcrypt and compare in constant time.
- Set session cookie `httpOnly`, `secure` in production, `sameSite`, and a store that is not MemoryStore.
- Call `req.login` after signup, and `req.logout(cb)` with a callback (v0.6+ is async).
- For OAuth use a `state` parameter and a fixed, registered callback URL.
- Guard routes with a small `ensureAuthenticated` middleware; also check authorization (ownership) separately.

## Avoid
- Calling `req.logout()` without a callback: it throws in current versions. Pass a callback and handle the error.
- Skipping `session.regenerate` on login: session fixation. Passport 0.6+ regenerates, so don't disable it.
- Serializing the whole user into the session: stale and large. Store the id.
- Using `session: false` for JWT but still mounting `passport.session()`: pick one model.
- Leaving the default MemoryStore in production: leaks memory and loses sessions on restart.
- Trusting `req.isAuthenticated()` as authorization: it only proves identity.

## Review
- [ ] Middleware order is session, initialize, session-strategy, routes.
- [ ] Failed login returns 401 without revealing which field was wrong.
- [ ] Passwords hashed, cookies hardened, production session store configured.
- [ ] Logout destroys the session and is tested.
- [ ] OAuth flows use `state` and exact redirect URIs.

---
name: better-auth
title: Better Auth
area: node
tags: [better-auth, authentication, sessions, oauth, plugins, typescript]
detect: [dep:better-auth]
related: [authjs, passport, drizzle, prisma, zod]
---
Better Auth: one `betterAuth()` server instance, a framework handler, a typed client, schema migrations from its CLI.

## Verify
- `npx @better-auth/cli generate`: emits the ORM schema for the configured plugins (review the diff).
- `npx @better-auth/cli migrate`: applies tables for the built-in Kysely adapter.
- `npx tsc --noEmit`: client plugins mirror server plugins, so inferred session types compile.
- `npx vitest run`: sign-up, sign-in and session tests against a throwaway database.

## Test first
Call the server API directly; no browser needed.
```ts
import { auth } from '../src/auth';

test('sign-in with a wrong password fails', async () => {
  await auth.api.signUpEmail({ body: { email: 'a@b.c', password: 'correct-horse-9', name: 'A' } });  // pragma: allowlist secret
  await expect(
    auth.api.signInEmail({ body: { email: 'a@b.c', password: 'nope-nope-nope' } }),  // pragma: allowlist secret
  ).rejects.toBeTruthy();
});
```

## Do
- Create `auth.ts` with `betterAuth({ database, emailAndPassword: { enabled: true }, socialProviders, plugins })`.
- Mount the handler: `toNextJsHandler(auth)` or `auth.handler` on a catch-all `/api/auth/*` route.
- Set `BETTER_AUTH_SECRET` and `BETTER_AUTH_URL` (or `baseURL`); set `trustedOrigins` for other frontends.
- Create the client with `createAuthClient()` and add the matching client plugins (for example `twoFactorClient()`).
- After adding or changing a plugin, rerun the CLI `generate` and migrate; plugins add tables and fields.
- Read sessions server-side with `auth.api.getSession({ headers })`.
- Turn on `emailVerification` and a `sendResetPassword` callback before production.
- Use the `nextCookies()` plugin when calling auth actions from Next server actions.

## Avoid
- Forgetting migrations after enabling a plugin: runtime errors about missing columns. Generate and migrate.
- A server plugin without its client plugin: methods and types are missing on the client.
- Reading the session from cookies by hand: use `getSession`, which validates and refreshes.
- Hardcoding a weak or missing secret: set `BETTER_AUTH_SECRET` from env.
- Wide `trustedOrigins` such as wildcards: CSRF surface. List exact origins.
- Disabling `useSecureCookies` in production behind HTTPS.

## Review
- [ ] Schema generated for the exact plugin set and migrated in all environments.
- [ ] Secret, base URL and trusted origins come from env.
- [ ] Server and client plugin lists match.
- [ ] Authorization is checked server-side on every protected route.
- [ ] Email verification and password reset flows have tests.

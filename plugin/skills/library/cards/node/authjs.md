---
name: authjs
title: Auth.js (NextAuth)
area: node
tags: [authjs, nextauth, oauth, sessions, nextjs, providers]
detect: [dep:next-auth, dep:@auth/core, dep:@auth/*]
related: [better-auth, passport, prisma, drizzle, zod]
---
Auth.js (NextAuth v5) setup: one central config, trusted callbacks, adapter-backed sessions, secrets and callback URLs correct.

## Verify
- `npx tsc --noEmit`: session and JWT module augmentation compiles.
- `npx auth secret`: generates `AUTH_SECRET` (v5 CLI); the app must refuse to boot without one in production.
- `grep -rn "AUTH_SECRET\|NEXTAUTH_SECRET" .env* .env.example`: the variable is documented and not committed with a real value.
- `npx vitest run`: callback logic tested as pure functions.

## Test first
Keep `authorize` and callbacks as plain functions so they test without a server.
```ts
import { authorizeCredentials } from '@/auth/authorize';

test('rejects wrong password and returns null, not throws', async () => {
  const db = { user: { find: async () => ({ id: '1', hash: await hashFor('right') }) } };
  expect(await authorizeCredentials({ email: 'a@b.c', password: 'wrong' }, db)).toBeNull();
  expect((await authorizeCredentials({ email: 'a@b.c', password: 'right' }, db))?.id).toBe('1');
});
```

## Do
- Export `{ handlers, auth, signIn, signOut }` from one `auth.ts` via `NextAuth({...})`; mount `handlers` at `app/api/auth/[...nextauth]/route.ts`.
- Use `auth()` in server components, route handlers and middleware instead of `getServerSession`.
- Env vars use the `AUTH_` prefix in v5 (`AUTH_SECRET`, `AUTH_GITHUB_ID`); set `AUTH_URL` or `trustHost: true` behind a proxy.
- Validate credentials input (zod) inside `authorize`, and return `null` on failure.
- Copy `user.id` and role into the token in `jwt`, then into `session` in `session` callback; extend types by module augmentation.
- With a database adapter, choose `session: { strategy: 'database' }`; Credentials provider forces JWT.
- Restrict `signIn` callback by verified email or domain; link accounts only for verified emails.
- Register exact callback URLs with each OAuth provider.

## Avoid
- `getServerSession(authOptions)` and `pages/api/auth` patterns from v4 in a v5 app: use `auth()` and the exported handlers.
- Doing auth only in middleware: check in each data access path too.
- Putting secrets or large objects in the JWT: it is sent on every request.
- `allowDangerousEmailAccountLinking: true` with unverified providers: account takeover.
- Throwing in `authorize` for bad passwords: return `null`.
- Using the Edge middleware with a Node-only adapter: split config into `auth.config.ts` for edge.

## Review
- [ ] `AUTH_SECRET` set in every environment and not in git.
- [ ] Session shape typed, and role checks happen server-side.
- [ ] Credentials flow rate-limited, hashed, and validated.
- [ ] OAuth callback URLs and `trustHost` match deployment.
- [ ] Middleware matcher excludes static assets and the auth routes.

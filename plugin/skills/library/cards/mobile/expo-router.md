---
name: expo-router
title: Expo Router
area: mobile
tags: [expo, react-native, routing, navigation, file-based, typescript]
detect: [dep:expo-router, file:app/_layout.tsx]
related: [expo, react-native, deep-links, react-native-performance]
---
Expo Router: file-based routing in the `app/` directory on top of React Navigation, with typed routes, layouts and universal links.

## Verify
- `npx tsc --noEmit`: typed routes (with `experiments.typedRoutes` enabled) catch bad `href` values.
- `npx expo-doctor`: checks the project for dependency and config problems.
- `npx expo export --platform web`: the route tree builds and bundles.
- `npx jest`: route and component tests with `expo-router/testing-library` pass.

## Test first
Render the real route tree in memory with the router testing library.
```tsx
import { renderRouter, screen } from 'expo-router/testing-library';

it('redirects signed-out users to /login', async () => {
  renderRouter('./app', { initialUrl: '/account' });
  expect(await screen.findByText('Sign in')).toBeTruthy();
  expect(screen).toHavePathname('/login');
});
```

## Do
- Put routes in `app/`, where a file is a screen, `_layout.tsx` is a layout (`Stack`, `Tabs`, `Slot`), `[id].tsx` is a dynamic segment, `(group)` is a folder with no URL segment, and `+not-found.tsx` is the fallback.
- Read params with `useLocalSearchParams<{ id: string }>()`, and note that values are strings.
- Navigate with `<Link href="/orders/7">`, `router.push`, `router.replace` and `router.back()`, using object hrefs `{ pathname: '/orders/[id]', params: { id } }` for type safety.
- Guard routes with `<Redirect href="/login" />` in a layout, or the protected-route pattern, after auth state has loaded.
- Keep the root layout for providers, fonts and splash control with `SplashScreen.preventAutoHideAsync()` and hide it once ready.
- Set `scheme` in the app config, and add associated domains and intent filters for universal links.
- Share screen options in the layout with `<Stack screenOptions={{ ... }} />`, and per screen with `<Stack.Screen options={...} />`.
- Use `unstable_settings = { initialRouteName }` in a group layout to guarantee a back stack on deep link entry.

## Avoid
- Mixing `app/` routes with manual `react-navigation` containers: two routers fight. Use one.
- `useRouter()` navigation during the first render: it throws before the navigator mounts. Use `<Redirect>` or run it in an effect after mount.
- Leaving non-route files in `app/` (components, helpers): each becomes a route. Keep them in `src/` or `components/`.
- Reading params as numbers or arrays without checking: they arrive as strings or `string[]`. Parse and validate.
- Auth checks that run only in screens: deep links bypass them. Guard in the layout.
- Ignoring that `href` strings are not checked without typed routes: turn them on and regenerate types.

## Review
- [ ] No non-route files under `app/`, and layouts own providers and guards.
- [ ] Params are parsed and validated, and typed routes are on.
- [ ] Deep link entry has a sensible back stack.
- [ ] Auth redirects wait for the loading state and cover deep links.
- [ ] Router tests cover redirect, dynamic param and not-found cases.

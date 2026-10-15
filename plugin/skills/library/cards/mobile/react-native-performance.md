---
name: react-native-performance
title: React Native Performance
area: mobile
tags: [react-native, performance, hermes, flatlist, rerenders, javascript]
detect: [dep:react-native, dep:@shopify/flash-list, dep:react-native-reanimated]
related: [react-native, expo, expo-router]
---
React Native performance: keep JS-thread work and re-renders small, use virtualized lists and native-driven animation, and measure on a release build.

## Verify
- `npx tsc --noEmit`: types hold after memoization refactors.
- `npx jest`: unit and component tests pass.
- `npx react-native run-android --mode release`: runs a release build on a device, where timing is meaningful (use `--configuration Release` with `run-ios`).
- `npx react-native-bundle-visualizer`: shows bundle composition (if the tool is installed).

## Test first
Prove a row does not re-render when unrelated state changes, using a render counter.
```tsx
import { render, fireEvent } from '@testing-library/react-native';

test('row does not re-render when the sibling counter changes', () => {
  const renders = jest.fn();
  const Row = React.memo(({ id }: { id: number }) => { renders(id); return <Text>{id}</Text>; });
  const App = () => {
    const [n, setN] = React.useState(0);
    return (<><Button title="inc" onPress={() => setN(n + 1)} /><Row id={1} /></>);
  };
  const { getByText } = render(<App />);
  fireEvent.press(getByText('inc'));
  expect(renders).toHaveBeenCalledTimes(1);
});
```

## Do
- Profile in a release build with Hermes, using the React DevTools Profiler for renders and the Perf Monitor for JS and UI frame rates.
- Render long lists with `FlatList` (set `keyExtractor`, `getItemLayout` for fixed heights, `windowSize`, `removeClippedSubviews`) or FlashList with `estimatedItemSize`.
- Memoize list rows with `React.memo`, and pass stable callbacks (`useCallback`) and props, so memo can skip.
- Run animations on the UI thread with Reanimated worklets (`useSharedValue`, `useAnimatedStyle`) or `useNativeDriver: true`.
- Defer heavy work with `InteractionManager.runAfterInteractions` and move parsing off the main frame path.
- Keep images sized to their display size, cache them (`expo-image` or a caching library), and avoid giant bitmaps.
- Cut startup cost: lazy-load screens, use inline requires (`inlineRequires` in Metro config), and drop unused libraries.
- Keep state local to the screen that needs it, and subscribe to slices (selectors) in the store.

## Avoid
- Judging performance in dev mode: dev builds are many times slower. Use release.
- Inline arrow functions and object literals as props to memoized rows: they defeat `memo`. Hoist or memoize.
- `ScrollView` with `map` for hundreds of items: all items mount. Use a virtualized list.
- `console.log` in hot paths on release builds: it blocks the JS thread. Strip with a babel plugin.
- Animating layout properties with the JS-driven `Animated` API: frames drop when JS is busy. Use native-driven transforms and opacity.
- A global context holding frequently changing values: every consumer re-renders. Split contexts or use selectors.
- Large JSON parsing and sorting on the JS thread during scroll.

## Review
- [ ] Measurements come from a release build with Hermes on a real mid-range device.
- [ ] Lists are virtualized, with keys and stable row props.
- [ ] Animations run natively, and heavy tasks are deferred.
- [ ] Re-render hot spots were found with the Profiler, not guessed.
- [ ] Startup and bundle size were checked after dependency changes.

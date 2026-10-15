---
name: leaflet
title: Leaflet
area: web
tags: [leaflet, maps, react-leaflet, tiles, markers, geojson]
detect: [dep:leaflet, dep:react-leaflet, dep:@types/leaflet]
related: [mapbox-gl, react, nextjs-app-router]
---
Leaflet maps: tile layers, markers, GeoJSON and the lifecycle, icon and SSR traps that break first.

## Verify
- `npx tsc --noEmit`: Leaflet types (`@types/leaflet`) and react-leaflet props.
- `npx vitest run`: logic tests (jsdom has no layout, so keep geometry in pure functions).
- `npm run build`: confirms the SSR build does not touch `window` at import time.
- `npx playwright test`: a real browser check that tiles, markers and popups render.

## Test first
Keep coordinate and bounds logic pure and test it; assert the map renders in a browser test.
```ts
import { toBounds } from "./geo";

test("toBounds covers all points with padding", () => {
  const b = toBounds([[10, 20], [12, 24]], 0.5);
  expect(b).toEqual([[9.5, 19.5], [12.5, 24.5]]);
});
```

## Do
- Import the stylesheet once: `import "leaflet/dist/leaflet.css"`. Give the map container an explicit height.
- Use coordinates as `[lat, lng]`; GeoJSON is `[lng, lat]`. Convert deliberately.
- Create the map once per container and call `map.remove()` on teardown.
- In React use `react-leaflet` components (`MapContainer`, `TileLayer`, `Marker`, `Popup`) and `useMap` inside `MapContainer` children.
- Set tile `attribution` as the tile provider requires, and respect its usage policy and API keys.
- Fix the default marker icon with `L.Icon` and imported image URLs, or use `L.divIcon`.
- Call `map.invalidateSize()` after the container changes size (tabs, modals).
- Use `fitBounds` for sets of points; cluster large marker sets with a cluster plugin or switch to canvas rendering (`preferCanvas: true`).

## Avoid
- Importing leaflet in server-rendered code: `window is not defined`. Load the map component client-only (a dynamic import with SSR disabled, or a client component guarded by mount).
- A container with no height: the map is invisible. Set `height` in CSS.
- Default marker icons broken by bundlers (404 on `marker-icon.png`): configure the icon URLs explicitly.
- Re-creating `MapContainer` props like `center` expecting updates: they are initial only. Use `useMap().setView` or a child effect.
- Initializing twice on the same div ("Map container is already initialized"): common in React strict mode without cleanup. Remove the map on unmount.
- Mixed up lat/lng order from GeoJSON: points land in the ocean. Swap them.
- Thousands of DOM markers: the page stalls. Cluster or use canvas.

## Review
- [ ] CSS imported, container sized, and attribution present.
- [ ] Lat/lng order is correct at each boundary.
- [ ] The map is destroyed on unmount and is client-only in SSR.
- [ ] Marker icons render in the production build.
- [ ] Large datasets are clustered or canvas-rendered.

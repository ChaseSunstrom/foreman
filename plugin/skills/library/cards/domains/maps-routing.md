---
name: maps-routing
title: Maps and routing
area: domains
tags: [maps, routing, tiles, leaflet, maplibre, directions]
detect: [dep:leaflet, dep:maplibre-gl, dep:mapbox-gl]
related: [geocoding, postgis, webrtc, address-validation]
---
Interactive maps and directions: coordinate order, tile and key handling, clustering, route requests with limits, and polyline decoding.

## Verify
- `npx vitest run map`: coordinate, bounds and polyline tests pass.
- `pytest -q tests/test_routing.py`: request building, polyline decode and fallback tests pass.
- `npx tsc --noEmit`: map options and GeoJSON types compile.

## Test first
Pin axis order and the date-line bounds case.
```ts
import { toLngLat, fitBounds } from "./geo";

test("axis order and antimeridian bounds", () => {
  expect(toLngLat({ lat: 52.52, lng: 13.405 })).toEqual([13.405, 52.52]); // MapLibre, GeoJSON
  const b = fitBounds([{ lat: 10, lng: 179 }, { lat: 12, lng: -179 }]);
  expect(b.west).toBe(179);
  expect(b.east).toBe(-179);       // wraps; width is 2 degrees, not 358
});
```

## Do
- Remember the orders: Leaflet uses `[lat, lng]`; MapLibre, Mapbox and GeoJSON use `[lng, lat]`. Convert in one helper.
- Keep API keys scoped (HTTP referrer or origin restriction); proxy server-side calls that need secret keys.
- Respect tile provider terms and attribution; do not hotlink the volunteer OSM tile servers for production traffic; use a hosted or self-hosted tile source.
- Cluster markers beyond a few hundred points, or render as a vector layer from GeoJSON; load by viewport bounds.
- Request routes server-side with a timeout, a profile (driving, walking, cycling), and cache by rounded origin and destination; request alternatives only when shown.
- Decode encoded polylines with the correct precision (5 or 6 digits) per provider.
- Show distance and duration with units by locale, and handle `NoRoute` and `ZERO_RESULTS` states.
- Provide a text alternative: list of stops or turn-by-turn steps, keyboard map controls and sufficient contrast.
- Destroy the map on unmount (`map.remove()`) and debounce resize or move events.

## Avoid
- Swapped lat and lng: points land in the ocean. Use the one helper and a test.
- Embedding secret keys in client bundles: abuse and bills. Restrict or proxy.
- Rendering thousands of DOM markers: freezes the page. Use clustering or layers.
- Straight-line distance as travel time: misleading. Use the routing API and label estimates.
- Polyline precision mismatch: route drawn wildly off. Match the provider.
- Re-creating the map on every state change: leaks WebGL contexts. Update layers and sources.

## Review
- [ ] Axis order has one conversion point.
- [ ] Keys are restricted and attribution shown.
- [ ] Large datasets are clustered or tiled.
- [ ] Routing errors and timeouts have UI states.
- [ ] Map is cleaned up on unmount.

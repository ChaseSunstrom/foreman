---
name: mapbox-gl
title: Mapbox GL JS
area: web
tags: [mapbox, maplibre, webgl, maps, vector-tiles, geojson]
detect: [dep:mapbox-gl, dep:react-map-gl, dep:maplibre-gl, dep:@types/mapbox-gl]
related: [leaflet, webgl, react]
---
Mapbox GL JS and MapLibre: WebGL vector maps driven by style sources and layers, with token, event-order and cleanup traps.

## Verify
- `npx tsc --noEmit`: style, layer and event types.
- `npx eslint .`: lint.
- `npx vitest run`: pure data and filter logic (WebGL is not available in jsdom, so mock the map object for wiring tests).
- `npx playwright test`: a real-browser smoke test that the canvas renders and a layer click fires.

## Test first
Keep GeoJSON building pure; mock the map for wiring.
```ts
import { toFeatureCollection } from "./geojson";

test("builds [lng, lat] point features", () => {
  const fc = toFeatureCollection([{ id: "a", lat: 10, lng: 20 }]);
  expect(fc.features[0].geometry.coordinates).toEqual([20, 10]);
  expect(fc.features[0].properties?.id).toBe("a");
});
```

## Do
- Set the access token from env (`mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_TOKEN` or the framework equivalent); use a URL-restricted public token. MapLibre needs no token with a free style.
- Import the library CSS once.
- Add sources and layers only after the `load` event (or check `map.isStyleLoaded()`); after a style change, re-add them on `style.load`.
- Update data with `source.setData(geojson)` rather than removing and re-adding layers.
- Coordinates are `[lng, lat]`.
- Handle `map.on("click", "layer-id", handler)` with the layer id, and change the cursor on `mouseenter` and `mouseleave`.
- Call `map.remove()` on unmount; remove listeners you added to the map.
- For many points use a clustered GeoJSON source (`cluster: true`) with layers or symbol layers, not DOM markers.

## Avoid
- Calling `addSource` or `addLayer` before the style has loaded: it throws "Style is not done loading". Wait for `load`.
- Secret (`sk.`) tokens in client code: they leak. Use a public token with URL restrictions.
- Swapping `[lat, lng]`: markers land in the wrong place. Use `[lng, lat]`.
- Forgetting `map.remove()`: WebGL contexts leak and the browser warns about too many contexts.
- Thousands of `Marker` DOM elements: slow. Use layers.
- Duplicate layer or source ids on hot reload: errors. Check `map.getLayer(id)` first.
- Mixing mapbox-gl and maplibre-gl CSS or classes in one map: pick one library and match `react-map-gl` import path to it.

## Review
- [ ] Token comes from env, is public, and is URL-restricted.
- [ ] Layers are added after load and re-added on style change.
- [ ] Data updates go through `setData`.
- [ ] The map and its listeners are removed on unmount.
- [ ] Large point sets use clustering or layers.

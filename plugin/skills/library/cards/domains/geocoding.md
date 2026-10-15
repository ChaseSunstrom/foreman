---
name: geocoding
title: Geocoding
area: domains
tags: [geocoding, coordinates, caching, distance, rate-limits, privacy]
detect: [dep:geopy]
related: [maps-routing, postgis, address-validation, money]
---
Address to coordinates and back: provider choice, cached results with confidence, lat/lng order, and honest distance math.

## Verify
- `pytest -q tests/test_geocode.py`: parsing, cache and ordering tests pass with the provider mocked.
- `python -c "from geopy.distance import geodesic; print(geodesic((52.52,13.405),(48.8566,2.3522)).km)"`: distance sanity check (about 878 km).
- `grep -rn "lat.*lng\|lng.*lat" src | head`: review argument order at call sites.

## Test first
Lat/lng swap is the classic bug; pin it with a point whose swap is invalid.
```python
from app.geo import to_point, distance_km

def test_point_order_and_range_validation():
    p = to_point(lat=52.52, lng=13.405)
    assert p == (13.405, 52.52)            # GeoJSON and PostGIS are (lng, lat)
    with pytest.raises(ValueError):
        to_point(lat=130.0, lng=13.4)      # latitude outside [-90, 90]
    assert 870 < distance_km((52.52, 13.405), (48.8566, 2.3522)) < 885
```

## Do
- Store lat and lng as numeric (or a PostGIS `geography`), with provider, precision or match type, confidence and `geocoded_at`.
- Cache by a normalized query key (trimmed, case-folded, whitespace-collapsed); respect the provider's terms on storing results.
- Keep the axis order in one place: GeoJSON, PostGIS and many APIs use (lng, lat); display and many SDKs use (lat, lng).
- Geocode asynchronously on write, not per read; retry with backoff on 429 and 5xx; batch where supported.
- Use haversine or geodesic for distance; for nearby queries use a spatial index and a bounding box first.
- Bias results with country or bounding-box parameters to cut ambiguity.
- Keep failures as data: status `unresolved` with the reason, and let users correct by pin drop.
- Reverse geocode only when needed; coordinates of people are personal data, so round them when precision is not needed.

## Avoid
- Treating every result as exact: a city centroid for a street query misleads. Store and show match precision.
- Euclidean distance on degrees: wrong, especially away from the equator. Use a geodesic formula.
- Calling the provider on each page view: cost and rate limits. Cache.
- Ignoring the antimeridian and poles in bounding boxes: split the query.
- Parsing addresses with regex before geocoding: pass the full string or structured fields.
- Float equality on coordinates for dedupe: compare within a tolerance or by cell id.

## Review
- [ ] Axis order is explicit and tested.
- [ ] Results carry precision and are cached.
- [ ] Failures and rate limits handled.
- [ ] Spatial queries use an index.
- [ ] Location data retention is justified.

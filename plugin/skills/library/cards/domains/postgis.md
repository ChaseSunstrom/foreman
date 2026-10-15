---
name: postgis
title: PostGIS and Geospatial
area: domains
tags: [postgis, gis, geometry, geography, spatial-index, srid]
detect: [dep:geoalchemy2, dep:django.contrib.gis, dep:shapely, dep:pyproj, dep:activerecord-postgis-adapter, dep:rgeo, dep:@turf/turf, dep:sequelize, dep:geopandas, dep:postgis-diesel]
related: [search, money, timezones]
---
Spatial data in PostgreSQL: correct SRIDs, geography versus geometry, GiST indexes and index-friendly queries.

## Verify
- `psql -c "select postgis_full_version()"`: the extension is installed and its version.
- `psql -c "select Find_SRID('public','places','geom')"`: the column's SRID.
- `psql -c "explain analyze select id from places where st_dwithin(geom, st_setsrid(st_makepoint(-73.98,40.75),4326)::geography, 1000)"`: the plan uses the GiST index, not a seq scan.
- `psql -c "select count(*) from places where not st_isvalid(geom)"`: no invalid geometries.

## Test first
Create a known layout and assert the query result and plan.
```sql
-- schema test (pgTAP-style or a plain script that raises on failure)
create temp table p(id int, geom geography(Point,4326));
insert into p values (1, st_point(-73.9855, 40.7580)::geography),   -- Times Sq
                     (2, st_point(-118.2437, 34.0522)::geography); -- LA
do $$ begin
  assert (select count(*) from p
          where st_dwithin(geom, st_point(-73.9857, 40.7484)::geography, 2000)) = 1;
end $$;
```
Cover too: antimeridian, poles, a point exactly on the boundary, an invalid polygon.

## Do
- Declare typed columns: `geometry(Point, 4326)` or `geography(Point, 4326)`; always set the SRID.
- Use `geography` for global lat/lon distance in meters; use `geometry` in a projected SRID (for example a UTM zone or a local state-plane code) for fast planar work.
- Remember axis order: PostGIS and GeoJSON use longitude, latitude (x, y).
- Index with `create index on places using gist (geom)`; `analyze` after bulk loads.
- Radius search: `ST_DWithin(a, b, meters)`, not `ST_Distance(a, b) < r`; nearest neighbors: `order by geom <-> point limit 10` (KNN).
- Bounding-box tiles or viewport: `geom && ST_MakeEnvelope(xmin, ymin, xmax, ymax, 4326)`.
- Validate with `ST_IsValid` and repair with `ST_MakeValid` on import; reject bad inputs at the boundary.
- Transform explicitly with `ST_Transform(geom, srid)`; keep stored SRID uniform.
- Return GeoJSON via `ST_AsGeoJSON` and limit coordinate precision.

## Avoid
- `ST_Distance(...) < x` in WHERE: cannot use the index, full scan. Use `ST_DWithin`.
- Swapped lat and lon: points land in the ocean. Use (lon, lat) consistently and test with a known city.
- Mixing SRIDs: error or silent nonsense. Transform to one SRID.
- Measuring in degrees: `ST_Distance` on SRID 4326 geometry returns degrees. Use geography or a projected SRID.
- Missing spatial index after table loads: slow queries. Create it and `VACUUM ANALYZE`.
- Rounding coordinates to 2 decimals "for cleanliness": about 1 km error. Keep 5 to 6 decimals.
- `ST_Buffer` on lat/lon geometry assuming meters: use geography or project first.
- Ignoring antimeridian crossings: polygons wrap the wrong way. Split or use geography.

## Review
- [ ] Every geometry column has a declared type and SRID.
- [ ] Spatial indexes exist and `EXPLAIN` shows them used.
- [ ] Distances use geography or a projected SRID, not degrees.
- [ ] Coordinate order is lon, lat everywhere, including API contracts.
- [ ] Invalid geometry is rejected or repaired on input.

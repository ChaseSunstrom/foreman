---
name: feature-stores
title: Feature stores
area: ml
tags: [feature-store, feast, point-in-time, mlops, features, serving]
detect: [dep:feast, file:feature_store.yaml]
related: [dvc, mlflow, scikit-learn, time-series-forecasting]
---
Share feature definitions between training and serving with point-in-time correct joins, freshness checks and one transformation path.

## Verify
- `feast apply`: the registry accepts the entity and feature view definitions.
- `pytest -q tests/test_features.py`: point-in-time joins and online/offline parity pass on fixtures.
- `python -m app.parity --sample 1000`: online values match offline values for the same entities and timestamps.

## Test first
```python
from app.features import training_frame

def test_no_feature_from_after_label_time():
    df = training_frame(entities, label_times)
    assert (df["feature_ts"] <= df["event_ts"]).all()
```

## Do
- Define entities, feature views, sources and TTLs in code; review them like any schema.
- Build training sets with point-in-time joins (as-of the label timestamp), never a latest-value join.
- Keep one transformation implementation used by both the batch pipeline and the online path.
- Materialise to the online store on a schedule and alert on freshness against each view's TTL.
- Give every feature an owner, a description, a type and a null policy.
- Version feature views when semantics change; keep old versions until models using them retire.
- Log the feature values served with each prediction to enable debugging and drift checks.
- Backfill with the same code as the incremental path.

## Avoid
- Joining the latest feature values onto historical labels: future leakage. Use as-of joins.
- Separate SQL for training and Python for serving: skew. Share logic or test parity.
- No TTL or freshness alerts: stale values served silently. Monitor materialisation lag.
- Changing a feature's meaning in place: old models break quietly. Create a new version.
- Storing high-cardinality raw events in the online store: cost and latency. Pre-aggregate.
- Treating the registry as optional: undocumented features proliferate. Gate merges on `apply`.

## Review
- [ ] Training data built with point-in-time joins.
- [ ] Parity test between online and offline values.
- [ ] TTLs set and freshness monitored.
- [ ] Feature changes versioned with owners.
- [ ] Served features logged for audit.

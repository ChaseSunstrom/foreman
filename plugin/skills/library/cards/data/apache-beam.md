---
name: apache-beam
title: Apache Beam
area: data
tags: [beam, pipelines, windowing, runners, dataflow, python]
detect: [dep:apache-beam, dep:beam-sdks-java-core]
related: [flink, spark, etl-pipelines]
---
Apache Beam pipelines: PCollections, windows and triggers, DoFn purity and tests with TestPipeline.

## Verify
- `python -m pytest -q`: transform tests on the DirectRunner.
- `python pipeline.py --runner=DirectRunner --input sample.json`: whole pipeline on a small sample.
- `python -c "import apache_beam as beam; print(beam.__version__)"`: the SDK resolves in the environment you deploy.

## Test first
Use `TestPipeline` with `assert_that` on a small in-memory input.
```python
import apache_beam as beam
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.util import assert_that, equal_to

def test_counts_words():
    with TestPipeline() as p:
        out = (p | beam.Create(["a b", "a"]) | beam.FlatMap(str.split)
                 | beam.combiners.Count.PerElement())
        assert_that(out, equal_to([("a", 2), ("b", 1)]))
```

## Do
- Write transforms as small `DoFn` or `PTransform` classes with typed inputs and outputs; test each alone.
- Use `beam.Map`, `FlatMap` and `Filter` for simple cases and `ParDo` with tagged outputs for side branches (dead-letter outputs).
- Window unbounded data explicitly (`beam.WindowInto(window.FixedWindows(60))`) before any aggregation or grouping.
- Set a trigger and allowed lateness deliberately for event-time windows; know the default is the watermark only.
- Prefer combiners (`CombinePerKey`) to `GroupByKey` followed by a manual reduce.
- Keep side inputs small; use them for lookups loaded once.
- Make DoFns idempotent and free of shared mutable state; do setup in `setup()` or `start_bundle()`.
- Use `TestStream` to test windows and late data.

## Avoid
- Aggregating an unbounded source without windowing: the pipeline errors or never emits. Add `WindowInto`.
- Side effects in a DoFn without idempotency: retries and bundle reprocessing duplicate them. Write idempotently or use a sink transform.
- Large `GroupByKey` on a hot key: worker OOM. Use `CombinePerKey` with fanout or key salting.
- Capturing unpicklable objects (clients, locks) in lambdas: pickling fails on workers. Create them in `setup()`.
- Relying on element order: PCollections are unordered. Sort after grouping if needed.
- Different SDK versions between launcher and workers: serialization errors. Pin and match.

## Review
- [ ] Unbounded data windowed; trigger and lateness stated.
- [ ] DoFns are retry-safe and hold no hidden state.
- [ ] Failed records go to a tagged dead-letter output.
- [ ] Each transform has a TestPipeline test.
- [ ] Runner and SDK versions pinned.

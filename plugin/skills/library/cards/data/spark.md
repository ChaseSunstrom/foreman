---
name: spark
title: Apache Spark
area: data
tags: [spark, pyspark, distributed, dataframes, etl, partitions]
detect: [dep:pyspark, dep:spark-sql_2.12, dep:spark-core_2.12, dep:spark-sql_2.13, dep:spark-core_2.13, dep:delta-spark, dep:findspark, dep:spark-submit]
related: [parquet-arrow, etl-pipelines, kafka, airflow, dbt]
---
Spark jobs: DataFrame API with explicit schemas, columnar formats, controlled shuffles and partitions.

## Verify
- `spark-submit --master "local[2]" job.py`: the job runs end to end on a local master.
- `pytest -q`: transform functions pass against a local SparkSession fixture.
- `python -c "from job import build; build(spark).explain(True)"`: plan shows pushed filters, pruned columns and the shuffles.
- `spark-submit --conf spark.sql.shuffle.partitions=8 --master "local[2]" job.py`: behavior is stable with a different shuffle size.

## Test first
Keep transforms as pure `DataFrame -> DataFrame` functions; test on tiny in-memory data with a shared local session.
```python
@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder.master("local[1]").config("spark.sql.shuffle.partitions", 1).getOrCreate()

def test_dedupes_latest(spark):
    df = spark.createDataFrame([("a", 1), ("a", 2)], "id string, v int")
    assert dedupe_latest(df).collect()[0].v == 2
```

## Do
- Declare schemas (`StructType` or DDL string) when reading CSV/JSON; do not infer in production.
- Prefer built-in functions (`pyspark.sql.functions`) over Python UDFs; use pandas UDFs when needed.
- Read and write Parquet or Delta; partition output by low-cardinality columns used in filters.
- Filter and select early so predicate and column pushdown apply.
- Broadcast small join sides with `broadcast(df)`; check for skew on big joins.
- Tune `spark.sql.shuffle.partitions` and let AQE (`spark.sql.adaptive.enabled`) coalesce.
- Cache only reused DataFrames and `unpersist()` afterward.
- Write idempotently: `mode("overwrite")` with dynamic partition overwrite for a partition, or merge on Delta.

## Avoid
- `collect()` or `toPandas()` on large data: driver out-of-memory. Aggregate first or write out.
- Python row-wise UDFs: serialization cost. Use built-ins or pandas UDFs.
- Thousands of tiny output files from over-partitioning: slow reads. `coalesce` or repartition before write.
- Relying on schema inference and header guessing: type drift between runs. Pass a schema.
- Reusing an unseeded `rand()` or relying on row order: results change between runs. Order explicitly.
- Count-then-process patterns that recompute lineage: `cache()` the shared stage.
- Hardcoding the master in code: breaks cluster submits. Pass `--master`.

## Review
- [ ] Schemas are explicit at read boundaries.
- [ ] No driver-side collection of unbounded data.
- [ ] The plan has pushed filters; joins use broadcast where small.
- [ ] Output layout (format, partitions, file sizes) is intentional.
- [ ] Writes are idempotent and re-runnable.
